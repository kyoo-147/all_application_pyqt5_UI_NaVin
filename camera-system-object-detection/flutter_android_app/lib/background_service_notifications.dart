import 'dart:async';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:flutter_background_service/flutter_background_service.dart';
import 'package:device_apps/device_apps.dart';
import 'package:flutter_android_app/triggers_connection.dart';

Future<void> initializeService([bool forceInitialize = false]) async {
  final service = FlutterBackgroundService();
  // if (await service.isRunning() && !forceInitialize) {
  //   debugPrint('Service already in execution. Returning...');
  //   return;
  // }
  await service.configure(
    androidConfiguration: AndroidConfiguration(
      onStart: onStart,
      autoStart: true,
      isForegroundMode: false,
    ),
    iosConfiguration: IosConfiguration(
      autoStart: true,
      onForeground: onStart,
      onBackground: onIosBackground,
    ),
  );
  service.startService();
}

bool onIosBackground(ServiceInstance service) {
  WidgetsFlutterBinding.ensureInitialized();

  return true;
}

@pragma('vm:entry-point')
void onStart(ServiceInstance service) async {
  DartPluginRegistrant.ensureInitialized();

  final triggersConnection = TriggersConnection(
    onUpdateState: (ConnectionState value) {
      try {
        service.invoke(
          'onUpdateState',
          {
            "state": value.index,
          },
        );
      } catch (e) {
        debugPrint(e.toString());
      }
    },
    onTriggerAlarmReceived: (Map<String, dynamic> alarmInfo) async {
      service.invoke('alarmReceived', alarmInfo);
    },
    ifAppIsClosed: (Map<String, dynamic> alarmInfo) {
      DeviceApps.openApp('dev.eduardonn.sursystem_android_app');
    },
  );

  service.on('stopService').listen((event) {
    service.stopSelf();
  });

  service.on('serverIPUpdate').listen((event) {
    triggersConnection.serverIP = event?['serverIP'];
  });

  service.on('alarmConsumed').listen((event) {
    triggersConnection.alarmReceived = null;
  });

  service.on('stopRequestingVideo').listen((event) {
    triggersConnection.setRequestVideo(false);
  });

  service.on('requestVideo').listen((event) {
    triggersConnection.setRequestVideo(true);
  });

  service.on('appOpened').listen((event) {
    // If app was closed when it received an alarm, it will open
    triggersConnection.setRequestVideo(true);

    service.invoke(
      'onUpdateState',
      {
        "state": triggersConnection.connectionState.index,
      },
    );

    if (triggersConnection.alarmReceived == null) {
      return;
    }
    service.invoke('alarmReceived', triggersConnection.alarmReceived);
    triggersConnection.alarmReceived = null;
  });
}
