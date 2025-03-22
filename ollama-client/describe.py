import paho.mqtt.client as mqtt
import json
import subprocess
import os
from pymongo import MongoClient

MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llava")
TOPIC_IN = "smartoffice/image/uploaded"
TOPIC_OUT = "smartoffice/image/described"

mongo = MongoClient(os.getenv("MONGO_URL", "mongodb://mongo:27017"))
images = mongo.smartoffice.images

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    path = data["path"]
    image_id = data["image_id"]

    result = subprocess.run(
        ["ollama", "run", OLLAMA_MODEL, "--image", path, "Beschreibe den Bildinhalt."],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    description = result.stdout.decode("utf-8").strip()

    # In DB schreiben
    images.update_one({"_id": image_id}, {"$set": {"description": description}})

    # Rückmeldung per MQTT
    client.publish(TOPIC_OUT, json.dumps({"image_id": image_id, "description": description}))

client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER)
client.subscribe(TOPIC_IN)
client.loop_forever()
