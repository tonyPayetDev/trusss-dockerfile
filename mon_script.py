
import os
import random
import base64
import requests

# Set essential values
model_id = "4w7v4jdw"
baseten_api_key = "AUmtSj8s.PbeDv3kJQtZ1XuejV0HrFv4lmS3F8vrp"
# Set prompts and controlnet image
values = {
  "positive_prompt": "A top down view of a river through the woods",
  "negative_prompt": "blurry, text, low quality",
  "controlnet_image": "https://storage.googleapis.com/logos-bucket-01/baseten_logo.png",
  "seed": random.randint(1, 1000000)
}
# Call model endpoint
res = requests.post(
    f"https://model-{model_id}.api.baseten.co/development/predict",
    headers={"Authorization": f"Api-Key {baseten_api_key}"},
    json={"workflow_values": values}
)
# Get output image
res = res.json()
if "result" in res and len(res["result"]) > 0:
    try:
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
        else:
            print("Erreur : Aucune image trouvée dans la réponse.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
else:
    print("Erreur : La réponse API ne contient pas suffisamment d'éléments dans 'result'.")
