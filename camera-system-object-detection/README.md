# Camera Surveillance System With Person Detection

This project's main goal is to detect suspicious presences in surveillance camera's footage using person detection to prevent home invasions.

The system for Windows allow users to create triggers that are fired when certain conditions are met, such as a person being detected in an area drawn by the user, time of the day, and the maximum amount of time the detection spends inside the area. When it fires, it sends a notification or sound an alarm on the user's phone through an Android app.

The Android app is used to receive the notifications sent by the Windows app and visualize the cameras' footage in real time through local network.

## Screenshots

### Windows
#### Home
<img src="screenshots/Interface_Home.jpg">

#### Triggers Manager
<img src="screenshots/Interface_Triggers_Manager.jpg">

#### Add Triggers
<img src="screenshots/Interface_Add_Trigger.jpg">

### Android
<img src="screenshots/Interfaces_Android.jpg">

## Technologies Applied

| Name                        | Purpose                   |
| --------------------------- | ------------------------- |
| [**PyQt5**](https://www.riverbankcomputing.com/software/pyqt/) | Interface for Windows |
| [**OpenCV**](https://opencv.org/) | Image manipulation and AI processing |
| [**Flutter**](https://flutter.dev/) | Interface for Android |
| [**SSD**](https://arxiv.org/abs/1512.02325) | AI model for object detection |