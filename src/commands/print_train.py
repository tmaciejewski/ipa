class PrintTrain:
    name = 'print_train'
    desc = 'prints train schedules'
    args = ['TRAIN_NAME']

    def run(self, db, args):
        train_id = list(db.get_train_id(args[0].decode('utf-8')))
        if train_id == []:
            print 'Train not found'
            return

        for schedule in db.get_schedules(train_id[0]['train_id']):
            print '-----------------------'
            for schedule_info in db.get_schedule_infos(schedule['schedule_id']):
                print schedule_info.values()
            print
