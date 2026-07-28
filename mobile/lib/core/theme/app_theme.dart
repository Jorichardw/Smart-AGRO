import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

/// Application theme configuration
class AppTheme {
  // Brand Colors
  static const Color primaryColor = Color(0xFF22C55E); // Green
  static const Color primaryDark = Color(0xFF16A34A);
  static const Color primaryLight = Color(0xFF4ADE80);
  
  static const Color secondaryColor = Color(0xFF3B82F6); // Blue
  static const Color secondaryDark = Color(0xFF2563EB);
  static const Color secondaryLight = Color(0xFF60A5FA);
  
  static const Color accentColor = Color(0xFFFBBF24); // Amber
  
  // Status Colors
  static const Color successColor = Color(0xFF10B981);
  static const Color errorColor = Color(0xFFEF4444);
  static const Color warningColor = Color(0xFFF59E0B);
  static const Color infoColor = Color(0xFF3B82F6);
  
  // Neutral Colors
  static const Color backgroundColor = Color(0xFFF9FAFB);
  static const Color surfaceColor = Colors.white;
  static const Color textPrimary = Color(0xFF111827);
  static const Color textSecondary = Color(0xFF6B7280);
  static const Color dividerColor = Color(0xFFE5E7EB);
  
  // Dark Theme Colors
  static const Color darkBackgroundColor = Color(0xFF111827);
  static const Color darkSurfaceColor = Color(0xFF1F2937);
  static const Color darkTextPrimary = Color(0xFFF9FAFB);
  static const Color darkTextSecondary = Color(0xFF9CA3AF);
  static const Color darkDividerColor = Color(0xFF374151);

  /// Light Theme
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      
      // Color Scheme
      colorScheme: const ColorScheme.light(
        primary: primaryColor,
        secondary: secondaryColor,
        surface: surfaceColor,
        background: backgroundColor,
        error: errorColor,
        onPrimary: Colors.white,
        onSecondary: Colors.white,
        onSurface: textPrimary,
        onBackground: textPrimary,
        onError: Colors.white,
      ),
      
      // App Bar
      appBarTheme: const AppBarTheme(
        elevation: 0,
        centerTitle: true,
        backgroundColor: surfaceColor,
        foregroundColor: textPrimary,
        systemOverlayStyle: SystemUiOverlayStyle(
          statusBarColor: Colors.transparent,
          statusBarIconBrightness: Brightness.dark,
        ),
        titleTextStyle: TextStyle(
          fontSize: 18,
          fontWeight: FontWeight.w600,
          color: textPrimary,
        ),
      ),
      
      // Card
      cardTheme: CardTheme(
        elevation: 2,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
        color: surfaceColor,
      ),
      
