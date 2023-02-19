import flask
import json
import datetime

import ipa_db
import ipa_config
import cache

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

main_cache = cache.Cache(limit=1, duration=3600)
train_cache = cache.Cache(limit=1000, duration=600)

@app.route('/trains')
def all_trains():
    try:
        trains = main_cache['']
    except KeyError:
        db = ipa_db.Db(ipa_config.db['dev'])
        trains = []
        for train in db.get_trains():
            trains.append({
                'train_name': train['train_name'],
                'stations': train['stations'].split(',')
                })
        main_cache[''] = trains

    return flask.jsonify(trains = trains)

@app.route('/trains/<path:train_name>')
def train(train_name):
    try:
        train = train_cache[train_name]
    except KeyError:
        db = ipa_db.Db(ipa_config.db['dev'])
        try:
            train = next(db.get_train_id(train_name))
            train['schedules'] = list(db.get_schedules(train['train_id']))
            for schedule in train['schedules']:
                schedule['info'] = list(db.get_schedule_infos(schedule['schedule_id']))
            train_cache[train_name] = train
        except StopIteration:
            return 'No train'

    return flask.jsonify(**train)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
