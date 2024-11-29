import network
import time
from microDNSSrv import MicroDNSSrv

# Configurar Wi-Fi
ssid = 'lab8'
password = 'la8arduino'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    time.sleep(1)

print('Conectado ao Wi-Fi com IP:', station.ifconfig()[0])

# Iniciar servidor DNS
dns = MicroDNSSrv.Create({ "esp32.local": station.ifconfig()[0] })

print("Servidor DNS rodando! Acesse o ESP32 em: http://esp32.local")

# Manter o código rodando indefinidamente
while True:
    time.sleep(1)
