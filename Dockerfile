FROM python:3.8
# Autres instructions

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    git \
    wget \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Installer truss avec plus de détails dans le processus
RUN pip install --upgrade truss -v

# Démarrer le terminal bash
EXPOSE 5000

CMD ["sh", "-c"]
