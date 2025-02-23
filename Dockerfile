FROM python:3.8-slim

# Installer les dépendances système nécessaires et nettoyer les caches pour réduire la taille de l'image
RUN apt-get update && apt-get install -y \
    git \
    wget \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Installer truss avec les détails du processus
RUN pip install --upgrade truss -v

# Si tu as d'autres dépendances à installer via un fichier requirements.txt, tu peux ajouter ces lignes :
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# Démarrer le terminal bash
CMD [ "bash" ]
