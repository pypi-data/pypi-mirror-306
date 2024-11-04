import datetime

from peewee import *

db = SqliteDatabase('my_app.db')


class BaseModel(Model):

    class Meta:
        database = db
