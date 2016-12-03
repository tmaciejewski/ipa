class PrintTrains:
    name = 'print_trains'
    desc = 'prints all trains from DB'
    args = []

    def run(self, db, _):
        for train in db.get_trains():
            print train['train_name'].encode('utf-8')
