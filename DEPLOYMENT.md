# Руководство по развертыванию FastAPI приложения

Это руководство описывает процесс развертывания FastAPI приложения с использованием GitHub Actions и Docker.

## 🚀 Быстрый старт

### Предварительные требования

#### На сервере:
- Ubuntu/Debian сервер с root доступом
- Минимум 1GB RAM, 1 CPU, 10GB диск
- Публичный IP адрес или домен

#### В GitHub репозитории:
- Репозиторий должен быть создан
- **ВАЖНО:** Имя репозитория должно быть в lowercase (например, `my-repo`, а не `My-Repo`), так как Docker registry требует lowercase имена
- Ветка `main` должна быть настроена как default
- GitHub Actions должны быть включены

## 📋 Подготовка сервера

### 1. Обновление системы
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Установка Docker
```bash
# Установка необходимых пакетов
sudo apt install apt-transport-https ca-certificates curl gnupg lsb-release -y

# Добавление GPG ключа Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Добавление репозитория Docker
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Установка Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io -y

# Запуск и включение Docker
sudo systemctl start docker
sudo systemctl enable docker
```

### 3. Создание пользователя для деплоя
```bash
# Создание пользователя
sudo useradd -m -s /bin/bash deploy

# Добавление в группу docker
sudo usermod -aG docker deploy

# Настройка SSH доступа
sudo mkdir -p /home/deploy/.ssh
sudo chmod 700 /home/deploy/.ssh
```

### 4. Настройка firewall (опционально)
```bash
# Разрешаем SSH и HTTP
sudo ufw allow ssh
sudo ufw allow 8000
sudo ufw --force enable
```

## 🔐 Настройка SSH доступа

### Генерация SSH ключа на локальной машине:
```bash
# Генерация ключа
ssh-keygen -t rsa -b 4096 -C "deploy@your-server"

# Копирование публичного ключа на сервер
ssh-copy-id -i ~/.ssh/id_rsa.pub deploy@your-server-ip
```

### На сервере:
```bash
# Добавление публичного ключа в authorized_keys
echo "ваш_публичный_ключ" >> /home/deploy/.ssh/authorized_keys
sudo chmod 600 /home/deploy/.ssh/authorized_keys
sudo chown -R deploy:deploy /home/deploy/.ssh
```

## ⚙️ Настройка GitHub Secrets

В вашем GitHub репозитории перейдите в **Settings → Secrets and variables → Actions** и добавьте следующие секреты:

### Обязательные секреты:

| Секрет | Описание | Пример |
|--------|----------|---------|
| `SSH_HOST` | IP адрес или домен сервера | `192.168.1.100` или `your-server.com` |
| `SSH_USER` | SSH пользователь | `deploy` |
| `SSH_KEY` | Приватный SSH ключ | Содержимое `~/.ssh/id_rsa` |

### Опциональные секреты:

| Секрет | Описание | Значение по умолчанию |
|--------|----------|---------------------|
| `SSH_PORT` | SSH порт | `22` |

## 🔄 Процесс развертывания

### Автоматический деплой

1. **Push в main ветку:**
   ```bash
   git add .
   git commit -m "Deploy to production"
   git push origin main
   ```

2. **GitHub Actions выполнит:**
   - Сборку Docker образа
   - Push в GitHub Container Registry
   - Подключение к серверу по SSH
   - Остановку старого контейнера
   - Запуск нового контейнера

### Ручной деплой

Если нужно развернуть вручную:

```bash
# На сервере
# Остановка старого контейнера
docker stop test-backend || true
docker rm test-backend || true

# Логин в GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u YOUR_USERNAME --password-stdin

# Скачивание образа
docker pull ghcr.io/YOUR_USERNAME/YOUR_REPO:latest

# Запуск контейнера
docker run -d \
  --name test-backend \
  --restart unless-stopped \
  -p 8000:8000 \
  ghcr.io/YOUR_USERNAME/YOUR_REPO:latest
```

## 📊 Мониторинг и проверка

### Проверка статуса приложения:
```bash
# Проверка запущенных контейнеров
docker ps

# Просмотр логов
docker logs test-backend

# Проверка API
curl http://localhost:8000/health
curl http://localhost:8000/
```

### Полезные команды для отладки:
```bash
# Вход в контейнер
docker exec -it test-backend /bin/bash

# Просмотр системных логов
sudo journalctl -u docker -f

# Проверка открытых портов
sudo netstat -tlnp | grep 8000
```

## 🔧 Конфигурация приложения

### Переменные окружения:

Приложение поддерживает следующие переменные окружения:

| Переменная | Описание | Значение по умолчанию |
|------------|----------|---------------------|
| `HOST` | Хост для сервера | `0.0.0.0` |
| `PORT` | Порт сервера | `8000` |
| `DEBUG` | Режим отладки | `false` |

### Кастомная конфигурация:
```bash
# Запуск с кастомными настройками
docker run -d \
  --name test-backend \
  -p 9000:9000 \
  -e PORT=9000 \
  -e DEBUG=true \
  ghcr.io/YOUR_USERNAME/YOUR_REPO:latest
```

## 🚨 Troubleshooting

### Проблема: Контейнер не запускается
```bash
# Проверить логи
docker logs test-backend

# Проверить образ
docker images
docker inspect ghcr.io/YOUR_USERNAME/YOUR_REPO:latest
```

### Проблема: SSH подключение не работает
```bash
# Проверить SSH ключ
ssh -T deploy@your-server-ip

# Проверить права доступа
ls -la /home/deploy/.ssh/
```

### Проблема: Порт 8000 занят
```bash
# Проверить занятые порты
sudo netstat -tlnp | grep 8000

# Найти процесс
sudo lsof -i :8000

# Изменить порт
docker run -d --name test-backend -p 8001:8000 your-image
```

### Проблема: GitHub Actions падает
```bash
# Проверить логи Actions в GitHub
# Проверить секреты в Settings
# Проверить права доступа пользователя deploy
```

## 🔄 Обновление приложения

### Автоматическое обновление:
Просто push в main ветку - GitHub Actions сделает все автоматически.

### Ручное обновление:
```bash
# На сервере
docker pull ghcr.io/YOUR_USERNAME/YOUR_REPO:latest
docker stop test-backend
docker rm test-backend
docker run -d --name test-backend --restart unless-stopped -p 8000:8000 ghcr.io/YOUR_USERNAME/YOUR_REPO:latest
```

## 🛡️ Безопасность

### Рекомендации:
- Используйте strong SSH ключи (RSA 4096+)
- Отключите password аутентификацию для SSH
- Настройте firewall (ufw)
- Регулярно обновляйте систему
- Используйте HTTPS (настройте reverse proxy как nginx)

### Настройка nginx как reverse proxy (опционально):
```bash
# Установка nginx
sudo apt install nginx -y

# Создание конфигурации
sudo nano /etc/nginx/sites-available/test-backend
```

Пример конфигурации nginx:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Включение сайта
sudo ln -s /etc/nginx/sites-available/test-backend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 📞 Поддержка

Если возникли проблемы:
1. Проверьте логи GitHub Actions
2. Проверьте логи Docker на сервере
3. Проверьте доступность API эндпоинтов
4. Проверьте SSH подключение

Для дополнительной помощи обратитесь к документации FastAPI и Docker.
