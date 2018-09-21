import tornado.ioloop
import tornado.escape
import tornado.web
import tornado.wsgi
import pyrestful.rest

from Data.UserDatabase import UserDataBase
from Services.Service import Service

# from Data.UserDatabaseGAE import UserDataBaseGAE
# from Services.ServiceGAE import ServiceGAE

if __name__ == '__main__':
    try:
        print("Start the services")
        database = UserDataBase()
        app = pyrestful.rest.RestService([Service], dict(database=database))
        app.listen(8085)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("\nStop the services")

# database = UserDataBaseGAE()
# app = pyrestful.rest.RestService([ServiceGAE], dict(database=database))
# application = tornado.wsgi.WSGIAdapter(app)
