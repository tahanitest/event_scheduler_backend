from app import app, db
from flask import request, jsonify
from app.models import Event


# set index route to return nothing, just so no error
@app.route('/')
def index():
    return ''


@app.route('/api/save', methods=['GET', 'POST'])
def save():
    try:
        # get headers first
        day = int(request.headers.get('day'))
        month = int(request.headers.get('month'))
        year = int(request.headers.get('year'))
        title = request.headers.get('title')
        notes = request.headers.get('notes')

        if not day and not month and not year and not title and not notes:
            return jsonify({ 'error #301': 'Invalid params' })

        if not isinstance(day, int) and not isinstance(month, int) and not isinstance(year, int):
            return jsonify({ 'error #302': 'Dates need to be whole numbers' })

        # create an event
        event = Event(day=day, month=month, year=year, title=title, notes=notes)

        # add to stage and commit to db
        db.session.add(event)
        db.session.commit()

        return jsonify({ 'success': 'event created' })
    except:
        return jsonify({ 'error #303': 'something went wrong' })


@app.route('/api/retrieve', methods=['GET', 'POST'])
def retrieve():
    try:
        day = request.headers.get('day')
        month = request.headers.get('month')
        year = request.headers.get('year')

        if day and month and year:
            results = Event.query.filter_by(day=day, month=month, year=year).all()
        elif not day and month and year:
            results = Event.query.filter_by(month=month, year=year).all()
        elif not day and not month and year:
            results = Event.query.filter_by(year=year).all()
        else:
            return jsonify({ 'error#304': 'Required params not included' })

        if not results:
            return jsonify({ 'success': 'No events scheduled with those dates.' })

        # remember that results is a list of db.Model objects
        parties = []

        for event in results:
            party = {
                'id': event.id,
                'title': event.title,
                'day': event.day,
                'month': event.month,
                'year': event.year,
                'notes': event.notes
            }

            parties.append(party)

        return jsonify(parties)

    except:
        return jsonify({ 'error#305': 'something went wrong' })


@app.route('/api/delete', methods=['GET', 'POST'])
def delete():
    try:
        event_id = request.headers.get('event_id')

        event = Event.query.filter_by(id=event_id).first()

        if not event:
            return jsonify({ 'error#306': 'Event does not exist.'})

        db.session.delete(event)
        db.session.commit()

        return jsonify({ 'success': f'Event {event_id} deleted.'})

    except:
        return jsonify({ 'error#307': 'Could not delete event.' })
