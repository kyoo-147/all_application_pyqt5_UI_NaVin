import 'package:flutter/material.dart';
import 'package:flutter_android_app/image_connection.dart';
import 'package:flutter_background_service/flutter_background_service.dart';

class ConnectedImage extends StatefulWidget {
  const ConnectedImage({Key? key}) : super(key: key);

  State<ConnectedImage> createState() => _ConnectedImageState();
}

class _ConnectedImageState extends State<ConnectedImage> {
  final _imageConnection =
      ImageConnection(FlutterBackgroundService().on('onUpdateState'));
  ImageConnection get serverConnection => _imageConnection;
  int cameraSelected = 0;
  bool _gridOn = true;

  _ConnectedImageState() {
    _imageConnection.addListener(() => setState(() {
          // _frameCount++;
        }));
  }

  @override
  Widget build(BuildContext build) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        _getImage(0),
        if (_gridOn) _getImage(1),
      ],
    );
  }

  Widget _getImage(int index) {
    return GestureDetector(
      onDoubleTap: () => setState(() => _gridOn = !_gridOn),
      child: _imageConnection.frame ??
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
