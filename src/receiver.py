# src/receiver.py
# MQTT Subscriber (Receiver) - Listens for messages from robots

import paho.mqtt.client as mqtt
import json
import logging
import sys
import time

from config import *
from jwt_token import generate_token

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class MQTTSecureReceiver:
    def __init__(self, client_id="robot1-receiver"):
        self.client_id = client_id
        self.client = None
        self.connected = False
        self.message_count = 0
        self.jwt_token = generate_token("robot1", "subscriber")
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
            self.client.on_message = self.on_message
            self.client.on_subscribe = self.on_subscribe
            
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
            self.client.subscribe(TOPIC_STATUS, qos=1)
            self.client.subscribe(TOPIC_COMMAND, qos=1)
            self.client.subscribe(TOPIC_ALERT, qos=1)
            logger.info(f"📡 Subscribed to topics")
        else:
            self.connected = False
            logger.error(f"❌ Connection failed with code: {rc}")
    
    def on_disconnect(self, client, userdata, rc):
        self.connected = False
        logger.warning(f"⚠️ Disconnected (code: {rc})")
    
    def on_subscribe(self, client, userdata, mid, granted_qos):
        logger.info(f"📋 Subscription confirmed (MID: {mid})")
    
    def on_message(self, client, userdata, msg):
        self.message_count += 1
        
        try:
            payload = json.loads(msg.payload.decode('utf-8'))
        except json.JSONDecodeError:
            payload = msg.payload.decode('utf-8')
        
        logger.info(f"📩 Message #{self.message_count} received")
        logger.info(f"   📌 Topic: {msg.topic}")
        logger.info(f"   📦 Payload: {json.dumps(payload, indent=2) if isinstance(payload, dict) else payload}")
        
        if msg.topic == TOPIC_STATUS:
            self.process_status_message(payload)
        
        print("-" * 60)
    
    def process_status_message(self, payload):
        if not isinstance(payload, dict):
            return
        
        device_id = payload.get('device_id', 'unknown')
        sensor_data = payload.get('sensor_data', {})
        
        print("\n📊 ROBOT STATUS UPDATE")
        print(f"   🤖 Device: {device_id}")
        print(f"   🌡️ Temperature: {sensor_data.get('temperature', 'N/A')}°C")
        print(f"   💧 Humidity: {sensor_data.get('humidity', 'N/A')}%")
        print(f"   📊 Pressure: {sensor_data.get('pressure', 'N/A')} hPa")
        
        temp = sensor_data.get('temperature', 0)
        if temp > 30:
            logger.warning(f"⚠️ High temperature alert: {temp}°C")
    
    def disconnect(self):
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            logger.info(f"👋 Disconnected. Total messages: {self.message_count}")

if __name__ == "__main__":
    print("=" * 60)
    print("👂 MQTT SECURE RECEIVER ")
    print("=" * 60)
    
    receiver = MQTTSecureReceiver("robot1-receiver")
    
    if not receiver.connect():
        print("❌ Failed to connect. Exiting...")
        sys.exit(1)
    
    print("\n📡 Listening for messages...")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("🛑 Stopping receiver...")
        receiver.disconnect()
        print("🏁 Program terminated")
