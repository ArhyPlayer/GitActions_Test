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

### GET /date
Возвращает текущую дату сервера в различных форматах.

**Response:**
```json
{
  "date": "2024-12-25",
  "formatted": "2024-12-25",
  "readable": "December 25, 2024",
  "day": 25,
  "month": 12,
  "year": 2024,
  "weekday": "Wednesday"
}
```

### GET /date/iso
Возвращает текущую дату в ISO формате.

**Response:**
```json
{
  "date": "2024-12-25"
}
```

### GET /date/formatted
Возвращает текущую дату в читаемом формате.

**Response:**
```json
{
  "date": "December 25, 2024"
}
```

### GET /date/today
Возвращает информацию о сегодняшней дате.

**Response:**
```json
{
  "today": "2024-12-25",
  "is_weekend": false,
  "day_of_week": "Wednesday",
  "day_of_year": 360
}
```

## CI/CD с GitHub Actions

Проект настроен для автоматического развертывания через GitHub Actions.

### Настройка секретов

В настройках репозитория (Settings → Secrets and variables → Actions) добавьте следующие секреты:

- `SSH_HOST` - IP адрес или домен удаленного сервера
- `SSH_USER` - имя пользователя для SSH подключения
- `SSH_KEY` - приватный SSH ключ (сгенерируйте с `ssh-keygen -t rsa -b 4096`)
- `SSH_PORT` - порт SSH (опционально, по умолчанию 22)

### Как работает деплой

1. **Build джоба**: Собирает Docker образ и пушит в GitHub Container Registry
2. **Deploy джоба**: Подключается к серверу по SSH и разворачивает приложение

Workflow запускается при пуше в main/master ветку.

### Требования к серверу

На сервере должен быть установлен Docker и настроен SSH доступ.

## Документация API

После запуска сервера документация Swagger UI будет доступна по адресу:
http://127.0.0.1:8000/docs
