import 'package:flutter/cupertino.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_background_service/flutter_background_service.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:io';
import 'dart:core';
import 'dart:async';
import 'dart:convert';
import 'package:flutter_android_app/triggers_notifications.dart';
import 'package:flutter_android_app/image_receiver.dart';

class TriggersConnection {
  final MAX_WAIT_TIME_MILSEC = 4000;
  final CHECK_CONNECTION_PERIOD_SEC = 20;
  final ALARM_PREFIX_MSG = 'trigger-alarm';
  final PACKET_PREFIX_MSG = 'frame-packet';
  final NOTIFICATION_PREFIX_MSG = 'trigger-notification';

  Socket? _socket;
  final _timeSinceLastResponse = Stopwatch();
  final triggersNotifications = TriggersNotifications();
  String? serverIP;
  ConnectionState _connectionState = ConnectionState.none;
  // String _connectionMessage = 'img-and-notif';
  String _connectionMessage = 'connected';
  Map<String, dynamic>? alarmReceived;
  var imageReceiver = ImageReceiver();

  Function onUpdateState;
  Function onTriggerAlarmReceived;
  Function ifAppIsClosed;

  set connectionState(value) {
    _connectionState = value;
    onUpdateState(value);
  }

  ConnectionState get connectionState => _connectionState;

  TriggersConnection({
    required this.onUpdateState,
    required this.onTriggerAlarmReceived,
    required this.ifAppIsClosed,
  }) {
    imageReceiver.frameStream.stream.listen((Uint8List frame) {
      print('[Triggers Connection] Frame arrived');
    });

    Timer.periodic(Duration(seconds: CHECK_CONNECTION_PERIOD_SEC), (_) {
      if (_timeSinceLastResponse.elapsedMilliseconds > MAX_WAIT_TIME_MILSEC) {
        connectNotifications();
      }
    });
    _timeSinceLastResponse.start();

    SharedPreferences.getInstance().then((prefs) {
      serverIP = prefs.getString('server_ip');
    });
    Future.delayed(const Duration(seconds: 5), connectNotifications);
  }

  void setRequestVideo(bool value) {
    _connectionMessage = value ? 'send-video' : 'connected';
  }

  Future<bool> connectNotifications() async {
    if (_connectionState == ConnectionState.waiting) {
      debugPrint('[Notifications] State is waiting. Returning');
      return false;
    }

    connectionState = ConnectionState.waiting;

    _socket?.destroy();

    // var prefs = await SharedPreferences.getInstance();
    // serverIP = prefs.getString('server_ip');

    print('[Notifications] Trying to connect to: $serverIP');
    if (serverIP == null) {
      debugPrint('serverIP is null');
      connectionState = ConnectionState.none;
      return false;
    }

    try {
      _socket = await Socket.connect(serverIP, 4445,
          timeout: const Duration(seconds: 5));
    } catch (e) {
      connectionState = ConnectionState.none;
      // print('[Notifications] Connection failed');
      // print('connection failed ${e.toString()}');
      return false;
    }

    if (_socket != null) {
      print('[Notifications] Connected');
      _timeSinceLastResponse.reset();
      connectionState = ConnectionState.done;
    } else {
      print('socket is null');
      connectionState = ConnectionState.none;
      return false;
    }

    _socket?.listen((Uint8List event) {
      String msg;
      // int eventLength = event.length;
      // print('event length: ${eventLength}');
      try {
        msg = utf8.decode(event);
      } catch (e) {
        print('Exception on decoding: $e');
        return;
      }
      // print('event length: ${event.length}');
      // String msg = event.sublist(0, 10).toString();
      print('[Triggers Connection] msg: $msg');

      if (msg.startsWith('connected?')) {
        // debugPrint('received connected');
        try {
          _socket!.write(_connectionMessage);
        } catch (e) {
          debugPrint('[Socket] Exception when sending');
        }
        _timeSinceLastResponse.reset();
        // } else if (msg.startsWith(PACKET_PREFIX_MSG)) {
        //   print('received packet');
        // imageReceiver.addPacket(event.sublist());
      } else if (msg.startsWith(ALARM_PREFIX_MSG)) {
        // ALARM RECEIVED
        print('[SOCKET] alarme recebido');
        _timeSinceLastResponse.reset();
        _handleAlarmReceived(event);
      } else if (msg.startsWith(NOTIFICATION_PREFIX_MSG)) {
        // NOTIFICATION RECEIVED
        _timeSinceLastResponse.reset();
        _handleNotificationReceived(event);
        print('[SOCKET] notificação recebida');
      }
    });

    return true;
  }

  void _handleNotificationReceived(event) {
    Map<String, dynamic>? info =
        _infoFromEvent(event, NOTIFICATION_PREFIX_MSG.length);
    if (info == null) {
      print('info is null');
      return;
    }
    triggersNotifications.notify(
        'Detecção Realizada', 'Local: ${info['local']}');
  }

  void _handleAlarmReceived(List<int> event) async {
    alarmReceived =
        onTriggerAlarmReceived(_infoFromEvent(event, ALARM_PREFIX_MSG.length));
    _checkIfAlarmWasReceived();
  }

  Map<String, dynamic>? _infoFromEvent(List<int> event, int jsonStartIndex) {
    // Reads message until it finds a '}', then stops and decode the json
    final int eventLength = event.length;
    final int bracketsCodeUnit = '}'.codeUnitAt(0);

    int i;
    for (i = jsonStartIndex; i < eventLength; i++) {
      if (event[i] == bracketsCodeUnit) {
        break;
      }
    }

    Map<String, dynamic>? info =
        jsonDecode(utf8.decode(event.sublist(jsonStartIndex, i + 1)));
    print('info: $info');
    // alarmReceived?['frame'] = await imageReceiver.frameStream.stream.last;
    // print('received alarm image');

    return info;
  }

  void _checkIfAlarmWasReceived() async {
    // Wait and check if message was received, if not, tell service to open the app
    await Future.delayed(const Duration(seconds: 1));
    if (alarmReceived != null) {
      print(
          '[Triggers Connection] alarmReceived is not null, calling ifAppIsClosed');
      ifAppIsClosed(alarmReceived);
    } else {
      print('[Triggers Connection] alarmReceived is null');
    }
  }
}
