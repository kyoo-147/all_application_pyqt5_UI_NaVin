import argparse


def startServer():
    """This function starts the Detection Server to receive an image from the Client
    and send the detection result of the Object Detection to the Client.

    To run Server.py, enter IP and PORT information of server in the console window
    to Open Object Detection Server

    .. note:: The default IP of the Server is localhost.
    .. note:: The default PORT of the Server is 7777.
    .. note:: DO NOT CLOSE PROGRAM UNTIL Socket Opened Message printed

        Example:
            Run Server.py on the console in the following format:
            >> python Server.py --ip=XX.XX.XX.XX --port=XXX
    """
    parser = argparse.ArgumentParser(description='THE-CROSS DetectorServer arg parser')
    parser.add_argument('--ip', type=str, help='Input Detection Server IP\n ex) 127.0.0.1',
                        default='localhost', required=False)
    parser.add_argument('--port', type=int, help='Input Detection Server Port\n ex) 7777',
                        default=7777, required=False)

    args = parser.parse_args()

    IP = args.ip
    PORT = args.port

    print('\n\n ==============================================\n'
          ' Initializing THE-CROSS DETECTOR SERVER PROGRAM\n',
          'Detector Server IP : ', IP, "\n",
          'Detector Server PORT : ', PORT, '\n',
          '==============================================\n\n',
          '*** It takes a long time, so please wait. ***\n\n')

    from DetectorServer import DetectorServer
    server = DetectorServer(IP, PORT)


if __name__ == "__main__":
    startServer()
