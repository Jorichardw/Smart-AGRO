/*
 * AGRO-BOT IoT Sensor Node
 * ESP32-based sensor monitoring system for Smart Agriculture
 * 
 * Features:
 * - Soil moisture monitoring
 * - Temperature & humidity sensing
 * - NPK sensor integration
 * - WiFi connectivity
 * - MQTT communication with backend
 * - Deep sleep for power saving
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <Wire.h>
#include <ArduinoJson.h>

// WiFi Configuration
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// MQTT Configuration
const char* mqtt_server = "your-mqtt-broker.com";
const int mqtt_port = 1883;
const char* mqtt_user = "agro_iot";
const char* mqtt_password = "iot_password";
const char* mqtt_client_id = "agro_esp32_001";

// MQTT Topics
const char* topic_sensors = "agro/sensors/data";
const char* topic_control = "agro/control/commands";
const char* topic_status = "agro/sensors/status";

// Pin Definitions
#define DHT_PIN 4            // DHT22 sensor pin
#define SOIL_MOISTURE_PIN 34 // Analog pin for soil moisture
#define NPK_RX 16           // NPK sensor RX
#define NPK_TX 17           // NPK sensor TX
#define RELAY_PUMP 25       // Water pump relay
#define LED_STATUS 2        // Status LED

// Sensor Configuration
#define DHT_TYPE DHT22
DHT dht(DHT_PIN, DHT_TYPE);

// Global Variables
WiFiClient espClient;
PubSubClient mqtt(espClient);
unsigned long lastSensorRead = 0;
const long sensorInterval = 30000; // Read sensors every 30 seconds
bool pumpState = false;

// Device Info
String deviceId = "ESP32_FARM_001";
String farmId = "FARM_001";
String location = "Plot_A";

void setup() {
  Serial.begin(115200);
  
  // Initialize pins
  pinMode(LED_STATUS, OUTPUT);
  pinMode(RELAY_PUMP, OUTPUT);
  pinMode(SOIL_MOISTURE_PIN, INPUT);
  
  // Initialize sensors
  dht.begin();
  
  // Connect to WiFi
  connectWiFi();
  
  // Connect to MQTT
  mqtt.setServer(mqtt_server, mqtt_port);
  mqtt.setCallback(mqttCallback);
  connectMQTT();
  
  // Send initial status
  sendStatus("online");
  
  Serial.println("AGRO-BOT IoT Node Started");
}

void loop() {
  // Maintain MQTT connection
  if (!mqtt.connected()) {
    connectMQTT();
  }
  mqtt.loop();
  
  // Read and send sensor data
  unsigned long currentMillis = millis();
  if (currentMillis - lastSensorRead >= sensorInterval) {
    lastSensorRead = currentMillis;
    readAndSendSensors();
  }
  
  // Blink status LED
  digitalWrite(LED_STATUS, millis() % 1000 < 100);
}

void connectWiFi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi Connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nWiFi Connection Failed!");
  }
}

void connectMQTT() {
  while (!mqtt.connected()) {
    Serial.print("Connecting to MQTT...");
    
    if (mqtt.connect(mqtt_client_id, mqtt_user, mqtt_password)) {
      Serial.println("Connected!");
      
      // Subscribe to control topic
      mqtt.subscribe(topic_control);
      
      // Send online status
      sendStatus("online");
    } else {
      Serial.print("Failed, rc=");
      Serial.print(mqtt.state());
      Serial.println(" Retrying in 5 seconds...");
      delay(5000);
    }
  }
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message received on topic: ");
  Serial.println(topic);
  
  // Parse JSON command
  StaticJsonDocument<256> doc;
  DeserializationError error = deserializeJson(doc, payload, length);
  
  if (error) {
    Serial.println("Failed to parse JSON command");
    return;
  }
  
  // Handle commands
  if (doc.containsKey("command")) {
    String command = doc["command"].as<String>();
    
    if (command == "pump_on") {
      controlPump(true);
    } else if (command == "pump_off") {
      controlPump(false);
    } else if (command == "read_sensors") {
      readAndSendSensors();
    } else if (command == "restart") {
      ESP.restart();
    }
  }
}

void readAndSendSensors() {
  // Read DHT22 (Temperature & Humidity)
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  
  // Read Soil Moisture
  int soilMoistureRaw = analogRead(SOIL_MOISTURE_PIN);
  float soilMoisture = map(soilMoistureRaw, 0, 4095, 0, 100);
  
  // Read NPK (simulated for now - actual NPK sensor requires RS485)
  float nitrogen = random(20, 50);
  float phosphorus = random(15, 40);
  float potassium = random(10, 35);
  
  // Create JSON payload
  StaticJsonDocument<512> doc;
  doc["device_id"] = deviceId;
  doc["farm_id"] = farmId;
  doc["location"] = location;
  doc["timestamp"] = millis();
  
  JsonObject sensors = doc.createNestedObject("sensors");
  sensors["temperature"] = isnan(temperature) ? 0 : temperature;
  sensors["humidity"] = isnan(humidity) ? 0 : humidity;
  sensors["soil_moisture"] = soilMoisture;
  sensors["nitrogen"] = nitrogen;
  sensors["phosphorus"] = phosphorus;
  sensors["potassium"] = potassium;
  
  JsonObject status = doc.createNestedObject("status");
  status["wifi_rssi"] = WiFi.RSSI();
  status["pump_active"] = pumpState;
  status["battery_voltage"] = 3.7; // If using battery
  
  // Serialize and publish
  char jsonBuffer[512];
  serializeJson(doc, jsonBuffer);
  
  if (mqtt.publish(topic_sensors, jsonBuffer)) {
    Serial.println("Sensor data sent:");
    Serial.println(jsonBuffer);
  } else {
    Serial.println("Failed to send sensor data");
  }
}

void controlPump(bool state) {
  pumpState = state;
  digitalWrite(RELAY_PUMP, state ? HIGH : LOW);
  
  Serial.print("Water pump ");
  Serial.println(state ? "ON" : "OFF");
  
  // Send confirmation
  StaticJsonDocument<128> doc;
  doc["device_id"] = deviceId;
  doc["action"] = "pump_control";
  doc["state"] = state ? "on" : "off";
  doc["timestamp"] = millis();
  
  char jsonBuffer[128];
  serializeJson(doc, jsonBuffer);
  mqtt.publish(topic_status, jsonBuffer);
}

void sendStatus(const char* status) {
  StaticJsonDocument<256> doc;
  doc["device_id"] = deviceId;
  doc["farm_id"] = farmId;
  doc["status"] = status;
  doc["uptime"] = millis();
  doc["ip_address"] = WiFi.localIP().toString();
  doc["mac_address"] = WiFi.macAddress();
  doc["firmware_version"] = "1.0.0";
  
  char jsonBuffer[256];
  serializeJson(doc, jsonBuffer);
  mqtt.publish(topic_status, jsonBuffer);
}

// Deep Sleep Mode (for battery-powered nodes)
void enterDeepSleep(int seconds) {
  Serial.printf("Entering deep sleep for %d seconds\n", seconds);
  sendStatus("sleeping");
  delay(100);
  esp_sleep_enable_timer_wakeup(seconds * 1000000ULL);
  esp_deep_sleep_start();
}
