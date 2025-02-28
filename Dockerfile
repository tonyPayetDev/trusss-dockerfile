FROM python:3.8-slim

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    git \
    wget \
    python3-pip \
    bash \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Cloner le repo Baseten si nécessaire
RUN git clone https://github.com/basetenlabs/truss-examples.git

# Copier les fichiers dans /app
COPY app.py mon_script.py config.yaml /app/

# Créer le dossier "data" et y copier le fichier comfy_ui_workflow.json
RUN mkdir -p /app/data
COPY data/comfy_ui_workflow.json /app/data/

# Créer le dossier models/controlnet
RUN mkdir -p /app/models/controlnet

# Installer les dépendances Python
RUN pip install Flask pillow --no-cache-dir
RUN pip install --upgrade truss -v --no-cache-dir

# Exposer le port 5000
EXPOSE 5000

# Lancer le serveur Flask
CMD ["python", "app.py"]
