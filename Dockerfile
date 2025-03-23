FROM python:3.11

RUN apt -qq update && \
    apt -qq install -y --no-install-recommends \
    ffmpeg \
    curl \
    git \
    gnupg2 \
    unzip \
    wget \
    python3-dev \
    python3-pip \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavfilter-dev \
    libavutil-dev \
    libswscale-dev \
    libswresample-dev \
    neofetch && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/

WORKDIR /usr/src/app

ENV UV_CACHE_DIR=/usr/src/app/.cache/uv

RUN pip install --no-cache-dir uv

COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

COPY . .

RUN mkdir -p AkenoX/plugins \
    && chown -R 1000:0 . \
    && chmod -R 777 /usr/src/app \
    && chmod -R 777 /usr

COPY start.sh /usr/src/app/start.sh
RUN chmod +x /usr/src/app/start.sh
CMD ["/usr/src/app/start.sh"]
