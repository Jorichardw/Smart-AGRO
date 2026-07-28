# 🚀 AGRO-BOT & AUTOMATION - Complete Setup and Run Guide

## ⚡ Quick Links
- **[Quick Start →](QUICKSTART.md)** - Get running in 10 minutes
- **[Production Deployment →](DEPLOYMENT_GUIDE.md)** - Full production setup
- **[Project Status →](PROJECT_STATUS.md)** - Current completion status
- **[Production Complete →](PRODUCTION_COMPLETE.md)** - What's implemented

---

# AGRO-BOT & AUTOMATION - Setup and Run Guide

## 🚀 Current Implementation Status

### ✅ **COMPLETED (Core Foundation)**
- **Database Schema**: Comprehensive PostgreSQL schema with 25+ tables
- **Backend API**: FastAPI application with authentication, users, and farms
- **Database Models**: SQLAlchemy models for all core entities
- **Services Layer**: Business logic services with CRUD operations
- **Authentication**: Firebase integration with JWT tokens
- **API Endpoints**: User management, farm management, and placeholder endpoints
- **Frontend Structure**: Next.js app with Tailwind CSS
- **Docker Setup**: Multi-service containerization
- **Project Structure**: Professional organization and architecture

### 🟡 **IN PROGRESS (Functional but Basic)**
- **API Documentation**: Auto-generated Swagger docs
- **Error Handling**: Basic error handling and logging
- **Security**: Role-based access control
- **File Upload**: Basic structure for image processing

### ❌ **NOT YET IMPLEMENTED**
- **AI/ML Services**: Disease detection, pest identification, yield prediction
- **Weather Integration**: External weather API integration
- **IoT Integration**: Real-time sensor data processing
- **Frontend Components**: React components and pages
- **Mobile App**: Flutter implementation
- **Admin Dashboard**: Management interface
- **Real-time Features**: WebSocket connections, live updates

## 🛠️ **Setup Instructions**

### **Prerequisites**
```bash
# Required software
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Docker & Docker Compose (optional)
```

### **1. Database Setup**

#### Option A: Using Docker (Recommended)
```bash
# Start PostgreSQL with Docker
cd "Smart AGRO"
docker-compose up -d postgres

# Database will be available at localhost:5432
# Database: agro_bot_db
# Username: agro_user  
# Password: agro_password
```

#### Option B: Local PostgreSQL
```bash
# Install PostgreSQL and create database
createdb agro_bot_db
createuser agro_user
# Set password and grant permissions
```

### **2. Backend Setup**
```bash
# Navigate to backend directory
cd "Smart AGRO/backend"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
copy .env.example .env
# Edit .env with your configuration

# Run database migrations
python -c "from app.core.database import create_tables; create_tables()"

# Test backend setup
cd ..
python test_backend.py
```

### **3. Frontend Setup**
```bash
# Navigate to frontend directory  
cd "Smart AGRO/frontend"

# Install dependencies
npm install

# Set up environment variables
copy .env.example .env.local
# Edit .env.local with your configuration
```

### **4. Firebase Setup (Optional for Development)**
```bash
# Create Firebase project at https://firebase.google.com
# Download service account key as firebase-config.json
# Place in backend/firebase-config.json

# For development, mock authentication will work without Firebase
```

## 🚀 **Running the Application**

### **Option 1: Using Docker Compose (Easiest)**
```bash
# From root directory
cd "Smart AGRO"

# Start all services
docker-compose up -d

# Services will be available at:
# Backend API: http://localhost:8000
# Frontend: http://localhost:3000
# Database: localhost:5432
# Redis: localhost:6379
```

### **Option 2: Manual Start (Development)**

#### Start Backend
```bash
cd "Smart AGRO/backend"

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# API will be available at http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

#### Start Frontend
```bash
cd "Smart AGRO/frontend"

# Start Next.js development server
npm run dev

