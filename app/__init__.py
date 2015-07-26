__author__ = 'Madison'


from flask import Flask

app = Flask(__name__)
from app import views


#
# print 'i am doing something'
# from flask import Flask
# # import app.config
# # import os.path
# # import app.db_controller
#
# print 'dir of flask: ', dir(Flask)
#
# #
# # if not os.path.isfile(config.DATABASE_LOC):   # create DB if needed
# #     print 'No DB present. Creating DB file '+ config.DATABASE_LOC
# #     open(config.DATABASE_LOC, 'a').close()
# #     db_controller.create_table()
#
# app = Flask(__name__, static_url_path='')
# # from app import views, db_controller, config
