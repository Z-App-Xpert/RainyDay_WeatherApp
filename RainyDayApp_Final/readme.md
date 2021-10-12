#Rainy Day Application
###Run import.py
To run this application the user must run import.py first.  
*	At the cmd line in the terminal type ‘python import.py.’  
*	The import.py file makes use of the sqlalchemy import, sqlalchemy.orm and the sqlalchemy.ext.declarative
**	These imports make use of the Object-Relational Mapper (ORM) which is mapped to the Heroku database
**	The chunk in range portion of the code allows the use of the import module to easily handle a large amount of data in a file.  Chunk allows the splitting of each line in the .csv file to import.  This assures proper import into the proper field of the table.
**	The file to import is zips.csv.  To assure data integrity, a customization to  a function in excel that adds leading zeros to the zip code field was used.
**	The class Location is used to define the table named Tbllocations.  This table is defined through the class for the attributes
*	Zipcode
*	City
*	State
*	Latitude
*	Longitude
*	Population
*	The primary key- id is defined here
*	The checkin_count is defined as a counter
*	The default SELF is used to initialize/assign the values
*	With the zips.csv file, the header row is skipped and each attribute is appended to commit to the table Tbllocations.
*	The database engine is connected to Heroku database engine with the DATABASE_URL string.  The string for this project is 
**	postgres://ajwkjnrqnbalur:93366a322e1bf35b3364d47073e82de1d5afcd69d5ed7e3b280dcfc74167c4ea@ec2-54-83-3-101.compute-1.amazonaws.com:5432/d97papfr8pull

###Next the application.py must be run to generate the website.
*	Here the database is setup by using the ORM and the classes User, Location and Checkin.  These classes represent the ‘things’ the application is working with.  These attributes are initialized, or passed through to the templates rendered in the @app.routes defined in the application.py file.
*	Next the index.html loads and the user either log’s-in or register’s.
*	The Log-In form uses the POST method to submit data. 
*	Next the email and password are passed in with the form and redirected to the Search page upon successful query of the database for the email and password.	
*	If there are invalid credentials, then the user is redirected to the login.html page before receiving an error message.
*	The Register page requires a POST method.
*	The new_user is defined from the input form with the attributes of name, email, and password.
*	Upon a successful add to the database, the user is redirected to the login.html page.
*	If there is an error on either the register or login page, then there is a session error message delivered to the user interface and then redirected to the register.html page.
*	Once on the Log-in page and the email and password are found in the database, then the user is redirected to the search.html page.
*	The search request method must by a POST, if it is a POST, then results are requested from the database.
*	Results are passed to the search.html page in the locations dataset.
*	For each location in locations the city, state and zipcode are displayed in a card-body class with a link to location.html using the three fields in the card as the hyperlink.
*	Once this is clicked then the locations/zipcode is opend to pull the tblLocations table data and the required weather data into template_data.
*	This template_data of weather and location attributes is passed to the location.html page in the city_data dataset.  This is displayed in a card body class.
*	And then if the user has not made a comment then the city comment is opened for the user to add a comment.  Once one comment is made by a user, then it cannot be edited.  If a new user signs on, then they can make a comment for this location.
*	The number of check-ins are tallied and displayed in the card body class titled ‘No. of checkins.’
*	This is kept track in the checkin_count column of the Tbllocations table.
*	The calculation occurs in the def comment where 1 is added to the current comment count as the comment is being committed to the database.
*	An API calls are made by entering the browser path <host>:/api/(zipcode)
*	The result returns the name of the location, its state, latitude, longitude, ZIP code, population, and the number of user check-ins to that location. Also, if there is no zipcode in the database for the one entered, then a 404 error is returned.




