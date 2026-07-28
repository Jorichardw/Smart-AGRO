# AGRO-BOT Mobile App (Flutter)

## 🚀 Features Implemented

### Core Infrastructure
- ✅ App theme (light & dark mode)
- ✅ Navigation with GoRouter
- ✅ Firebase integration (Auth, Storage, Messaging, Analytics, Crashlytics)
- ✅ Local storage (Hive & SharedPreferences)
- ✅ Push notifications
- ✅ Connectivity monitoring
- ✅ Logging system

### Features
- Dashboard with quick access cards
- Farm management (list, detail, add, edit)
- Weather monitoring with forecasts
- Disease detection with camera
- Pest detection with AI
- IoT device dashboard
- Marketplace for agricultural products
- Government schemes browser
- AI voice assistant
- Profile management
- Settings and preferences
- Notifications center

### Screens Structure

```
lib/
├── core/
│   ├── config/          # App configuration, Firebase options
│   ├── routing/         # GoRouter navigation setup
│   ├── services/        # Notification, Storage services
│   ├── theme/           # App theme configuration
│   └── utils/           # Logger, helpers
├── features/
│   ├── onboarding/      # Splash, Onboarding pages
│   ├── auth/            # Login, Register, Forgot Password
│   ├── dashboard/       # Main dashboard
│   ├── farms/           # Farm list, detail, management
│   ├── weather/         # Weather monitoring
│   ├── disease_detection/  # AI disease detection
│   ├── pest_detection/  # AI pest detection
│   ├── iot/             # IoT device dashboard
│   ├── marketplace/     # Agricultural marketplace
│   ├── government_schemes/ # Government schemes
│   ├── ai_assistant/    # AI voice assistant
│   ├── profile/         # User profile
│   ├── settings/        # App settings
│   └── notifications/   # Notifications center
└── shared/
    ├── providers/       # Global state providers
    ├── widgets/         # Reusable widgets
    └── models/          # Data models
```

## 🛠️ Setup Instructions

### Prerequisites
- Flutter SDK 3.16+
- Dart SDK 3.0+
- Android Studio / Xcode
- Firebase project configured

### Installation

```bash
# Install dependencies
cd mobile
flutter pub get

# Generate code
flutter pub run build_runner build --delete-conflicting-outputs

# Run the app
flutter run

# Build for production
flutter build apk --release  # Android
flutter build ios --release  # iOS
```

### Firebase Configuration

1. Create a Firebase project at [console.firebase.google.com](https://console.firebase.google.com)
2. Add Android and iOS apps
3. Download configuration files:
   - `google-services.json` → `android/app/`
   - `GoogleService-Info.plist` → `ios/Runner/`
4. Update `lib/core/config/firebase_options.dart` with your project credentials

### Environment Variables

Create a `.env` file:
```
API_URL=https://api.agro-bot.com
DEBUG=false
```

## 📱 Build & Release

### Android

```bash
# Generate signing key
keytool -genkey -v -keystore agro-bot-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias agro-bot

# Update android/key.properties
storePassword=your_password
keyPassword=your_password
keyAlias=agro-bot
storeFile=agro-bot-key.jks

# Build release APK
flutter build apk --release

# Build App Bundle for Play Store
flutter build appbundle --release
```

### iOS

```bash
# Open Xcode
open ios/Runner.xcworkspace

# Configure signing & capabilities
# Build archive for App Store
flutter build iosarchive
```

## 🎨 App Features

### 1. Dashboard
- Weather summary
- Farm status cards
- Quick actions (Disease Detection, IoT, Weather)
- Recent alerts
- Analytics summary

### 2. Farm Management
- List all farms
- Add/Edit farm details
- View farm plots
- Crop management
- Soil health monitoring

### 3. Weather
- Current weather conditions
- 7-day forecast
- Weather alerts
- Historical data
- Location-based weather

### 4. Disease Detection
- Capture plant images
- AI-powered disease identification
- Treatment recommendations
- Detection history
- Severity assessment

### 5. Pest Detection
- Identify pests from images
- AI classification
- Control measures
- Pest life cycle info

### 6. IoT Dashboard
- Real-time sensor data
- Device management
- Historical charts
- Alerts & notifications
- Remote control

### 7. Marketplace
- Browse products
- Categories (Seeds, Fertilizers, Equipment)
- Shopping cart
- Order tracking
- Reviews & ratings

### 8. Government Schemes
- Browse available schemes
- Apply for schemes
- Track applications
- Eligibility checker
- Document upload

### 9. AI Assistant
- Voice-enabled chat
- Farming advice
- Multilingual support
- Chat history
- Context-aware responses

### 10. Profile & Settings
- User profile management
- Theme toggle (Light/Dark)
- Language selection
- Notification preferences
- Biometric authentication

## 📦 Dependencies

### Core
- `flutter_riverpod` - State management
- `go_router` - Navigation
- `dio` - HTTP client
- `hive` - Local database
- `shared_preferences` - Key-value storage

### Firebase
- `firebase_core`
- `firebase_auth`
- `firebase_storage`
- `firebase_messaging`
- `firebase_analytics`
- `firebase_crashlytics`

### UI
- `flutter_svg`
- `cached_network_image`
- `shimmer`
- `lottie`
- `fl_chart`

### Device Features
- `camera`
- `image_picker`
- `geolocator`
- `google_maps_flutter`
- `speech_to_text`
- `flutter_tts`

## 🧪 Testing

```bash
# Run unit tests
flutter test

# Run integration tests
flutter test integration_test

# Code coverage
flutter test --coverage
```

## 📄 License

MIT License - See LICENSE file for details

---

**Made with ❤️ for Farmers**
