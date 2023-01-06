import os
from peewee import *
from playhouse.flask_utils import PaginatedQuery
import datetime
import random
import pydotenv
from baselib import *

env = pydotenv.Environment()

DATABASE = env.get('DATABASE', './wapp_file_manager.database.db')
__DEMO__ = env.get('__DEMO__', True)

if (__DEMO__):
    print(__DEMO__)
    print(DATABASE)
    if (os.path.exists(DATABASE)):
        os.unlink(DATABASE)

bFirstStart = not os.path.exists(DATABASE)
db = SqliteDatabase(DATABASE)
lClasses = []

# Link: Модели
class Tab(Model):
    title = CharField(default="")
    path = CharField(default="")
    selected_file = CharField(default="")

    class Meta:
        database = db
lClasses.append(Tab)

class TabsHistory(Model):
    name = CharField(default="")
    tab = ForeignKeyField(Tab, backref='tabs_histories')
    path = CharField(default="")
    selected_file = CharField(default="")

    class Meta:
        database = db
lClasses.append(TabsHistory)

class ModelsWrapper():
    oR = {}

    def __init__(self, oR) -> None:
        self.oR = oR

db.connect()

# Link: DEMO
if (bFirstStart):
    db.create_tables(lClasses)

    if (__DEMO__):
        aConfigDirs=fnLoadConfigDirs()        
        for sTitle, sDir in aConfigDirs["tabs"].items():
            Tab.create(title=sTitle,path=sDir)
        print(model_to_dict(Tab.select()[0]))
        print(model_to_dict(Tab.select()[1]))
        


        