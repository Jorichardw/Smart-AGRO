import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../features/auth/presentation/pages/login_page.dart';
import '../../features/auth/presentation/pages/register_page.dart';
import '../../features/auth/presentation/pages/forgot_password_page.dart';
import '../../features/dashboard/presentation/pages/dashboard_page.dart';
import '../../features/farms/presentation/pages/farms_list_page.dart';
import '../../features/farms/presentation/pages/farm_detail_page.dart';
import '../../features/weather/presentation/pages/weather_page.dart';
import '../../features/disease_detection/presentation/pages/disease_detection_page.dart';
import '../../features/pest_detection/presentation/pages/pest_detection_page.dart';
import '../../features/iot/presentation/pages/iot_dashboard_page.dart';
import '../../features/marketplace/presentation/pages/marketplace_page.dart';
import '../../features/government_schemes/presentation/pages/schemes_page.dart';
import '../../features/ai_assistant/presentation/pages/ai_assistant_page.dart';
import '../../features/profile/presentation/pages/profile_page.dart';
import '../../features/settings/presentation/pages/settings_page.dart';
import '../../features/notifications/presentation/pages/notifications_page.dart';
import '../../features/onboarding/presentation/pages/splash_page.dart';
import '../../features/onboarding/presentation/pages/onboarding_page.dart';

/// App Router Configuration
class AppRouter {
  static final GoRouter router = GoRouter(
    initialLocation: '/splash',
    debugLogDiagnostics: true,
    routes: [
      // Splash & Onboarding
      GoRoute(
        path: '/splash',
        name: 'splash',
        builder: (context, state) => const SplashPage(),
      ),
      GoRoute(
        path: '/onboarding',
        name: 'onboarding',
        builder: (context, state) => const OnboardingPage(),
      ),
      
      // Authentication
      GoRoute(
        path: '/login',
        name: 'login',
        builder: (context, state) => const LoginPage(),
      ),
      GoRoute(
        path: '/register',
        name: 'register',
        builder: (context, state) => const RegisterPage(),
      ),
      GoRoute(
        path: '/forgot-password',
        name: 'forgot-password',
        builder: (context, state) => const ForgotPasswordPage(),
      ),
      
      // Main App
      GoRoute(
        path: '/',
        name: 'dashboard',
        builder: (context, state) => const DashboardPage(),
      ),
      
      // Farms
      GoRoute(
        path: '/farms',
        name: 'farms',
        builder: (context, state) => const FarmsListPage(),
        routes: [
          GoRoute(
            path: ':id',
            name: 'farm-detail',
            builder: (context, state) {
              final farmId = state.pathParameters['id']!;
              return FarmDetailPage(farmId: farmId);
            },
          ),
        ],
      ),
      
      // Weather
      GoRoute(
        path: '/weather',
        name: 'weather',
        builder: (context, state) => const WeatherPage(),
      ),
      
      // Disease Detection
      GoRoute(
        path: '/disease-detection',
        name: 'disease-detection',
        builder: (context, state) => const DiseaseDetectionPage(),
      ),
      
      // Pest Detection
      GoRoute(
        path: '/pest-detection',
        name: 'pest-detection',
        builder: (context, state) => const PestDetectionPage(),
      ),
      
      // IoT Dashboard
      GoRoute(
        path: '/iot',
        name: 'iot',
        builder: (context, state) => const IoTDashboardPage(),
      ),
      
      // Marketplace
      GoRoute(
        path: '/marketplace',
        name: 'marketplace',
        builder: (context, state) => const MarketplacePage(),
      ),
      
      // Government Schemes
      GoRoute(
        path: '/schemes',
        name: 'schemes',
        builder: (context, state) => const SchemesPage(),
      ),
      
      // AI Assistant
      GoRoute(
        path: '/ai-assistant',
        name: 'ai-assistant',
        builder: (context, state) => const AIAssistantPage(),
      ),
      
      // Profile & Settings
      GoRoute(
        path: '/profile',
        name: 'profile',
        builder: (context, state) => const ProfilePage(),
      ),
      GoRoute(
        path: '/settings',
        name: 'settings',
        builder: (context, state) => const SettingsPage(),
      ),
      
      // Notifications
      GoRoute(
        path: '/notifications',
        name: 'notifications',
        builder: (context, state) => const NotificationsPage(),
      ),
    ],
    
    // Error handling
    errorBuilder: (context, state) => Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.error_outline, size: 64, color: Colors.red),
            const SizedBox(height: 16),
            Text(
              'Page Not Found',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 8),
            Text(
              state.uri.toString(),
              style: Theme.of(context).textTheme.bodySmall,
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: () => context.go('/'),
              child: const Text('Go to Dashboard'),
            ),
          ],
        ),
      ),
    ),
  );
}
