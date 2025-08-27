FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m appuser
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
# fly 上会把 /data 挂载成卷；这里 mkdir 不冲突，只是确保目录存在与权限正确
RUN mkdir -p /data && chown -R appuser:appuser /data /app
USER appuser

# 👇 关键：让你的应用按照 _resolve_db_uri() 逻辑优先用这个环境变量
ENV FLASK_ENV=production \
    CACHE_TTL_SECONDS=600 \
    DATABASE_URL=sqlite:////data/banff.db

EXPOSE 8000
CMD ["gunicorn", "-w", "2", "-k", "gthread", "-b", "0.0.0.0:8000", "wsgi:app"]
