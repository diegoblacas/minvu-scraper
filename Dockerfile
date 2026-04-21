FROM python:3.11-slim

# Instalar dependencias del sistema necesarias para Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libcairo2 \
    libatspi2.0-0 \
    libgtk-3-0 \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Instalar navegadores de Playwright
RUN playwright install

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
