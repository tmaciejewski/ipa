class PrintTrain:
    name = 'print_train'
    desc = 'prints train schedules'
    args = ['TRAIN_NAME']

    def run(self, db, args):
        train_id = list(db.get_train_id(args[0]))
        if train_id == []:
            print('Train not found')
            return

        for schedule in db.get_schedules(train_id[0]['train_id']):
            print('-' * 100)
            print(schedule['schedule_date'])
            print('-' * 100)

            for schedule_info in db.get_schedule_infos(schedule['schedule_id']):
                print('%30s | %20s | %5s min | %20s | %5s min' \
                        % (schedule_info['station_name'], \
                           str(schedule_info['arrival_time']), \
                           str(schedule_info['arrival_delay']), \
                           str(schedule_info['departure_time']), \
                           str(schedule_info['departure_delay'])))
