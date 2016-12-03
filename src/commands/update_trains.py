import datetime

def log(msg, *args):
    timestamp = datetime.datetime.now().ctime()
    print timestamp, msg % args

class UpdateTrains:
    name = 'update_trains'
    desc = 'updated trains in DB based on preconfigured set of stations'
    args = []

    def run(self, db, _):
        active_scheduled_ids = {schedule['schedule_id'] for schedule in db.get_active_schedules()} 
        schedule_ids = active_scheduled_ids | self.get_schedule_ids_from_stations()

        for schedule_id in schedule_ids:
            try:
                self.update_train_schedule(db, schedule_id)
            except Exception as e:
                log('Failed to update train schedule %s: %s', schedule_id, e.message)

        db.commit()

    def get_schedule_ids_from_stations(self):
        schedule_ids = set()

        for station_name in ipa_config.stations:
            station_id = ipa_config.stations[station_name]
            arrivals = []
            try:
                arrivals, _ = station.get_station(station_id)
                log('Visitied station %s', station_name)
            except:
                log('Cannot get trains from station %s', station_name)

            for train in arrivals:
                schedule_ids.add(train['id'])

        return schedule_ids

    def update_train_schedule(self, db, schedule_id):
        schedule_info = train.get_train(schedule_id)

        if schedule_info != []:
            train_name = schedule_info[0]['name']
            schedule_date = schedule_info[0]['date']
            train_id = self.get_train_id(db, train_name)

            db.update_schedule(schedule_id, schedule_date, train_id)
            for i in range(len(schedule_info)):
                self.update_train_schedule_info(db, schedule_id, i, schedule_info[i])

            log('Updated train schedule %s %s', schedule_id, train_name)
        else:
            db.mark_as_inactive(schedule_id)
            log('Mark %s as inactive train', schedule_id)

    def get_train_id(self, db, train_name):
        result = list(db.get_train_id(train_name))
        if result == []:
            db.add_train(train_name)
            result = list(db.get_train_id(train_name))
        return result[0]['train_id']

    def update_train_schedule_info(self, db, schedule_id, stop_number, schedule_info):
        station_id = self.get_station_id(db, schedule_info['stop_name'])

        if schedule_info['arrival_delay'] != '':
            arrival_delay = schedule_info['arrival_delay']
        else:
            arrival_delay = None

        if schedule_info['arrival_time'] != '':
            arrival_time = schedule_info['date'] + ' ' + schedule_info['arrival_time']
        else:
            arrival_time = None

        if schedule_info['departure_delay'] != '':
            departure_delay = schedule_info['departure_delay']
        else:
            departure_delay = None

        if schedule_info['departure_time'] != '':
            departure_time = schedule_info['date'] + ' ' + schedule_info['departure_time']
        else:
            departure_time = None

        db.update_schedule_info(schedule_id, stop_number, station_id, {
            'arrival_delay': arrival_delay,
            'arrival_time': arrival_time,
            'departure_delay': departure_delay,
            'departure_time': departure_time
        })

    def get_station_id(self, db, station_name):
        result = list(db.get_station_id(station_name))
        if result == []:
            db.add_station(station_name)
            result = list(db.get_station_id(station_name))
        return result[0]['station_id']
