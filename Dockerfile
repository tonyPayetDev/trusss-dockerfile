# Utiliser une image de base avec Python 3.8
FROM python:3.8-slim

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Installer Truss
RUN pip install truss

# Cloner le dépôt ComfyUI et installer les dépendances
# RUN git clone https://github.com/comfyanonymous/ComfyUI.git && \
#     cd ComfyUI && \
#     git checkout b1fd26fe9e55163f780bf9e5f56bf9bf5f035c93 && \
#     pip install -r requirements.txt

# # Installer les nœuds personnalisés
# RUN cd ComfyUI/custom_nodes && \
#     git clone https://github.com/LykosAI/ComfyUI-Inference-Core-Nodes --recursive && \
#     cd ComfyUI-Inference-Core-Nodes && \
#     pip install -e .[cuda12] && \
#     cd .. && \
#     git clone https://github.com/ZHO-ZHO-ZHO/ComfyUI-Gemini --recursive && \
#     cd ComfyUI-Gemini && \
#     pip install -r requirements.txt && \
#     cd .. && \
#     git clone https://github.com/kijai/ComfyUI-Marigold --recursive && \
#     cd ComfyUI-Marigold && \
#     pip install -r requirements.txt && \
#     cd .. && \
#     git clone https://github.com/omar92/ComfyUI-QualityOfLifeSuit_Omar92 --recursive && \
#     cd .. && \
#     git clone https://github.com/Fannovel16/comfyui_controlnet_aux --recursive && \
#     cd comfyui_controlnet_aux && \
#     pip install -r requirements.txt

# # Télécharger les modèles nécessaires
# RUN cd ComfyUI/models/controlnet && \
#     wget -O control-lora-canny-rank256.safetensors [URL_DU_MODELE]

# Télécharger comfy_ui_workflow.json depuis GitHub
# RUN mkdir -p /app/data && \
#     wget -O /app/data/comfy_ui_workflow.json https://raw.githubusercontent.com/[UTILISATEUR]/[REPO]/main/data/comfy_ui_workflow.json
COPY .env /app/.env
ENV API_KEY="NrXqhEpQ.LQx9rNYXMYWlKLk2HrDYY4b8mqi9Ebl1"

# Cloner et exécuter Truss pour comfyui-truss
RUN git clone https://github.com/basetenlabs/truss-examples.git && \
    cd truss-examples/comfyui-truss && \

# Exposer le port utilisé par l'application
EXPOSE 5000

# Définir la commande de démarrage
CMD ["python", "ComfyUI/main.py", "--listen", "--port", "5000"]
