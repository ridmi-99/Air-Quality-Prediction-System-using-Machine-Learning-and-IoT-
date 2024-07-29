#include <DHT.h>

#define DHTPIN A5
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

const float R0_Methane = 3;
const float R0_CO = 9.83;
const float R0_Hydrogen = 2.3;
const int MQ2Pin = A1;

float calculateResistance(int sensorValue) {
  float sensorVoltage = sensorValue * (5.0 / 1023.0);
  float Rs = (5.0 - sensorVoltage) / sensorVoltage;
  return Rs;
}

// Function to calculate methane concentration
float calculateMethaneConcentration(int sensorValue) {
  float Rs = calculateResistance(sensorValue);
  float ratio = Rs / R0_Methane;
  // Example formula, adjust based on the datasheet
  float concentration = pow((ratio / 9.9), (1 / -0.6)); // Placeholder formula
  return concentration;
}

// Function to calculate CO concentration
float calculateCOConcentration(int sensorValue) {
  float Rs = calculateResistance(sensorValue);
  float ratio = Rs / R0_CO;
  // Example formula, adjust based on the datasheet
  float concentration = pow((ratio / 9.9), (1 / -0.6)); // Placeholder formula
  return concentration;
}

// Function to calculate smoke concentration
float calculatehydrogenConcentration(int sensorValue) {
  float Rs = calculateResistance(sensorValue);
  float ratio = Rs / R0_Hydrogen;
  // Example formula, adjust based on the datasheet
  float concentration = pow((ratio / 9.9), (1 / -0.6)); // Placeholder formula
  return concentration;
}

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  int sensorValue = analogRead(MQ2Pin);
  float methaneConcentration = calculateMethaneConcentration(sensorValue);
  float COConcentration = calculateCOConcentration(sensorValue);
  float hydrogenConcentration = calculatehydrogenConcentration(sensorValue);

  float humidity = dht.readHumidity();
  float temperatureCelsius = dht.readTemperature();
  float temperatureFahrenheit = dht.readTemperature(true);

  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.print("%\t");

  Serial.print("Temperature (Celsius): ");
  Serial.print(temperatureCelsius);
  Serial.print("°C\t");

  Serial.print("Temperature (Fahrenheit): ");
  Serial.print(temperatureFahrenheit);
  Serial.println("°F");

  Serial.print("Methane Concentration: ");
  Serial.println(methaneConcentration);
  Serial.print("CO Concentration: ");
  Serial.println(COConcentration);
  Serial.print("Hydrogen Concentration: ");
  Serial.println(hydrogenConcentration);
  Serial.println("----------------------------");

  delay(60000);
}