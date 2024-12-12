# Código completo atualizado com o efeito de retrocesso gradual entre azul e verde

import machine
import neopixel
import time
import dht

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

# Configurações dos sensores
TEMP_SENSOR_PIN = 4  # GPIO do DHT22
LIGHT_SENSOR_PIN = 26  # GPIO do sensor de luminosidade
dht_sensor = dht.DHT22(machine.Pin(TEMP_SENSOR_PIN))
light_sensor = machine.ADC(machine.Pin(LIGHT_SENSOR_PIN))

# Função para exibir uma cor sólida em uma fita
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

# Função para ler o DHT22 com tentativas
def read_dht_sensor(dht_sensor, retries=3):
    for attempt in range(retries):
        try:
            dht_sensor.measure()
            temperature = dht_sensor.temperature()
            return temperature
        except Exception as e:
            if attempt >= 2:
                print(f"Tentativa {attempt + 1} falhou ao ler o DHT22: {e}")
            time.sleep(1)  # Pequeno atraso antes de nova tentativa
    print("Erro persistente ao ler o DHT22.")
    return None  # Retorna None em caso de falha

# Função para ler o sensor de luminosidade com tentativas
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

# Loop principal
step_counter = 0
total_steps = 20  # Quantidade de passos na transição gradual
current_color = COLOR_BLUE
while True:
    try:
        # Lê temperatura do DHT22 com tentativas
        temperature = read_dht_sensor(dht_sensor)
        print("Temperatura:", temperature)
        # Lê luminosidade (normalizada entre 0.0 e 1.0)
        light_level = read_light_sensor(light_sensor)
        print("Luminosidade", light_level)

        if temperature is not None and light_level is not None:
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
            if temperature > 29:
                blink(np1, np2, NUM_LEDS, NUM_LEDS, (255, 0, 0), brightness=1.0)
                #time.sleep(1)

            elif light_level < 0.5:  # Baixa luminosidade
                blink(np1, np2, NUM_LEDS, NUM_LEDS, (255, 255, 255), brightness=1.0)
                #time.sleep(1)

        # Aguarda antes de repetir
        time.sleep(0.1)

    except Exception as e:
        print("Erro ao ler sensores:", e)
        time.sleep(2)
