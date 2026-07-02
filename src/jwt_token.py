# src/jwt_token.py
# JWT Token Generator for MQTT Authentication

import jwt
import datetime
from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRY_HOURS

def generate_token(device_id="robot1", role="publisher"):
    """
    Generate a JWT token for MQTT authentication
    
    Args:
        device_id (str): The device identifier
        role (str): The role of the device
    
    Returns:
        str: JWT token string
    """
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXPIRY_HOURS)
    
    payload = {
        "device": device_id,
        "role": role,
        "exp": expiration_time,
        "iat": datetime.datetime.utcnow(),
        "iss": "graduation-project",
        "aud": "mosquitto-broker"
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def decode_and_verify_token(token):
    """
    Decode and verify a JWT token
    
    Args:
        token (str): The JWT token to verify
    
    Returns:
        dict: The decoded payload if valid
    """
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        print(f"✅ Token is valid for device: {decoded.get('device')}")
        return decoded
    except jwt.ExpiredSignatureError:
        print("❌ Token has expired!")
        return None
    except jwt.InvalidTokenError as e:
        print(f"❌ Invalid token: {e}")
        return None

if __name__ == "__main__":
    print("🔑 Generating test token...")
    token = generate_token("robot1", "publisher")
    print(f"Token: {token}\n")
    
    print("🔍 Verifying token...")
    decode_and_verify_token(token)
