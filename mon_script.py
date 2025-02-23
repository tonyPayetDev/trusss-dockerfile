
import os
import random
import base64
import requests

# Set essential values
model_id = "2qjggr2q"
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
import requests
import base64
import os

# Effectuer la requête POST à l'API
res = requests.post(
    f"https://model-{model_id}.api.baseten.co/development/predict",
    headers={"Authorization": f"Api-Key {baseten_api_key}"},
    json={"workflow_values": values}
)

# Récupérer la réponse JSON
res = res.json()

# Vérifier que la réponse contient bien la clé "result" et qu'elle a des éléments
if "result" in res and len(res["result"]) > 1:
    preamble = "data:image/png;base64,"
    try:
        # Décoder l'image en base64
        output = base64.b64decode(res["result"][1]["image"].replace(preamble, ""))
        
        # Sauvegarder l'image dans un fichier
        with open("comfyui.png", 'wb') as img_file:
            img_file.write(output)

        # Ouvrir l'image (sur macOS, sinon adapte à ton OS)
        os.system("open comfyui.png")

    except KeyError as e:
        print(f"Erreur: La clé 'image' est manquante dans la réponse ou la structure est incorrecte. ({e})")
    except Exception as e:
        print(f"Erreur lors du traitement de l'image: {e}")
else:
    print("Erreur : La réponse API ne contient pas suffisamment d'éléments dans 'result'.")
