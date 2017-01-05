import unittest
import datetime
import time

import ipa_db
import ipa_config

class TestDb(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.db = ipa_db.Db(ipa_config.db['test'])

    def setUp(self):
        self.db.remove_schema()
        self.db.create_schema()

    def test_adding_trains(self):
        name = ['train', 'other train']

        self.assertEqual(list(self.db.get_train_id(name[0])), [])
        self.assertEqual(list(self.db.get_train_id(name[1])), [])

        self.db.add_train(name[0])
        self.db.add_train(name[1])
        self.db.commit()

        self.assertEqual(list(self.db.get_train_id(name[0])), [{'train_name': name[0], 'train_id': 1}])
        self.assertEqual(list(self.db.get_train_id(name[1])), [{'train_name': name[1], 'train_id': 2}])

    def test_train_name_uniqueness(self):
        name = 'train'
        self.db.add_train(name)
        with self.assertRaises(ipa_db.DbError):
            self.db.add_train(name)
        self.db.commit()
        self.assertEqual(list(self.db.get_train_id(name)), [{'train_name': name, 'train_id': 1}])

    def test_adding_stations(self):
        name = ['station', 'other station']

        self.assertEqual(list(self.db.get_station_id(name[0])), [])
        self.assertEqual(list(self.db.get_station_id(name[1])), [])

        self.db.add_station(name[0])
        self.db.add_station(name[1])
        self.db.commit()

        self.assertEqual(list(self.db.get_station_id(name[0])), [{'station_id': 1}])
        self.assertEqual(list(self.db.get_station_id(name[1])), [{'station_id': 2}])

    def test_station_name_uniqueness(self):
        name = 'station'
        self.db.add_station(name)
        with self.assertRaises(ipa_db.DbError):
            self.db.add_station(name)
        self.db.commit()
        self.assertEqual(list(self.db.get_station_id(name)), [{'station_id': 1}])

    def test_updating_schedules(self):
        schedule_id = 123
        schedule_date = datetime.date(2010, 12, 21)
        train_id = 1
        train_name = "train name"
        expected_schedule = {'schedule_id': schedule_id, 'schedule_date': schedule_date}

        self.assertEqual(list(self.db.get_schedules(train_id)), [])

        self.db.add_train(train_name)
        self.db.update_schedule(schedule_id, str(schedule_date), train_id)
        self.db.commit()

        self.assertEqual(list(self.db.get_schedules(train_id)), [expected_schedule])

    def test_active_schedules(self):
        schedule_id = 123
        schedule_date = datetime.date(2010, 12, 21)
        train_id = 10

        self.db.update_schedule(schedule_id, str(schedule_date), train_id)
        self.db.commit()
        self.assertEqual(list(self.db.get_active_schedules()), [{'schedule_id': schedule_id}])

        self.db.set_active(schedule_id, False)
        self.db.commit()
        self.assertEqual(list(self.db.get_active_schedules()), [])

        self.db.set_active(schedule_id, True)
        self.db.commit()
        self.assertEqual(list(self.db.get_active_schedules()), [{'schedule_id': schedule_id}])

    def test_updating_schedule_infos(self):
        schedule_id = 222

        info = [
            {'arrival_time': None, 'arrival_delay': None,
             'departure_time': '2016-12-21 12:01:30', 'departure_delay': 3},
            {'arrival_time': '2016-12-21 12:05:00', 'arrival_delay': -10,
             'departure_time': '2016-12-21 12:08:00', 'departure_delay': 0},
            {'arrival_time': '2016-12-21 12:10:10', 'arrival_delay': 0,
             'departure_time': None, 'departure_delay': None},
        ]

        self.assertEqual(list(self.db.get_schedule_infos(schedule_id)), [])

        self.db.add_station('station 1')
        self.db.add_station('station 2')
        self.db.add_station('station 3')

        self.db.update_schedule_info(schedule_id, 0, 1, info[0])
        self.db.update_schedule_info(schedule_id, 2, 3, info[2])
        self.db.update_schedule_info(schedule_id, 1, 2, info[1])
        self.db.commit()

        self.assertEqual(list(self.db.get_schedule_infos(schedule_id)),
                         [{'arrival_delay': None,
                           'arrival_time': None,
                           'departure_delay': 3,
                           'departure_time': datetime.datetime(2016, 12, 21, 12, 1, 30),
                           'station_name': 'station 1'},
                          {'arrival_delay': -10,
                           'arrival_time': datetime.datetime(2016, 12, 21, 12, 5, 0),
                           'departure_delay': 0,
                           'departure_time': datetime.datetime(2016, 12, 21, 12, 8, 0),
                           'station_name': 'station 2'},
                          {'arrival_delay': 0,
                           'arrival_time': datetime.datetime(2016, 12, 21, 12, 10, 10),
                           'departure_delay': None,
                           'departure_time': None,
                           'station_name': 'station 3'}])


if __name__ == '__main__':
    unittest.main()
