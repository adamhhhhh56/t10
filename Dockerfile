# Базовый образ с Python 3.12
FROM python:3.12-slim

# Установим system-зависимости для nemo и звуковых пакетов
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл с зависимостями
COPY requirements.txt /app/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем весь проект
COPY . /app
WORKDIR /app

# Команда по умолчанию (можно менять на свой файл)
CMD ["python", "main.py"]
