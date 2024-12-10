# Relatório de Projeto: Colete Inteligente para Pet

Aluna: **Ana Flavia Marcacini**  
Número: 12526541  

Aluno: **Davi Araujo Martins**   
Número: 10337787  

Aluno: **Guilherme Elui de Souza**   
Número: 11796152  

## 1. Introdução

Este projeto teve como objetivo o desenvolvimento de um **colete inteligente para pets**, que visou melhorar a segurança, o conforto e a personalização dos animais de estimação. O colete incorpora sensores para monitorar condições ambientais e físicas do pet e oferece opções de personalização temática, como roupas para datas comemorativas. A comunicação entre o colete e o usuário é feita via **Bluetooth**, por meio de aplicativo para celular. O projeto foi desenvolvido utilizando o microcontrolador **ESP32**, diversos sensores e sistemas de personalização.

## 2. Objetivos

Os objetivos principais deste projeto são:

- **Monitoramento de condições ambientais**: Utilização de sensores para monitorar temperatura, umidade e luminosidade.
- **Aumento da segurança do pet**: Sistema automático de LEDs que se acendem em condições de baixa luminosidade.
- **Personalização temática**: Permitir que o colete seja adaptado a temas como Halloween e Natal.
- **Conforto e funcionalidade**: Design ergonômico, fácil de ajustar e confortável para o uso diário.

## 3. Metodologia

A construção do colete seguiu uma abordagem iterativa, com as seguintes etapas:

1. **Escolha dos componentes**: Seleção do ESP32 e sensores (DHT22, P7, NEO6M) para coleta de dados em tempo real.
2. **Desenvolvimento do hardware**: Integração dos sensores no colete, priorizando conforto e funcionalidade. Também foi incorporada uma fita de LED endereçável, para oferecer maior flexibilidade na personalização da iluminação.
3. **Programação e integração de sistemas**: Desenvolvimento do código para processamento dos dados dos sensores, utilizando o **Bluetooth** para comunicação com o aplicativo no celular.
4. **Testes e ajustes**: Validação dos sensores em diferentes condições e ajustes no design e no código.

## 4. Descrição dos Componentes

- **ESP32**: Microcontrolador central que gerencia os sensores e controla os LEDs. A comunicação com o aplicativo é realizada via Bluetooth.
- **Sensores**:
  - **Sensor de temperatura e umidade DHT22**: Para monitoramento das condições ambientais.
  - **Sensor de luminosidade P7**: Para detectar a luminosidade ambiente e ativar LEDs automaticamente em caso de baixa luminosidade.
  - **Módulo GPS NEO6M**: Para determinar a localização do pet, possibilitando rastreamento.
- **Fita de LED endereçável 12V**: Fita de LEDs que pode ser controlada individualmente, oferecendo personalização nas cores e padrões de iluminação. Componente utilizado para a funcionalidade de visibilidade noturna.
- **Estrutura do colete**: Material confortável, durável e ajustável, adequado para o uso diário e fácil de colocar no pet.

## 5. Funcionalidades

O colete inteligente possui as seguintes funcionalidades:

- **Monitoramento ambiental**: Sensores de temperatura, umidade e luminosidade fornecem dados contínuos sobre as condições ao redor do pet.
- **Visibilidade noturna**: A fita de LED endereçável é acionada automaticamente em condições de baixa luminosidade, garantindo maior segurança ao pet em ambientes escuros.
- **Personalização temática**: O design do colete pode ser facilmente adaptado para temas sazonais, como Halloween e Natal, com roupas adicionais.
- **Controle remoto via Bluetooth**: O colete pode ser integrado a um aplicativo móvel, permitindo monitoramento e ajustes nas configurações dos sensores.

## 6. Público-alvo

O colete inteligente é voltado para os seguintes públicos:

