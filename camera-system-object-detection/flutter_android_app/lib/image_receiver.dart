import 'dart:async';
import 'dart:typed_data';
import 'package:flutter/cupertino.dart';

class ImageReceiver {
  late Uint8List _frameReceived;
  int _indexFillingFrame = 0;
  int _imageSize = 0;
  int _timesFrameNotFound = 0;
  bool _hasFirstFrame = false;
  int _eventLength = 0;

  final timesFrameNotFoundStreamController = StreamController<int>();
  final frameStream = StreamController<Uint8List>();

  ImageReceiver() {
    timesFrameNotFoundStreamController.add(0);
  }

  void addPacket(Uint8List event) {
    _eventLength = event.length;

    int startIndexToSearchFirstFrame = 0;
    if (_hasFirstFrame) {
      int bytesLeftToFillImage = _imageSize - _indexFillingFrame;
      if (_eventLength < bytesLeftToFillImage) {
        _frameReceived.setAll(_indexFillingFrame, event);
        _indexFillingFrame += _eventLength;
      } else {
        try {
          _frameReceived.setAll(
              _indexFillingFrame, event.getRange(0, bytesLeftToFillImage));
        } catch (e) {
          debugPrint(e.toString());
          return;
        }

        frameStream.add(_frameReceived);
        _hasFirstFrame = false;
        _indexFillingFrame = 0;

        if (_eventLength > bytesLeftToFillImage) {
          handleFirstImagePacket(event, bytesLeftToFillImage);
        }
      }
    } else {
      handleFirstImagePacket(event, startIndexToSearchFirstFrame);
    }
  }

  bool handleFirstImagePacket(Uint8List event, startIndex) {
    int imageStartIndex = searchFirstPacket(event, startIndex);
    if (imageStartIndex != -1) {
      int imageInEventLength = _eventLength - imageStartIndex;

      if (imageInEventLength >= _imageSize) {
        try {
          _frameReceived.setAll(_indexFillingFrame,
              event.getRange(imageStartIndex, imageStartIndex + _imageSize));
        } catch (e) {
          debugPrint(e.toString());
          return false;
        }
        // displayImage();
        frameStream.add(_frameReceived);
        _hasFirstFrame = false;
        _indexFillingFrame = 0;

        bool hasData = imageInEventLength != _imageSize;

        return hasData;
      } else {
        try {
          _frameReceived.setAll(_indexFillingFrame,
              event.getRange(imageStartIndex, _eventLength));
        } catch (e) {
          debugPrint(e.toString());
          return false;
        }
        _indexFillingFrame += _eventLength - imageStartIndex;
        return false;
      }
    } else {
      return false;
    }
  }

  int searchFirstPacket(Uint8List msg, int startIndex) {
    // If the first four elements are '-' (ASCII 45), it's the first frame
    int streak = 0;

    int bytesVerified = 0;
    for (int i = startIndex; i < _eventLength; i++) {
      bytesVerified++;
      if (msg[i] == 45) {
        if (++streak == 4) {
          _hasFirstFrame = true;
          _imageSize = msg.sublist(i + 1, i + 5).buffer.asInt32List()[0];
          _frameReceived = Uint8List(_imageSize);
          return i + 5; // Start index of image data
        }
      } else {
        streak = 0;
      }
    }
    _hasFirstFrame = false;
    timesFrameNotFoundStreamController.add(++_timesFrameNotFound);

    return -1;
  }
}
