# AGRO-BOT IoT Device Code

## 📡 Overview

IoT sensor nodes for real-time farm monitoring using ESP32 microcontrollers and various agricultural sensors.

## 🛠️ Hardware Requirements

### ESP32 Sensor Node
- **Microcontroller**: ESP32 DevKit V1
- **Sensors**:
  - DHT22 - Temperature & Humidity
  - Capacitive Soil Moisture Sensor
  - NPK Sensor (RS485)
  - Light Sensor (BH1750)
  - pH Sensor (optional)
- **Actuators**:
  - 5V Relay Module (for pump control)
  - Water solenoid valve
- **Power**:
  - 5V 2A Power Supply
  - 18650 Li-ion battery (for remote nodes)
  - Solar panel (optional)

## 📋 Pin Connections

```
ESP32          Component
----------------------------
GPIO 4      -> DHT22 Data
GPIO 34     -> Soil Moisture Analog
GPIO 16     -> NPK Sensor RX
GPIO 17     -> NPK Sensor TX
GPIO 25     -> Relay (Pump Control)
GPIO 2      -> Status LED
GPIO 21     -> I2C SDA (for BH1750)
GPIO 22     -> I2C SCL (for BH1750)
3.3V        -> Sensor VCC
GND         -> Sensor GND
```

## 🚀 Setup Instructions

### 1. Install Arduino IDE
```bash
# Download from: https://www.arduino.cc/en/software

# Install ESP32 Board Support
# In Arduino IDE:
# File -> Preferences -> Additional Board URLs:
# https://dl.espressif.com/dl/package_esp32_index.json
```

### 2. Install Required Libraries
```
In Arduino IDE Library Manager, install:
- WiFi (built-in)
- PubSubClient by Nick O'Leary
- DHT sensor library by Adafruit
- ArduinoJson by Benoit Blanchon
- Adafruit Unified Sensor
```

### 3. Configure WiFi and MQTT
```cpp
// Update in esp32_sensor_node.ino:
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* mqtt_server = "your-mqtt-broker.com";
```

### 4. Upload Code
```
1. Connect ESP32 via USB
2. Select Board: "ESP32 Dev Module"
3. Select Port: COM port of your device
4. Click Upload
```

## 📊 Data Format

### Sensor Data (Published to `agro/sensors/data`)
```json
{
  "device_id": "ESP32_FARM_001",
  "farm_id": "FARM_001",
  "location": "Plot_A",
  "timestamp": 1234567890,
  "sensors": {
    "temperature": 25.5,
    "humidity": 65.2,
    "soil_moisture": 45.8,
    "nitrogen": 35,
    "phosphorus": 28,
    "potassium": 22
  },
  "status": {
    "wifi_rssi": -45,
    "pump_active": false,
    "battery_voltage": 3.7
  }
}
```

### Control Commands (Subscribe to `agro/control/commands`)
```json
{
  "command": "pump_on",
  "device_id": "ESP32_FARM_001",
  "duration": 300
}
```

Available commands:
- `pump_on` - Turn on water pump
- `pump_off` - Turn off water pump
- `read_sensors` - Force immediate sensor reading
- `restart` - Restart device

## 🔧 Calibration

### Soil Moisture Sensor
```cpp
// Calibrate in air (dry)
int dryValue = analogRead(SOIL_MOISTURE_PIN); // ~4095

// Calibrate in water (wet)
int wetValue = analogRead(SOIL_MOISTURE_PIN); // ~1500

// Update mapping
float soilMoisture = map(reading, wetValue, dryValue, 100, 0);
```

### NPK Sensor
```
1. Connect NPK sensor via RS485 to TTL converter
2. Follow manufacturer calibration procedure
3. Update sensor reading function
```

## 📡 MQTT Topics

| Topic | Direction | Description |
|-------|-----------|-------------|
| `agro/sensors/data` | Publish | Sensor readings |
| `agro/control/commands` | Subscribe | Control commands |
| `agro/sensors/status` | Publish | Device status |

## 🔋 Power Optimization

### Battery-Powered Mode
```cpp
// Enable deep sleep between readings
void loop() {
  readAndSendSensors();
  enterDeepSleep(300); // Sleep for 5 minutes
}
```

### Power Consumption
- Active mode: ~80-160mA
- WiFi transmission: ~170-260mA
- Deep sleep: ~10µA
- Estimated battery life (2500mAh): 
  - Continuous: ~12-15 hours
  - With deep sleep (5min intervals): ~30-45 days

## 🛡️ Security

### Over-The-Air (OTA) Updates
```cpp
#include <ArduinoOTA.h>

void setup() {
  ArduinoOTA.setHostname("agro-esp32-001");
  ArduinoOTA.setPassword("your-ota-password");
  ArduinoOTA.begin();
}

void loop() {
  ArduinoOTA.handle();
}
```

### MQTT Authentication
- Use strong MQTT credentials
- Enable TLS/SSL for production
- Implement certificate pinning

## 🧪 Testing

### Serial Monitor
```
1. Open Serial Monitor (115200 baud)
2. Watch for sensor readings
3. Send test commands via MQTT
```

### MQTT Test Client
```bash
# Subscribe to sensor data
mosquitto_sub -h your-mqtt-broker.com -t "agro/sensors/#" -u agro_iot -P password

# Send test command
mosquitto_pub -h your-mqtt-broker.com -t "agro/control/commands" -u agro_iot -P password -m '{"command":"pump_on","device_id":"ESP32_FARM_001"}'
```

## 🐛 Troubleshooting

### WiFi Connection Issues
- Check SSID and password
- Ensure 2.4GHz WiFi (ESP32 doesn't support 5GHz)
- Move closer to router
- Check router firewall settings

### MQTT Connection Issues
- Verify broker address and port
- Check MQTT credentials
- Ensure broker allows external connections
- Check firewall rules

### Sensor Reading Issues
- Verify pin connections
- Check sensor power supply
- Test sensors individually
- Review serial monitor output

## 📦 Production Deployment

### Enclosure
- Use waterproof IP65 rated enclosure
- Add ventilation holes for DHT sensor
- Mount securely near crops

### Installation
1. Connect all sensors
2. Secure ESP32 in enclosure
3. Connect power supply
4. Mount at appropriate height (30-50cm above ground)
5. Test all sensors
6. Monitor for 24 hours

### Maintenance
- Check battery voltage monthly
- Clean sensors quarterly
- Update firmware as needed
- Replace sensors annually

## 📞 Support

For issues or questions:
- Email: iot@agro-bot.com
- Documentation: https://docs.agro-bot.com/iot

---

**Version:** 1.0.0  
**Last Updated:** 2024
