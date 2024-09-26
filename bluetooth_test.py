import bluetooth
import time

# Create a BLE object
ble = bluetooth.BLE()

# Activate BLE
ble.active(True)

# Define UUIDs
SERVICE_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef0")
CHARACTERISTIC_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef1")

# Create a characteristic
characteristic = (CHARACTERISTIC_UUID, bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY)

# Create a service
service = (SERVICE_UUID, (characteristic,))

# Register the service
try:
    ble.gatts_register_services((service,))
    print("Services registered.")
except Exception as e:
    print("Failed to register services:", e)

# Start advertising
def advertise():
    # Construct the advertising data
    advertising_data = (
        b'\x02\x01\x06' +                     # Flags
        b'\x03\x03' + SERVICE_UUID[4:6] + b'\x00' +  # Service UUID
        b'\x0F\x09' + b'My ESP32 BLE'         # Complete Local Name
    )
    ble.gap_advertise(100, advertising_data)

advertise()
print("Advertising started. Waiting for connections...")

# Main loop
while True:
    time.sleep(1)
