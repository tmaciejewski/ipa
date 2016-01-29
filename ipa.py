#!/usr/bin/env python

import ipa_db
import ipa_config
import station
import train
import sys

def create_db(db, _):
    """creates new DB"""
    db.remove()
    db.create()

def print_trains(db, _):
    """prints all trains from DB"""
    for train in db.get_trains():
        print train.encode('utf-8')

def get_trains_from_stations():
    trains = {}

    for station_id, station_name in ipa_config.stations:
        try:
            arrivals, _ = station.get_station(station_id)
            print 'Visitied station', station_name.encode('utf-8')
        except:
            print 'Cannot get trains from station', station_name.encode('utf-8')

        for train in arrivals:
            trains[train[0]] = train

    return trains

def update_train(db, train):
    try:
        db.update_train(train[0], train[1], train[2], train[3], train[5])
        print 'Updated train', train[0], train[1].encode('utf-8')
    except Exception as e:
        print 'Failed to update train', train[0], train[1].encode('utf-8'), ':', e.message

def update_train_schedule(db, train_id):
    try:
        schedule = [(stop[3], stop[4], stop[5], stop[6], stop[7])
                        for stop in train.get_train(train_id)]
        db.update_schedule(train_id, schedule)
        print 'Updated train schedule', train_id
    except Exception as e:
        print 'Failed to update train schedule', train_id, ':', e.message

def update_trains(db, _):
    """updated trains in DB based on preconfigured set of stations"""

    trains = get_trains_from_stations()
    for train_id in trains:
        update_train(db, trains[train_id])
        update_train_schedule(db, train_id)

def print_train(db, args):
    """prints train all-time schedule"""
    for schedule in db.get_train_schedules(args[0]):
        print schedule
        print '-----------------------'
        for schedule_info in db.get_schedule_info(schedule[0]):
            print schedule_info
        print

if __name__ == "__main__":
    commands = [create_db, print_trains, update_trains, print_train]
    command = None

    if len(sys.argv) > 1:
        for c in commands:
            if c.__name__ == sys.argv[1]:
                command = c
                break

    if command:
        db = ipa_db.Db(ipa_config.db_name)
        command(db, sys.argv[2:])
    else:
        print 'Commands:'
        for c in commands:
            print '\t', c.__name__, '--', c.__doc__
