#!/usr/bin/env python

import sys
import os
import datetime

import ipa_db
import ipa_config

def escape(name):
    return name.replace('/', '_')

def make_head(f, title):
    f.write('<html>\n')
    f.write('   <head>\n')
    f.write('       <title>' + title + '</title>\n')
    f.write('       <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n')
    f.write('       <link rel="stylesheet" href="style.css" type="text/css" />\n')
    f.write('   </head>\n')

def make_footer(f):
    now = datetime.datetime.now()
    f.write('       <p class="timestamp">Generated %d.%.2d.%.2d %.2d:%.2d</p>\n' \
            % (now.year, now.month, now.day, now.hour, now.minute))
    f.write('   </body>\n')
    f.write('</html>\n')

def get_delay_class(info):
    try:
        arr_delay = int(info[4].split()[0])
    except:
        arr_delay = 0

    try:
        dep_delay = int(info[6].split()[0])
    except:
        dep_delay = 0

    delay = max(arr_delay, dep_delay)

    if delay >= 60:
        return 'critical'
    elif delay >= 20:
        return 'moderate'
    elif delay >= 5:
        return 'minor'
    else:
        return 'normal'

def make_station_row(f, stations, date, date_freq):
    f.write('           <tr>')
    i = 0
    for station in stations:
        if i % date_freq == 0:
            if station != '':
                f.write('<th rowspan=2 class="date">' + date + '</th>')
            else:
                f.write('<th rowspan=2 class="date"></th>')
        f.write('<th>' + station.encode('utf-8') + '</th>')
        i += 1
    f.write('</tr>')

def make_time_row(f, schedule_info):
    f.write('           <tr>')
    for info in schedule_info:
        f.write('<td class="' + get_delay_class(info) + '">')
        f.write('<p class="arr">&#8594; ' + info['sched_arrive_time'][:5] + ' (' + info['sched_arrive_delay'] + ')</p>')
        f.write('<p class="dep">' + info['sched_departure_time'][:5] + ' (' + info['sched_departure_delay'] + ') &#8594;</p></td>')
    f.write('</tr>\n')

def gen_train(output_dir, train, schedules, schedule_infos):
    name = train.encode('utf-8')
    stations_width = max([len(schedule_infos[schedule]) for schedule in schedule_infos])
    with open(os.path.join(output_dir, escape(name) + '.html'), 'w') as f:
        make_head(f, name)
        f.write('   <body>\n')
        f.write('       <h1>' + name + '</h1>\n')
        f.write('       <table>\n')

        date_freq = 10
        for schedule in schedules:
            stations = [info['stop_name'] for info in schedule_infos[schedule['train_id']]]
            while len(stations) < stations_width:
                stations.append('')
            make_station_row(f, stations, schedule['train_date'], date_freq)
            make_time_row(f, schedule_infos[schedule['train_id']])

        f.write('       </table>\n')
        make_footer(f)

def gen_index(output_dir, trains):
    with open(os.path.join(output_dir, "index.html"), 'w') as f:
        make_head(f, 'InfoPasazer Archiver')
        f.write('   <body>\n')
        f.write('       <h1>InfoPasazer Archiver</h1>\n')

        for train in trains:
            name = train['train_number'].encode('utf-8')
            f.write('       <span><a href="' + escape(name) + '.html">' + name + '</a></span>\n')

        make_footer(f)

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print 'No output dir given'
        sys.exit(1)

    output_dir = sys.argv[1]

    if not os.path.isdir(output_dir):
        print 'Not a directory'
        sys.exit(2)

    db = ipa_db.Db(ipa_config.db_name)
    trains = list(db.get_trains())
    gen_index(output_dir, trains)
    for train in trains:
        schedules = list(db.get_train_schedules(train['train_number']))
        schedule_infos = {}
        for schedule in schedules:
            schedule_infos[schedule['train_id']] = list(db.get_schedule_info(schedule['train_id']))
        gen_train(output_dir, train['train_number'], schedules, schedule_infos)
