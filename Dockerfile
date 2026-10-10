FROM python:3.14.8-slim@sha256:a2b82f3c48559aa0a8446d9af49826b6e2b2016f4cd2afabfe6013ec53729170

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update \
    && apt-get install --yes --no-install-recommends --only-upgrade \
        gzip=1.13-1+deb13u1 \
        libc-bin=2.41-12+deb13u4 \
        libc6=2.41-12+deb13u4 \
        libpcre2-8-0=10.46-1~deb13u3 \
        libsqlite3-0=3.46.1-7+deb13u2 \
        libssl3t64=3.5.7-1~deb13u3 \
        openssl=3.5.7-1~deb13u3 \
        openssl-provider-legacy=3.5.7-1~deb13u3 \
        perl-base=5.40.1-6+deb13u1 \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --system --gid 10001 bot \
    && useradd --system --uid 10001 --gid bot --home-dir /app --no-create-home bot

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir --requirement requirements.txt \
    && python -m pip uninstall --yes setuptools pip

COPY --chown=bot:bot bot.py ./

USER 10001:10001

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD ["python", "-c", "import os; os.kill(1, 0)"]

CMD ["python", "bot.py"]
