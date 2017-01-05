import mysql.connector
import ipa_db_schema

class DbError(Exception):
    def __init__(self, message):
        super(DbError, self).__init__(message)

class Db:
    def __init__(self, db_config):
        db_config['buffered'] = True
        self.conn = mysql.connector.connect(**db_config)

    def __del__(self):
        self.conn.close()

    def _execute(self, sql, args = tuple()):
        c = self.conn.cursor()
        try:
            c.execute(sql, args)
        except Exception as e:
            print(e)
            raise DbError(str(e))
        else:
            return c

    def _format_select(self, cursor):
        names = [desc[0] for desc in cursor.description]
        for row in cursor:
            yield dict(zip(names, row))

    def commit(self):
        self.conn.commit()

    def remove_schema(self):
        for table in ipa_db_schema.tables:
            self._execute(table.drop)

    def create_schema(self):
        for table in ipa_db_schema.tables:
            self._execute(table.create)

    def select_query(self, query, args = tuple()):
        return self._format_select(self._execute(query, args))

    def get_trains(self):
        return self.select_query('''SELECT train_name, GROUP_CONCAT(station_name ORDER BY stop_number) AS stations
                                    FROM schedule_info
                                    JOIN (SELECT train_name, MAX(schedule_id) AS last_schedule_id
                                          FROM schedule JOIN train USING (train_id) GROUP BY train_id) t
                                        ON t.last_schedule_id = schedule_info.schedule_id
                                    JOIN station USING (station_id)
                                    GROUP BY train_name ORDER BY train_name''')

    def get_active_schedules(self):
        return self.select_query('SELECT schedule_id FROM schedule WHERE active = 1')

    def set_active(self, schedule_id, active):
        active_value = 1 if active else 0
        self._execute('''UPDATE schedule SET active = %s WHERE schedule_id = %s''', (active_value, schedule_id))

    def add_train(self, train_name):
        self._execute('''INSERT INTO train VALUES('', %s)''', (train_name,))

    def get_train_id(self, train_name):
        return self.select_query('SELECT train_id, train_name FROM train WHERE train_name = %s', (train_name,))

    def add_station(self, station_name):
        self._execute('''INSERT INTO station VALUES('', %s)''', (station_name,))

    def get_station_id(self, station_name):
        return self.select_query('SELECT station_id FROM station WHERE station_name = %s', (station_name,))

    def update_schedule(self, schedule_id, schedule_date, train_id):
        self._execute('''REPLACE INTO schedule VALUES(%s, %s, %s, 1)''', (schedule_id, schedule_date, train_id))

    def get_schedules(self, train_id):
        return self.select_query('''SELECT schedule_id, schedule_date FROM schedule INNER JOIN train USING (train_id)
                                    WHERE schedule.train_id = %s ORDER BY schedule_date''', (train_id,))

    def update_schedule_info(self, schedule_id, stop_number, station_id, info):
        self._execute('''REPLACE INTO schedule_info VALUES
                         (%s, %s, %s, %s, %s, %s, %s)''',
                         (schedule_id, stop_number, station_id,
                          info['arrival_time'], info['arrival_delay'],
                          info['departure_time'], info['departure_delay']))

    def get_schedule_infos(self, schedule_id):
        return self.select_query('''SELECT station_name, departure_time, departure_delay, arrival_time, arrival_delay
                                    FROM schedule_info INNER JOIN station USING (station_id)
                                    WHERE schedule_id = %s ORDER BY stop_number''', (schedule_id,))
