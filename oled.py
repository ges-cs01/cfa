from machine import Pin, I2C
import ssd1306

# Configuração do I2C
i2c = I2C(0, scl=Pin(22), sda=Pin(21))  # Ajuste os pinos conforme necessário

# Inicializa o display SSD1306
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Função para exibir a mensagem
def display_message(message):
    oled.fill(0)  # Limpa o display
    lines = message.split('\n')  # Divide a mensagem em linhas
    for i, line in enumerate(lines):
        oled.text(line, 0, i * 10)  # Ajuste a posição y para cada linha
    oled.show()

# Mensagem a ser exibida
message = "hello"

# Exibe a mensagem
display_message(message)
