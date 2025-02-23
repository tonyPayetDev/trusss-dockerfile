import os 
import random
import base64
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Set essential values
model_id = "4w7v4jdw"
baseten_api_key = "AUmtSj8s.PbeDv3kJQtZ1XuejV0HrFv4lmS3F8vrp"

@app.route('/generate-image', methods=['GET'])
def generate_image():
    # Récupérer les paramètres depuis l'URL
    positive_prompt = request.args.get('positive_prompt', "A top down view of a river through the woods")
    negative_prompt = request.args.get('negative_prompt', "blurry, text, low quality")
    controlnet_image = request.args.get('controlnet_image', "https://storage.googleapis.com/logos-bucket-01/baseten_logo.png")
    seed = random.randint(1, 1000000)

    values = {
        "positive_prompt": positive_prompt,
        "negative_prompt": negative_prompt,
       # // "controlnet_image": controlnet_image,
        "seed": seed
    }

    try:
        # Call model endpoint
        res = requests.post(
            f"https://model-{model_id}.api.baseten.co/development/predict",
            headers={"Authorization": f"Api-Key {baseten_api_key}"},
            json={"workflow_values": values}
        )

        # Process the response
        res = res.json()
        print("Request values:", values)  # Affiche les valeurs envoyées
        print("API response:", res)  # Affiche la réponse de l'API

        if "result" in res and len(res["result"]) > 0:
            # Extraire l'image en base64
            preamble = "data:image/png;base64,"
            image_data = res["result"][0].get("data", "")

            if image_data:
                # Si l'image commence par un préambule, on le supprime et on décode
                if image_data.startswith(preamble):
                    image_data = image_data.replace(preamble, "")
                
                # Décoder l'image en base64
                output = base64.b64decode(image_data)

                # Sauvegarder l'image dans un fichier
                with open("comfyui.png", 'wb') as img_file:
                    img_file.write(output)

                # Retourner l'URL de l'image générée avec votre URL externe
                return jsonify({
                    "message": "Image generated successfully!",
                    "image_url": "http://wo4wo8owgckwkokcgcsko04s.45.90.121.197.sslip.io/comfyui.png"
                }), 200
            else:
                return jsonify({"error": "No image found in the response."}), 400
        else:
            return jsonify({"error": "API response doesn't contain a valid 'result'."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/comfyui.png', methods=['GET'])
def get_image():
    try:
        with open("comfyui.png", "rb") as img_file:
            return img_file.read(), 200, {'Content-Type': 'image/png'}
    except FileNotFoundError:
        return jsonify({"error": "Image not found."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
