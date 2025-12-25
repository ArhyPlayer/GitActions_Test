# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY main.py .

# Открываем порт 8000
EXPOSE 8000

# Устанавливаем переменные окружения по умолчанию
ENV HOST=0.0.0.0 \
    PORT=8000 \
    DEBUG=false

# Запускаем приложение
CMD ["uvicorn", "main:app", "--host", "${HOST}", "--port", "${PORT}"]
