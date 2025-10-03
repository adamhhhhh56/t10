FROM vastai/pytorch:latest

# System deps + build tools
RUN apt-get update && apt-get install -y \
    ffmpeg git build-essential libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip/setuptools
RUN pip install --upgrade pip setuptools wheel packaging Cython

# Копируем зависимости без NeMo GitHub
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Ставим NeMo toolkit[all] + GitHub ASR пакет в один шаг
RUN pip install --upgrade --ignore-installed \
    nemo_toolkit[all] \
    "git+https://github.com/NVIDIA/NeMo.git@main#egg=nemo_toolkit[asr]"

# Копируем проект
COPY . /app
WORKDIR /app

CMD ["python", "main.py"]
