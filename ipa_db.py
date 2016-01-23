import sqlite3

class Db:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)

    def __del__(self):
        self.conn.close()

    def __execute(self, sql, args = tuple()):
        c = self.conn.cursor()
        c.execute(sql, args)
        return c

    def __commit(self):
        self.conn.commit()

    def remove(self):
        self.__execute('DROP TABLE IF EXISTS trains')
        self.__execute('DROP TABLE IF EXISTS schedule')
        self.__commit()

    def create(self):
        self.__execute('''CREATE TABLE trains(
            train_id integer PRIMARY KEY,
            train_number text,
            train_operator text,
            train_date text,
            train_relation text
        )''')
        self.__execute('''CREATE TABLE schedule(
            train_id integer,
            stop_id integer,
            stop_name text,
            sched_arrive_time text,
            sched_arrive_delay text,
            sched_departure_time text,
            sched_departure_delay text
        )''')
        self.__commit()

    def get_trains(self):
        for row in self.__execute('SELECT DISTINCT train_number FROM trains'):
            yield row[0]

    def update_train(self, id, number, operator, date, relation):
        self.__execute('DELETE FROM trains WHERE train_id = ?', (id,))

        self.__execute('''INSERT INTO trains VALUES (
            ?, ?, ?, ?, ?)''',
            (id, number, operator, date, relation)
        )

        self.__commit()

    def update_schedule(self, id, schedule):
        self.__execute('DELETE FROM schedule WHERE train_id = ?', (id,))

        stop_id = 1
        for stop in schedule:
            self.__execute('''INSERT INTO schedule VALUES (
                ?, ?, ?, ?, ?, ?, ?)''',
                (id, stop_id, stop[0], stop[1], stop[2], stop[3], stop[4])
            )

        self.__commit()

    def get_train_schedules(self, name):
        for row in self.__execute('SELECT train_id FROM trains WHERE train_number = ? ORDER BY train_id', (name,)):
            yield row[0]

    def get_schedule_info(self, id):
        for row in self.__execute('SELECT * FROM schedule WHERE train_id = ? ORDER BY stop_id', (id,)):
            yield row
