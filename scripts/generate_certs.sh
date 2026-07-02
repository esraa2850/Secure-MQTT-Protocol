#!/bin/bash
# Script to generate certificates
# This script creates all required certificates for MQTT TLS

# Create CA certificate
openssl genrsa -out private/ca.key 4096
openssl req -x509 -new -key private/ca.key -sha256 -days 365 -out certs/ca.crt -subj "/C=EG/ST=Cairo/L=Cairo/O=IndustrialCybersecurity/OU=MQTT Security/CN=Industrial CA"

# Create Server certificate
openssl genrsa -out private/server.key 2048
openssl req -new -key private/server.key -out server.csr -subj "/C=EG/ST=Cairo/L=Cairo/O=IndustrialCybersecurity/OU=MQTT Security/CN=localhost"
openssl x509 -req -in server.csr -CA certs/ca.crt -CAkey private/ca.key -CAcreateserial -out certs/server.crt -days 365 -sha256
rm server.csr

# Create Client certificate (robot1)
openssl genrsa -out private/robot1.key 2048
openssl req -new -key private/robot1.key -out robot1.csr -subj "/C=EG/ST=Cairo/L=Cairo/O=IndustrialCybersecurity/OU=MQTT Security/CN=robot1"
openssl x509 -req -in robot1.csr -CA certs/ca.crt -CAkey private/ca.key -CAcreateserial -out certs/robot1.crt -days 365 -sha256
rm robot1.csr

# Set permissions
chmod 600 private/*.key
chmod 644 certs/*.crt

echo "✅ Certificates generated successfully!"
