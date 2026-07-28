import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:hive_flutter/hive_flutter.dart';

import 'core/config/app_config.dart';
import 'core/config/firebase_options.dart';
import 'core/routing/app_router.dart';
import 'core/theme/app_theme.dart';
import 'core/services/notification_service.dart';
import 'core/services/storage_service.dart';
import 'core/utils/logger.dart';
import 'shared/providers/connectivity_provider.dart';
import 'shared/providers/theme_provider.dart';

/// Background message handler for Firebase messaging
@pragma('vm:entry-point')
Future<void> firebaseMessagingBackgroundHandler(RemoteMessage message) async {
  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
  Logger.info('Background message received: ${message.messageId}');
}

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Firebase
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  
  // Initialize Hive for local storage
  await Hive.initFlutter();
  await StorageService.init();
  
  // Initialize notifications
  await NotificationService.init();
  
  // Set Firebase messaging background handler
  FirebaseMessaging.onBackgroundMessage(firebaseMessagingBackgroundHandler);
  
  // Set system UI overlay style
  SystemChrome.setSystemUIOverlayStyle(
    const SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.dark,
      systemNavigationBarColor: Colors.white,
      systemNavigationBarIconBrightness: Brightness.dark,
    ),
  );
  
  // Set preferred orientations
  await SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);
  
  Logger.info('AGRO-BOT Mobile App Starting...');
  
  runApp(
    ProviderScope(
      child: AgroBotApp(),
    ),
  );
}

class AgroBotApp extends ConsumerWidget {
  const AgroBotApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final appRouter = ref.watch(appRouterProvider);
    final themeMode = ref.watch(themeModeProvider);
    final connectivity = ref.watch(connectivityProvider);
    
    return MaterialApp.router(
      title: AppConfig.appName,
      debugShowCheckedModeBanner: false,
      
      // Routing
      routerConfig: appRouter,
      
      // Theme
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: themeMode,
      
      // Localization
      supportedLocales: const [
        Locale('en', 'US'), // English
        Locale('hi', 'IN'), // Hindi
        Locale('ta', 'IN'), // Tamil
        Locale('te', 'IN'), // Telugu
        Locale('kn', 'IN'), // Kannada
        Locale('ml', 'IN'), // Malayalam
        Locale('bn', 'IN'), // Bengali
        Locale('gu', 'IN'), // Gujarati
        Locale('mr', 'IN'), // Marathi
        Locale('pa', 'IN'), // Punjabi
      ],
      
      // Performance
      builder: (context, child) {
        return MediaQuery(
          // Prevent font scaling beyond reasonable limits
          data: MediaQuery.of(context).copyWith(
            textScaleFactor: MediaQuery.of(context).textScaleFactor.clamp(0.8, 1.3),
          ),
          child: ConnectivityWrapper(
            connectivity: connectivity,
            child: child ?? const SizedBox(),
          ),
        );
      },
    );
  }
}

/// Wrapper widget to handle connectivity status
class ConnectivityWrapper extends StatelessWidget {
  final ConnectivityState connectivity;
  final Widget child;
  
  const ConnectivityWrapper({
    super.key,
    required this.connectivity,
    required this.child,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          child,
          if (connectivity == ConnectivityState.disconnected)
            Positioned(
              top: MediaQuery.of(context).padding.top,
              left: 0,
              right: 0,
              child: Container(
                padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                decoration: BoxDecoration(
                  color: Colors.red.shade600,
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.1),
                      blurRadius: 4,
                      offset: const Offset(0, 2),
                    ),
                  ],
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(
                      Icons.wifi_off_rounded,
                      color: Colors.white,
                      size: 16,
                    ),
                    const SizedBox(width: 8),
                    Text(
                      'No Internet Connection',
                      style: Theme.of(context).textTheme.bodySmall?.copyWith(
                        color: Colors.white,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }
}

/// Provider for app router
final appRouterProvider = Provider<GoRouter>((ref) {
  return AppRouter.router;
});