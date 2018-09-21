from Data.User import User

class UserDataBaseGAE(object):
    DB = dict()
    id_seq = 1

    def insert(self, name, key):
        sequence = self.id_seq
        while self.exists(sequence) == True:
            sequence += 1

        user = User(sequence, name, key)
        self.DB.insert({'userid': user.get_Id(), 'name': user.get_Name(), 'key': user.get_Key()})
        self.id_seq += 1
        return sequence

    def update(self, userid, name, key):
        if self.exists(userid):
            user = self.find(userid)
            user.set_Name(str(name))
            user.set_Key(str(key))
            return True
        else:
            return False

    def delete(self, userid):
        if self.exists(userid):
            del self.DB[userid]
            return True
        else:
            return False

    def find(self, userid):
        if self.exists(userid):
            return self.DB[userid]
        else:
            return None

    def exists(self, userid):
        if userid in self.DB:
            return True
        else:
            return False

    def all(self):
        return self.DB