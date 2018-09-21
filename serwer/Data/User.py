class User(object):
    def __init__(self, userid, name, key):
        self.userid = userid
        self.name = name
        self.key = key

    def set_Name(self, name):
        self.name = name

    def set_Key(self, key):
        self.key = key

    # Getters
    def get_Id(self):
        return self.userid

    def get_Name(self):
        return self.name

    def get_Key(self):
        return self.key

