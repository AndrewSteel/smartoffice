from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId
import shutil
import os
import requests

app = FastAPI()

# MongoDB-Verbindung
client = MongoClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
db = client.smartoffice
images = db.images

UPLOAD_DIR = "./uploads"
OLLAMA_CLIENT_URL = os.getenv("OLLAMA_CLIENT_URL", "http://ollama-client:5001/describe")

# CORS für das Web-Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/images/")
def list_images():
    all_images = list(images.find())
    for img in all_images:
        img["id"] = str(img["_id"])
        del img["_id"]
    return all_images

import paho.mqtt.publish as publish

MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt")
MQTT_TOPIC = "smartoffice/image/uploaded"

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    # ... (wie vorher: speichern, Mongo-Eintrag)

    # MQTT-Nachricht senden
    publish.single(
        topic=MQTT_TOPIC,
        payload=json.dumps({"image_id": image_id, "path": file_path}),
        hostname=MQTT_BROKER
    )

    return {"message": "Bild hochgeladen", "id": image_id}
