import 'package:hive_flutter/hive_flutter.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Local Storage Service
class StorageService {
  static late Box _box;
  static late SharedPreferences _prefs;

  /// Initialize storage
  static Future<void> init() async {
    // Initialize Hive
    await Hive.initFlutter();
    _box = await Hive.openBox('agro_bot_storage');
    
    // Initialize SharedPreferences
    _prefs = await SharedPreferences.getInstance();
  }

  // ========== Box Storage (Hive) ==========

  /// Save data to Hive box
  static Future<void> save(String key, dynamic value) async {
    await _box.put(key, value);
  }

  /// Get data from Hive box
  static dynamic get(String key, {dynamic defaultValue}) {
    return _box.get(key, defaultValue: defaultValue);
  }

  /// Check if key exists in Hive box
  static bool contains(String key) {
    return _box.containsKey(key);
  }

  /// Remove data from Hive box
  static Future<void> remove(String key) async {
    await _box.delete(key);
  }

  /// Clear all data from Hive box
  static Future<void> clear() async {
    await _box.clear();
  }

  // ========== Preferences Storage ==========

  /// Save string to preferences
  static Future<bool> saveString(String key, String value) async {
    return await _prefs.setString(key, value);
  }

  /// Get string from preferences
  static String? getString(String key) {
    return _prefs.getString(key);
  }

  /// Save int to preferences
  static Future<bool> saveInt(String key, int value) async {
    return await _prefs.setInt(key, value);
  }

  /// Get int from preferences
  static int? getInt(String key) {
    return _prefs.getInt(key);
  }

  /// Save bool to preferences
  static Future<bool> saveBool(String key, bool value) async {
    return await _prefs.setBool(key, value);
  }

  /// Get bool from preferences
  static bool? getBool(String key) {
    return _prefs.getBool(key);
  }

  /// Save double to preferences
  static Future<bool> saveDouble(String key, double value) async {
    return await _prefs.setDouble(key, value);
  }

  /// Get double from preferences
  static double? getDouble(String key) {
    return _prefs.getDouble(key);
  }

  /// Remove from preferences
  static Future<bool> removePreference(String key) async {
    return await _prefs.remove(key);
  }

  /// Clear all preferences
  static Future<bool> clearPreferences() async {
    return await _prefs.clear();
  }
}
