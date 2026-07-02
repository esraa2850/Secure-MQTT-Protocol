# src/sender.py
# MQTT Publisher (Sender) - Simulates a robot sending sensor data

import paho.mqtt.client as mqtt
import json
import time
import logging
import sys
from datetime import datetime

from config import *
from jwt_token import generate_token

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class MQTTSecureSender:
    def __init__(self, client_id="robot1-sender"):
        self.client_id = client_id
        self.client = None
        self.connected = False
        self.jwt_token = generate_token("robot1", "publisher")
        logger.info(f"🔑 JWT Token generated")
    
    def connect(self):
        try:
            self.client = mqtt.Client(
                client_id=self.client_id,
                clean_session=True,
                protocol=mqtt.MQTTv311
            )
            
            # TLS Configuration
            self.client.tls_set(
                ca_certs=CA_CERT,
                certfile=CLIENT_CERT,
                keyfile=CLIENT_KEY,
                cert_reqs=mqtt.ssl.CERT_REQUIRED,
                tls_version=mqtt.ssl.PROTOCOL_TLSv1_2
            )
            
            # JWT Authentication
            self.client.username_pw_set(
                username="robot1",
                password=self.jwt_token
            )
            
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            self.client.on_publish = self.on_publish
            
            logger.info(f"🔗 Connecting to {BROKER_HOST}:{BROKER_PORT}...")
            self.client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
            self.client.loop_start()
            time.sleep(1)
            return self.connected
            
        except Exception as e:
            logger.error(f"❌ Connection failed: {e}")
            return False
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            logger.info("✅ Successfully connected to MQTT broker!")
        else:
            self.connected = False
            logger.error(f"❌ Connection failed with code: {rc}")
    
    def on_disconnect(self, client, userdata, rc):
        self.connected = False
        logger.info("🔌 Disconnected from broker")
    
    def on_publish(self, client, userdata, mid):
        logger.info(f"📤 Message published (ID: {mid})")
    
    def send_sensor_data(self, temperature, humidity, pressure=1013):
        if not self.connected:
            logger.error("❌ Not connected to broker!")
            return False
        
        payload = {
            "device_id": "robot1",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "sensor_data": {
                "temperature": temperature,
                "humidity": humidity,
                "pressure": pressure
            },
            "message_type": "telemetry"
        }
        
        message = json.dumps(payload)
        result = self.client.publish(
            topic=TOPIC_STATUS,
            payload=message,
            qos=1,
            retain=False
        )
        
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            logger.info(f"📨 Sent: {message[:100]}...")
            return True
        else:
            logger.error(f"❌ Failed to publish")
            return False
    
    def disconnect(self):
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            logger.info("👋 Disconnected cleanly")

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 MQTT SECURE SENDER - Graduation Project")
    print("=" * 60)
    
    sender = MQTTSecureSender("robot1-sender")
    
    if not sender.connect():
        print("❌ Failed to connect. Exiting...")
        sys.exit(1)
    
    print("\n📊 Sending sensor data...")
    print("-" * 40)
    
    # Send multiple readings
    readings = [
        (25.5, 65.2, 1013.0),
        (26.1, 63.8, 1012.8),
        (24.9, 67.5, 1013.2),
        (25.8, 64.1, 1013.1),
        (26.4, 62.0, 1012.9)
    ]
    
    for i, (temp, hum, press) in enumerate(readings, 1):
        print(f"\n📡 Reading #{i}:")
        print(f"   🌡️ Temperature: {temp}°C")
        print(f"   💧 Humidity: {hum}%")
        print(f"   📊 Pressure: {press} hPa")
        
        success = sender.send_sensor_data(temp, hum, press)
        print(f"   {'✅' if success else '❌'} Message {'sent' if success else 'failed'}")
        time.sleep(2)
    
    print("\n" + "=" * 60)
    sender.disconnect()
    print("🏁 Program completed!")
