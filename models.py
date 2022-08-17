# Importing the app variable that is a member of the app package. The app variable is a Flask
# instance, which represents the web application.
from app import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
# TODO: connect to a local postgresql database
db = SQLAlchemy(app)
#-----------------------



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
  # Creating a relationship between the Show and Venue tables.
    shows = db.relationship('Show', backref='venues',lazy='dynamic')    # Can reference show.venue (as well as venue.shows)

    def __repr__(self):
        return f'<Venue {self.id} {self.name}>'
   
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
# The Artist class is a model for the artists table in the database. It has the following columns: id,
# name, city, state, phone, genres, image_link, facebook_link, website_link, seeking_venue, and
# # seeking_description.
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
   # Creating a relationship between the Show and Artist tables.
    shows = db.relationship('Show', backref='artists', lazy='dynamic')    # Can reference show.artist (as well as artist.shows)

    def __repr__(self):
        return f'<Artist {self.id} {self.name}>'

# The Show class has a relationship with the Artist and Venue classes.
class Show(db.Model):
  __tablename__ = 'shows'
  id = db.Column(db.Integer,primary_key=True)
  show_start_time = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)
# Creating a foreign key relationship between the Artist and Show tables.
  artist_id = db.Column(db.Integer,db.ForeignKey('artists.id',ondelete='CASCADE',),nullable=False)
# The above code is creating a foreign key relationship between the Venue and Show tables.
  venue_id = db.Column(db.Integer,db.ForeignKey('venues.id',ondelete='CASCADE'),nullable=False)
  def __repr__(self):
        return f'<Show {self.id} {self.show_start_time} artist_id={artist_id} venue_id={venue_id}>'
