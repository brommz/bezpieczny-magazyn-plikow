import hashlib

class MD5(object):
    def __init__(self, key):
        self.md5 = hashlib.md5()
        self.hash = None
        self.calc(key)

    def calc(self, key):
        self.md5.update(key)
        self.hash = self.md5.hexdigest()
        return self.getHash()

    def getHash(self):
        return self.hash