from machine import Pin, ADC, PWM
from time import sleep

# Constantes
PIN_SENSOR = 34
PIN_BUZZER = 2
VOLTAGEM_LIMITE = 2.0
TEMPO_BUZZER = 0.5  # Tempo em segundos

# Configuração do sensor e do buzzer
sensor1 = ADC(Pin(PIN_SENSOR))
buzzer = PWM(Pin(PIN_BUZZER), freq=440, duty=512)  # Duty médio (50%)
# buzzer = Pin(PIN_BUZZER, Pin.OUT)

# Configuração do ADC
sensor1.atten(ADC.ATTN_11DB)
sensor1.width(ADC.WIDTH_12BIT)

def ler_sensor():
    """Lê o valor do sensor e converte para voltagem."""
    valor = sensor1.read()
    voltaje = (3.3 / ((2**12) - 1)) * valor
    return voltaje

def acionar_buzzer(estado):
    """Liga ou desliga o buzzer."""
    buzzer.duty(estado)

while True:
    voltaje = ler_sensor()
    print("Voltagem lida:", voltaje)
    
    if voltaje > VOLTAGEM_LIMITE:
        acionar_buzzer(100)  # Liga o buzzer
    else:
        acionar_buzzer(0)  # Desliga o buzzer se a voltagem estiver abaixo do limite

    sleep(0.025)  # Espera 25 ms
