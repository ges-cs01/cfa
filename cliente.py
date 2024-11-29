import network
import socket
import time

# Configurar Wi-Fi
ssid = 'lab8'
password = 'lab8arduino'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    time.sleep(1)

print('Conectado ao Wi-Fi com IP:', station.ifconfig()[0])

# Função para criar o cliente HTTP
def http_get(url, port=80):
    addr_info = socket.getaddrinfo(url, port)
    addr = addr_info[0][-1]
    
    s = socket.socket()
    s.connect(addr)
    s.send(b"GET / HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n".format(url))
    
    response = b""
    while True:
        chunk = s.recv(1024)
        if not chunk:
            break
        response += chunk
    
    s.close()
    return response

# Endereço do servidor (use o IP ou o nome DNS configurado)
server_url = 'esp32.local'

# Fazer a requisição GET e imprimir a resposta
response = http_get(server_url)
print("Resposta do servidor:")
print(response.decode())
