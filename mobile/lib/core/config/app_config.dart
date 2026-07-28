/// App Configuration
class AppConfig {
  static const String appName = 'AGRO-BOT';
  static const String appTagline = 'Smart Agriculture Platform';
  static const String appVersion = '1.0.0';
  static const int appBuildNumber = 1;
  
  // API Configuration
  static const String baseUrl = String.fromEnvironment(
    'API_URL',
    defaultValue: 'http://10.0.2.2:8000', // Android emulator localhost
  );
  static const String apiVersion = 'v1';
  static const String apiPrefix = '/api/$apiVersion';
  
  // Timeouts (in seconds)
  static const int connectTimeout = 30;
  static const int receiveTimeout = 30;
  static const int sendTimeout = 30;
  
  // Pagination
  static const int defaultPageSize = 20;
  static const int maxPageSize = 100;
  
  // Cache
  static const Duration cacheValidDuration = Duration(hours: 1);
  static const int maxCacheSize = 50 * 1024 * 1024; // 50MB
  
  // Image Upload
  static const int maxImageSize = 10 * 1024 * 1024; // 10MB
  static const double imageQuality = 0.8;
  static const int maxImageWidth = 1920;
  static const int maxImageHeight = 1080;
  
  // Location
  static const double defaultLatitude = 28.6139;
  static const double defaultLongitude = 77.2090;
  static const double locationAccuracy = 100; // meters
  
  // Notification
  static const String notificationChannelId = 'agro_bot_notifications';
  static const String notificationChannelName = 'AGRO-BOT Notifications';
  static const String notificationChannelDescription = 
      'Notifications for weather alerts, disease detection, and farm updates';
  
  // Storage Keys
  static const String storageKeyAuthToken = 'auth_token';
  static const String storageKeyRefreshToken = 'refresh_token';
  static const String storageKeyUserId = 'user_id';
  static const String storageKeyUserData = 'user_data';
  static const String storageKeyThemeMode = 'theme_mode';
  static const String storageKeyLanguage = 'language';
  static const String storageKeyNotificationsEnabled = 'notifications_enabled';
  static const String storageKeyBiometricEnabled = 'biometric_enabled';
  
  // Feature Flags
  static const bool enableAnalytics = true;
  static const bool enableCrashReporting = true;
  static const bool enableBiometric = true;
  static const bool enableVoiceAssistant = true;
  static const bool enableOfflineMode = true;
  
  // Weather
  static const int weatherForecastDays = 7;
  static const Duration weatherUpdateInterval = Duration(hours: 3);
  
  // IoT
  static const Duration iotDataUpdateInterval = Duration(seconds: 30);
  static const int maxIoTDevicesPerFarm = 50;
  
  // Marketplace
  static const String defaultCurrency = 'INR';
  static const String currencySymbol = '₹';
  
  // Support
  static const String supportEmail = 'support@agro-bot.com';
  static const String supportPhone = '+91-1800-123-4567';
  static const String websiteUrl = 'https://agro-bot.com';
  static const String privacyPolicyUrl = 'https://agro-bot.com/privacy';
  static const String termsOfServiceUrl = 'https://agro-bot.com/terms';
  
  // Social Media
  static const String facebookUrl = 'https://facebook.com/agrobot';
  static const String twitterUrl = 'https://twitter.com/agrobot';
  static const String instagramUrl = 'https://instagram.com/agrobot';
  static const String linkedinUrl = 'https://linkedin.com/company/agrobot';
  
  // Deep Links
  static const String deepLinkScheme = 'agrobot';
  static const String universalLinkHost = 'agro-bot.com';
  
  // Map
  static const double defaultMapZoom = 15.0;
  static const double mapMinZoom = 8.0;
  static const double mapMaxZoom = 20.0;
  
  // AI
  static const double diseaseConfidenceThreshold = 0.7;
  static const double pestConfidenceThreshold = 0.6;
  static const int maxChatHistoryMessages = 50;
  
  // Development
  static const bool isDevelopment = bool.fromEnvironment('DEBUG', defaultValue: false);
  static const bool enableLogging = true;
  static const bool enableMockData = false;
}
