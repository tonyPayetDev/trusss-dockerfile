import os
import random
import base64
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Set essential values
model_id = "2qjggr2q"
baseten_api_key = "AUmtSj8s.PbeDv3kJQtZ1XuejV0HrFv4lmS3F8vrp"

@app.route('/generate-image', methods=['GET'])
def generate_image():
    # Set prompts and controlnet image
    values = {
        "positive_prompt": "A top down view of a river through the woods",
        "negative_prompt": "blurry, text, low quality",
        "controlnet_image": "https://storage.googleapis.com/logos-bucket-01/baseten_logo.png",
        "seed": random.randint(1, 1000000)
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
        if "result" in res and len(res["result"]) > 0:
            # Extraire l'image en base64 (au bon endroit)
            preamble = "data:image/png;base64,"
            image_data = res["result"][0].get("data", "")

            # Vérifier si l'image est présente
            if image_data:
                # Si l'image commence par un préambule, on le supprime et on décode
                if image_data.startswith(preamble):
                    image_data = image_data.replace(preamble, "")
                
                # Décoder l'image en base64
                output = base64.b64decode(image_data)

                # Sauvegarder l'image dans un fichier
                with open("comfyui.png", 'wb') as img_file:
                    img_file.write(output)

                # Ouvrir l'image (sur Windows)
                os.system("start comfyui.png")

                return jsonify({"message": "Image generated successfully!"}), 200
            else:
                return jsonify({"error": "No image found in the response."}), 400
        else:
            return jsonify({"error": "API response doesn't contain a valid 'result'."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
