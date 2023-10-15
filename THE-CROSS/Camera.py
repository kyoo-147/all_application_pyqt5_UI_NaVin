import numpy as np
import cv2
import DetectorConnector

from PyQt5.QtCore import QThread, pyqtSignal
from ImageUtils import draw_area

IMAGE_PATH = "Images/"
'''IMAGE_PATH : The folder location where the image to be transmitted to the camera is stored.'''
DETECTOR_SERVER_IP = 'localhost'
'''DETECTOR_SERVER_IP : IP Address to connect to DETECTOR SERVER.'''
DETECTOR_SERVER_PORT = 7777
'''DETECTOR_SERVER_PORT : Port Number to connect to DETECTOR SERVER'''


class VideoThread(QThread):
    """It is a class that receives an image of a real-time camera,
    transmits the image to DETECTOR SERVER, and receives and returns results from DETECTOR SERVER.
    """

    change_pixmap_signal = pyqtSignal(np.ndarray, np.ndarray, list, list, list, list)
    '''change_pixmap_signal : pyqtSignal variable for 
    asynchronously calling the processing method of the main function.'''

    def __init__(self, left_camera_num, right_camera_num):
        """A function to initialize the VideoThread class

        Save the number of the camera to receive the real-time image,
        and create classes to connect and communicate with the Object Detection server.

        :param int left_camera_num: the left camera number used in OpenCV VideoCapture Method.
        :param int right_camera_num: the right camera number used in OpenCV VideoCapture Method.

        .. note:: left_camera_num & right_camera_num must be equal to or greater than -1.
        """

        super().__init__()
        self._run_flag = True

        # Save Camera Numbers used in OpenCV VideoCapture Method
        self.left_camera_num = left_camera_num
        self.right_camera_num = right_camera_num

        # Create Instance that connect to Server and communicate with server
        self.conn = DetectorConnector.Connector(DETECTOR_SERVER_IP, DETECTOR_SERVER_PORT)

    def setCameraNumber(self, left_num, right_num):
        """Setter Method that changes the camera number.

        :param int left_num: the left camera number used in OpenCV VideoCapture Method.
        :param int right_num: the right camera number used in OpenCV VideoCapture Method.

        .. note:: left_num & right_num must be equal to or greater than -1.
        """

        self.left_camera_num = left_num
        self.right_camera_num = right_num

    def isRun(self):
        """This Method Returns whether the VideoThread class is working."""
        return self._run_flag

    def run(self):
        """This function reads the image from the camera, sends the image to the server,
        receives the object detection result from the server,
        and returns the result to the function connected to the pyqtSignal.

        Until self._run_flag = TRUE, This method will be looping

        """

        # capture from web cam
        cam_left = cv2.VideoCapture(self.left_camera_num)
        cam_right = cv2.VideoCapture(self.right_camera_num)

        # Turn on the flag for looping
        self._run_flag = True

        # Looping
        while self._run_flag:

            # read real-time image from the two cameras
            ret_left, cv_img_left = cam_left.read()
            ret_right, cv_img_right = cam_right.read()

            # create variables to save the object detection result received from server
            pos_left = []
            pos_right = []
            custom_pos_left = [[], [], [], []]
            custom_pos_right = [[], [], [], []]

            if ret_left is False:
                # if the left camera can not be approached
                img_result_left = np.array([])
            else:
                # save real-time image from the left camera
                img_result_left = cv_img_left
                # send the image to server and receive the object detection result
                result = self.conn.processing(cv_img_left)
                print(result)
                if result is not None:
                    pos_left = result[0]
                    custom_pos_left = result[1]

            if ret_right is False:
                # if the right camera can not be approached
                img_result_right = np.array([])
            else:
                # save real-time image from the right camera
                img_result_right = cv_img_right
                # send the image to server and receive the object detection result
                result = self.conn.processing(cv_img_right)
                if result is not None:
                    pos_right = result[0]
                    custom_pos_right = result[1]

            # Emit Object Detection Result List To the method that connected to pyqt5signal (=Main Processing Method)
            self.change_pixmap_signal.emit(img_result_left, img_result_right,
                                           pos_left, pos_right, custom_pos_left, custom_pos_right)

        # shut down capture system
        cam_left.release()
        cam_right.release()

    def stop(self):
        """This Method stops looping by turn off the run flag"""
        self._run_flag = False

    def close(self):
        """This Method stops looping, disconnect to server and exit thread of VideoThread Instance"""
        self.stop()
        self.conn.disconnect()
        self.exit()


