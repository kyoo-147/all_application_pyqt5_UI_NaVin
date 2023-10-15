import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:wakelock/wakelock.dart';
import 'package:flutter_background_service/flutter_background_service.dart';
import 'package:vibration/vibration.dart';

class AlarmPage extends StatefulWidget {
  const AlarmPage({Key? key}) : super(key: key);

  @override
  State<AlarmPage> createState() => _AlarmPage();
}

class _AlarmPage extends State<AlarmPage> {
  final int TIME_ALARM_ON = 10;
  final List<int> VIBRATION_PATTERN = [1000, 2000];
  String _alarmName = 'Alarm Name';
  Uint8List? _frame;

  @override
  void initState() {
    super.initState();
    Wakelock.enable();
    FlutterBackgroundService().invoke('alarmConsumed');
    Future.delayed(Duration(seconds: TIME_ALARM_ON), () {
      Wakelock.disable();
      // SystemNavigator.pop();
      Vibration.cancel();
    });

    startVibration();
  }

  void startVibration() async {
    if (await Vibration.hasVibrator() == true) {
      Vibration.vibrate(
        duration: TIME_ALARM_ON,
        pattern: VIBRATION_PATTERN,
        repeat: 1,
        amplitude: 40,
      );
    }
  }

  void loadTriggerInfo() {
    final args =
        ModalRoute.of(context)!.settings.arguments as Map<String, dynamic>;
    _alarmName = args['local'];
    // _frame = args['frame'];
  }

  @override
  Widget build(BuildContext context) {
    loadTriggerInfo();

    return Container(
      decoration: const BoxDecoration(
        gradient: LinearGradient(
            begin: Alignment.bottomLeft,
            end: Alignment.topRight,
            colors: [
              Colors.blue,
              Colors.cyan,
            ]),
      ),
      child: SafeArea(
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Container(
                    margin: const EdgeInsets.symmetric(vertical: 12.0),
                    child: const Text(
                      'Trigger Fired',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        color: Colors.white,
                        decoration: TextDecoration.none,
                        fontSize: 24,
                      ),
                    ),
                  ),
                  Text(
                    _alarmName,
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                      color: Colors.white,
                      decoration: TextDecoration.none,
                      fontSize: 36,
                    ),
                  ),
                ],
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  alarmButton(
                    backgroundColor: Colors.green,
                    onPressed: () {
                      Vibration.cancel();
                      Navigator.pop(context);
                    },
                    text: 'Check',
                  ),
                  alarmButton(
                    backgroundColor: Colors.red,
                    onPressed: () => SystemNavigator.pop(),
                    text: 'Ignore',
                  ),
                ],
              )
            ],
          ),
        ),
      ),
    );
  }

  Widget alarmButton(
      {required backgroundColor, required onPressed, required text}) {
    return Container(
      margin: const EdgeInsets.only(top: 46.0),
      child: ElevatedButton(
        style: TextButton.styleFrom(
          backgroundColor: backgroundColor,
          shape: const RoundedRectangleBorder(
            borderRadius: BorderRadius.all(
              Radius.circular(36.0),
            ),
          ),
        ),
        onPressed: onPressed,
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 20.0, horizontal: 8.0),
          child: Text(
            text,
            style: const TextStyle(color: Colors.white, fontSize: 20.0),
          ),
        ),
      ),
    );
  }
}
