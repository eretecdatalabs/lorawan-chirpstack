import paho.mqtt.client as mqtt
import json
from datetime import datetime

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        filename = f"lorawan_{datetime.now().strftime('%Y%m%d')}.json"
        with open(filename, "a", encoding='utf-8') as f:
            json.dump(payload, f)
            f.write("\n")
        print(f"Message received on topic: {msg.topic}")
        print(f"Payload saved to: {filename}")
    except Exception as e:
        print(f"Error processing message: {e}")
        print(f"Topic: {msg.topic}")
        print(f"Raw payload: {msg.payload}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("localhost", 1883, 60)
client.subscribe("application/+/device/+/event/up")
client.on_message = on_message

print("Connecting to MQTT broker...")
client.loop_forever()