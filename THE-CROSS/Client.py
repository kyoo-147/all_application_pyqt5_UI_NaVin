import argparse


def startClient():
    """Before starting the client program, This function informs the server information entered by the user
    and informs the precautions.

    To run Client.py, enter IP and PORT information of server in the console window
    to allow the Client program to connect to the server.

    .. note:: The IP and PORT entered in the Client must be the same as the IP and PORT of the Server.
    .. note:: The default IP of the Client is localhost.
    .. note:: The default PORT of the Client is 7777.

    .. Warning:: DONT CLOSE & USE THE PROGRAM UNTIL SUCCESSFULLY CAMERA CONNECTED

        Example:
            Run Client.py on the console in the following format:
            >> python Client.py --ip=XX.XX.XX.XX --port=XXX
    """

    parser = argparse.ArgumentParser(description='THE-CROSS Client arg parser')
    parser.add_argument('--ip', type=str, help='Input Detection Server IP\n ex) 127.0.0.1',
                        default='localhost', required=False)
    parser.add_argument('--port', type=int, help='Input Detection Server Port\n ex) 7777',
                        default=7777, required=False)

    args = parser.parse_args()

    IP = args.ip
    PORT = args.port

    print('\n\n ==================== [ THE CROSS CLIENT ] ====================\n'
          '            - Initializing THE-CROSS CLIENT PROGRAM\n',
          '           - Detector Server IP : ', IP, "\n",
          '           - Detector Server PORT : ', PORT, '\n',
          '==============================================================\n\n',
          '========================= [!CAUTION!] ========================\n',
          '>>> DONT CLOSE PROGRAM UNTIL SUCCESSFULLY CAMERA CONNECTED <<<\n',
          '==============================================================\n\n')

    import main
    main.start(IP, PORT)


if __name__ == "__main__":
    startClient()
