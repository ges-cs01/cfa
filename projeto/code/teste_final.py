import bluetooth
import time
import machine
from machine import Pin, Timer, UART
import ustruct
from micropyGPS import MicropyGPS
from dht import DHT22  # Importa a biblioteca DHT22
import neopixel

# Configurações dos LEDs
LED_PIN_1 = 18
LED_PIN_2 = 19
NUM_LEDS = 4  # Número de LEDs por fita (assumindo o mesmo para ambas)
np1 = neopixel.NeoPixel(machine.Pin(LED_PIN_1), NUM_LEDS)
np2 = neopixel.NeoPixel(machine.Pin(LED_PIN_2), NUM_LEDS)

# Função para calcular uma cor gradualmente entre duas cores
def interpolate_color(color1, color2, step, total_steps):
    return tuple(
        int(color1[i] + (color2[i] - color1[i]) * (step / total_steps)) for i in range(3)
    )

# Padrão de cores: Azul e Verde
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)

# Configuração do pino para o LED
led = Pin(2, Pin.OUT)

LIGHT_SENSOR_PIN = 26  # GPIO do sensor de luminosidade
light_sensor = machine.ADC(machine.Pin(LIGHT_SENSOR_PIN))

# Configuração do sensor DHT22 (GPIO 4)
dht_sensor = DHT22(Pin(4))

# Configuração do GPS (UART1 - GPIO 16 e GPIO 17)
gps_uart = UART(1, baudrate=9600, tx=17, rx=16)
gps = MicropyGPS(9)  # Inicia a instância do MicropyGPS com o fuso horário local

# Função para converter as coordenadas GPS para formato decimal, incluindo o sinal de negativo
def to_decimal(degrees, minutes, hemisphere):
    decimal_value = degrees + (minutes / 60)
    if hemisphere in ['S', 'W']:  # Se o hemisfério for sul ou oeste, o valor será negativo
        decimal_value = -decimal_value
    return decimal_value

def solid_color(np, num_leds, color, brightness=1.0):
    adjusted_color = tuple(int(c * brightness) for c in color)
    for i in range(num_leds):
        np[i] = adjusted_color
    np.write()
    
# Função para piscar os LEDs simultaneamente
def blink(np1, np2, num_leds1, num_leds2, color, brightness=1.0, times=10, delay_ms=200):
    for _ in range(times):
        # Liga ambas as fitas
        solid_color(np1, num_leds1, color, brightness)
        solid_color(np2, num_leds2, color, brightness)
        time.sleep_ms(delay_ms)
        # Apaga ambas as fitas
        solid_color(np1, num_leds1, (0, 0, 0))
        solid_color(np2, num_leds2, (0, 0, 0))
        time.sleep_ms(delay_ms)

# Função auxiliar para limitar valores entre 0 e 1
def clamp(value, min_value=0, max_value=1):
    return max(min(value, max_value), min_value)

def read_light_sensor(light_sensor, retries=3):
    for attempt in range(retries):
        try:
            light_raw = light_sensor.read_u16()
            light_level = light_raw / 65535  # Normaliza para 0.0 a 1.0
            return light_level
        except Exception as e:
            if attempt >= 2:
                print(f"Tentativa {attempt + 1} falhou ao ler o sensor de luminosidade: {e}")
            time.sleep(1)  # Pequeno atraso antes de nova tentativa
    print("Erro persistente ao ler o sensor de luminosidade.")
    return None  # Retorna None em caso de falha

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

            # Handle commands
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
                self.get_location()  # Get location
            elif self.ble_msg == 'read_dht22':
                self.read_dht22()  # Read DHT22 sensor
            elif self.ble_msg == 'read_light':
                self.read_light_sensor_class()

            self.ble_msg = ""  # Clear the message

    def get_location(self):
        location = self.get_gps_coordinates()
        if location:
            lat, lon = location
            map_link = f"https://www.google.com/maps?q={lat},{lon}"
            self.send(f"Location: {map_link}")
        else:
            self.send("GPS data not available.")

    def get_gps_coordinates(self):
        try:
            while gps_uart.any():
                data = gps_uart.read(32)
                for byte in data:
                    gps.update(chr(byte))

            if gps.latitude[0] is not None and gps.longitude[0] is not None:
                latitude_decimal = to_decimal(gps.latitude[0], gps.latitude[1], gps.latitude[2])
                longitude_decimal = to_decimal(gps.longitude[0], gps.longitude[1], gps.longitude[2])
                return latitude_decimal, longitude_decimal
            else:
                return None
        except Exception as e:
            print(f"Erro ao obter coordenadas GPS: {e}")
            return None

    def read_dht22(self):
        try:
            dht_sensor.measure()  # Lê o sensor
            temp = dht_sensor.temperature()
            hum = dht_sensor.humidity()
            self.send(f"Temperature: {temp:.1f}°C, Humidity: {hum:.1f}%")
        except Exception as e:
            print(f"Erro ao ler DHT22: {e}")
            self.send("Error reading DHT22 sensor.")

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

def read_dht22_rt(self):
    try:
        dht_sensor.measure()  # Lê o sensor
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        print(f"Temperature: {temp:.1f}°C, Humidity: {hum:.1f}%")
    except Exception as e:
        print(f"Erro ao ler DHT22: {e}")
        
# Loop principal
step_counter = 0
total_steps = 20  # Quantidade de passos na transição gradual
current_color = COLOR_BLUE
while True:
    try:
        # Lê temperatura do DHT22 com tentativas
        temperature = read_dht22_rt(dht_sensor)
        # Lê luminosidade (normalizada entre 0.0 e 1.0)
        light_level = read_light_sensor(light_sensor)
        print("Luminosidade", light_level)

        if light_level is not None and read_dht22_rt is not None:
            # Controle de luminosidade
            brightness = 1.0 - 0.9*light_level  # Mais escuro => LEDs mais fortes
            brightness = clamp(brightness)

            # Efeito de fila alternando entre azul e verde
            
            led_states = [current_color] * NUM_LEDS  # Estado inicial da fila (azul)
            for step in range(step_counter, step_counter+5):
                transition_color = interpolate_color(COLOR_BLUE, COLOR_GREEN, step, total_steps)
                
                # Move a "fila" uma posição para frente
                led_states = [transition_color] + led_states[:-1]
                
                # Atualiza os LEDs das duas fitas
                for i in range(NUM_LEDS):
                    np1[i] = tuple(int(c * brightness) for c in led_states[i])
                    np2[i] = tuple(int(c * brightness) for c in led_states[i])
                np1.write()
                np2.write()
                
                time.sleep(0.1)
            
            step_counter += 5
            if step_counter >= total_steps:
                step_counter = 0  # Reiniciar para manter a transição contínua
                # Alternar cores ao chegar no fim da transição
                if current_color == COLOR_BLUE:
                    current_color = COLOR_GREEN
                else:
                    current_color = COLOR_BLUE

            # Controle de temperatura: pisca vermelho se > 25°C
            #if temperature > 26:
            #    blink(np1, np2, NUM_LEDS, NUM_LEDS, (255, 0, 0), brightness=1.0)
            #    time.sleep(1)

            if light_level < 0.6:  # Baixa luminosidade
                blink(np1, np2, NUM_LEDS, NUM_LEDS, (255, 255, 255), brightness=1.0)
                time.sleep(1)

        # Aguarda antes de repetir
        time.sleep(5)

    except Exception as e:
        print("Erro ao ler sensores:", e)
        time.sleep(2)