class CameraSetup:
    """It is a class to receive real-time images of the camera
    and set the area through clicking on the image screen.
    """

    def __init__(self, camera_num):
        """A function to initialize the CameraSetup class

        :param int camera_num: the specific camera number used in OpenCV VideoCapture Method.

        .. note:: camera_num must be equal to or greater than -1.
        """

        super().__init__()
        # Save the coordinates clicked on the camera's real-time image screen.
        self.touch_list = []
        # Set OpenCV Window Name
        self.windowName = 'Camera Setup :: Save & Exit Button is KEY Q'
        # Flag that determines whether it works or not.
        self.isRun = True

        # Save received camera number
        self.Camera_Number = camera_num

        # Set Initial Camera Output Image
        self.CAMERA_NO_SIGNAL_IMG = cv2.imread(IMAGE_PATH + "camera_no_signal.png")

    def addXY_inList(self, x, y):
        """It is a function that stores coordinates input through screen clicks.

        :param int x: The x-coordinate entered through the screen click.
        :param int y: The y-coordinate entered through the screen click.

        .. note:: the x, y must be equal to or greater than zero.
        .. note:: the x, y must be equal to or less than the maximum size of the screen.

        .. warning:: If the number of already stored coordinates is more than 4, the already stored coordinates are removed except for the currently received coordinates.

        """
        if len(self.touch_list) >= 4:
            self.clear_List()
        self.touch_list.append([x, y])

    def clear_List(self):
        """It is a function that removes all coordinate values stored in the list (self.touch_list)"""
        self.touch_list = []

    def click_event(self, event, x, y, flags, param):
        """This function is called when a screen click event occurs.
        This function is called when a screen click event occurs,
        and receives the coordinates clicked on the screen and stores the coordinates in the list (self.touch_list).

        :param opencv_event event: Types of events that occurred.
        :type opencv_event: The event type defined in OpenCV.

        :param int x: The x-coordinate entered through the screen click.
        :param int y: The y-coordinate entered through the screen click.

        :param flags: It is a parameter to comply with the form defined in OpenCV.
        :param param: It is a parameter to comply with the form defined in OpenCV.

        .. warning:: The function should not be called except for calls by click events.

        """

        # if the event type is Left Button Down, save the coordinate
        if event == cv2.EVENT_LBUTTONDOWN:
            print('x : ', x, ' y : ', y)
            self.addXY_inList(x, y)

    def runSetup(self):
        """This function creates a window window for camera setting
        and delivers the coordinates clicked on the screen to function click_event.

        :return: A list of 4 or less coordinates stored.
        """

        # Set Camera Setup Window Name
        cv2.namedWindow(self.windowName)

        # Register Event
        cv2.setMouseCallback(self.windowName, self.click_event)

        # Set VideoCapture Instance to Receive Real-time Image
        cap = cv2.VideoCapture(self.Camera_Number)

        # Looping
        while self.isRun:
            # Read Image through OpenCV VideoCapture.read()
            ret, frame = cap.read()

            # if the camera can not be approached, show NO_SIGNAL_IMAGE on Window
            if ret is False:
                frame = self.CAMERA_NO_SIGNAL_IMG
            else:
                # If the camera works well, draw the coordinates that have already been clicked on
                # the real-time image together
                frame = draw_area(frame, self.touch_list)

            # Show the processed picture to the user.
            cv2.imshow(self.windowName, frame)

            # Detects the user's keyboard input at 0.001 second intervals.
            key = cv2.waitKey(1)

            # If the user presses the Q key, return and terminate the coordinates stored so far.
            if key & 0xFF == ord('q') or key & 0xFF == ord('Q'):
                self.isRun = False
                cv2.destroyWindow(self.windowName)
                cap.release()
                cv2.waitKey(10)
                return self.touch_list
