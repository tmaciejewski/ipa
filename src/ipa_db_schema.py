class Train:
    drop = 'DROP TABLE IF EXISTS train'
    create = '''CREATE TABLE train(
        train_id INTEGER NOT NULL AUTO_INCREMENT,
        train_name VARCHAR(100) UNIQUE,
        PRIMARY KEY(train_id)
    ) CHARACTER SET utf8'''

class Schedule:
    drop = 'DROP TABLE IF EXISTS schedule'
    create = '''CREATE TABLE schedule(
        schedule_id INTEGER NOT NULL,
        schedule_date DATE NOT NULL,
        train_id INTEGER NOT NULL,
        active INTEGER NOT NULL,
        PRIMARY KEY(schedule_id)
    ) CHARACTER SET utf8'''

class Station:
    drop = 'DROP TABLE IF EXISTS station'
    create = '''CREATE TABLE station(
        station_id INTEGER NOT NULL AUTO_INCREMENT,
        station_name VARCHAR(100) UNIQUE,
        PRIMARY KEY (station_id)
    ) CHARACTER SET utf8'''

class ScheduleInfo:
    drop = 'DROP TABLE IF EXISTS schedule_info'
    create = '''CREATE TABLE schedule_info(
        schedule_id INTEGER NOT NULL,
        stop_number INTEGER NOT NULL,
        station_id INTEGER NOT NULL,
        arrival_time DATETIME DEFAULT NULL,
        arrival_delay INTEGER DEFAULT NULL,
        departure_time DATETIME DEFAULT NULL,
        departure_delay INTEGER DEFAULT NULL,
        PRIMARY KEY(schedule_id, stop_number)
    ) CHARACTER SET utf8'''

tables = [Train, Schedule, Station, ScheduleInfo]

