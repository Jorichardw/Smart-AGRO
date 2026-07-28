# 🚀 AGRO-BOT Quick Start Guide

Get the entire Smart Agriculture Platform running in under 10 minutes!

---

## Prerequisites

Before starting, ensure you have:

- [x] **Docker** & **Docker Compose** installed
- [x] **Git** installed
- [x] **8GB RAM** minimum (16GB recommended)
- [x] **20GB free disk space**
- [x] **Internet connection** (for API services)

---

## Option 1: Development Mode (Recommended for Testing)

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-org/agro-bot-automation.git
cd agro-bot-automation
```

### Step 2: Configure Environment

#### Backend Configuration
```bash
cd backend
cp .env.example .env

# Edit .env and update these essential variables:
# - SECRET_KEY (generate with: openssl rand -hex 32)
# - WEATHER_API_KEY (get free key from openweathermap.org)
# - Firebase credentials (optional for testing)
```

#### Frontend Configuration
```bash
cd ../frontend
cp .env.example .env.local

# Update NEXT_PUBLIC_API_URL if needed (default: http://localhost:8000)
```

### Step 3: Start Services
```bash
# Return to project root
cd ..

# Start all services with Docker Compose
docker-compose up -d

# Wait for services to be ready (~2 minutes)
# You can watch the logs with:
docker-compose logs -f
```

### Step 4: Initialize Database
```bash
# The database tables are auto-created on first run
# Optional: Load seed data
docker exec -i agro_postgres psql -U agro_user -d agro_bot_db < database/init/02-seed-data.sql
```

### Step 5: Access Applications

- **Frontend Web App:** http://localhost:3000
- **API Documentation:** http://localhost:8000/docs
- **API Health Check:** http://localhost:8000/health
- **Database:** localhost:5432

### Step 6: Test the System

#### Register a User
1. Go to http://localhost:3000
2. Click "Login" → "Register now"
3. Fill in details and register
4. Login with your credentials

#### Test API Endpoints
```bash
# Health check
curl http://localhost:8000/health

# Get current weather (no auth required)
curl "http://localhost:8000/api/v1/weather/current?lat=28.6139&lon=77.2090"

# Login and get token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"your@email.com","password":"yourpassword"}'
```

---

## Option 2: Production Mode

### Step 1: Clone & Configure
```bash
git clone https://github.com/your-org/agro-bot-automation.git
cd agro-bot-automation
```

### Step 2: Set Production Environment Variables

#### Backend
```bash
cd backend
cp .env.example .env.production

# Edit .env.production with production values:
nano .env.production

# CRITICAL: Update these for production:
# - DATABASE_URL (production database)
# - SECRET_KEY (strong random key)
# - REDIS_PASSWORD (strong password)
# - All API keys
# - Firebase credentials
# - SMTP settings for emails
```

#### Frontend
```bash
cd ../frontend
cp .env.example .env.production

# Edit .env.production:
nano .env.production

# Update:
# - NEXT_PUBLIC_API_URL=https://api.yourdomain.com
# - Firebase configuration
```

### Step 3: SSL Certificates

#### Option A: Let's Encrypt (Recommended)
```bash
# Stop any web server on port 80/443
sudo systemctl stop nginx

# Get certificate
sudo certbot certonly --standalone \
  -d yourdomain.com \
  -d api.yourdomain.com \
  --email your@email.com

# Copy certificates
mkdir -p nginx/ssl
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/key.pem
```

#### Option B: Self-Signed (Testing Only)
```bash
mkdir -p nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/key.pem \
  -out nginx/ssl/cert.pem \
  -subj "/CN=yourdomain.com"
```

### Step 4: Update Nginx Configuration
```bash
# Edit nginx/nginx.conf
nano nginx/nginx.conf

# Replace all instances of 'yourdomain.com' with your actual domain
```

### Step 5: Deploy
```bash
# Return to project root
cd ..

# Build and start production services
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Monitor startup
docker-compose -f docker-compose.prod.yml logs -f
```

### Step 6: Verify Deployment
```bash
# Check all services are running
docker-compose -f docker-compose.prod.yml ps

# Test health endpoints
curl https://yourdomain.com/health
curl https://api.yourdomain.com/health

# Check logs for any errors
docker-compose -f docker-compose.prod.yml logs backend
```

---

## Mobile App Setup (Flutter)

### Step 1: Install Flutter
```bash
# Download Flutter SDK from: https://flutter.dev/docs/get-started/install
# Or use brew/apt:
brew install flutter  # macOS
# OR
sudo snap install flutter --classic  # Linux
```

### Step 2: Setup Project
```bash
cd mobile

# Get dependencies
flutter pub get

# Generate code
flutter pub run build_runner build --delete-conflicting-outputs
```

### Step 3: Configure Firebase
```bash
# 1. Create Firebase project at console.firebase.google.com
# 2. Add Android and iOS apps
# 3. Download config files:
#    - google-services.json → android/app/
#    - GoogleService-Info.plist → ios/Runner/
# 4. Update lib/core/config/firebase_options.dart with your credentials
```

### Step 4: Run App
```bash
# List available devices
flutter devices

# Run on device/emulator
flutter run

# Or build release
flutter build apk --release  # Android
flutter build ios --release  # iOS
```

---

## IoT Device Setup (ESP32)

### Step 1: Install Arduino IDE
```bash
# Download from: https://www.arduino.cc/en/software

