FROM python:3.12-slim

WORKDIR /app

# Copier le code du microservice
COPY . .

# Installer Poetry et les dépendances
RUN pip install --no-cache-dir poetry && poetry install

# Lancer Uvicorn
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
