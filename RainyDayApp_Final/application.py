import os
import requests
import json
import time
from flask import Flask, request, session, render_template, redirect, url_for, jsonify, abort
from flask_session import Session
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database with ORM and the classes User, Location and Checkin to set up Tblusers, Tbllocations, and Tblcheckings
engine = create_engine(os.getenv("DATABASE_URL"))
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class User(Base):
    __tablename__ = 'Tblusers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50), unique=True)
    password = Column(String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

#checkin counts are tracked here in the Tbllocations table
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

    def __init__(self, zipcode, city, state, latitude, longitude, population, checkin_count=0):
        self.zipcode = zipcode
        self.city = city
        self.state = state
        self.latitude = latitude
        self.longitude = longitude
        self.population = population 
        self.checkin_count = checkin_count

class Checkin(Base):
    __tablename__ = 'Tblcheckings'
    id = Column(Integer, primary_key=True)
    email = Column(String(50))
    comment = Column(Text)
    zipcode = Column(String(5))

    def __init__(self, email, comment, zipcode):
        self.email = email
        self.comment = comment
        self.zipcode = zipcode

#Homepage
@app.route('/')
def index():
    return render_template("index.html")

#Login - email and password are passed in through the form.  This is a POST and if successful user, then redirected to the Search page
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        session['error'] = ''
        return render_template('login.html')
    else:
        email = request.form['email']
        passw = request.form['password']
        try:
            data = User.query.filter_by(email=email, password=passw).first()
            if data is not None:
                session['logged_in'] = True
                session['name'] = data.name
                session['email'] = email
                session['error'] = ''
                return redirect(url_for('search'))
            else:                
                session['error'] = 'Invalid credentials'
                print(session['error'])
                return render_template('login.html')
        except:
            session['error'] = 'Database Error in login'
            print(session['error'])
            return render_template('login.html')

#register - after the successful registration of the user, redirect to the Login page, otherwise redirect back to the registration page		
@app.route('/register', methods=['GET', 'POST'])
def register(): 
    if request.method == 'POST':
        try:
            new_user = User(name=request.form['name'], email=request.form['email'], password=request.form['password'])
            db_session.add(new_user)
            db_session.commit()
            session['success'] = 'Registered'
            return redirect(url_for('login'))
        except:
            session['error'] = 'Database Error in register'
            print(session['error'])
            return render_template('register.html')            

    session['error'] = ''    
    return render_template('register.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))     

#after successful login search page opens by POST Method. The Locations class which is the tbllocations table returns a results dataset and passes the dataset locations 
#to the search page displayed in a card-body class with a link to location.html using the three fields in the card as the hyperlink.
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        session['error'] = ''
        session['found'] = False
        return render_template("search.html")            
    else:
        results = []
        search_text = request.form['search_text']
        print(search_text)
        if search_text != '':
            try:
                results += Location.query.filter(Location.zipcode.ilike('%{}%'.format(search_text))).order_by(Location.zipcode).all()
                results += Location.query.filter(Location.city.ilike('%{}%'.format(search_text))).order_by(Location.zipcode).all()
                results += Location.query.filter(Location.state.ilike('%{}%'.format(search_text))).order_by(Location.zipcode).all()
                if results:   
                    session['found'] = True
                    return render_template("search.html", locations=results)
                else:
                    session['found'] = False
                    session['error'] = 'Not found'
                    return render_template("search.html")   
            except:
                session['found'] = False
                session['error'] = 'Database Error in search'
                print(session['error'])
                return render_template('search.html')           
        else:
            session['found'] = False
            session['error'] = 'Please enter value to search'
            return render_template("search.html")  

#data from API and search results are combined here and passed as the city_data dataset.  This is the result from clicking the location link from the results of the search page.			
@app.route("/location/<zipcode>", methods=['GET'])
def location(zipcode):
    weather = requests.get("https://api.darksky.net/forecast/d823e7369fb9e7df22fae0c603556431/42.37,-71.11").json()
    template_data = weather["currently"]
    city_data = Location.query.filter_by(zipcode=zipcode).first()

    if city_data is None:
        return redirect(url_for("search"))

    checkin_data = Checkin.query.filter_by(zipcode=zipcode, email=session['email']).first()
    if checkin_data is not None:
        template_data['comment'] = checkin_data.comment
    else: 
        template_data['comment'] = False

    template_data['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(template_data['time']))
    template_data['city'] = city_data.city
    template_data['state'] = city_data.state
    template_data['zipcode'] = city_data.zipcode
    template_data['latitude'] = city_data.latitude
    template_data['longitude'] = city_data.longitude
    template_data['population'] = city_data.population
    template_data['checkin_count'] = city_data.checkin_count

    return render_template("location.html", city_data=template_data)

#When a comment is added at checking then there is an UPDATE of the check_in count by 1 in the tbllocations table.	
@app.route("/comment", methods=['POST'])
def comment():
    comment = request.form['comment']
    zipcode = request.form['zipcode']

    location = Location.query.filter_by(zipcode=zipcode).first()
    location.checkin_count += 1
    db_session.commit()

    comment = Checkin(session['email'], comment, zipcode)

    db_session.add(comment)
    db_session.commit()   
    return redirect(url_for("location", zipcode=zipcode)) 

#API calls are made by entering the browser path<host>:/api/zipcode. The return is displayed in JSON format and if no zipcode is found and 404 error is displayed.
@app.route("/api/<zipcode>", methods=['GET'])
def api(zipcode):    
    location = Location.query.filter_by(zipcode=zipcode).first()
    if location:
        data = {
            "place_name": location.city,
            "state": location.state,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "zip": location.zipcode,
            "population": location.population,
            "check_ins": location.checkin_count
        }
        return jsonify(data)
    else:
        abort(404)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    app.run(debug=True)