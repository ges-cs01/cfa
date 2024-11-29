import socket
from machine import Pin

led = Pin(2, Pin.OUT)

def web_page():
    if led.value() == 1:
        led_state = "ON"
    else:
        led_state = "OFF"

    html = """<html><head><title>ESP32 Web Server</title></head>
    <body><h1>ESP32 Web Server</h1>
    <p>LED is <strong>{}</strong></p>
    <p><a href="/?led=on"><button>Turn ON</button></a></p>
    <p><a href="/?led=off"><button>Turn OFF</button></a></p>
    </body></html>""".format(led_state)
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)

    if '/?led=on' in request:
        led.value(1)
    if '/?led=off' in request:
        led.value(0)

    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()