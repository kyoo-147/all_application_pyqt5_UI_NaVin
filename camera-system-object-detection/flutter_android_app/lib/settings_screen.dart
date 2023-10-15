import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_background_service/flutter_background_service.dart';

class SettingsData {
  bool? receiveNotifications;
  bool? receiveAlarms;
  String? serverIP;

  bool? get _receiveAlarms => receiveAlarms;
  bool? get _receiveNotifications => receiveNotifications;
  String? get _serverIP => serverIP;

  SettingsData(this.receiveNotifications, this.receiveAlarms, this.serverIP);
}

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  final textController = TextEditingController();
  bool? _receiveNotifications;
  bool? _receiveAlarms;

  _SettingsScreenState() {
    Future<SettingsData?> settings = getStoredSettings();
    settings.then((settings) => setState(() {
          _receiveNotifications = settings?._receiveNotifications ?? true;
          _receiveAlarms = settings?._receiveAlarms ?? true;
          textController.text = settings?._serverIP ?? '192.168.0.';
        }));
  }

  void saveSettings() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('server_ip', textController.text);
    await prefs.setBool('receive_notifications', _receiveNotifications ?? true);
    await prefs.setBool('receive_alarms', _receiveAlarms ?? true);

    bool isServiceRunning = await FlutterBackgroundService().isRunning();
    while (!isServiceRunning) {
      await Future.delayed(const Duration(seconds: 3));
      isServiceRunning = await FlutterBackgroundService().isRunning();
    }

    FlutterBackgroundService()
        .invoke("serverIPUpdate", {'serverIP': textController.text});
  }

  Future<SettingsData?> getStoredSettings() async {
    final prefs = await SharedPreferences.getInstance();
    SettingsData settings = SettingsData(
      prefs.getBool('receive_notifications'),
      prefs.getBool('receive_alarms'),
      prefs.getString('server_ip'),
    );
    return settings;
  }

  // @override
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Settings'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Row(
              children: [
                const Text('Receive Notifications'),
                Checkbox(
                  value: _receiveNotifications ?? false,
                  onChanged: (value) =>
                      setState(() => _receiveNotifications = value),
                ),
              ],
            ),
            Row(
              children: [
                const Text('Receive Alarms'),
                Checkbox(
                  value: _receiveAlarms ?? false,
                  onChanged: (value) => setState(() => _receiveAlarms = value),
                ),
              ],
            ),
            Row(
              children: <Widget>[
                const Flexible(
                  child: Text('Server IP Address:'),
                ),
                Flexible(
                  child: TextField(
                    autocorrect: false,
                    controller: textController,
                    decoration:
                        const InputDecoration(hintText: 'Server IP Address'),
                    textAlign: TextAlign.center,
                  ),
                ),
              ],
            ),
            Flexible(
              child: Container(
                width: 200,
                height: 35,
                margin: const EdgeInsets.only(top: 40.0),
                child: ElevatedButton(
                  onPressed: () {
                    saveSettings();
                    Navigator.pop(context);
                  },
                  child: const Text('Save', style: TextStyle(fontSize: 15)),
                ),
              ),
            ),
            const Spacer(),
          ],
        ),
      ),
    );
  }
}
