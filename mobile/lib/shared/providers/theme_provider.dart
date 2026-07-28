import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/services/storage_service.dart';
import '../../core/config/app_config.dart';

/// Theme Mode Provider
final themeModeProvider = StateNotifierProvider<ThemeModeNotifier, ThemeMode>((ref) {
  return ThemeModeNotifier();
});

/// Theme Mode Notifier
class ThemeModeNotifier extends StateNotifier<ThemeMode> {
  ThemeModeNotifier() : super(ThemeMode.light) {
    _loadThemeMode();
  }

  /// Load theme mode from storage
  Future<void> _loadThemeMode() async {
    final themeMode = StorageService.getString(AppConfig.storageKeyThemeMode);
    if (themeMode != null) {
      state = ThemeMode.values.firstWhere(
        (mode) => mode.toString() == themeMode,
        orElse: () => ThemeMode.light,
      );
    }
  }

  /// Set theme mode
  Future<void> setThemeMode(ThemeMode mode) async {
    state = mode;
    await StorageService.saveString(
      AppConfig.storageKeyThemeMode,
      mode.toString(),
    );
  }

  /// Toggle theme
  Future<void> toggleTheme() async {
    final newMode = state == ThemeMode.light ? ThemeMode.dark : ThemeMode.light;
    await setThemeMode(newMode);
  }
}
