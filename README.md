# 🔐 Secure MQTT Communication System for Industrial IoT

## 📌 Project Overview
This project implements a secure MQTT communication system for industrial IoT environments with:

- **TLS 1.2** encryption for secure data transmission
- **X.509 Client Certificates** for device authentication
- **JWT (JSON Web Tokens)** for authorization
- **Non-Repudiation** through digital signatures

## 🏗️ System Architecture
Robot (Sender) ---[TLS + Certificates]---> Mosquitto Broker ---> Receiver (Subscriber)
|
v
JWT Token Validation

## 🔒 Security Features
| Feature | Implementation |
|---------|---------------|
| Encryption | TLS 1.2 |
| Authentication | X.509 Certificates |
| Authorization | JWT Tokens |
| Non-Repudiation | Digital Signatures |
| Integrity | TLS Encryption |

## 📋 Prerequisites
- Linux (Kali/Ubuntu)
- Python 3.8+
- Mosquitto MQTT Broker
- OpenSSL

## 🚀 Installation

### 1. Install System Dependencies
```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients openssl python3-pip -y
