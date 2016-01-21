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
        self.__commit()

    def create(self):
        self.__execute('''CREATE TABLE trains(
            train_id integer PRIMARY KEY,
            train_number text,
            train_operator text,
            train_date text,
            train_relation text
        )''')
        self.__commit()

    def get_trains(self):
        for row in self.__execute('SELECT * FROM trains'):
            yield row

    def add_train(self, id, number, operator, date, relation):
        self.__execute('''INSERT INTO trains VALUES (
            ?, ?, ?, ?, ?
        )''', (id, number, operator, date, relation))
        self.__commit()
