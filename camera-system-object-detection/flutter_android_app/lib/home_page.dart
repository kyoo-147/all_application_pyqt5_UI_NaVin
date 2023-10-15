import 'package:device_apps/device_apps.dart';
import 'package:flutter/material.dart';
import 'package:flutter_background_service/flutter_background_service.dart';
import 'package:flutter_android_app/image_connection.dart';
import 'package:flutter_windowmanager/flutter_windowmanager.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> with WidgetsBindingObserver {
  final imageConnection =
      ImageConnection(FlutterBackgroundService().on('onUpdateState'));
  bool _gridOn = false;
  AppLifecycleState? appLifecycleState;

  _HomePageState() {
    imageConnection.addListener(() => setState(() {
          // _frameCount++;
        }));
  }

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);

    Future.delayed(const Duration(seconds: 2),
        () => appLifecycleState = AppLifecycleState.resumed);

    FlutterBackgroundService()
        .on('alarmReceived')
        .listen((Map<String, dynamic>? triggerInfo) async {
      await FlutterWindowManager.addFlags(
          FlutterWindowManager.FLAG_SHOW_WHEN_LOCKED);
      await FlutterWindowManager.addFlags(
          FlutterWindowManager.FLAG_TURN_SCREEN_ON);

      if (appLifecycleState == AppLifecycleState.paused) {
        DeviceApps.openApp('dev.eduardonn.sursystem_android_app');
      }

      Navigator.pushNamed(context, '/alarm', arguments: triggerInfo);
    });

    FlutterBackgroundService().invoke("appOpened");
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    imageConnection.stop();
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    appLifecycleState = state;
    switch (state) {
      case AppLifecycleState.resumed:
        imageConnection.start();
        break;
      default:
        imageConnection.stop();
        break;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        actions: [
          RawMaterialButton(
            onPressed: () => Navigator.pushNamed(context, '/settings'),
            child: const Padding(
              padding: EdgeInsets.all(8.0),
              child: Icon(
                Icons.settings,
                size: 36,
              ),
            ),
          ),
        ],
        title: const Text('Camera Surveillance System'),
      ),
      backgroundColor: Colors.grey[400],
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Spacer(),
          if (_gridOn)
            OrientationBuilder(
              builder: (context, orientation) {
                if (orientation == Orientation.portrait) {
                  return Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      _imageWidget(),
                      _imageWidget(),
                    ],
                  );
                } else {
                  return Row(
                    children: [
                      _imageWidget(),
                      _imageWidget(),
                    ],
                  );
                }
              },
            )
          else
            _imageWidget(),
          const Spacer(),
          Align(
            alignment: Alignment.bottomCenter,
            child: Container(
              margin: const EdgeInsets.only(top: 12.0),
              padding: const EdgeInsets.all(5.0),
              child: Row(
                children: [
                  Row(
                    children: <Widget>[
                      const Text(
                        'Data packets discarded: ',
                        style: TextStyle(
                          fontSize: 12,
                          decoration: TextDecoration.none,
                          color: Colors.black,
                        ),
                      ),
                      StreamBuilder<int>(
                          stream: imageConnection.imageReceiver
                              .timesFrameNotFoundStreamController.stream,
                          builder: (context, snapshot) {
                            return Text(
                              '${snapshot.data}',
                              style: const TextStyle(
                                fontSize: 12,
                                decoration: TextDecoration.none,
                                color: Colors.black,
                              ),
                            );
                          }),
                    ],
                  ),
                  const Spacer(),
                  StreamBuilder<Map<String, dynamic>?>(
                    stream: FlutterBackgroundService().on('onUpdateState'),
                    builder: (context, snapshot) {
                      if (!snapshot.hasData) {
                        return stateText('Disconnected', Colors.red);
                      }

                      final data = snapshot.data!;

                      switch (ConnectionState.values[data['state']]) {
                        case ConnectionState.done:
                          return stateText('Connected', Colors.green);
                        case ConnectionState.waiting:
                          return stateText('Trying to Connect', Colors.blue);
                        default:
                          return stateText('Disconnected', Colors.red);
                      }
                    },
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Text stateText(String text, Color color) {
    return Text(
      text,
      style: TextStyle(
        color: color,
      ),
    );
  }

  Widget _imageWidget() {
    return GestureDetector(
      onTap: () => setState(() => _gridOn = !_gridOn),
      child: imageConnection.frame ??
          AspectRatio(
            aspectRatio: 16 / 9,
            child: Container(
              color: Colors.black,
              margin: const EdgeInsets.all(2.0),
              child: const Center(
                child: Text(
                  'No Signal',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 32.0,
                  ),
                ),
              ),
            ),
          ),
    );
  }
}
