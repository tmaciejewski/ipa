#!/usr/bin/env python

import ipa_db
import ipa_config
import station
import sys

def create_db(db):
    """creates new DB"""
    db.remove()
    db.create()

def print_trains(db):
    """prints all trains from DB"""
    for train in db.get_trains():
        print train

def visit_stations(db):
    """visits stations and saves trains"""
    trains = {}

    for station_id, station_name in ipa_config.stations:
        print 'Visiting station', station_name
        arrivals, departures = station.get_station(station_id)
        for train in arrivals:
            trains[train[0]] = train

    for train_id in trains:
        try:
            db.add_train(train_id,
                         trains[train_id][1],
                         trains[train_id][2],
                         trains[train_id][3],
                         trains[train_id][5])
            print 'Added train', train_id
        except:
            print 'Failed to add train', train_id

if __name__ == "__main__":
    commands = [create_db, print_trains, visit_stations]
    command = None

    if len(sys.argv) > 1:
        for c in commands:
            if c.__name__ == sys.argv[1]:
                command = c
                break

    if command:
        db = ipa_db.Db(ipa_config.db_name)
        command(db)
    else:
        for c in commands:
            print '\t', c.__name__, '--', c.__doc__
