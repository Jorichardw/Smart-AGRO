import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:connectivity_plus/connectivity_plus.dart';

/// Connectivity State
enum ConnectivityState {
  connected,
  disconnected,
  unknown,
}

/// Connectivity Provider
final connectivityProvider = StreamProvider<ConnectivityState>((ref) {
  return Connectivity().onConnectivityChanged.map((result) {
    if (result.contains(ConnectivityResult.none)) {
      return ConnectivityState.disconnected;
    } else {
      return ConnectivityState.connected;
    }
  });
});
