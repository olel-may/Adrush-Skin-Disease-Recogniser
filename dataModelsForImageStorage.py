from sqlalchemy import Table, MetaData, Column, Integer, Text, String, create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import mapper, sessionmaker

__author__ = 'dolel'

SQLALCHEMY_DATABASE_URI = 'your_database_server://user_account:password@host_for_your_database/database_name'
#Engine, which the Session will use for connection resources
database_engine = create_engine(SQLALCHEMY_DATABASE_URI)
#Creating the Configured Session Class
Session = sessionmaker(bind=database_engine)
session = Session()


class SkinImage(object):
    def __init__(self, patientAge=None, patientLocation=None, skinConditionDescription=None, skinImageName=None, skinImageExtension=None, skinImageId=None):
      self.skinImageId = skinImageId
      self.patientAge = patientAge
      self.patientLocation = patientLocation
      self.skinConditionDescription = skinConditionDescription
      self.skinImageName = skinImageName
      self.skinImageExtension = skinImageExtension

    def saveSkinImage(self):
      try:
          session.add(self)
          session.commit()
          return self.skinImageId
      except InvalidRequestError:
          session.rollback()

    def retrieveImages(self):
      return session.query(SkinImage).all()

    def getImageName(self):
      return session.query(SkinImage).filter(SkinImage.skinImageId == self.skinImageId).first()


skinImageTable = Table('skinImages', MetaData(),
                       Column('skinImageId', Integer, primary_key=True, autoincrement=True),
                       Column('patientAge', Integer, nullable=False),
                       Column('patientLocation', String, nullable=False),
                       Column('skinConditionDescription', Text, nullable=False),
                       Column('skinImageName', String(30), nullable=False),
                       Column('skinImageExtension', String(5), nullable=False))
mapper(SkinImage, skinImageTable)