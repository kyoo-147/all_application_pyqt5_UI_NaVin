import socket
import json
import time
import base64
import sys
import numpy
import cv2


def receiveAll(sock, count):
    """This function receives and returns all buffers transmitted from the server so far through the socket.

    The buffer is read through the socket, but the read size is limited.
    The size limit is limited by the value stored in the count variable.

    :param socket.socket sock: A Socket variable for communicating with the server.
    :param int count: A variable that stores a limit on the total read size

    :return buffer: returns all buffers transmitted from the server
    :return None: return None if There is no new Buffer

    :raises socket.timeout: In the process of reading the buffer through the socket, when the time limit is set in the socket and exceeds the time limit
    """

    # Create A buffer variable to save received buffer
    buf = b''

    # Looping if count >= 0
    while count:
        try:
            # receive new buffer
            newbuf = sock.recv(count)
        except socket.timeout:
            # if socket timeout
            return None

        # if there is no new buffer
        if not newbuf:
            return None

        # if there is a new buffer, Save and Reduce count variable by the size input.
        buf += newbuf
        count -= len(newbuf)
    return buf


class Connector:
    """A class for communicating with an object detection server. This class is responsible for
    connecting to the server, transmitting images to the server, and receiving and processing results from the server
    """

    def __init__(self, ip, port):
        """A function to initialize the Connector class

        Save the IP and PORT of the server you want to connect to and try to connect with the server.

        :param str ip: String type IP address. ex) 127.0.0.1
        :param int port: Int type PORT number ex)7777

        """
        self.isRun = True
        self.notReceived_Before = False
        self.TCP_SERVER_IP = ip
        self.TCP_SERVER_PORT = port
        self.connectCount = 0
        self.connectServer()

    def connectServer(self):
        """This function attempts to connect to the server.Create a socket to connect to the server,
        and try to connect to the server using the socket that you created. If the connection fails,
        try to reconnect a total of 10 times. If the connection fails 10 times in total, exit the program.
        """
        try:
            # Create a socket to connect to the server.
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Try to connect with the server.
            self.sock.connect((self.TCP_SERVER_IP, self.TCP_SERVER_PORT))
            print(
                u'Client socket is connected with Server socket [ TCP_SERVER_IP: ' + self.TCP_SERVER_IP
                + ', TCP_SERVER_PORT: ' + str(self.TCP_SERVER_PORT) + ' ]')
            self.connectCount = 0
        except Exception as e:
            # print an error message on the console window.
            print(e)

            # Increase the number of Trying to connect to the server.
            self.connectCount += 1
            # If the connection with the server fails 10 times, the program will be terminated.
            if self.connectCount == 10:
                print(u'Connect fail %d times. exit program' % self.connectCount)
                sys.exit()
            print(u'%d times try to connect with server' % self.connectCount)

            # Retry connecting to the server.
            self.connectServer()

    def processing(self, image):
        """This function uses a socket to transmit the image and the size of the image to the server,
        receives the result data and the size of the result data from the server,
        and returns the object detection result.

        :param ndarray image: 3D ND array containing photo data.
        :type ndarray: 3D NdArray form returned by OpenCV VideoCapture.read()

        .. Note:: image must not be None, image must be 3D ndarray Type

        :returns: multi dimension list type [people_position_list, custom_object_position_list]

        .. Note:: peaple_position_list is composed of 1D list ( [xmin, ymax, xmax, ymin] )
        .. Note:: custom_object_position_list is composed of 2D list [object-classNum-1, object-classNum-2, ...]
        .. Note:: object-class is 1D Array that composed of 1D list ( [xmin, ymax, xmax, ymin] )

        .. Note:: The structure of the return form is as follows.
        .. Note:: [ [[xmin, ymax, xmax, ymin], ...] , [   [[xmin, ymax, xmax, ymin], ..], [..], [..], [..], ...  ] ]

        .. Warning:: This function must be called after being connected to the server.

        """
        try:
            # Setting image encoding parameter
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

            # Encoding Image using cv2.imencode function
            _, img_encode = cv2.imencode('.jpg', image, encode_param)

            # Convert encoded image data into numpy array type
            data = numpy.array(img_encode)

            # Encoding data using base64.b64encode function to send string data to server
            stringData = base64.b64encode(data)

            # Get converted into string type data length
            length = str(len(stringData))

            # Send string data and its length to server
            self.sock.sendall(length.encode('utf-8').ljust(64))
            self.sock.send(stringData)

            # Receive object detection result's length from Server
            result_len = receiveAll(self.sock, 64)

            if result_len is None:
                return None

            result_len = result_len.decode('utf-8')

            # Receive object detection result from Server using result length
            result = receiveAll(self.sock, int(result_len))

            if len(result) == 0:
                return None

            # decode received object detection result
            result_decoded = result.decode('utf-8')

            # Parsing received object detection result using json.loads(str)
            result_list = json.loads(result_decoded)

            # return object detection result
            return result_list

        # If a problem occurs during the communication process,
        except Exception as e:
            # print Error Message on console window
            print(e)

            # If it is not terminated by the user ( = means self.isRun is True )
            if self.isRun is True:
                # Close socket to try to connect to Server again
                self.sock.close()

                # To end the socket safely, use time.sleep(1)
                time.sleep(1)

                # ReTry to connect to Server
                self.connectServer()

    def disconnect(self):
        """This function is to terminate the connection with the server."""

        # Turn off the flag
        self.isRun = False

        print('Closing Socket..')

        # Close Socket
        self.sock.close()
        # To end the socket safely, use time.sleep(1)
        time.sleep(1)

        print('Closed Socket')
