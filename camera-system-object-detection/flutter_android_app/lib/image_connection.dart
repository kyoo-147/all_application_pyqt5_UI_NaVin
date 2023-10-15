import 'package:flutter/cupertino.dart';
import 'package:flutter_background_service/flutter_background_service.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:io';
import 'dart:core';
import 'dart:async';
import 'dart:typed_data';
import 'package:flutter_android_app/image_receiver.dart';

class ImageConnection extends ChangeNotifier {
  final FRAGMENT_SIZE = 1000;
  final MAX_WAIT_TIME_MILSEC = 5000;

  // Frame variables
  late Uint8List _frameReceived;

  Uint8List get frameReceived => _frameReceived;
  // bool _autoConnect = false;
  ConnectionState _connectionState = ConnectionState.none;
  final _timeSinceLastResponse = Stopwatch();
  Socket? _socket;
  final Stream<Map<String, dynamic>?> _connectionStream;
  Timer? _connectionCheckerTimer;
  var imageReceiver = ImageReceiver();

  Widget? frame;

  ImageConnection(this._connectionStream) {
    imageReceiver.frameStream.stream.listen(displayImage);

    _connectionStream.listen((Map<String, dynamic>? event) {
      switch (ConnectionState.values[event?['state']]) {
        case ConnectionState.done:
          // If Notifications Connection is established, start Image Connection
          start();
          break;
        default:
          // If Notifications Connection is lost, stop Image Connection
          stop();
      }
    });
  }

  void start() {
    FlutterBackgroundService().invoke('requestVideo');
    _connect();
    _connectionCheckerTimer =
        Timer.periodic(const Duration(seconds: 5), (Timer _) {
      if (_timeSinceLastResponse.elapsedMilliseconds > MAX_WAIT_TIME_MILSEC) {
        try {
          FlutterBackgroundService().invoke('requestVideo');
          _connect();
        } catch (e) {
          debugPrint('socket exception');
        }
      }
    });
    _timeSinceLastResponse.start();
  }

  void stop() {
    _socket?.destroy();
    _connectionState = ConnectionState.none;
    _connectionCheckerTimer?.cancel();
    _timeSinceLastResponse
      ..reset()
      ..stop();
  }

  void _connect() async {
    if (_connectionState == ConnectionState.waiting) {
      return;
    }
    _connectionState = ConnectionState.waiting;

    _socket?.destroy();

    final prefs = await SharedPreferences.getInstance();
    String? serverIP = prefs.getString('server_ip');

    try {
      _socket = await Socket.connect(serverIP, 4444,
          timeout: const Duration(seconds: 5));
      _socket?.handleError((error) => debugPrint('socket error'));
    } catch (e) {
      _connectionState = ConnectionState.none;
      return;
    }

    // Connected to image server
    FlutterBackgroundService().invoke('stopRequestingVideo');
    _connectionState = ConnectionState.done;
    _timeSinceLastResponse.reset();

    _socket?.listen((event) {
      _timeSinceLastResponse.reset();

      try {
        imageReceiver.addPacket(event);
      } catch (e) {
        debugPrint(e.toString());
      }
    });
  }

  void displayImage(Uint8List frameReceived) {
    try {
      Image img = Image.memory(
        frameReceived,
        gaplessPlayback: true,
      );
      frame = img;
      notifyListeners();
    } catch (e) {
      debugPrint('Exception: ${e.toString()}');
    }
  }
}
