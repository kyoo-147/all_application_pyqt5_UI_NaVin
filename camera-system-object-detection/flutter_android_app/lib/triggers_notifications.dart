import 'package:flutter/material.dart';
import 'package:device_apps/device_apps.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:url_launcher/url_launcher.dart';

class TriggersNotifications {
  FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin =
      FlutterLocalNotificationsPlugin();
  final AndroidInitializationSettings initializationSettingsAndroid =
      AndroidInitializationSettings('@mipmap/ic_launcher');
  final AndroidNotificationDetails androidPlatformChannelSpecifics =
      AndroidNotificationDetails(
    'your channel id',
    'your channel name',
    channelDescription: 'your channel description',
    importance: Importance.max,
    priority: Priority.high,
    ticker: 'ticker',
    // fullScreenIntent: true,
    // visibility: NotificationVisibility.public,
  );
  int _notificationsID = 0;
  NotificationDetails? platformChannelSpecifics;

  TriggersNotifications() {
    final InitializationSettings initializationSettings =
        InitializationSettings(android: initializationSettingsAndroid);
    flutterLocalNotificationsPlugin.initialize(initializationSettings,
        onSelectNotification: selectNotification);

    platformChannelSpecifics =
        NotificationDetails(android: androidPlatformChannelSpecifics);
  }

  void notify(String title, String body) async {
    await flutterLocalNotificationsPlugin.show(
        _notificationsID++, title, body, platformChannelSpecifics,
        payload: 'item x');
  }

  void selectNotification(String? payload) async {
    debugPrint('notification selected\npayload: $payload');
    try {
      // final url = Uri.parse('com.mobilesursystem.open/alarm');
      // if (!await launchUrl(url)) {
      //   throw 'Could not launch $url';
      // }
      print(
          '[Notification Click] openApp result: ${await DeviceApps.openApp('dev.eduardonn.sursystem_android_app')}');
    } catch (e) {
      print(e);
    }
  }
}
