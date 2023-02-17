import mysql.connector
import ipa_db_schema

class Db:
    def __init__(self, db_config):
        print('db fake __init__')

    def __del__(self):
        print('db fake __del__')

    def remove_schema(self):
        print('db fake remove_schema')

    def create_schema(self):
        print('db fake create_schema')

    def get_trains(self):
        print('db fake get_trains')
        return [{'train_name': 'train1', 'stations': 'station1,station2'}]

    def get_active_schedules(self):
        print('db fake get_trains')

    def set_active(self, schedule_id, active):
        print('db fake set_active')

    def add_train(self, train_name):
        print('db fake add_train')

    def get_train_id(self, train_name):
        print('db fake get_train_id(%s)' % train_name)
        yield {'train_id': 'some_id'}

    def add_station(self, station_name):
        print('db fake add_station')

    def get_station_id(self, station_name):
        print('db fake get_station_id')

    def update_schedule(self, schedule_id, schedule_date, train_id):
        print('db fake update_schedule')

    def get_schedules(self, train_id):
        print('db fake get_schedules(%s)' % train_id)
        return []

    def update_schedule_info(self, schedule_id, stop_number, station_id, info):
        print('db fake update_schedule_info')

    def get_schedule_infos(self, schedule_id):
        print('db fake get_schedule_infos(%s)' % schedule_id)
        return []