# Add ESP32 board support:
# File → Preferences → Additional Board URLs:
# https://dl.espressif.com/dl/package_esp32_index.json
```

### Step 2: Install Libraries
In Arduino IDE Library Manager, install:
- WiFi (built-in)
- PubSubClient
- DHT sensor library
- ArduinoJson
- Adafruit Unified Sensor

### Step 3: Configure & Upload
```bash
# 1. Open iot/esp32_sensor_node/esp32_sensor_node.ino
# 2. Update WiFi credentials
# 3. Update MQTT broker address
# 4. Select Board: "ESP32 Dev Module"
# 5. Select correct COM port
# 6. Click Upload
```

### Step 4: Monitor
```bash
# Open Serial Monitor (115200 baud)
# You should see:
# - WiFi connection status
# - MQTT connection status
# - Sensor readings every 30 seconds
```

---

## Common Commands

### Development

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Rebuild services
docker-compose build

# View logs
docker-compose logs -f [service_name]

# Execute commands in container
docker-compose exec backend python -m app.main
docker-compose exec postgres psql -U agro_user -d agro_bot_db

# Restart specific service
docker-compose restart backend
```

### Production

```bash
# Deploy/Update
docker-compose -f docker-compose.prod.yml up -d --build

# Scale services
docker-compose -f docker-compose.prod.yml up -d --scale backend=3

# View resource usage
docker stats

# Backup database
docker exec agro_postgres_prod pg_dump -U agro_user agro_bot_db > backup.sql

# Restore database
docker exec -i agro_postgres_prod psql -U agro_user agro_bot_db < backup.sql
```

---

## Troubleshooting

### Services Won't Start

```bash
# Check if ports are already in use
netstat -tuln | grep -E '3000|8000|5432|6379'

# Kill conflicting processes
sudo lsof -ti:3000 | xargs kill -9

# Check Docker daemon
sudo systemctl status docker

# Restart Docker
sudo systemctl restart docker
```

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# View PostgreSQL logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres

# Connect to database manually
docker-compose exec postgres psql -U agro_user -d agro_bot_db
```

### Frontend Not Loading

```bash
# Check backend API is running
curl http://localhost:8000/health

# Check frontend logs
docker-compose logs frontend

# Rebuild frontend
docker-compose build frontend
docker-compose up -d frontend

# Clear browser cache and retry
```

### API Returns 500 Errors

```bash
# Check backend logs
docker-compose logs backend

# Common issues:
# 1. Missing environment variables
# 2. Database not initialized
# 3. Redis not running
# 4. Invalid API keys

# Restart backend
docker-compose restart backend
```

### Mobile App Build Fails

```bash
# Clean build
flutter clean
flutter pub get

# Update Flutter
flutter upgrade

# Check for issues
flutter doctor -v

# Fix gradlew permission (Android)
chmod +x android/gradlew
```

### IoT Device Won't Connect

```bash
# Common issues:
# 1. Wrong WiFi credentials
# 2. ESP32 only supports 2.4GHz WiFi
# 3. MQTT broker not accessible
# 4. Firewall blocking MQTT port (1883)

# Test MQTT broker
mosquitto_sub -h your-broker.com -t "test" -u agro_iot -P password

# Check serial monitor output for error messages
```

---

## System Requirements

### Development
- **CPU:** 4 cores
- **RAM:** 8 GB
- **Disk:** 20 GB SSD
- **OS:** Windows 10+, macOS 11+, Ubuntu 20.04+

### Production
- **CPU:** 8 cores (16 recommended)
- **RAM:** 16 GB (32 GB recommended)
- **Disk:** 200 GB SSD
- **OS:** Ubuntu 22.04 LTS, CentOS 8+
- **Network:** 1 Gbps

---

## Default Credentials

### Development Database
- **Host:** localhost
- **Port:** 5432
- **Database:** agro_bot_db
- **Username:** agro_user
- **Password:** agro_password

### Redis
- **Host:** localhost
- **Port:** 6379
- **Password:** (none in development)

### MQTT Broker (for IoT)
- **Host:** localhost
- **Port:** 1883
- **Username:** agro_iot
- **Password:** iot_password

**⚠️ Change all default passwords in production!**

---

## Next Steps

After getting the system running:

1. **Explore the API** - Visit http://localhost:8000/docs
2. **Test Features** - Create farms, upload images for disease detection
3. **Check Mobile App** - Build and test on device/emulator
4. **Connect IoT Device** - Upload firmware to ESP32
5. **Read Documentation** - See DEPLOYMENT_GUIDE.md and PRODUCTION_COMPLETE.md
6. **Configure Production** - Follow production deployment steps
7. **Add Monitoring** - Set up Prometheus and Grafana
8. **Run Tests** - Execute test suites
9. **Secure System** - Change default passwords, configure firewall
10. **Deploy!** - Follow production deployment guide

---

## Support

- **Documentation:** See DEPLOYMENT_GUIDE.md, PRODUCTION_COMPLETE.md
- **Issues:** Create GitHub issue
- **Email:** support@agro-bot.com
- **API Docs:** http://localhost:8000/docs

---

## Quick Links

- [Main README](README.md)
- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [Production Completion Guide](PRODUCTION_COMPLETE.md)
- [Mobile App Guide](mobile/README.md)
- [IoT Device Guide](iot/README.md)

---

**Happy Farming! 🌾**

Made with ❤️ for Smart India Hackathon 2025
