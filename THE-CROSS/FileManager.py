import json
import os

PATH = "config.json"

# ===== SETTING INITIAL CONFIG VALUES =====#

INCREASE_TIME_DEFAULT = 5
INCREASE_TIME_SPECIAL = 8

LEFT_CAMERA_NUMBER = 0
RIGHT_CAMERA_NUMBER = -1

CROSSWALK_TIME = 10
CARLANE_TIME = 100
CHANGE_TERM = 5

LEFT_CAMERA_CROSSWALK_POS = [[0, 0], [0, 0], [0, 0], [0, 0]]
RIGHT_CAMERA_CROSSWALK_POS = [[0, 0], [0, 0], [0, 0], [0, 0]]
LEFT_CAMERA_CARLANE_POS = [[0, 0], [0, 0], [0, 0], [0, 0]]
RIGHT_CAMERA_CARLANE_POS = [[0, 0], [0, 0], [0, 0], [0, 0]]

optionList = ['INCREASE_TIME_NORMAL', 'INCREASE_TIME_SPECIAL',
              'CROSSWALK_TIME', 'CARLANE_TIME', 'CHANGE_TERM',
              'LEFT_CAMERA_NUMBER', 'RIGHT_CAMERA_NUMBER', 'LEFT_CAMERA_CROSSWALK_POS',
              'RIGHT_CAMERA_CROSSWALK_POS', 'LEFT_CAMERA_CARLANE_POS', 'RIGHT_CAMERA_CARLANE_POS']
optionValues = [INCREASE_TIME_DEFAULT, INCREASE_TIME_SPECIAL,
                CROSSWALK_TIME, CARLANE_TIME, CHANGE_TERM,
                LEFT_CAMERA_NUMBER, RIGHT_CAMERA_NUMBER, LEFT_CAMERA_CROSSWALK_POS,
                RIGHT_CAMERA_CROSSWALK_POS, LEFT_CAMERA_CARLANE_POS, RIGHT_CAMERA_CARLANE_POS]


# =========================================#


class configManager:
    """This class is for importing and storing the setting values of the client program.
    """

    config = dict()
    """It is a dict object that stores the setting value of the client program."""

    def __init__(self):
        """A function to initialize the configManager class

        Check if the config.json file already exists and read the setting values from the config.json file.
        If there is no config.json file, create a new one and save it to the config.json file
        using the initial values at the top of FileManager.py.
        """

        # if there is no config.json file
        if os.path.isfile(PATH) is not True:
            # Create config.json file
            fd = open(PATH, 'w', encoding='UTF-8')
            fd.write("{}")
            fd.close()

            # Store initial config datas in new created config.json file
            self.recoveryOptions()

        # read config.json and store config.json data in self.config ( dict variable ) using json.load()
        with open(PATH, 'r', encoding="UTF-8") as pf:
            self.config = json.load(pf)
            pf.close()

        return

    def setConfig(self, option, value):
        """This function changes the setting value.

        :param str option: json key-value you want to change
        :param value: value you want to set

        """

        # change self.config
        self.config[option] = value

        # save changed self.config in config.json
        self.saveJSON()
        return

    def recoveryOptions(self):
        """This function initializes the config.json file."""

        # Read initial values from global variables of the top of FileManager.py and change self.config
        for i in range(len(optionList)):
            self.config[optionList[i]] = optionValues[i]

        # save changed self.config in config.json
        self.saveJSON()
        return

    def getConfig(self):
        """This function returns a self.config object."""

        return self.config

    def saveJSON(self):
        """This function stores the self.config object in the form of json in the config.json file."""

        with open(PATH, 'w', encoding='UTF-8') as pf:
            json.dump(self.config, pf, indent='\t', ensure_ascii=False)
        pf.close()
