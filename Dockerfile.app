FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && pip install poetry && poetry install --no-interaction --no-ansi
EXPOSE 8080
CMD ["poetry", "run", "python", "-m", "app.main"]
