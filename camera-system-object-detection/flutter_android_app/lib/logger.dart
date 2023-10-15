import 'dart:async';
import 'dart:core';

import 'package:flutter/material.dart';

class Logger extends StatefulWidget {
  static TextEditingController logTextController = TextEditingController();
  static StreamController<String> _textStream = StreamController<String>();

  Logger({Key? key}) : super(key: key);
  // Stream<String> textStream = Stream<String>();

  static void log(String msg) {
    _textStream.add(' $msg');
  }

  @override
  State<Logger> createState() => _LoggerState();
}

class _LoggerState extends State<Logger> {
  String _text = '';
  // final ScrollController _controller = ScrollController();

  _LoggerState() {
    Logger._textStream.stream.listen(
      (event) {
        setState(() => _text += event);
      },
    );
    // Logger.log('');
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.all(8.0),
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border.all(color: Colors.black54, width: 4.0),
      ),
      child: ListView(
        // controller: _controller,
        padding: const EdgeInsets.all(8.0),
        shrinkWrap: true,
        children: [
          Text(_text),
        ],
      ),
    );
  }
}
