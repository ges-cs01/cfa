#include <Adafruit_Sensor.h>

#include <DHT_U.h>
#include <DHT.h>


// Example testing sketch for various DHT humidity/temperature sensors
// Written by ladyada, public domain

// REQUIRES the following Arduino libraries:
// - DHT Sensor Library: https://github.com/adafruit/DHT-sensor-library
// - Adafruit Unified Sensor Lib: https://github.com/adafruit/Adafruit_Sensor

#include "DHT.h"
#define DHTPIN 2
// Digital pin connected to the DHT sensor
// Uncomment whatever type you're using!
//#define DHTTYPE DHT11
// DHT 11
#define DHTTYPE DHT22
// DHT 22 (AM2302),

//#define DHTTYPE DHT21
// DHT 21 (AM2301)
// Initialize DHT sensor.
DHT SENSORHT(DHTPIN, DHTTYPE);
void setup() {
Serial.begin(9600);
Serial.println("Teste do sensor!");
SENSORHT.begin();
}



void loop() {
// Wait a few seconds between measurements.
delay(2000);
// Sensor readings may also be up to 2
float umidade = SENSORHT.readHumidity();
// Read temperature as Celsius (the default)
float temperatura = SENSORHT.readTemperature();
  Serial.print("Umidade relativa do ar: ");
  Serial.print(umidade);
  Serial.println("%");
  Serial.print("Temperatura do ar: ");
  Serial.print(temperatura);
  Serial.println("°C ");
  Serial.println("========================");
}
