# Importing the app variable that is a member of the app package. The app variable is a Flask
# instance, which represents the web application.
from app import app

# Importing the SQLAlchemy class from the flask_sqlalchemy module.
from flask_sqlalchemy import SQLAlchemy



 #TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#




# The Venue class is a model that represents a venue in the database.
class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean,default=False)
    seeking_description = db.Column(db.String(600))
    Shows = db.relationship('show')
    venues = db.relationship('Venue',secondary='shows',back_populates='venues',lazy='dynamic')

 # TODO: implement any missing fields, as a database migration using Flask-Migrate



# The Artist class is a model for the artists table in the database. It has the following columns: id,
# name, city, state, phone, genres, image_link, facebook_link, website_link, seeking_venue, and
# seeking_description.
class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean,default=False)
    seeking_description = db.Column(db.String(600))
    Shows = db.relationship('show')
    venues = db.relationship('Venue',secondary='shows',back_populates='artists',lazy='dynamic')




# The Show class has a relationship with the Artist and Venue classes.
class Show(db.Model):
  __tablename__ = 'shows'
  id = db.Column(db.Integer,primary_key=True)
  show_start_time = db.Column(db.DateTime, nullable=False)
  artist = db.relationship('Artist')
  artist_id = db.Column(db.Integer,db.ForeignKey('artists.id',ondelete='CASCADE',),nullable=False)
  venue = db.relationship('Venue')
  venue_id = db.Column(db.Integer,db.ForeignKey('venues.id',ondelete='CASCADE'),nullable=False)