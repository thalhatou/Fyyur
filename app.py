#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from jinja2.utils import markupsafe 
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from datetime import datetime, timezone
from sqlalchemy import or_, desc
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

# Importing the db, Artist, Venue, and Show classes from the models.py file.
from models import db, Artist, Venue, Show
migrate = Migrate(app,db)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  # num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  # Creating a variable called current_time and assigning it the value of the current time.
  current_time = datetime.now()
  Group_venue_by_city_state = ''

  data = [] # data dictionary

  # query Venue db and return all records
  venues = Venue.query.all()

  for venue in venues:
    up_coming_shows = venue.shows

    filtered_upcoming_shows = [show for show in  up_coming_shows if show.show_start_time > current_time]

    if Group_venue_by_city_state == venue.city + venue.state:
      data[len(data) - 1]["venues"].append({
        "id": venue.id, 
        "name": venue.name,
        "num_upcoming_shows": len(filtered_upcoming_shows)
      })
    else:
      Group_venue_by_city_state == venue.city + venue.state
      # After all venues are added to the list for a given location, add it to the data dictionary
      data.append({
        "city": venue.city, 
        "state": venue.state, 
        "venues": [{
          "id": venue.id, 
          "name": venue.name, 
          "num_upcoming_shows": len(filtered_upcoming_shows)
        }]
      })

  return render_template('pages/venues.html', areas=data);
  

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  # venue search implementation
  Search_term = request.form.get('search_term')
  search_format = "%{}%".format(Search_term.lower())
  search_query= Venue.query.filter(or_(Venue.name.ilike(search_format), Venue.city.ilike(search_format), Venue.state.ilike(search_format))).all()
  response = {'count':len(search_query),'data':search_query}
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
# Getting the venue_id from the database.
  venue_query = Venue.query.get(venue_id)
 # Querying the database for all the shows in the database.
  shows = Show.query.all()
  filter_shows = [show for show in shows if show.venue_id == venue_id]
  # if it finds a venue with that ID
  if venue_query:
    venue_data = venue_query
    data = {
      "id": venue_data.id, 
      "name": venue_data.name, 
      "genres": venue_data.genres, 
      "addres": venue_data.address, 
      "city": venue_data.city, 
      "state": venue_data.state, 
      "phone": venue_data.phone, 
      "website": venue_data.website_link, 
      "facebook_link": venue_data.facebook_link, 
      "seeking_talent": venue_data.seeking_talent, 
      "seeking_description": venue_data.seeking_description, 
      "image_link": venue_data.image_link, 
      }
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  try:
   # Creating a new instance of the class Venue.
    Newvenue = Venue()
    Newvenue.name = request.form.get('name')
    Newvenue.genres = ', '.join(request.form.getlist('genres'))
    Newvenue.address = request.form.get('address')
    Newvenue.city = request.form.get('city')
    Newvenue.state = request.form.get('state')
    Newvenue.phone = request.form.get('phone')
    Newvenue.facebook_link = request.form.get('facebook_link')
    Newvenue.image_link = request.form.get('image_link')
    Newvenue.website_link = request.form.get('website_link')
    Newvenue.seeking_talent = True if request.form.get('seeking_talent')!= None else False
    Newvenue.seeking_description = request.form.get('seeking_description')
    db.session.add(Newvenue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    error = True
    db.session.rollback()
  
    flash('An error occured, venue could not be added.')
  finally:
    db.session.close()
  # on successful db insert, flash success
  # flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  error = False
  try:
  # Deleting all the shows that are associated with the venue_id.
    Show.query.filter_by(venue_id=venue_id).delete()
   # Deleting the venue with the id of venue_id.
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' has been successfully deleted')
  except:
    error=True
    db.session.rollback()
    flash('Venue ' + request.form['name'] + ' An error has occured, venue could not be deleted')
  finally:
    db.session.close()
    return render_template('pages/home.html')
  


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.order_by(Artist.name).all()  # Sorting alphabetically
 # Creating a list of dictionaries.
  data = []
  for artist in artists:
        data.append({
            "id": artist.id,
            "name": artist.name
        })

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  Search_term = request.form.get('search_term')
  search_format = "%{}%".format(Search_term.lower())
  search_query= Artist.query.filter(or_(Artist.name.ilike(search_format), Artist.city.ilike(search_format), Artist.state.ilike(search_format))).all()
  response = {'count':len(search_query),'data':search_query}
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  #Getting the artist_id from the database.
  artist_query = Artist.query.get(artist_id)
  upcoming_shows = []
  past_shows = []
  # if it finds a venue with that ID
  if artist_query:
    artist_data = artist_query
    data = {
      "id": artist_data.id, 
      "name": artist_data.name, 
      "genres": artist_data.genres, 
      "city": artist_data.city, 
      "state": artist_data.state, 
      "phone": artist_data.phone, 
      "website": artist_data.website_link, 
      "facebook_link": artist_data.facebook_link, 
      "seeking_venue": artist_data.seeking_venue, 
      "seeking_description":artist_data.seeking_description, 
      "image_link": artist_data.image_link, 
      }
  
  return render_template('pages/show_artist.html', artist=data)



