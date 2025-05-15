import paho.mqtt.client as mqtt
import json

BROKER = "broker.hivemq.com"
OUTPUT_FILE = "keepquiet_mac_data.jsonl"
TOPIC = "keepquiet/status"

# Callback appelé quand un message est reçu
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)

        print(f"📥 Reçu : {data}")

        # Sauvegarde dans un fichier JSON Lines
        with open(OUTPUT_FILE, "a") as f:
            f.write(json.dumps(data) + "\n")

    except Exception as e:
        print(f"⚠️ Erreur lors du traitement du message : {e}")

# Initialisation du client MQTT
client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.subscribe(TOPIC)

print(f"🟢 Abonné au topic '{TOPIC}' sur {BROKER}")
client.loop_forever()
