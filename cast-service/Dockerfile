FROM python:3.8-slim

WORKDIR /app

# Copier les fichiers requirements.txt dans le conteneur
COPY requirements.txt ./

# Installer les dépendances
RUN apt-get update \
    && apt-get install -y gcc \
    && apt-get clean \
    && pip install -r requirements.txt \
    && rm -rf /root/.cache/pip

# Copier le reste du code source dans le conteneur
COPY ./app ./app

# Changer le répertoire de travail pour que `python` trouve le module correctement
WORKDIR /app/app

# Définir la commande par défaut
CMD ["python", "main.py"]
