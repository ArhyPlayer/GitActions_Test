# Test Backend API

Простое тестовое приложение на FastAPI, возвращающее текущее время сервера.

## Установка зависимостей

```bash
pip install -r requirements.txt
```

## Запуск сервера

```bash
uvicorn main:app --reload
```

Сервер будет доступен по адресу: http://127.0.0.1:8000

## API Endpoints

### GET /
Базовый эндпоинт для проверки работы сервера.

**Response:**
```json
{
  "message": "Test backend is running"
}
```

### GET /time
Возвращает текущее время сервера.

**Response:**
```json
{
  "server_time": "2024-12-25T12:30:45.123456",
  "timestamp": 1735129845,
  "timezone": null
}
```

### GET /health
Проверка здоровья приложения.

**Response:**
```json
{
  "status": "healthy"
}
```

## Документация API

После запуска сервера документация Swagger UI будет доступна по адресу:
http://127.0.0.1:8000/docs
