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

## Запуск через Docker

### Сборка образа
```bash
docker build -t test-backend .
```

### Запуск контейнера
```bash
docker run -p 8000:8000 test-backend
```

### Настройка через переменные окружения
При запуске контейнера можно переопределить переменные окружения:
```bash
docker run -p 9000:9000 -e PORT=9000 -e HOST=0.0.0.0 test-backend
```

Доступные переменные окружения:
- `HOST` - хост для привязки сервера (по умолчанию: 0.0.0.0)
- `PORT` - порт для сервера (по умолчанию: 8000)
- `DEBUG` - режим отладки (по умолчанию: false)

Сервер будет доступен по адресу: http://localhost:8000

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
