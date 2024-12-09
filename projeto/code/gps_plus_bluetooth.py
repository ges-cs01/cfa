import bluetooth
import time
from machine import Pin, Timer, UART
import ustruct
from micropyGPS import MicropyGPS

# Configuração do pino para o LED
led = Pin(2, Pin.OUT)

# Configuração do GPS (UART1 - GPIO 16 e GPIO 17)
gps_uart = UART(1, baudrate=9600, tx=17, rx=16)
gps = MicropyGPS(9)  # Inicia a instância do MicropyGPS com o fuso horário local

# Função para converter as coordenadas GPS para formato decimal, incluindo o sinal de negativo
def to_decimal(degrees, minutes, hemisphere):
    decimal_value = degrees + (minutes / 60)
    if hemisphere in ['S', 'W']:  # Se o hemisfério for sul ou oeste, o valor será negativo
        decimal_value = -decimal_value
    return decimal_value

# Criação do servidor Bluetooth
class ESP32_BLE:
    def __init__(self, name):
        self.led = Pin(2, Pin.OUT)
        self.timer1 = Timer(0)
        self.name = name
        self.ble = bluetooth.BLE()
        self.ble.active(True)
        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()

        # Store the received message
        self.ble_msg = ""

    def connected(self):
        self.led.value(1)  # Turn LED on when connected
        self.timer1.deinit()

    def disconnected(self):
        self.timer1.init(period=100, mode=Timer.PERIODIC, callback=lambda t: self.led.value(not self.led.value()))

    def ble_irq(self, event, data):
        if event == 1:  # Connection
            print("Device connected!")
            self.connected()
        elif event == 2:  # Disconnection
            print("Device disconnected!")
            self.ble.gap_advertise(None)
            self.advertiser()
            self.disconnected()
        elif event == 3:  # GATT write
            buffer = self.ble.gatts_read(self.rx)
            self.ble_msg = buffer.decode('UTF-8').strip()
            print(f"Received message: {self.ble_msg}")

            # Control LED or handle GPS location based on the received message
            if self.ble_msg == 'turn_on':
                self.led.value(1)  # Turn LED ON
                self.send('LED is turned ON.')
            elif self.ble_msg == 'turn_off':
                self.led.value(0)  # Turn LED OFF
                self.send('LED is turned OFF.')
            elif self.ble_msg == 'read_LED':
                led_state = 'ON' if self.led.value() else 'OFF'
                self.send(f'LED is {led_state}.')
            elif self.ble_msg == 'location':
                self.get_location()  # Get location when the command is 'location'

            self.ble_msg = ""  # Clear the message

    def get_location(self):
        # Lê as coordenadas do GPS em tempo real
        location = self.get_gps_coordinates()
        if location:
            lat, lon = location
            # Gera um link do Google Maps
            map_link = f"https://www.google.com/maps?q={lat},{lon}"
            self.send(f"Location: {map_link}")
        else:
            self.send("GPS data not available.")

    def get_gps_coordinates(self):
        # Lê os dados do GPS continuamente e tenta extrair latitude e longitude
        try:
            while gps_uart.any():
                data = gps_uart.read(32)
                for byte in data:
                    gps.update(chr(byte))  # Atualiza o GPS com os dados recebidos

            # Verifica se as coordenadas GPS são válidas
            if gps.latitude[0] is not None and gps.longitude[0] is not None:
                # Converte as coordenadas para formato decimal, considerando o hemisfério
                latitude_decimal = to_decimal(gps.latitude[0], gps.latitude[1], gps.latitude[2])
                longitude_decimal = to_decimal(gps.longitude[0], gps.longitude[1], gps.longitude[2])
                return latitude_decimal, longitude_decimal
            else:
                return None
        except Exception as e:
            print(f"Erro ao obter coordenadas GPS: {e}")
            return None

    def register(self):
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'

        BLE_NUS = bluetooth.UUID(NUS_UUID)
        BLE_RX = (bluetooth.UUID(RX_UUID), bluetooth.FLAG_WRITE)
        BLE_TX = (bluetooth.UUID(TX_UUID), bluetooth.FLAG_NOTIFY)

        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART,)
        ((self.tx, self.rx),) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        self.ble.gatts_notify(0, self.tx, (data + '\n').encode('utf-8'))

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        adv_data = bytearray([0x02, 0x01, 0x02]) + bytearray([len(name) + 1, 0x09]) + name
        self.ble.gap_advertise(500, adv_data)
        print(f"Advertising: {adv_data.hex()}")

# Setup do BLE
ble = ESP32_BLE("ESP32BLE")

# Loop principal para atualização contínua do GPS
while True:
    time.sleep(1)


