import requests
import os
import shutil

SET_ID = "me02"

if os.path.exists(f"cards/{SET_ID}/"):
    shutil.rmtree(f"cards/{SET_ID}")

os.makedirs(f"cards/{SET_ID}")

initial = requests.get(f"https://api.tcgdex.net/v2/en/sets/{SET_ID}")
initial = initial.json()

cards = initial["cards"]

for i, card in enumerate(cards):
    print(f"Downloading card {i+1}/{len(cards)}")
    image = requests.get(card["image"] + "/high.png")
    with open(f"cards/{SET_ID}/{i+1}.png", "wb") as f:
        f.write(image.content)