# Frontend will be available at http://localhost:3000
```

## 📖 **Testing the Setup**

### **1. Test Backend API**
```bash
# Health check
curl http://localhost:8000/health

# API info
curl http://localhost:8000/api/info

# API documentation
open http://localhost:8000/docs
```

### **2. Test Frontend**
```bash
# Open in browser
open http://localhost:3000

# Should show AGRO-BOT homepage with API status
```

### **3. Test Database Connection**
```bash
# From backend directory
python -c "from app.core.database import test_connection; print(test_connection())"
```

## 🔧 **Development Workflow**

### **Backend Development**
```bash
cd backend

# Run with auto-reload
uvicorn app.main:app --reload

# Add new model
# 1. Create model in app/models/
# 2. Add to app/models/__init__.py
# 3. Create service in app/services/
# 4. Add API endpoints in app/api/v1/endpoints/
# 5. Update API router in app/api/v1/__init__.py

# Database changes
python -c "from app.core.database import create_tables; create_tables()"
```

### **Frontend Development**
```bash
cd frontend

# Run development server
npm run dev

# Add new components in src/components/
# Add new pages in src/pages/
# API calls in src/services/
```

## 🧪 **API Testing**

### **Authentication Flow**
```bash
# 1. Register user (mock token for development)
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "firebase_id_token": "mock_token_123",
    "email": "farmer@example.com",
    "first_name": "John",
    "last_name": "Farmer",
    "role": "farmer"
  }'

# 2. Login (get access token)
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "firebase_id_token": "mock_token_123"
  }'

# 3. Use token for authenticated requests
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### **Farm Management**
```bash
# Create farm (requires authentication)
curl -X POST http://localhost:8000/api/v1/farms/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Green Valley Farm",
    "address": "123 Farm Road",
    "total_area": 25.5,
    "farm_type": "organic"
  }'

# Get farms
curl -X GET http://localhost:8000/api/v1/farms/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🚨 **Troubleshooting**

### **Common Issues**

#### Database Connection Error
```bash
# Check if PostgreSQL is running
docker ps  # or
pg_isready -h localhost -p 5432

# Check connection string in backend/.env
DATABASE_URL=postgresql://agro_user:agro_password@localhost:5432/agro_bot_db
```

#### Import Errors
```bash
# Ensure Python path is correct
cd backend
python -c "import app.main; print('Backend imports OK')"

# Reinstall dependencies
pip install -r requirements.txt
```

#### Frontend Build Errors
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check Node.js version
node --version  # Should be 18+
```

#### Port Conflicts
```bash
# Check what's running on ports
netstat -an | findstr :8000  # Backend
netstat -an | findstr :3000  # Frontend
netstat -an | findstr :5432  # Database

# Kill processes if needed
taskkill /f /pid PID_NUMBER  # Windows
kill -9 PID_NUMBER          # Linux/Mac
```

## 🔄 **Next Development Steps**

### **Priority 1: Complete Core Features**
1. Implement weather API integration
2. Build basic disease detection (image upload)
3. Create farmer profile management
4. Add crop management functionality

### **Priority 2: Enhance User Experience**  
1. Build React components and pages
2. Implement authentication flow in frontend
3. Add real-time notifications
4. Create responsive mobile design

### **Priority 3: Advanced Features**
1. Integrate AI/ML models for disease detection
2. Implement IoT data collection
3. Build marketplace functionality
4. Add analytics and reporting

## 📞 **Support**

### **Logs and Debugging**
```bash
# Backend logs
tail -f backend/logs/agro_bot.log

# Frontend logs  
# Check browser console

# Database logs
docker logs agro_postgres
```

### **Development Tools**
- **API Documentation**: http://localhost:8000/docs
- **Database Admin**: pgAdmin or DBeaver
- **API Testing**: Postman, curl, or built-in docs
- **Code Quality**: Black, flake8 for Python; ESLint for JavaScript

---

**Built for Smart India Hackathon 2025**  
*AI-Powered Smart Agriculture Platform*