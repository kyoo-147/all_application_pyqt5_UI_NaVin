# object-detection
[![License:MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/nalindas9/object-detection/blob/master/LICENSE)

## About
Using MobileNet SSD model to run inference and detect objects in the scene. Using PyQT5 for FrontEnd GUI.

## Output

### Without GUI
https://user-images.githubusercontent.com/44141068/154607601-e4b968fe-e034-4513-92e0-e4ab2f0bc3c0.mp4

### With GUI
https://user-images.githubusercontent.com/44141068/154788541-899940ae-7207-496e-a886-74ffd1d95f9b.mp4

## System and library requirements

- Ubuntu==18.04.5 LTS
- Python==3.6.9
- numpy==1.19.5
- opencv_python==4.1.2.30
- pillow
- PyQt5==5.15.6
- PyYAML==6.0

## How to Run
1. Clone this repo. <br>
2. Navigate into the folder `object-detection` <br>
3. Create and activate [Virtual Environment](https://docs.python.org/3/library/venv.html) <br>
4. Upgrade pip using `python -m pip install --upgrade pip`.
5. Install requirements.txt using command `pip install -r requirements.txt`.
6. To run the code, from the terminal, run the command `python3 main.py` <br>
7. You should see a window pop up. Click on open webcam to start detecting.
7. To stop detecting, simply click on stop webcam. To shutdown, click on cross topright corner.:)


