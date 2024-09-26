from machine import Pin, Timer
from time import sleep_ms
import ubluetooth

class ESP32_BLE:
    def __init__(self, name):
        self.led = Pin(2, Pin.OUT)
        self.timer1 = Timer(0)
        self.name = name
        self.ble = ubluetooth.BLE()
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
            self.advertiser()
            self.disconnected()
        elif event == 3:  # GATT write
            buffer = self.ble.gatts_read(self.rx)
            self.ble_msg = buffer.decode('UTF-8').strip()
            print(f"Received message: {self.ble_msg}")

            # Control LED based on the received message
            if self.ble_msg == 'turn_on':
                self.led.value(1)  # Turn LED ON
                self.send('LED is turned ON.')
            elif self.ble_msg == 'turn_off':
                self.led.value(0)  # Turn LED OFF
                self.send('LED is turned OFF.')
            elif self.ble_msg == 'read_LED':
                led_state = 'ON' if self.led.value() else 'OFF'
                self.send(f'LED is {led_state}.')
            
            self.ble_msg = ""  # Clear the message

    def register(self):
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
        
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)
        
        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART,)
        ((self.tx, self.rx),) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        self.ble.gatts_notify(0, self.tx, (data + '\n').encode('utf-8'))

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        adv_data = bytearray([0x02, 0x01, 0x02]) + bytearray([len(name) + 1, 0x09]) + name
        self.ble.gap_advertise(100, adv_data)
        print(f"Advertising: {adv_data.hex()}")

led = Pin(2, Pin.OUT)
but = Pin(0, Pin.IN)
ble = ESP32_BLE("ESP32BLE")

def buttons_irq(pin):
    led.value(not led.value())
    ble.send('LED state will be toggled.')
    print('LED state will be toggled.')
    
but.irq(trigger=Pin.IRQ_FALLING, handler=buttons_irq)

while True:
    sleep_ms(100)

