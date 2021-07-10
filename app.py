#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask_migrate import Migrate, show # i have added this
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for ,jsonify ,abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys
import os
from datetime import datetime
#from app import db
from sqlalchemy.dialects.postgresql import JSON
from extensions import csrf
#----------------------------------------------------------------------------#
# App Config.
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://abeer@localhost:5432/fyyur'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'any secret string'
csrf.init_app(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db,compare_type=True)
#from models import Result
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

from models import *
#----------------------------------------------------------------------------#
moment = Moment(app)
app.config.from_object('config')


# TODO: connect to a local postgresql database


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
  # num_shows should be aggregated based on number of upcoming shows per venue.
    data = Venue.query.all()
    venue = Venue.query.all()
    return render_template('pages/venues.html', areas=data,venue=venue)


@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term')
    search_results = Venue.name_search(search_term)
    response = {
        'count': len(search_results),
        'data': search_results
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/areas/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)

  if not venue: 
    return render_template('errors/404.html')
  results_past_show_art = db.session.query(Show, Artist).join(Artist).filter(Venue.id== venue_id).filter(Show.start_time<datetime.now()).all()
  print(results_past_show_art)
  past_shows = []
  for show in results_past_show_art:
           past_shows.append({
             "artist_id": show.Artist.id,
              "artist_name": show.Artist.name,
              "artist_image_link": show.Artist.image_link,
              "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
             # "start_time": show.Show.start_time.strftime('%Y-%m-%d %H:%M:%S')
              #"start_time":show['start_time']
            })
  print(past_shows)
  results_upcoming_show_art = db.session.query(Show, Artist).join(Artist).filter(Venue.id== venue_id).filter(Show.start_time>datetime.now()).all()
  upcoming_shows = []
  for show in results_upcoming_show_art:
    upcoming_shows.append({
      "artist_id": show.Artist.id,
      "artist_name": show.Artist.name,
      "artist_image_link": show.Artist.image_link,
     # "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S")    
    })
  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
 }
  return render_template('pages/show_venue.html',venue=data)
#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
      form = VenueForm()

      return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
     # TODO: insert form data as a new Venue record in the db, instead
    ## this is to check the validation of the fildes of the website fieldes
     form = VenueForm()
     if form.validate_on_submit():
       print ("submitted")
     else:
        for error in form.errors: 
         flash(error)

        return render_template('forms/new_venue.html',form=form) 
    ######
      #name
     name = request.form.get('name')
     city = request.form.get('city')
     state = request.form.get('state')
     address = request.form.get('address')
     phone = request.form.get('phone')
     image_link = request.form.get('image_link','')
     facebook_link= request.form.get('facebook_link','')
     website_link= request.form.get('website_link','')
     seeking_description= request.form.get('seeking_description','')
     genres= request.form.get('genres','')
     seeking_talent = request.form.get('seeking_talent','')
      #####this is for seeking_talent
     if seeking_talent == "y":
        seeking_talent = True
     elif seeking_talent == "":
        seeking_talent = False
              #####
     venue_form = Venue(name=name,city=city,state=state,address=address,phone=phone,image_link= image_link,facebook_link= facebook_link,website_link= website_link,seeking_description= seeking_description ,genres= genres,  seeking_talent=seeking_talent) 
    
      #########
     db.session.add(venue_form)
     db.session.commit()
      ########
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
     flash('Venue ' + request.form['name'] + ' was successfully listed!')
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
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term')
    search_results = Artist.name_search(search_term)
    response = {
        'count': len(search_results),
        'data': search_results
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):  
  #data = Artist.query.filter_by(id=artist_id).first()
  #return render_template('pages/show_artist.html', artist=data)
      ''' Getting a venue '''
      #try:
      artist_query = db.session.query(Artist).get(artist_id)
      if not artist_query: 
         return render_template('errors/404.html')
       # results_upcoming_show_art = db.session.query(Show, Artist).join(Artist).filter(Venue.id== venue_id).filter(Show.start_time>datetime.now()).all()
   
      upcoming_shows_query = db.session.query(Show).join(Venue).filter(Artist.id==artist_id).filter(Show.start_time>datetime.now()).all()
      #results = db.session.query(Artist, Venue).join(Venue).all()
      past_shows = []
      upcoming_shows = []
      upcoming_shows_query = db.session.query(Artist, Venue, Show).select_from(Show).join(Venue).join(Artist).filter_by(id=artist_id).filter(Show.start_time>datetime.now()).all()
      past_shows_query = db.session.query(Artist, Venue, Show).select_from(Show).join(Venue).join(Artist).filter_by(id=artist_id).filter(Show.start_time<datetime.now()).all()

      for show in past_shows_query:
       past_shows.append({
        "venue_id": show.Venue.id,
        "venue_name": show.Venue.name,
        "artist_image_link": show.Venue.image_link,
       # "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
      })
      for show in upcoming_shows_query:
        upcoming_shows.append({
          "venue_id": show.Venue.id,
          "venue_name": show.Venue.name,
          "artist_image_link": show.Venue.image_link,
         # "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
        })

      data = {
        "id": artist_query.id,
        "name": artist_query.name,
        "genres": artist_query.genres,
        "city": artist_query.city,
        "state": artist_query.state,
        "phone": artist_query.phone,
        "website": artist_query.website_link,
        "facebook_link": artist_query.facebook_link,
        "seeking_venue": artist_query.seeking_venue,
        "seeking_description": artist_query.seeking_description,
        "image_link": artist_query.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),

  }

      return render_template('pages/show_venue.html', venue=data)
      #except:
          #flash('Record not found')
         # return render_template('errors/404.html')
