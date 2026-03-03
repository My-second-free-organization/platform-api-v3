FROM python:3.12-slim AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim
RUN groupadd -g 1001 app && useradd -u 1001 -g app -m app
WORKDIR /app
COPY --from=build /install /usr/local
COPY src/ ./src/
USER app
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
