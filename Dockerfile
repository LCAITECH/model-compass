# Model Compass web app: one uvicorn worker, meant to sit behind the
# host's existing Cloudflare Tunnel (see deploy/README.md). No database
# and no background work; the dataset is read from dataset/ at startup.
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Runtime dependencies come from pyproject.toml, the single list. The
# project itself is not pip-installed: interfaces/web/app.py finds the
# dataset relative to its own file, so it has to run from this tree.
COPY pyproject.toml ./
RUN python -c "import tomllib; print('\n'.join(tomllib.load(open('pyproject.toml', 'rb'))['project']['dependencies']))" > /tmp/requirements.txt \
    && pip install -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

COPY dataset ./dataset
COPY decision ./decision
COPY interfaces ./interfaces

RUN useradd --system --no-create-home --shell /usr/sbin/nologin compass
USER compass

EXPOSE 8000

HEALTHCHECK --interval=60s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/', timeout=4)"

# --proxy-headers: cloudflared forwards the visitor's scheme and address.
CMD ["uvicorn", "interfaces.web.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--proxy-headers", "--forwarded-allow-ips", "*"]
