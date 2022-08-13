# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import logging
from itertools import groupby
from logging import Formatter, FileHandler

import babel
import dateutil.parser
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from forms import *

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String)
    shows = db.relationship('Show', backref='venue')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String)
    shows = db.relationship('Show', backref='artist')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    venues_query = Venue.query.all()
    # grouped array
    venues_grouped = []

    # sort venues
    sorted_venues = sorted(venues_query, key=lambda a: (a.city, a.state))
    # group by city & state
    grouped = [list(result) for key, result in groupby(sorted_venues, key=lambda a: (a.city, a.state))]
    # create final object
    for group in grouped:
        venues_group = []
        upcoming = 0

        for venue in group:
            # determine upcoming shows
            for show in venue.shows:
                # if start time greater than now
                if show.start_time > datetime.today():
                    # increase upcoming by 1
                    upcoming += 1
            # create venue object
            data = {'id': venue.id, 'name': venue.name, 'num_upcoming_shows': upcoming}
            # append to final object
            venues_group.append(data)
        # append new venue
        venues_grouped.append({'city': group[0].city, 'state': group[0].state, 'venues': venues_group})

    return render_template('pages/venues.html', areas=venues_grouped);


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    response = {
        "count": 1,
        "data": [{
            "id": 2,
            "name": "The Dueling Pianos Bar",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # retrieve venue
    venue = Venue.query.get(venue_id)
    past_shows = []
    upcoming_shows = []
    # get venue shows
    venue_shows = venue.shows

    # iterate through venue shows
    for show in venue_shows:
        # set past show if start_time is past
        if show.start_time < datetime.today():
            past_shows.append({'artist_id': show.artist_id, 'artist_name': show.artist.name,
                               'artist_image_link': show.artist.image_link, 'start_time': str(show.start_time)})
        # set upcoming show if start_time future
        else:
            upcoming_shows.append({'artist_id': show.artist_id, 'artist_name': show.artist.name,
                                   'artist_image_link': show.artist.image_link, 'start_time': str(show.start_time)})
    data = {
        'id': venue.id,
        'name': venue.name,
        'genres': venue.genres,
        'address': venue.address,
        'city': venue.city,
        'state': venue.state,
        'phone': venue.phone,
        'website': venue.website_link,
        'facebook_link': venue.facebook_link,
        'seeking_talent': venue.seeking_talent,
        'seeking_description': venue.seeking_description,
        'image_link': venue.image_link,
        'past_shows': past_shows,
        'upcoming_shows': upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

# GET Venue Form
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


# POST Venue Form Data
@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False
    form = VenueForm(request.form)

    try:
        venue = Venue(name=form.name.data, city=form.city.data, state=form.state.data, address=form.address.data,
                      phone=form.phone.data,
                      genres=form.genres.data, image_link=form.image_link.data, facebook_link=form.facebook_link.data,
                      website_link=form.website_link.data, seeking_talent=form.seeking_talent.data,
                      seeking_description=form.seeking_description.data)

        db.session.add(venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if not error:
        flash('Venue ' + form.name.data + ' was successfully listed!')
    else:
        flash('An error occurred. Venue' + form.name.data + 'could not be listed.')

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
    # query all artists
    artists = Artist.query.with_entities(Artist.id, Artist.name).all()

    return render_template('pages/artists.html', artists=artists)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    response = {
        "count": 1,
        "data": [{
            "id": 4,
            "name": "Guns N Petals",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    artist = Artist.query.get(artist_id)
    shows = artist.shows
    upcoming_shows = []
    past_shows = []

    # sort shows by date
    for show in shows:
        if show.start_time < datetime.today():
            past_shows.append(
                {'venue_id': show.venue_id, 'venue_name': show.venue.name, 'venue_image_link': show.venue.image_link,
                 'start_time': str(show.start_time)})
        else:
            upcoming_shows.append(
                {'venue_id': show.venue_id, 'venue_name': show.venue.name, 'venue_image_link': show.venue.image_link,
                 'start_time': str(show.start_time)})

    data = {
        'id': artist.id,
        'name': artist.name,
        'genres': artist.genres,
        'city': artist.city,
        'state': artist.state,
        'phone': artist.phone,
        'website': artist.website_link,
        'facebook_link': artist.facebook_link,
        'seeking_venue': artist.seeking_venue,
        'seeking_description': artist.seeking_description,
        'image_link': artist.image_link,
        'past_shows': past_shows,
        'upcoming_shows': upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    # Get artist
    artist = Artist.query.get(artist_id)
    # Populate form fields
    form = ArtistForm(obj=artist)

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # artist record with ID <artist_id> using the new attributes
    form = ArtistForm(request.form)
    artist = Artist.query.get(artist_id)
    error = False
    try:
        # set update fields
        artist.name = form.name.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.genres = form.genres.data
        artist.image_link = form.image_link.data
        artist.facebook_link = form.facebook_link.data
        artist.website_link = form.website_link.data
        artist.seeking_venue = form.seeking_venue.data
        artist.seeking_description = form.seeking_description.data

        # commit updates
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    # Retrieve venue object
    venue = Venue.query.get(venue_id)
    # populate form
    form = VenueForm(obj=venue)

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # venue record with ID <venue_id> using the new attributes
    form = VenueForm(request.form)
    venue = Venue.query.get(venue_id)
    error = False
    try:
        # Update fields
        venue.name = form.name.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.address = form.address.data
        venue.phone = form.phone.data
        venue.image_link = form.image_link.data
        venue.facebook_link = form.facebook_link.data
        venue.genres = form.genres.data
        venue.website_link = form.website_link.data
        venue.seeking_description = form.seeking_description.data
        venue.seeking_talent = form.seeking_talent.data

        # Commit update
        db.session.commit()
    except:
        error = False
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
    form = ArtistForm(request.form)
    error = False
    try:
        artist = Artist(name=form.name.data, city=form.city.data, state=form.state.data, phone=form.phone.data,
                        genres=form.genres.data, image_link=form.image_link.data, facebook_link=form.facebook_link.data,
                        website_link=form.website_link.data, seeking_venue=form.seeking_venue.data,
                        seeking_description=form.seeking_description.data)
        db.session.add(artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if not error:
        flash('Artist ' + form.name.data + ' was successfully listed!')
    else:
        flash('An error occured. Artist ' + form.name.data + ' could not be listed')

    # on successful db insert, flash success
    # flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # retrieve shows
    shows = Show.query.all()
    data = []

    for show in shows:
        data.append({'venue_id': show.venue_id, 'venue_name': show.venue.name, 'artist_id': show.artist_id,
                     'artist_name': show.artist.name, 'artist_image_link': show.artist.image_link,
                     'start_time': str(show.start_time)})

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    form = ShowForm(request.form)
    error = False
    try:
        # set form data
        show = Show(start_time=form.start_time.data, artist_id=form.artist_id.data, venue_id=form.venue_id.data)
        # add model to session
        db.session.add(show)
        # add data to database
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if not error:
        flash('Show was successfully listed!')
    else:
        flash('An error occurred. Show could not be listed.')

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

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
