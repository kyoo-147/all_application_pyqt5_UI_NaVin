class Serviceman:
    """Collect information on the required serviceman"""

    def __init__(self, serviceNumber, firstName, givenNames, lastNames):
        """Initialise serviceman class"""
        self.serviceNumber = serviceNumber
        self.firstName = firstName
        self.givenNames = givenNames
        self.lastName = lastNames

    def set_first_name(self, firstName):
        self.firstName = firstName

    def set_given_names(self, givenNames):
        self.givenNames = givenNames

    def set_last_name(self, lastName):
        self.lastName = lastName

    def set_service_number(self, serviceNumber):
        self.serviceNumber = serviceNumber

    def get_first_name(self):
        return self.firstName

    def get_given_names(self):
        return self.givenNames

    def get_last_name(self):
        return self.lastName

    def get_service_number(self):
        return self.serviceNumber
