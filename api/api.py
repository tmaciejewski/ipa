import flask
import ipa_db
import ipa_config

import json
import datetime

class DateTimeEncoder(flask.json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        if isinstance(o, datetime.date):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)

app = flask.Flask(__name__)
app.json_encoder = DateTimeEncoder
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

@app.route('/trains')
def all_trains():
    db = ipa_db.Db(ipa_config.db['dev'])
    trains = []
    for train in db.get_trains():
        trains.append({
            'train_name': train['train_name'],
            'stations': train['stations'].split(',')
            })
    return flask.jsonify(trains = trains)

@app.route('/trains/<path:train_name>')
def train(train_name):
    db = ipa_db.Db(ipa_config.db['dev'])
    try:
        train = next(db.get_train_id(train_name))
        train['schedules'] = list(db.get_schedules(train['train_id']))
        for schedule in train['schedules']:
            schedule['info'] = list(db.get_schedule_infos(schedule['schedule_id']))

        return flask.jsonify(**train)
    except StopIteration:
        return 'No train'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
