FROM python:3.8-slim

WORKDIR /app

# Copier les fichiers requirements.txt dans le conteneur
COPY requirements.txt /app/

# Installer les dépendances
RUN apt-get update \
    && apt-get install -y gcc \
    && apt-get clean \
    && pip install --no-cache-dir -r requirements.txt

# Copier le reste du code source dans le conteneur
COPY . /app/

# Changer le répertoire de travail pour que `uvicorn` trouve le module correctement
WORKDIR /app/app

# Définir la commande par défaut
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