- **Donos de pets**: Que buscam melhorar a segurança e o bem-estar de seus animais de estimação.
- **Pet shops e clínicas veterinárias**: Que podem oferecer uma solução inovadora para seus clientes.
- **Feiras e eventos de pets**: Onde o colete personalizado pode atrair o público interessado em novidades no mercado pet.
- **Donos de pets em áreas urbanas**: Onde é necessário garantir visibilidade adicional para os animais, especialmente à noite ou em locais com pouca luz.

## 7. Resultados Obtidos

Durante a execução do projeto, foram obtidos os seguintes resultados:

- **Validação dos Sensores**:
  - O **sensor de temperatura e umidade DHT22** funcionou adequadamente, fornecendo leituras consistentes e precisas das condições ambientais. O sensor foi capaz de monitorar a temperatura e umidade do ambiente ao redor do pet, oferecendo dados em tempo real, que podem ser acessados facilmente via Bluetooth.
  
  - O **módulo GPS NEO6M** também apresentou bom desempenho, fornecendo a localização precisa do pet. Ao conectar-se ao aplicativo via Bluetooth, é gerado um link direto para o **Google Maps**, permitindo que o dono do pet acompanhe a posição do animal em tempo real. O link gerado pelo GPS pode ser acessado facilmente, facilitando o rastreamento do pet em caso de fuga ou deslocamento não autorizado.

- **Eficiência do Sistema de LEDs**:
  Inicialmente um LED endereçável unitário de 5V foi testado, e, em condições de baixa luminosidade detectados através do sensor P7, foi verificado que o LED realmente brilhou mais intensamente, conforme o código desenvolvido para essa funcionalidade. Entretanto, a fita de LED de 12V não foi ainda integrada ao circuito devido à diferença de voltagem e aos desafios que tal fato implica, mesmo assim, diante do teste inicial, a ideia de aumentar a visibilidade do pet durante a noite se mostrou promissora e eficiente nos primeiros testes com o LED de 5V.

- **Conforto do Colete**:
  O design do colete foi ajustado para garantir que ele fosse confortável e fácil de ajustar ao corpo do pet, sem comprometer a funcionalidade do sistema de sensores. O colete é feito de material leve e respirável, garantindo que o pet se sinta à vontade enquanto utiliza o dispositivo.

### Dificuldades Encontradas

A principal das dificuldades enfrentadas foi a **conexão da fita de LED endereçável com o ESP32**, pois a nossa fita de LED requer **12V**, enquanto o ESP32 opera com **3,3V**. Embora o circuito adicional necessário para ajustar a tensão ainda não tenha sido implementado, realizamos um teste preliminar com um **LED unitário endereçável de 5V**. Em condições de baixa luminosidade, o LED realmente brilhou mais intensamente, como esperado, com o código desenvolvido para essa funcionalidade. Isso demonstrou a viabilidade da ideia de utilizar LEDs endereçáveis para melhorar a visibilidade do pet em ambientes com pouca luz.


## 8. Conclusão

O desenvolvimento do colete inteligente para pets ofereceu uma solução prática para a segurança e maior personalização dos animais de estimação. O sistema de monitoramento, aliado ao controle de visibilidade noturna, demonstrou ser eficiente. O projeto também enfrentou desafios técnicos, como a adaptação da fita de LED de 12V ao ESP32, mas a ideia foi testada com sucesso em um LED unitário de 5V, comprovando sua eficácia em condições de baixa luminosidade. Sendo assim, o projeto abre portas para novas possibilidades, como a integração com sistemas de saúde para pets, uso de mais sensores, criação do circuito adicional para LED 12V e/ou um aumento na personalização do design.

## 9. Referências

- [**Documentação Técnica** sobre o uso de sensores em dispositivos com Micropython](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html).
- [**Documentação do ESP32** para IoT e integração com sensores](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/gpio.html).
- [**Projetos anteriores** de wearables aplicados, incluindo funcionalidades de monitoramento e personalização](https://github.com/FNakano/CFA).