#  Update
#  ----------------------------------------------------------------

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
 # Getting the artist_id from the database.
  artist = Artist.query.get(artist_id)
  if not artist:
    return redirect(url_for('index'))
  else:
    form = ArtistForm(obj=artist)
  artist={
    "id": artist_id,
    "name": artist.name,
# The above code is splitting the genres column into a list of genres.
    "genres":artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website_link": artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  try:
   artist_data = Artist.query.get(artist_id)
   artist_data.name = request.form.get('name')
   artist_data.genres = ', '.join(request.form.getlist('genres'))
   artist_data.city = request.form.get('city')
   artist_data.state = request.form.get('state')
   artist_data.phone = request.form.get('phone')
   artist_data.facebook_link = request.form.get('facebook_link')
   artist_data.image_link = request.form.get('image_link')
   artist_data.website_link = request.form.get('website_link')
   artist_data.seeking_venue = True if request.form.get('seeking_venue')!= None else False
   artist_data.seeking_description = request.form.get('seeking_description')
   db.session.add(artist_data)
   db.session.commit()
  except:

   db.session.rollback()
 

  finally:
   db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  if not venue:
    return redirect(url_for('index'))
  else:
    form = VenueForm(obj=venue)
  venue={
    "id": venue_id,
    "name": venue.name,
# The above code is splitting the genres column into a list of genres.
    "genres":venue.genres,
    "city": venue.city,
    "state": venue.state,
    "address":venue.address,
    "phone": venue.phone,
    "website_link": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  try:
    venue_data = Venue.query.get(venue_id)
    venue_data.name = request.form.get('name')
    venue_data.genres = ', '.join(request.form.getlist('genres'))
    venue_data.address = request.form.get('address')
    venue_data.city = request.form.get('city')
    venue_data.state = request.form.get('state')
    venue_data.phone = request.form.get('phone')
    venue_data.facebook_link = request.form.get('facebook_link')
    venue_data.image_link = request.form.get('image_link')
    venue_data.website_link = request.form.get('website_link')
    venue_data.seeking_talent = True if request.form.get('seeking_talent')!= None else False
    venue_data.seeking_description = request.form.get('seeking_description')
    db.session.add(venue_data)
    db.session.commit()
  except:
    db.session.rollback()
  
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))







#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form)
  error = False
  try:
  # Creating a new instance of the Artist class.
    newArtist = Artist()
    newArtist.name = request.form.get('name')
# Taking the list of genres and joining them together with a comma and a space.
    newArtist.genres = ', '.join(request.form.getlist('genres'))
    newArtist.address = request.form.get('address')
    newArtist.city = request.form.get('city')
    newArtist.state = request.form.get('state')
    newArtist.phone = request.form.get('phone')
    newArtist.facebook_link = request.form.get('facebook_link')
    newArtist.image_link = request.form.get('image_link')
    newArtist.website_link = request.form.get('website_link')
   # The above code is checking if the checkbox is checked or not. If it is checked, it will return
   # True, otherwise it will return False.
    newArtist.seeking_venue = True if request.form.get('seeking_venue')!= None else False
    newArtist.seeking_description = request.form.get('seeking_description')
    db.session.add(newArtist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')

  except:
    error = True
    db.session.rollback()
  
    flash('An error occured, artist could not be added.')
  
  finally:
    db.session.close()

  # on successful db insert, flash success
  # flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


@app.route('/artists/<artist_id>/delete', methods=['DELETE'])
def delete_artist(artist_id):
  # TODO: Complete this endpoint for taking a artist_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  try:
  # Deleting all the shows that are associated with the artist_id.
    Show.query.filter_by(artist_id=artist_id).delete()
    # Deleting the artist with the id of artist_id.
    Artist.query.filter_by(id=artist_id).delete()
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' has been successfully deleted')
  except:
    error=True
    db.session.rollback()
    flash('Artist ' + request.form['name'] + ' An error has occured, Artist could not be deleted')
  finally:
    db.session.close()
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data = []
  shows = Show.query.all()  # getting all the shows
  for show in shows:
    artist = Artist.query.get(show.artist_id)
    venue = Venue.query.get(show.venue_id)
    data.append({
            "venue_id":show.venue_id,
            "venue_name":venue.name,
            "artist_id":show.artist_id ,
            "artist_name": artist.name,
            "artist_image_link":artist.image_link,
            "start_time":format_datetime(str(show.show_start_time))
        })
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm(request.form)
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  try:
    error = False
    newShow = Show(
      artist_id = form.artist_id.data,
      venue_id = form.venue_id.data,
      show_start_time = form.start_time.data
    )
    db.session.add(newShow)
    db.session.commit()
    #on successful db insert, flash success
    flash('Show was successfully listed!')
  except:
    error = True
    db.session.rollback()
    flash('An error occured, show could not be added.')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
  
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')



@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
