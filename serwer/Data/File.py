class User(object):
    fileId = int
    name = str

    def __init__(self, fileId, name):
        self.fileId = fileId
        self.name = name

    # Setters
    def set_Name(self, name):
        self.name = name

    # Getters
    def get_Id(self):
        return self.fileId

    def get_Name(self):
        return self.name

