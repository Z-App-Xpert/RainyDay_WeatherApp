import csv
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Check for environment variable
#The string for this project is 
#	postgres://ajwkjnrqnbalur:93366a322e1bf35b3364d47073e82de1d5afcd69d5ed7e3b280dcfc74167c4ea@ec2-54-83-3-101.compute-1.amazonaws.com:5432/d97papfr8pull

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(os.getenv("DATABASE_URL"))
db_session = scoped_session(sessionmaker(bind=engine))

#creates appropriate table objects and appropriate mapping calls to create Tbllocations
Base = declarative_base()
class Location(Base):
    __tablename__ = 'Tbllocations'
    id = Column(Integer, primary_key=True)
    zipcode = Column(String(5))
    city = Column(String(50))
    state = Column(String(3))
    latitude = Column(String(10))
    longitude = Column(String(10))    
    population = Column(Integer)
    checkin_count = Column(Integer)

    def __init__(self, zipcode, city, state, latitude, longitude, population, checkin_count = 0):
        self.zipcode = zipcode
        self.city = city
        self.state = state
        self.latitude = latitude
        self.longitude = longitude
        self.population = population 
        self.checkin_count = checkin_count

Base.metadata.create_all(bind=engine)
#Read through the data input file, skip the first row and insert data using db_session
with open('zips.csv', 'r') as csvfile:
    csv_r = csv.reader(csvfile)
    next(csv_r) #skip header
    zips = []
    for row in csv_r:
        zipcode, city, state, latitude, longitude, population = row
        zips.append(Location(zipcode, city, state, latitude, longitude, population, 0))

    print('inserting...')        
#chunk helps to split a list into manageable sizes to assure data interaction does not overload users machine memory capacity.
    for chunk in range(0, len(zips)-50, 50):        
        db_session.add_all([zips[i] for i in range(chunk, chunk + 50)])
        db_session.commit()
        db_session.flush()        
    