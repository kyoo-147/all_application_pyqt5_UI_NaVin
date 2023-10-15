import socket
import numpy
import base64
import cv2
import json

import ImageDetector


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

        # receive new buffer
        newbuf = sock.recv(count)

        # if there is no new buffer
        if not newbuf:
            return None

        # if there is a new buffer, Save and Reduce count variable by the size input.
        buf += newbuf
        count -= len(newbuf)
    return buf


class DetectorServer:
    """This class is for opening a server, waiting for client access, and receiving image data from the client,
    detecting an object from that image data, and sending the object detection result to the client
    when the client successfully accesses the server.
    """

    def __init__(self, ip, port):
        """A function to initialize the DetectorServer class

        To open the server, save the server's IP address and PORT address and
        open the server socket to wait for the client to access.
        When the client accesses, it waits for the image to be transmitted from the client.

        :param str ip: The IP address of the server.
        :param int port: The PORT number of the server.
        """

        self.TCP_IP = ip
        self.TCP_PORT = port
        self.socketOpen()
        self.receiveImages()

    def socketClose(self):
        """This function closes the socket of the server."""
        self.sock.close()
        time.sleep(1)
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is close')

    def socketOpen(self):
        """This function opens the socket of the server and waits for the client to access.
        If the client has successfully accessed the server, store the socket of the connected client.
        """

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.TCP_IP, self.TCP_PORT))
        self.sock.listen(1)
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is open')
        self.conn, self.addr = self.sock.accept()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(
            self.TCP_PORT) + ' ] is connected with client')

    def receiveImages(self):
        """This function waits for image data transmitted from the client. If the image data arrives successfully,
        object-detection is performed from the image data and the object detection result is sent to the client.
        """

        try:
            # Looping for receiving data from client and send object detect result (from received data ) to server
            while True:

                # Save the size of the data to be received from the client.
                length = receiveAll(self.conn, 64)

                if length is None:
                    continue

                # Decode information about the size of the data to be received from the client.
                length_decoded = length.decode('utf-8')

                # Image data is received and stored based on information on-
                # -the size of the data to be received from the client.
                stringData = receiveAll(self.conn, int(length_decoded))

                # decode image data using base64.b64decode function
                data = numpy.frombuffer(base64.b64decode(stringData), numpy.uint8)

                # convert decoded image data to 3D numpy array type
                img = cv2.imdecode(data, 1)

                # Save object detection result using processing function
                result = self.processing(img)

                # Send the object detection result to client
                self.sendResult(result)

        # If a problem occurs during the communication process,
        except Exception as e:
            # print error message on console window
            print(e)

            # Close Server Socket to retry to connect to client
            self.socketClose()

            # Re-Open Server Socket
            self.socketOpen()

            # Re-Receive Image from client
            self.receiveImages()

    def processing(self, data):
        """This function is a function that attempts to detect an object from the input image data,
        stores and returns the result.

        :param 3D-ndarray data: 3D ndarray type data, which has image data.

        :returns: multi dimension list type [pos_result, custom_result]

        .. Note:: pos_result is composed of 1D list ( [xmin, ymax, xmax, ymin] )
        .. Note:: custom_result is composed of 2D list [object-classNum-1, object-classNum-2, ...]
        .. Note:: object-class is 1D list that composed of 1D list ( [xmin, ymax, xmax, ymin] )

        .. Note:: The structure of the return form is as follows.
        .. Note:: [ [[xmin, ymax, xmax, ymin], ...] , [   [[xmin, ymax, xmax, ymin], ..], [..], [..], [..], ...  ] ]

        .. Warning:: This function must be called after being connected to the client.
        """
        pos_result = ImageDetector.Detector(data)
        custom_result = ImageDetector.CustomDetector(data)
        return [pos_result, custom_result]

    def sendResult(self, result):
        """This function sends data to the client.

        :param result: object you want to send to the client.

        """

        print('result-->', result)

        result_encoded_json = json.dumps(result).encode('utf-8')
        length = str(len(result_encoded_json))

        self.conn.sendall(length.encode('utf-8').ljust(64))
        self.conn.send(result_encoded_json)
