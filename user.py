class user:
    def __init__(self):
        self.name = None
        self.surname = None
        self.middleName = None
        self.age = None
        self.symptomes = []
        self.address = None
        self.gender = None
        self.diseases = []
        self.symptomes = None
        self.address = None
        self.gender = None
    def setSurname(self, surname):
        self.surname = surname
    def setName(self, name):
        self.name = name
    def setMiddleName(self, middleName):
        self.middleName = middleName
    def setAge(self, age):
        self.age = age
    def setAddress(self, address):
        self.address = address
    def setSymptomes(self, symptomes):
        self.symptomes = symptomes
    def setDiseases(self, diseases):
        self.diseases = diseases
    def setGender(self, gender):
        self.gender = gender

    def getSurname(self):
        return self.surname
    def getName(self):
        return self.name
    def getMiddleName(self):
        return self.middleName
    def getAge(self):
        return str(self.age)
    def getAddress(self):
        return self.address
    def getSymptomes(self):
        return self.symptomes
    def getDiseases(self):
        return self.diseases
    def getGender(self):
        return self.gender
