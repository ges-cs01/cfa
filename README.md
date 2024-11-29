# Diário da Primeira Parte da Disciplina de Computação Física

**Aluno:** Guilherme Elui de Souza  
**Número:** 11796152

---

### **08/ago: Introdução ao Curso e Primeiros Passos no Micropython**

A primeira aula teve como objetivo a introdução ao curso, à ferramenta Micropython e aos principais componentes que envolvem a criação e o emprego de circuitos. Recebemos uma visão geral das possibilidades do ESP32. Explicação de como o Micropython é usado para programar dispositivos como o ESP32 e como podemos interagir com o hardware de forma eficiente usando Python.

Foi discutido o uso do Thonny como ambiente de desenvolvimento para o Micropython. O objetivo inicial foi entender a interação do Micropython com o ESP32 e configurar a IDE para escrever e executar scripts. Para testar a instalação, foi sugerido código simples para acender e apagar o LED embutido do ESP32 e a utilização de um sensor LDR.

---

### **15/ago: Configuração do WebREPL no ESP32**

Fomos apresentados ao conceito de WebREPL, uma maneira de acessar o Micropython no ESP32 remotamente via Wi-Fi. O WebREPL permite que o código seja executado e depurado de forma mais prática, sem a necessidade de estar fisicamente conectado ao dispositivo. A instalação do WebREPL foi detalhada, e configuramos o ESP32 para funcionar como um ponto de acesso Wi-Fi. Isso significou que poderíamos nos conectar ao ESP32 via navegador e interagir com o Micropython diretamente da web.
Foram testados componentes simples como buzzer e leds.

**Atividade Prática:**
- Habilitação do WebREPL no ESP32.
- Conexão ao ESP32 via Wi-Fi e uso do console Python remotamente.

---

### **22/ago: Mini-projeto TM + SI**

Nesta aula formamos um grupo e foi proposta uma atividade que utilizasse componentes eletrônicos simples, como leds e switches, para construir um produto. Nosso grupo projetou uma braçadeira para proporcionar uma ferramenta discreta e eficiente para pessoas autistas comunicarem que estão em um momento de sobrecarga, ansiedade ou desconforto, através de um LED azul que acende ao pressionar um botão.

---

### **29/ago: Conexão e Uso de Display OLED com o ESP32**

Nessa aula, a tarefa foi conectar um display OLED ao ESP32 e aprender como interagir com ele usando Micropython. O display OLED foi utilizado como ferramenta para mostrar dados.

Exploramos bibliotecas de Micropython que facilitam a comunicação com o display, como o [`ssd1306`](https://github.com/ges-cs01/cfa/blob/main/ssd1306.py), que permite desenhar textos, formas e até imagens na tela OLED. [Código OLED](https://github.com/ges-cs01/cfa/blob/main/oled.py).

**Atividade Prática:**
- Conexão do display OLED ao ESP32.
- Exibição de texto simples no display OLED.

---

### **05/set: Semana da Pátria - Feriado**

Não houve aula nesse dia devido ao feriado da Semana da Pátria.

---

### **12/set: Ponto de Acesso Wi-Fi no ESP32**

Na aula de 12 de setembro, aprendemos como configurar o ESP32 para funcionar como um ponto de acesso Wi-Fi (AP). Isso nos permitiu configurar o ESP32 como um servidor web que pode ser acessado por outros dispositivos na rede local [Código mDNS](https://github.com/ges-cs01/cfa/blob/main/mdns.py). Ainda, testamos um sensor touch combinado com um sensor de batimento cardíaco e um buzzer, o que pareceu funcionar, mas com difilculdades na conversão dos dados de frequência para um formato adequado: [Código Freq. Cardíaca](https://github.com/ges-cs01/cfa/blob/main/frequencia_cardiaca.py).

**Atividade Prática:**
- Configuração do ESP32 como Ponto de Acesso Wi-Fi.
- Teste da conexão com o ESP32 via navegador.

---

### **19/set: Implementação de um Servidor Web no ESP32**

A aula do dia 19 focou na implementação de um servidor web simples no ESP32. Usamos o ambiente de desenvolvimento Micropython para criar um servidor que poderia receber requisições HTTP e retornar respostas. Isso permitiu que o ESP32 funcionasse como uma plataforma, capaz de interagir com outros dispositivos pela web. [Código Server](https://github.com/ges-cs01/cfa/blob/main/server.py) e [Código Cliente](https://github.com/ges-cs01/cfa/blob/main/cliente.py).

**Atividade Prática:**
- Desenvolvimento e implementação de um servidor web no ESP32.
- Teste de requisições HTTP entre o ESP32 e outros dispositivos.


### **26/set: Utilização de Bluetooth no ESP32**

Na última aula de setembro fiz a utilização de Bluetooth no ESP32. Realizei a configuração no ESP32 para se comunicar via Bluetooth, e controlar sensores e outros módulos. O ESP32 oferece suporte a Bluetooth Low Energy (BLE), o que foi explorado nessa aula. Para controle e conexão utilizei o aplicativo para Android Serial Bluetooth Terminal. [Código Bluetooth](https://github.com/ges-cs01/cfa/blob/main/bluetooth_test.py).

**Atividade Prática:**
- Configuração do Bluetooth no ESP32.
- Testes de comunicação Bluetooth com dispositivos compatíveis.

---

### **03/out: Formação de Grupo e Teste com Arduino e Sensor DHT**

Formamos os grupos de trabalho para o projeto final da disciplina. Ao invés de utilizar o ESP32 como plataforma principal para o desenvolvimento do projeto, testamos um sensor DHT, que mede umidade e temperatura, com o Arduino, [Código DHT](https://github.com/ges-cs01/cfa/blob/main/dht_arduino.ino). Houve uma dificuldade na conexão do Arduino com o Linux. O problema foi solucionado ao removermos o brltty.

**Atividade Prática:**
- Formação dos grupos para o projeto final.
- Testes práticos com o Arduino e o sensor DHT para medição de temperatura e umidade.

---

### 10/out: **Semana de Sistemas de Informação (SSI)**

Na semana de Sistemas de Informação, as atividades foram suspensas para foco nos eventos e palestras relacionados à área.

---

### **17/out em diante: Atendimento para o Projeto Final**

A partir do dia 17 de outubro, iniciaram-se as orientações para o desenvolvimento de projetos finais.
