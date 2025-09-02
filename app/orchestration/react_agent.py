"""ReAct agent for sequential reasoning when >=2 tools selected."""
import asyncio
from app.orchestration.state import ChatState
from app.tools.kb_stub import run_kb_stub
from app.tools.ocr_stub import run_ocr_stub
from app.tools.stream_stub1 import run_stream_stub1
from app.tools.stream_stub2 import run_stream_stub2
from app.models.llm import call_llm

TOOL_MAP = {
    "kb_stub": run_kb_stub,
    "ocr_stub": run_ocr_stub,
    "stream_stub1": run_stream_stub1,
    "stream_stub2": run_stream_stub2,
}

async def run_react_agent(state: ChatState) -> None:
    state.thoughts.append("ReAct: sequential tool reasoning.")
    for tool in state.selected_tools:
        func = TOOL_MAP.get(tool)
        if not func:
            continue
        if tool == "ocr_stub":
            gen = func(state.attachments)
        else:
            gen = func(state.user_input)
        state.tool_outputs[tool] = []
        async for chunk in gen:
            state.tool_outputs[tool].append(chunk)
            state.thoughts.append(f"[{tool}] {chunk}")
        await asyncio.sleep(0.2)
    await fan_in(state)
    await reducer(state)

async def fan_in(state: ChatState) -> None:
    state.thoughts.append("All tool outputs gathered (ReAct).")

async def reducer(state: ChatState) -> None:
    messages = [
        {"role": "system", "content": "Combine tool results and user input."},
        {"role": "user", "content": state.user_input},
    ]
    for tool, outputs in state.tool_outputs.items():
        messages.append({"role": "assistant", "content": f"{tool}: {'; '.join(outputs)}"})
    state.final_response = await call_llm(messages)
