#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import render_template, request, flash, redirect, url_for
import logging
from logging import DEBUG, Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys

#Ali:
from models import *



moment = Moment(app)
app.config.from_object('config')


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

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

  venues = Venue.query.group_by(Venue.id, Venue.state, Venue.city).all()
  curr_time = datetime.now()
  venueStateCity = ''
  data = []

  # loop through all venues in db
  for venue in venues:
    #set upconing shows
    upcoming_shows = venue.show.filter(Show.start_time > curr_time).all()
    #check if curr record has same state & city, add it to that group
    if venueStateCity == venue.city + venue.state:
      data[len(data) - 1]["venues"].append({
        "id": venue.id,
        "name":venue.name,
        "num_upcoming_shows": len(upcoming_shows) # a count of the number of shows
      })
    # if not having same Sate/City, create new group and add append to it.
    else:
      venueStateCity = venue.city + venue.state
      data.append({
        "city":venue.city,
        "state":venue.state,
        "venues": [{
          "id": venue.id,
          "name":venue.name,
          "num_upcoming_shows": len(upcoming_shows)
        }]
      })
  return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
 
  searchedVenue=request.form.get('search_term', '')
  curr_time = datetime.utcnow()
  num_upcoming_shows= 0
  #query db for venue.name containing that serach word
  venues = Venue.query.filter(Venue.name.ilike(f'%{searchedVenue}%')).all()
  #setup response skiliton
  response={
  "count": len(venues),
  "data":[]
  }
  for venue in venues:
      num_upcoming_shows = 0
      matchedShows = Show.query.filter_by(venue_id=venue.id).all()
      #Check how many upcoming shows for that venue
      for show in matchedShows:
          if show.start_time > curr_time:
              num_upcoming_shows += 1
      # register response
      response['data'].append({
          "id": venue.id,
          "name": venue.name,
          "num_upcoming_shows": num_upcoming_shows
  })
  # print(response)  #Check point
  return render_template('pages/search_venues.html', results=response, search_term=searchedVenue)



@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  # Prepare required variables
  venue = Venue.query.get(venue_id)
  shows = Show.query.filter_by(venue_id=venue_id).all()
  curr_time = datetime.utcnow()
  past_shows = []
  upcoming_shows = []

  # iterate through available shows in the db for that venue
  for show in shows:
    data = {
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": format_datetime(str(show.start_time))
        }
    if show.start_time > curr_time:
        upcoming_shows.append(data)
    else:
        past_shows.append(data)

  # forming data response
  data={
  "id": venue.id,
  "name": venue.name,
  "genres": venue.genres,
  "address": venue.address,
  "city": venue.city,
  "state": venue.state,
  "phone": venue.phone,
  "website": venue.website,
  "facebook_link": venue.facebook_link,
  "seeking_talent": venue.seeking_talent,
  "seeking_description":venue.seeking_description,
  "image_link": venue.image_link,
  "past_shows": past_shows,
  "upcoming_shows": upcoming_shows,
  "past_shows_count": len(past_shows),
  "upcoming_shows_count": len(upcoming_shows)
  }

  # print (data)  #Check point

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # Creat Venue instance from form input
  form = VenueForm()
  try:
    venue = Venue(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        address=form.address.data,
        phone=form.phone.data,
        genres=form.genres.data,
        facebook_link=form.facebook_link.data,
        website=form.website.data,
        image_link=form.image_link.data,
        seeking_talent=form.seeking_talent.data,
        seeking_description=form.seeking_description.data,
    )
    #push it to db
    db.session.add(venue)
    db.session.commit()

    # on successful db insert, flash success
    flash('Venue ' + venue.name + ' was successfully listed!')

  # In case creation did not go well:
  except Exception as e:
    print(f'Error ==> {e}')
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    db.session.rollback()
  #close db connection
  finally:
    db.session.close()

  return render_template('pages/home.html')
  
# Deletion of venue
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  #return None

  # Below is the related code to delete. If time allows, will implement a button to execute it.

  # Get the venue by id from form
  try:
    venue = Venue.query.get(venue_id)
    #delete venue from db
    db.session.delete(venue)
    db.session.commit()
    # flash message of successful deletion
    flash(f'Venue {venue_id} was successfully deleted.')
  # In case deletion failed:
  except Exception as e:
    db.session.rollback()
    print(sys.exc_info())
    print(f'Error ==> {e}')
    flash(f'An error occurred. Venue {venue_id} named {venue.name}could not be deleted.')
  finally:
    db.session.close()

  return render_template('pages/home.html')



@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  
  if venue: 
    form.name.data = venue.name
    form.city.data = venue.city
    form.state.data = venue.state
    form.phone.data = venue.phone
    form.address.data = venue.address
    form.genres.data = venue.genres
    form.facebook_link.data = venue.facebook_link
    form.image_link.data = venue.image_link
    form.website.data = venue.website
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description

  return render_template('forms/edit_venue.html', form=form, venue=venue)

  
