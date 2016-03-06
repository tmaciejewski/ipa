import sqlite3

class Db:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)

    def __del__(self):
        self.conn.close()

    def _execute(self, sql, args = tuple()):
        c = self.conn.cursor()
        c.execute(sql, args)
        return c

    def _commit(self):
        self.conn.commit()

    def _format_select(self, cursor):
        names = [desc[0] for desc in cursor.description]
        for row in cursor:
            yield dict(zip(names, row))

    def remove(self):
        self._execute('DROP TABLE IF EXISTS trains')
        self._execute('DROP TABLE IF EXISTS schedule')
        self._commit()

    def create(self):
        self._execute('''CREATE TABLE trains(
            train_id integer PRIMARY KEY,
            train_number integer,
            train_name text,
            train_operator text,
            train_date text,
            train_relation text
        )''')

        self._execute('''CREATE INDEX trains_train_number_idx
                         ON trains (train_number)''')

        self._execute('''CREATE TABLE schedule(
            train_id integer,
            stop_id integer,
            stop_name text,
            sched_arrive_time text,
            sched_arrive_delay text,
            sched_departure_time text,
            sched_departure_delay text,
            PRIMARY KEY(train_id, stop_id)
        )''')
        self._commit()

    def get_trains(self):
        return self._format_select(self._execute('SELECT * FROM trains GROUP BY train_number ORDER BY train_number'))

    def update_train(self, id, number, name, operator, date, relation):
        self._execute('DELETE FROM trains WHERE train_id = ?', (id,))

        self._execute('''INSERT INTO trains VALUES (
            ?, ?, ?, ?, ?, ?)''',
            (id, number, name, operator, date, relation)
        )

        self._commit()

    def update_schedule(self, id, schedule):
        self._execute('DELETE FROM schedule WHERE train_id = ?', (id,))

        stop_id = 1
        for stop in schedule:
            self._execute('''INSERT INTO schedule VALUES (
                ?, ?, ?, ?, ?, ?, ?)''',
                (id, stop_id, stop[0], stop[1], stop[2], stop[3], stop[4])
            )
            stop_id += 1

        self._commit()

    def get_train_schedules(self, number):
        return self._format_select(self._execute('SELECT * FROM trains WHERE train_number = ? ORDER BY train_date', (number,)))

    def get_schedule_info(self, id):
        return self._format_select(self._execute('SELECT * FROM schedule WHERE train_id = ? ORDER BY stop_id', (id,)))
