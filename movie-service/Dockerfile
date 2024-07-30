FROM python:3.8-slim

WORKDIR /app

# Copier les fichiers requirements.txt dans le conteneur
COPY requirements.txt /app/requirements.txt

# Installer les dépendances
RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean \
    && pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

# Copier le reste du code source dans le conteneur
COPY . /app/

# Définir la commande par défaut
CMD ["python", "app/main.py"]
