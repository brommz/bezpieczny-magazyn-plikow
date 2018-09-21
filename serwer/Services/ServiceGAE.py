import hashlib
import os, uuid

import pyrestful.rest
from Data.User import User
from pyrestful import mediatypes
from pyrestful.rest import get, post

from MyCrypto.HMAC import HMAC, calcHMAC

class ServiceGAE(pyrestful.rest.RestHandler):
    def initialize(self, database):
        self.database = database

    @post(_path = "/CreateUser", _types = [str, str], _produces = mediatypes.APPLICATION_JSON)
    def createUser(self, Login, Key):
        userid = 1234
        return {"created_user": [{"userId": userid}, { "key": "kluczDoTworzeniaHMAC"}] }

    @get(_path = "/Hmac/{Key}", _types = [str], _produces = mediatypes.APPLICATION_JSON)
    def getHmac(self, Key):
        hmac = calcHMAC(str(Key), 'test', hashlib.md5)
        print hmac
        return { 'hmac': hmac.hexdigest() }

    @get(_path = "/FileList", types = [int, str, str, int, str], _produces = mediatypes.APPLICATION_JSON)
    def fileList(self, TimeStamp, Command, FileName, UserId, HMAC):
        return { "fileList": ["test2.txt", "test4.txt", "test1.txt", "test5.txt"] }

    @post(_path = "/UploadFile", _produces = mediatypes.APPLICATION_JSON)
    def uploadFile(self, TimeStamp, Command, FileName, UserId, HMAC):
        return { "uploadedFile:": 'ok' }

    @get(_path = "/UploadFilePage", _produces = mediatypes.APPLICATION_JSON)
    def newFile(self):
        self.render("fileuploadform.html")

    @get(_path = "/File", types = [str], _produces = mediatypes.APPLICATION_JSON)
    def downloadFile(self, TimeStamp, Command, FileName, UserId, HMAC):
        file_name = './files/' + str(FileName)
        buf_size = 4096
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + FileName)
        data = '2343453454545'
        self.write(data)
        self.finish()

    #     @get(_path = "/User/{userid}", _types = [int],_produces = mediatypes.APPLICATION_JSON)
    # def getUser(self, userid):
    #     response = User(userid, 'nazwa', 'klucz')
    #     print(response)
    #     return response
