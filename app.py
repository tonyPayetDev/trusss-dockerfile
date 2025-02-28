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
os.makedirs(OUTPUT_DIR, exist_ok=True)

def pil_to_b64(pil_img):
    """Convertit une image PIL en base64."""
    buffered = BytesIO()
    pil_img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

@app.route('/generate-image', methods=['POST'])
def generate_image():
    """Génère une image en appelant l'API Baseten et renvoie une URL accessible."""
    try:
        data = request.json

        positive_prompt = data.get("positive_prompt", "A top down view of a river through the woods")
        negative_prompt = data.get("negative_prompt", "blurry, text, low quality")
        controlnet_image = data.get("controlnet_image")
        seed = random.randint(1, 1000000)  # Génère un seed aléatoire

        # Vérifier si une image locale est fournie
        if controlnet_image and os.path.exists(controlnet_image):
            with Image.open(controlnet_image) as img:
                controlnet_image = {"type": "image", "data": pil_to_b64(img)}
        elif isinstance(controlnet_image, str) and controlnet_image.startswith("http"):
            controlnet_image = {"type": "url", "data": controlnet_image}
        else:
            return jsonify({"error": "Image locale non trouvée ou URL invalide."}), 400

        values = {
            "positive_prompt": positive_prompt,
            "negative_prompt": negative_prompt,
            "controlnet_image": controlnet_image,
            "seed": seed
        }

        print(f"🔹 Requête envoyée avec : {values}")

        # Appel à l'API Baseten
        response = requests.post(
            f"https://model-{MODEL_ID}.api.baseten.co/development/predict",
            headers={"Authorization": f"Api-Key {BASETEN_API_KEY}"},
            json={"workflow_values": values}
        )

        response_json = response.json()
        print(f"🔹 Réponse de l'API : {response_json}")

        # Vérifier si l'API retourne une image en base64
        if "result" in response_json and response_json["result"]:
            image_data = response_json["result"][0].get("data", "")

            if image_data.startswith("data:image/png;base64,"):
                image_data = image_data.replace("data:image/png;base64,", "")

            # Générer un nom unique pour l'image
            image_filename = f"{uuid.uuid4().hex}.png"
            image_path = os.path.join(OUTPUT_DIR, image_filename)

            # Décoder et sauvegarder l'image
            with open(image_path, "wb") as img_file:
                img_file.write(base64.b64decode(image_data))

            # Construire l'URL de l'image
            image_url = f"http://{request.host}/images/{image_filename}"

            return jsonify({
                "message": "Image générée avec succès !",
                "image_url": image_url
            }), 200
        else:
            return jsonify({"error": "La réponse de l'API ne contient pas d'image valide."}), 400

    except Exception as e:
        print(f"⚠️ Erreur : {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/images/<filename>', methods=['GET'])
def get_image(filename):
    """Retourne l'image générée via une URL publique."""
    image_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/png')
    return jsonify({"error": "Image non trouvée."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
