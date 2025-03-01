import os
import random
import base64
import requests
from flask import Flask, jsonify, request, send_file
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Set essential values
model_id = "v316pljq"
baseten_api_key = "1VlO7CAN.VepxLs43kkaBjAvOzfdACHLsFaR6QzQP"

def encode_image_to_base64(image_url):
    response = requests.get(image_url)
    return base64.b64encode(response.content).decode("utf-8")

@app.route('/generate-image', methods=['GET'])
def generate_image():
    positive_prompt = request.args.get('positive_prompt', "A top down view of a river through the woods")
    negative_prompt = request.args.get('negative_prompt', "blurry, text, low quality")
    controlnet_image = request.args.get('controlnet_image', "https://storage.googleapis.com/logos-bucket-01/baseten_logo.png")
    seed = random.randint(1, 10)

    values = {
        "positive_prompt": positive_prompt,
        "negative_prompt": negative_prompt,
        "controlnet_image": "https://storage.googleapis.com/logos-bucket-01/baseten_logo.png",
        "seed": seed
    }

    try:
        # Call model endpoint
        res = requests.post(
            f"https://model-{model_id}.api.baseten.co/environments/production/predict",
            headers={"Authorization": f"Api-Key {baseten_api_key}"},
            json={"workflow_values": values}
        )

        res = res.json()
        print("API response:", res)

        if "result" in res and len(res["result"]) > 1:
            preamble = "data:image/png;base64,"
            image_data = res["result"][1].get("image", "")

            if image_data.startswith(preamble):
                image_data = image_data.replace(preamble, "")

            img_bytes = base64.b64decode(image_data)

            # Sauvegarder l'image dans /mnt/data/
            image_path = "/mnt/data/comfyui.png"
            with open(image_path, 'wb') as img_file:
                img_file.write(img_bytes)

            # Ouvrir l'image (si en local)
            os.system(f"open {image_path}")

            return jsonify({
                "message": "Image generated successfully!",
                "image_url": "/get-image"
            }), 200
        else:
            return jsonify({"error": "No valid image found in response."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour récupérer l'image
@app.route('/get-image', methods=['GET'])
def get_image():
    image_path = "/mnt/data/comfyui.png"
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/png')
    else:
        return jsonify({"error": "Image not found."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
