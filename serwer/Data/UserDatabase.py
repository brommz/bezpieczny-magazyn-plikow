from Data.User import User
from tinydb import TinyDB, Query, where


class UserDataBase(object):
    DB = TinyDB('userDB.json')
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
            #self.DB[userid] = user # todo tak niee w tinydb
            return True
        else:
            return False

    def delete(self, userid):
        if self.exists(userid):
            self.DB.remove(where('userid') == userid)
            return True
        else:
            return False

    def find(self, userid):
        UserQuery = Query()
        if self.exists(int(userid)):
            return self.DB.get(UserQuery.userid == int(userid))
        else:
            return None

    def exists(self, userid):
        # return True
        UserQuery = Query()
        return self.DB.get(UserQuery.userid == int(userid)) != None
        # UserQuery = Query()
        # if len(self.DB.search(UserQuery.userid == userid)) > 0:
        #     return True
        # else:
        #     return False

    def all(self):
        return self.DB