#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id): 
  form = ArtistForm()
  artist = Artist.query.filter_by(id=artist_id).first()
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
    Artists_id= request.form.get('artist_id')
    name = request.form.get('n ame')
    print(name)
    city = request.form.get('city')
    state = request.form.get('state')
    phone = request.form.get('phone')
    image_link = request.form.get('image_link','')
    facebook_link= request.form.get('facebook_link','')
    website_link= request.form.get('website_link','')
    seeking_description= request.form.get('seeking_description','')
    genres= request.form.get('genres','')
    seeking_venue= request.form.get('seeking_venue','')
      #####this is for seeking_venue
    if seeking_venue == "y":
        seeking_venue = True
    elif seeking_venue == "":
        seeking_venue = False
    ###
    #########
    Artists_edit = Artist.query.filter_by(id=artist_id).first()
    if Artists_edit is not None:
      Artists_edit.name = name
      Artists_edit.city = city
      Artists_edit.state = state
      Artists_edit.phone = phone
      Artists_edit.image_link = image_link
      Artists_edit.facebook_link = facebook_link
      Artists_edit.website_link = website_link
      Artists_edit.seeking_description = seeking_description
      Artists_edit.genres = genres
      Artists_edit.seeking_venue = seeking_venue
      db.session.commit()  
      print(Artists_edit)
    else: 
     flash('Artist ' + request.form['name'] + ' was none so it is could not be edited ')
  # artist record with ID <artist_id> using the new attributes
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.filter_by(id=venue_id).first()
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

  # TODO: populate form with values from venue with ID <venue_id>
  name = request.form.get('name')
  city = request.form.get('city')
  state = request.form.get('state')
  address = request.form.get('address')
  phone = request.form.get('phone')
  image_link = request.form.get('image_link','')
  facebook_link= request.form.get('facebook_link','')
  website_link= request.form.get('website_link','')
  seeking_description= request.form.get('seeking_description','')
  genres= request.form.get('genres','')
  seeking_talent = request.form.get('seeking_talent','')
      #####this is for seeking_talent
  if seeking_talent == "y":
        seeking_talent = True
  elif seeking_talent == "":
        seeking_talent = False

    #########
  Venue_show_id = Venue.query.filter_by(id=venue_id).first()

  if Venue_show_id is not None:
     Venue_show_id.name = name
     Venue_show_id.city = city
     Venue_show_id.state = state
     Venue_show_id.phone = phone
     Venue_show_id.image_link = image_link
     Venue_show_id.facebook_link = facebook_link
     Venue_show_id.website_link = website_link
     Venue_show_id.seeking_description = seeking_description
     Venue_show_id.genres = genres
     Venue_show_id.seeking_venue = seeking_talent
     db.session.commit()  
  else: 
       flash('Venue ' + request.form['name'] + ' was none so it is could not be edited ')
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

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
    # TODO: insert form data as a new Venue record in the db, instead
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    #address = request.form.get('address')
    phone = request.form.get('phone')
    image_link = request.form.get('image_link','')
    facebook_link= request.form.get('facebook_link','')
    website_link= request.form.get('website_link','')
    seeking_description= request.form.get('seeking_description','')
    genres= request.form.get('genres','')
    seeking_venue= request.form.get('seeking_venue','')
      #####this is for seeking_venue
    if seeking_venue == "y":
        seeking_venue = True
    elif seeking_venue == "":
        seeking_venue = False
              #####
    artist_form = Artist(seeking_venue=seeking_venue,name=name,genres= genres,seeking_description= seeking_description ,website_link= website_link,facebook_link= facebook_link, image_link= image_link,phone=phone,state=state,city=city) 
    #########
    db.session.add(artist_form)
    db.session.commit()
    ########
  # TODO: modify data to be the data object returned from db insertion
  # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')
    ########
#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  #shows_query = db.session.query(Show).join(Artist).join(Venue).all()
  shows_query = db.session.query(Show, Artist, Venue).select_from(Show).join(Artist).join(Venue).all()
  print(shows_query)
  data = []
  for show in shows_query: 
    data.append({
      "venue_id": show.Venue.id,
      "venue_name": show.Venue.name,
      "artist_id": show.Artist.id,
      "artist_name": show.Artist.name, 
      "artist_image_link": show.Artist.image_link,
      #"start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
    })
  return render_template('pages/shows.html', shows=data)

def format_datetime(value, format='medium'):
    # instead of just date = dateutil.parser.parse(value)
    if isinstance(value, str):
        date = dateutil.parser.parse(value)
    else:
        date = value
@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
       form = ShowForm()
       return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
    #id_show32
     id= request.form.get('id')
     print(id)
     Artists_id= request.form.get('artist_id')
     Venue_id= request.form.get('venue_id')
     start_time= request.form.get('start_time')
    ###
     show_form = Show(id=id,start_time=start_time) 
    #########
     db.session.add(show_form)
     count = Show.query.count()
     Artists_show_id = Artist.query.filter_by(id=Artists_id).first()
     show_show_id = Show.query.filter_by(id=Artists_id).first()
     print(Artists_show_id)
     Artists_show_id.show_id = count
     db.session.commit()    

     ###
     Venue_show_id = Venue.query.filter_by(id=Venue_id).first()
     Venue_show_id.show_id =count
     print(Venue_show_id)
     db.session.commit()    


     db.session.commit()    
  # on successful db insert, flash success
     flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
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
