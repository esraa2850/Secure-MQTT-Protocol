# src/config.py
# Configuration file for MQTT secure communication

import os
from pathlib import Path

# Get the project root directory
BASE_DIR = Path(__file__).parent.parent

# Certificate paths
CERTS_DIR = BASE_DIR / "certs"
PRIVATE_DIR = BASE_DIR / "private"

# MQTT Broker settings
BROKER_HOST = "localhost"
BROKER_PORT = 8883

# Certificate files
CA_CERT = str(CERTS_DIR / "ca.crt")
CLIENT_CERT = str(CERTS_DIR / "robot1.crt")
CLIENT_KEY = str(PRIVATE_DIR / "robot1.key")

# JWT settings
JWT_SECRET = "industrial-secret"
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 1

# MQTT Topics
TOPIC_STATUS = "factory/robot1/status"
TOPIC_COMMAND = "factory/robot1/command"
TOPIC_ALERT = "factory/robot1/alert"
