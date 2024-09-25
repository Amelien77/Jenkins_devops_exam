FROM python:3.8-slim

WORKDIR /app

# Copier les fichiers requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances
RUN apt-get update \
    && apt-get install -y gcc \
    && apt-get clean \
    && pip install -r requirements.txt \
    && rm -rf /root/.cache/pip

# Copier le reste du code source dans le conteneur
COPY ./app /app

# Ajouter le répertoire actuel au PYTHONPATH pour que Python puisse trouver le module
ENV PYTHONPATH=/app

# Lancer l'application avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--
