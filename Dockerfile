FROM python:3.8-slim

# Installer les dépendances système nécessaires et nettoyer les caches pour réduire la taille de l'image
# Installer les dépendances système nécessaires, bash et nettoyer les caches pour réduire la taille de l'image
RUN apt-get update && apt-get install -y \
    git \
    wget \
    python3-pip \
    bash \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier de l'application (assure-toi que `app.py` est dans le même dossier que ton Dockerfile)
COPY app.py .

# Installer Flask
RUN pip install Flask
RUN pip install --upgrade truss -v


# Exposer le port 5000 pour accéder au serveur
EXPOSE 5000
RUN git clone https://github.com/basetenlabs/truss-examples.git
COPY mon_script.py truss-examples/comfyui-truss/
COPY app.py truss-examples/comfyui-truss/

# Changer le répertoire de travail vers "comfyui-truss"
WORKDIR /app/truss-examples/comfyui-truss

# Lancer le serveur Flask
CMD ["python", "app.py"]
#CMD [ "bash" ]