@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  venue = Venue.query.get(venue_id)
  try: 
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.genres = request.form.getlist('genres')
    venue.image_link = request.form['image_link']
    venue.facebook_link = request.form['facebook_link']
    venue.website = request.form['website']
    venue.seeking_talent = True if 'seeking_talent' in request.form else False 
    venue.seeking_description = request.form['seeking_description']

    db.session.commit()

    flash(f'Venue was successfully updated!')
  except Exception as e: 
    print (f'Error => {e}')
    db.session.rollback()
    print(sys.exc_info())

    flash(f'An error occurred. Venue could not be changed.')
  finally: 
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

    


#  Artists
#  ----------------------------------------------------------------

@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  # Get all artist data from artists table through Artist model.
  data = db.session.query(Artist).all()

  return render_template('pages/artists.html', artists=data)



@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  
  searchedArtist = request.form.get('search_term', '')
  #query db for artist.name containing that serach word
  artists = Artist.query.filter(Artist.name.ilike(f'%{searchedArtist}%')).all()
  # print (artists)   #check point
  data = []
  for artist in artists:
      data.append({
          "id": artist.id,
          "name": artist.name,
          "num_upcoming_shows": len(db.session.query(Show).filter(Show.artist_id == artist.id).filter(Show.start_time > datetime.now()).all()),
      })
      #print ('artist', artist)   # check point
  response={
  "count": len(artists),
  "data": data
  }
  #print ('response: ', response)  #check point

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  #get artist dtails from db by id coming from the search form
  artist = Artist.query.get(artist_id)
  #get all shows of this artist
  shows = Show.query.filter_by(artist_id=artist_id).all()
  # time comparison with shows on db
  curr_time = datetime.now()
  upcoming_shows = []
  past_shows = []

  # loop over shows to get their required details
  for show in shows:
    data = {
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "venue_image_link": show.venue.image_link,
      "start_time": format_datetime(str(show.start_time))
    }
    #decide past and upcoming shows
    if show.start_time > curr_time:
      upcoming_shows.append(data)
    else:
      past_shows.append(data)
  #Create dataset that is fed to the website page
  data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "facebook_link": artist.facebook_link,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }

  return render_template('pages/show_artist.html', artist=data)


# #  Update
# #  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

  form = ArtistForm()

  #query artist details (from artist to be edited from the form)
  artist = Artist.query.get(artist_id)

  # TODO: populate form with fields from artist with ID <artist_id>
  
  # put the queried data in a template suitable for the form to render
  if artist: 
    form.name.data = artist.name
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.genres.data = artist.genres
    form.facebook_link.data = artist.facebook_link
    form.image_link.data = artist.image_link
    form.website.data = artist.website
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description

  return render_template('forms/edit_artist.html', form=form, artist=artist)




@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  # put the necessary checks to make sure fields are not empty:

  # get artist details
  artist = Artist.query.get(artist_id)

  try: 
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.genres = request.form.getlist('genres')
    artist.image_link = request.form['image_link']
    artist.facebook_link = request.form['facebook_link']
    artist.website = request.form['website']
    artist.seeking_venue = True if 'seeking_venue' in request.form else False 
    artist.seeking_description = request.form['seeking_description']   
       
    db.session.commit()
    # Flash success message
    flash(f'Artist was successfully updated!')

  # In case of issues:
  except Exception as e:
    db.session.rollback()
    # flash error messages
    print (f'Error => {e}')
    print(sys.exc_info())
    
  # Close db connection
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))



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

  # # on successful db insert, flash success
  # flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # # TODO: on unsuccessful db insert, flash an error instead.
  # # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  # return render_template('pages/home.html')

  try:
    form = ArtistForm()
    #form artist dataset
    artist = Artist(name=form.name.data, city=form.city.data, state=form.state.data, phone=form.phone.data, genres=form.genres.data, image_link=form.image_link.data, facebook_link=form.facebook_link.data)
    
    #push to db
    db.session.add(artist)
    db.session.commit()
    #flash success message
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except Exception as e:
    print(f'Error ==> {e}')
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  q_shows = db.session.query(Show).join(Artist).join(Venue).all()

  data = []
  for show in q_shows: 
    data.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.artist.name, 
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S') 
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  #flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  #return render_template('pages/home.html')

  try: 
    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']

    #create the show
    show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
    # push show to db
    db.session.add(show)
    db.session.commit()
    #flash success message
    flash('Show was successfully listed')
  except Exception as e: 
    print(f'Error => {e}')
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Show could not be listed.')
  finally: 
    db.session.close()
    
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
    app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':u
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
