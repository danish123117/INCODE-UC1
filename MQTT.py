import paho.mqtt.client as mqtt
import json
from datetime import datetime
import random
import time

# MQTT broker details
broker_address = "127.0.0.1"
broker_port = 1883
topic = "json/danishabbas/EMG1000/attrs"

# Function to generate random heart rate data
def generate_heart_rate_data(index):
    c = []
    for i in range(8):
        c.append(random.random() * 0.02)
    return {
        "TimeStamp": datetime.now().isoformat(),
        "index": index,
        "data": c,
        "Feaisability": [True, True, True, True, True, True, True, True]
    }

# MQTT on_connect callback
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print(f"Connection failed with code {rc}")

# Create an MQTT client instance
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

# Set the on_connect callback
client.on_connect = on_connect

# Connect to the MQTT broker
client.connect(broker_address, broker_port, 60)

# Start the MQTT loop
client.loop_start()
index = 0
try:
    while True:
        # Generate random heart rate data
        heart_rate_data = generate_heart_rate_data(index)
        index += 1
        # Convert data to JSON format
        json_data = json.dumps(heart_rate_data)

        # Publish the JSON message to the specified topic
        client.publish(topic, json_data)

        # Print the published message
        print(f"Published: {json_data}")

        # Wait for a while before publishing the next message
        time.sleep(5)

except KeyboardInterrupt:
    # Handle keyboard interrupt (Ctrl+C) to gracefully disconnect from MQTT broker
    print("Disconnecting from MQTT broker")
    client.disconnect()
    client.loop_stop()

#        "device_id": "EMG1000",