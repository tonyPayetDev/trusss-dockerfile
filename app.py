import os
import random
import base64
import requests
from flask import Flask, jsonify, request, send_file
from PIL import Image
from io import BytesIO
import uuid

app = Flask(__name__)

# Charger les variables d'environnement
MODEL_ID = os.getenv("MODEL_ID", "4w7v4jdw")
BASETEN_API_KEY = os.getenv("BASETEN_API_KEY", "AUmtSj8s.PbeDv3kJQtZ1XuejV0HrFv4lmS3F8vrp")

# Dossier pour stocker les images générées
OUTPUT_DIR = "generated_images"
IMAGE_PATH = "comfyui.png"

def generate_image():
    """Appelle l'API Baseten et enregistre l'image générée avec des logs détaillés."""
    values = {
        "positive_prompt": "A beautiful sunset over the ocean",
        "negative_prompt": "blurry, dark, low quality",
        "controlnet_image": "https://storage.googleapis.com/logos-bucket-01/baseten_logo.png",
        "seed": random.randint(1, 1000000)
    }

    print("🚀 Envoi de la requête à l'API Baseten...")
    print(f"🔹 Données envoyées : {values}")

    try:
        res = requests.post(
            f"https://model-{MODEL_ID}.api.baseten.co/development/predict",
            headers={"Authorization": f"Api-Key {BASETEN_API_KEY}"},
            json={"workflow_values": values}
        )

        print(f"📡 Réponse reçue - Code HTTP : {res.status_code}")

        if res.status_code == 200:
            res_json = res.json()
            print(f"✅ Réponse JSON : {res_json}")

            if "result" in res_json and len(res_json["result"]) > 1 and "image" in res_json["result"][1]:
                preamble = "data:image/png;base64,"
                image_data = res_json["result"][1]["image"]

                print(f"🖼️ Extraction de l'image base64 (taille : {len(image_data)} caractères)...")

                output = base64.b64decode(image_data.replace(preamble, ""))

                with open(IMAGE_PATH, "wb") as img_file:
                    img_file.write(output)

                print(f"✅ Image enregistrée : {IMAGE_PATH}")
            else:
                print("⚠️ Format de réponse inattendu :", res_json)

        else:
            print(f"❌ Erreur API - Statut {res.status_code} : {res.text}")

    except Exception as e:
        print(f"❌ Exception lors de la requête : {e}")

@app.route("/get-image", methods=["GET"])
def get_image():
    """Endpoint API pour récupérer l'image enregistrée."""
    print("📡 Requête reçue : /get-image")
    
    if os.path.exists(IMAGE_PATH):
        print(f"✅ Envoi de l'image {IMAGE_PATH}...")
        return send_file(IMAGE_PATH, mimetype="image/png")
    else:
        print("❌ Erreur : Image non trouvée")
        return {"error": "Image non trouvée"}, 404
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
