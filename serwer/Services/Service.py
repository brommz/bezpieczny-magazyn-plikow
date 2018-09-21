import hashlib
import os, uuid
import time

import pyrestful.rest
from pyrestful import mediatypes
from pyrestful.rest import get, post

from MyCrypto.HMAC import HMAC, calcHMAC

class Service(pyrestful.rest.RestHandler):
    def initialize(self, database):
        self.database = database

    @get(_path = "/User/{Userid}", _types = [int],_produces = mediatypes.APPLICATION_JSON)
    def getUser(self, Userid):
        if not self.database.exists(Userid):
            self.gen_http_error(404, 'Error 404 : do not exists the customer : %d' % Userid)
            return
        response = self.database.find(Userid)
        #response = User(1, 'nazwa', 'klucz')
        print('Pobrany user:' + response)
        return response

    @get(_path = "/CreateUser", _types = [str,str], _produces = mediatypes.APPLICATION_JSON)
    def createUser(self, Login, Key):
        print 'CreateUser'
        userid = self.database.insert(str(Login), str(Key))
        print 'User utworzony, jego Id: ' + str(userid) + ' login: ' + str(Login) + ' key: ' + str(Key)
        return {"created_user_id": userid}

    @get(_path = "/Hmac/{Key}", _types = [str], _produces = mediatypes.APPLICATION_JSON)
    def getHmac(self, Key):
        hmac = calcHMAC(str(Key), 'test', hashlib.md5)
        print 'Wygenerowany HMAC:' + hmac.hexdigest()
        return { 'hmac': hmac.hexdigest()}

    @post(_path = "/UploadFile", _types = [float,str,str,str,str], _produces = mediatypes.APPLICATION_JSON)
    def uploadFile(self, TimeStamp, Command, FileName, UserId, HMAC):
        print 'Rozpoczecie uplodu pliku: ' + FileName + 'UserId:' + UserId
        if not self.isTimeStampOk(TimeStamp):
            return { "error": "Timestamp problem. Possible replay attack" }
        message = Command + str(UserId)
        if not self.checkHMAC(message, UserId, HMAC):
            return { "error": "HMAC not valid" }

        fileinfo = self.request.files['filearg'][0]
        print "fileinfo is", fileinfo
        fname = fileinfo['filename']
        cname = str(fname)
        fh = open('./files/' + UserId + '/' + cname, 'w')
        fh.write(fileinfo['body'])
        self.finish(cname + " is uploaded!!")
        print 'Plik uploadowany, nazwa: ' + fname
        return { "uploadedFile:": fname }

    @post(_path = "/UploadFileTest", _produces = mediatypes.APPLICATION_JSON)
    def uploadFileTest(self):
        fileinfo = self.request.files['filearg'][0]
        print "fileinfo is", fileinfo
        fname = fileinfo['filename']
        cname = str(fname)
        fh = open('./files/' + cname, 'w')
        fh.write(fileinfo['body'])
        self.finish(cname + " is uploaded!!")
        return { "uploadedFile:": fname }

    @get(_path = "/UploadFilePage", _produces=mediatypes.APPLICATION_JSON)
    def newFile(self):
        self.render("fileuploadform.html")

    @get(_path = "/File", _types=[float,str,str,str,str], _produces=mediatypes.APPLICATION_JSON)
    def downloadFile(self, TimeStamp, Command, FileName, UserId, HMAC):
        print 'Prosba o pobranie pliku, nazwa: ' + FileName + ' UserId: ' + UserId
        if not self.isTimeStampOk(TimeStamp):
            return { "error": "Timestamp problem. Possible replay attack" }
        message = Command + FileName + str(UserId)
        if not self.checkHMAC(message, UserId, HMAC):
            return { "error": "HMAC not valid" }

        file_name = './files/' + UserId + '/' + str(FileName)
        buf_size = 409600
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + FileName)
        with open(file_name, 'r') as f:
            while True:
                data = f.read(buf_size)
                if not data:
                    break
                self.write(data)
        try:
            self.finish()
        except SystemError:
            pass
        print 'Poprawnie pobrany plik'

    @get(_path = "/FileList", _types=[float, str, str, str], _produces=mediatypes.APPLICATION_JSON)
    def fileList(self, TimeStamp, Command, UserId, HMAC):
        if not self.isTimeStampOk(TimeStamp):
            return { "error": "Timestamp problem. Possible replay attack" }
        message = Command + str(UserId)
        if not self.checkHMAC(message, UserId, HMAC):
            return { "error": "HMAC not valid" }

        return { "fileList": os.listdir('./files/' + UserId + '/') }

    @get(_path = "/Time/{timestamp}", _types = [float], _produces = mediatypes.APPLICATION_JSON)
    def testTime(self, timestamp):
        timeNow = time.time()
        return { 'timeNow, timeDiff': [ timeNow, timeNow-timestamp] }

    @get(_path = "/CheckHMAC", _types=[float,str,str,str,str], _produces = mediatypes.APPLICATION_JSON)
    def testOthers(self, TimeStamp, Command, FileName, UserId, HMAC):
        message = Command + FileName + str(UserId)
        hmacReturn = self.checkHMAC(message, UserId, HMAC)
        return { 'zlozenie z ktorego licze HMAC, wyliczony HMAC:', [message, hmacReturn] }

    # do 500 ms roznicy mowi ze nie bylo ataku powtorzeniowego bo nikt by nie zdazyl
    def isTimeStampOk(self, timeStamp, testing = False):
        # return True
        # if testing == False:
        #     return True
        timeNow = time.time()
        # do 2 ms timestamp, 19 - wynika z braku synchro zegarow i jest roznica 19 sekund :/
        if (timeNow - timeStamp <= 2 + 19) and (timeNow - timeStamp > 0):
            return True
        print 'Timestamp jest zly, bo timeNow mam: ' + str(timeNow) + ' a timeStamp jest: ' + str(timeStamp)
        return False

    # sprawdza HMAC poprzez wyliczenie i porownanie
    def checkHMAC(self, message, userId, HMAC, testing = False):
        # return True
        # if testing == False:
        #     return True
        user = self.database.find(userId)
        hmac = calcHMAC(str(user.get('key')), str(message), hashlib.md5)

        if testing == True:
            return hmac

        if hmac.hexdigest().upper() == HMAC.upper():
            return True
        print 'checkHMAC nie przeszlo. Sprawdz jak liczysz bo moze ze zlych danych'
        return False

