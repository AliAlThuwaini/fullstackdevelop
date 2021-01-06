from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Ali
from flask_migrate import Migrate # Enable db migration




#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
db = SQLAlchemy(app)
# Migration
migrate = Migrate(app, db)




#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
  __tablename__ = 'venues'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  address = db.Column(db.String)
  phone = db.Column(db.String(120))
  image_link = db.Column(db.String)
  facebook_link = db.Column(db.String)
  #Ali: adding the missing columns
  website = db.Column(db.String)
  seeking_talent = db.Column(db.Boolean)
  seeking_description = db.Column(db.String)
  genres = db.Column(db.ARRAY(db.String))

  #setting up the relationship:
  #lazy changed to dynamic to git red of the following error: AttributeError: 'InstrumentedList' object has no attribute 'filter' when applying: upcoming_shows = venue.show.filter(Show.start_time > curr_time).all() in venue controller
  show = db.relationship('Show', backref= 'venue', lazy='dynamic')

  # define dunder repr method to help in db troubleshooting
  def __repr__(self):
    return f'<Venue_id: {self.id}, Vendue_name: {self.name}>'


class Artist(db.Model):
  __tablename__ = 'artists'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres = db.Column(db.ARRAY(db.String))
  image_link = db.Column(db.String, nullable=False)
  facebook_link = db.Column(db.String)
  #Ali: adding the missing columns
  website = db.Column(db.String)
  seeking_venue = db.Column(db.Boolean)
  seeking_description = db.Column(db.String)

  #setting up the relationship:
  show = db.relationship('Show', backref= 'artist', lazy=True)

  # define dunder repr method to help in db troubleshooting
  def __repr__(self):
    return f'<Artist_id: {self.id}, Artist_name: {self.name}>'


class Show(db.Model):
  __tablename__ = 'shows'
  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

  # reltionships:
  venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)

  # define dunder repr method to help in db troubleshooting
  def __repr__(self):
    return f'<Show_id: {self.id}, Venue_id: {self.venue_id}, Artist_id: {self.artist_id}>'
