import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import '../config/app_config.dart';
import '../utils/logger.dart';

/// Notification Service
class NotificationService {
  static final FlutterLocalNotificationsPlugin _localNotifications =
      FlutterLocalNotificationsPlugin();
  static final FirebaseMessaging _firebaseMessaging = FirebaseMessaging.instance;

  /// Initialize notifications
  static Future<void> init() async {
    // Initialize local notifications
    const androidSettings = AndroidInitializationSettings('@mipmap/ic_launcher');
    const iosSettings = DarwinInitializationSettings(
      requestAlertPermission: true,
      requestBadgePermission: true,
      requestSoundPermission: true,
    );
    
    const initSettings = InitializationSettings(
      android: androidSettings,
      iOS: iosSettings,
    );

    await _localNotifications.initialize(
      initSettings,
      onDidReceiveNotificationResponse: _onNotificationTapped,
    );

    // Create notification channel for Android
    const androidChannel = AndroidNotificationChannel(
      AppConfig.notificationChannelId,
      AppConfig.notificationChannelName,
      description: AppConfig.notificationChannelDescription,
      importance: Importance.high,
      playSound: true,
    );

    await _localNotifications
        .resolvePlatformSpecificImplementation<
            AndroidFlutterLocalNotificationsPlugin>()
        ?.createNotificationChannel(androidChannel);

    // Initialize Firebase messaging
    await _initFirebaseMessaging();
  }

  /// Initialize Firebase Messaging
  static Future<void> _initFirebaseMessaging() async {
    // Request permission
    NotificationSettings settings = await _firebaseMessaging.requestPermission(
      alert: true,
      badge: true,
      sound: true,
      provisional: false,
    );

    if (settings.authorizationStatus == AuthorizationStatus.authorized) {
      Logger.info('User granted notification permissions');
    } else {
      Logger.warning('User declined or has not accepted notification permissions');
    }

    // Get FCM token
    String? token = await _firebaseMessaging.getToken();
    Logger.info('FCM Token: $token');

    // Listen to token refresh
    _firebaseMessaging.onTokenRefresh.listen((newToken) {
      Logger.info('FCM Token refreshed: $newToken');
      // TODO: Send token to backend
    });

    // Handle foreground messages
    FirebaseMessaging.onMessage.listen((RemoteMessage message) {
      Logger.info('Foreground message received: ${message.messageId}');
      _showLocalNotification(message);
    });

    // Handle notification taps when app is in background
    FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message) {
      Logger.info('Notification tapped: ${message.messageId}');
      _handleNotificationTap(message);
    });
  }

  /// Show local notification
  static Future<void> _showLocalNotification(RemoteMessage message) async {
    final notification = message.notification;
    final android = message.notification?.android;

    if (notification != null) {
      await _localNotifications.show(
        notification.hashCode,
        notification.title,
        notification.body,
        NotificationDetails(
          android: AndroidNotificationDetails(
            AppConfig.notificationChannelId,
            AppConfig.notificationChannelName,
            channelDescription: AppConfig.notificationChannelDescription,
            importance: Importance.high,
            priority: Priority.high,
            icon: android?.smallIcon ?? '@mipmap/ic_launcher',
          ),
          iOS: const DarwinNotificationDetails(
            presentAlert: true,
            presentBadge: true,
            presentSound: true,
          ),
        ),
        payload: message.data.toString(),
      );
    }
  }

  /// Handle notification tap
  static void _onNotificationTapped(NotificationResponse response) {
    Logger.info('Notification tapped: ${response.payload}');
    // TODO: Navigate to relevant screen based on payload
  }

  /// Handle Firebase notification tap
  static void _handleNotificationTap(RemoteMessage message) {
    Logger.info('Firebase notification tapped: ${message.data}');
    // TODO: Navigate to relevant screen based on data
  }

  /// Show custom notification
  static Future<void> showNotification({
    required String title,
    required String body,
    String? payload,
  }) async {
    await _localNotifications.show(
      DateTime.now().millisecondsSinceEpoch % 100000,
      title,
      body,
      const NotificationDetails(
        android: AndroidNotificationDetails(
          AppConfig.notificationChannelId,
          AppConfig.notificationChannelName,
          channelDescription: AppConfig.notificationChannelDescription,
          importance: Importance.high,
          priority: Priority.high,
        ),
        iOS: DarwinNotificationDetails(
          presentAlert: true,
          presentBadge: true,
          presentSound: true,
        ),
      ),
      payload: payload,
    );
  }

  /// Cancel notification
  static Future<void> cancelNotification(int id) async {
    await _localNotifications.cancel(id);
  }

  /// Cancel all notifications
  static Future<void> cancelAllNotifications() async {
    await _localNotifications.cancelAll();
  }

  /// Get FCM token
  static Future<String?> getFCMToken() async {
    return await _firebaseMessaging.getToken();
  }

  /// Subscribe to topic
  static Future<void> subscribeToTopic(String topic) async {
    await _firebaseMessaging.subscribeToTopic(topic);
    Logger.info('Subscribed to topic: $topic');
  }

  /// Unsubscribe from topic
  static Future<void> unsubscribeFromTopic(String topic) async {
    await _firebaseMessaging.unsubscribeFromTopic(topic);
    Logger.info('Unsubscribed from topic: $topic');
  }
}
