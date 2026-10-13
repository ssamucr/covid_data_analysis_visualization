FROM python:3.11-slim

# Hugging Face Spaces ejecuta el contenedor como usuario 1000
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"
WORKDIR /home/user/app

COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY --chown=user . .

# Spaces expone el puerto 7860. Un solo worker con hilos: el dataset (~250 MB en memoria) se carga una vez.
EXPOSE 7860
CMD ["gunicorn", "main:server", "--bind", "0.0.0.0:7860", "--workers", "1", "--threads", "4", "--timeout", "120"]