      // Input Decoration
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: surfaceColor,
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: dividerColor),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: dividerColor),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: primaryColor, width: 2),
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: errorColor),
        ),
      ),
      
      // Elevated Button
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          elevation: 0,
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
          backgroundColor: primaryColor,
          foregroundColor: Colors.white,
          textStyle: const TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
      
      // Text Button
      textButtonTheme: TextButtonThemeData(
        style: TextButton.styleFrom(
          foregroundColor: primaryColor,
          textStyle: const TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
      
      // Bottom Navigation Bar
      bottomNavigationBarTheme: const BottomNavigationBarThemeData(
        elevation: 8,
        backgroundColor: surfaceColor,
        selectedItemColor: primaryColor,
        unselectedItemColor: textSecondary,
        type: BottomNavigationBarType.fixed,
        selectedLabelStyle: TextStyle(fontSize: 12, fontWeight: FontWeight.w600),
        unselectedLabelStyle: TextStyle(fontSize: 12),
      ),
      
      // Floating Action Button
      floatingActionButtonTheme: const FloatingActionButtonThemeData(
        elevation: 4,
        backgroundColor: primaryColor,
        foregroundColor: Colors.white,
      ),
      
      // Divider
      dividerTheme: const DividerThemeData(
        color: dividerColor,
        thickness: 1,
        space: 1,
      ),
      
      // Chip
      chipTheme: ChipThemeData(
        backgroundColor: backgroundColor,
        selectedColor: primaryColor.withOpacity(0.2),
        labelStyle: const TextStyle(fontSize: 12),
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),
      
      // Typography
      textTheme: const TextTheme(
        displayLarge: TextStyle(fontSize: 32, fontWeight: FontWeight.w700, color: textPrimary),
        displayMedium: TextStyle(fontSize: 28, fontWeight: FontWeight.w700, color: textPrimary),
        displaySmall: TextStyle(fontSize: 24, fontWeight: FontWeight.w600, color: textPrimary),
        headlineMedium: TextStyle(fontSize: 20, fontWeight: FontWeight.w600, color: textPrimary),
        headlineSmall: TextStyle(fontSize: 18, fontWeight: FontWeight.w600, color: textPrimary),
        titleLarge: TextStyle(fontSize: 16, fontWeight: FontWeight.w600, color: textPrimary),
        titleMedium: TextStyle(fontSize: 14, fontWeight: FontWeight.w500, color: textPrimary),
        titleSmall: TextStyle(fontSize: 12, fontWeight: FontWeight.w500, color: textPrimary),
        bodyLarge: TextStyle(fontSize: 16, fontWeight: FontWeight.w400, color: textPrimary),
        bodyMedium: TextStyle(fontSize: 14, fontWeight: FontWeight.w400, color: textPrimary),
        bodySmall: TextStyle(fontSize: 12, fontWeight: FontWeight.w400, color: textSecondary),
        labelLarge: TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: textPrimary),
        labelSmall: TextStyle(fontSize: 10, fontWeight: FontWeight.w400, color: textSecondary),
      ),
      
      // Icon Theme
      iconTheme: const IconThemeData(
        color: textPrimary,
        size: 24,
      ),
      
      // Font Family
      fontFamily: 'Inter',
    );
  }

  /// Dark Theme
  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      
      // Color Scheme
      colorScheme: const ColorScheme.dark(
        primary: primaryColor,
        secondary: secondaryColor,
        surface: darkSurfaceColor,
        background: darkBackgroundColor,
        error: errorColor,
        onPrimary: Colors.white,
        onSecondary: Colors.white,
        onSurface: darkTextPrimary,
        onBackground: darkTextPrimary,
        onError: Colors.white,
      ),
      
      // App Bar
      appBarTheme: const AppBarTheme(
        elevation: 0,
        centerTitle: true,
        backgroundColor: darkSurfaceColor,
        foregroundColor: darkTextPrimary,
        systemOverlayStyle: SystemUiOverlayStyle(
          statusBarColor: Colors.transparent,
          statusBarIconBrightness: Brightness.light,
        ),
        titleTextStyle: TextStyle(
          fontSize: 18,
          fontWeight: FontWeight.w600,
          color: darkTextPrimary,
        ),
      ),
      
      // Card
      cardTheme: CardTheme(
        elevation: 2,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
        color: darkSurfaceColor,
      ),
      
      // Input Decoration
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: darkSurfaceColor,
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: darkDividerColor),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: darkDividerColor),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: primaryColor, width: 2),
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: errorColor),
        ),
      ),
      
      // Elevated Button
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          elevation: 0,
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
          backgroundColor: primaryColor,
          foregroundColor: Colors.white,
          textStyle: const TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
      
      // Text Button
      textButtonTheme: TextButtonThemeData(
        style: TextButton.styleFrom(
          foregroundColor: primaryColor,
          textStyle: const TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
      
      // Bottom Navigation Bar
      bottomNavigationBarTheme: const BottomNavigationBarThemeData(
        elevation: 8,
        backgroundColor: darkSurfaceColor,
        selectedItemColor: primaryColor,
        unselectedItemColor: darkTextSecondary,
        type: BottomNavigationBarType.fixed,
        selectedLabelStyle: TextStyle(fontSize: 12, fontWeight: FontWeight.w600),
        unselectedLabelStyle: TextStyle(fontSize: 12),
      ),
      
      // Floating Action Button
      floatingActionButtonTheme: const FloatingActionButtonThemeData(
        elevation: 4,
        backgroundColor: primaryColor,
        foregroundColor: Colors.white,
      ),
      
      // Divider
      dividerTheme: const DividerThemeData(
        color: darkDividerColor,
        thickness: 1,
        space: 1,
      ),
      
      // Chip
      chipTheme: ChipThemeData(
        backgroundColor: darkBackgroundColor,
        selectedColor: primaryColor.withOpacity(0.2),
        labelStyle: const TextStyle(fontSize: 12),
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),
      
      // Typography
      textTheme: const TextTheme(
        displayLarge: TextStyle(fontSize: 32, fontWeight: FontWeight.w700, color: darkTextPrimary),
        displayMedium: TextStyle(fontSize: 28, fontWeight: FontWeight.w700, color: darkTextPrimary),
        displaySmall: TextStyle(fontSize: 24, fontWeight: FontWeight.w600, color: darkTextPrimary),
        headlineMedium: TextStyle(fontSize: 20, fontWeight: FontWeight.w600, color: darkTextPrimary),
        headlineSmall: TextStyle(fontSize: 18, fontWeight: FontWeight.w600, color: darkTextPrimary),
        titleLarge: TextStyle(fontSize: 16, fontWeight: FontWeight.w600, color: darkTextPrimary),
        titleMedium: TextStyle(fontSize: 14, fontWeight: FontWeight.w500, color: darkTextPrimary),
        titleSmall: TextStyle(fontSize: 12, fontWeight: FontWeight.w500, color: darkTextPrimary),
        bodyLarge: TextStyle(fontSize: 16, fontWeight: FontWeight.w400, color: darkTextPrimary),
        bodyMedium: TextStyle(fontSize: 14, fontWeight: FontWeight.w400, color: darkTextPrimary),
        bodySmall: TextStyle(fontSize: 12, fontWeight: FontWeight.w400, color: darkTextSecondary),
        labelLarge: TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: darkTextPrimary),
        labelSmall: TextStyle(fontSize: 10, fontWeight: FontWeight.w400, color: darkTextSecondary),
      ),
      
      // Icon Theme
      iconTheme: const IconThemeData(
        color: darkTextPrimary,
        size: 24,
      ),
      
      // Font Family
      fontFamily: 'Inter',
    );
  }
}
