#!/usr/bin/env python

import sys
import os

import ipa_db
import ipa_config

def escape(name):
    return name.replace('/', '_')

def make_head(f, title):
    f.write('   <head>\n')
    f.write('       <title>' + title + '</title>\n')
    f.write('       <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n')
    f.write('       <link rel="stylesheet" href="style.css" type="text/css" />\n')
    f.write('   </head>\n')

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

    if delay > 60:
        return 'critical'
    elif delay > 20:
        return 'moderate'
    elif delay > 5:
        return 'minor'
    else:
        return 'normal'

def gen_train(output_dir, db, train):
    name = train.encode('utf-8')
    with open(os.path.join(output_dir, escape(name) + '.html'), 'w') as f:
        f.write('<html>\n')
        make_head(f, name)
        f.write('   <body>\n')
        f.write('       <h1>' + name + '</h1>\n')
        f.write('       <table>\n')
        f.write('       <thead><tr>\n<th>Date</th>')

        schedules = list(db.get_train_schedules(train))

        for info in db.get_schedule_info(schedules[0][0]):
            f.write('               <th>' + info[2].encode('utf-8') + '</th>')

        f.write('       </tr></thead>\n')
        f.write('       <tbody>\n')

        for schedule in schedules:
            f.write('           <tr>')
            f.write('<td class="date">' + schedule[3] + '</td>')
            for info in db.get_schedule_info(schedule[0]):
                f.write('<td class="' + get_delay_class(info) + '"><p class="arr">&#8594; ' + info[3][:5] + ' (' + info[4] + ')</p><p class="dep">' + info[5][:5] + ' (' + info[6] + ') &#8594;</p></td>')
            f.write('</tr>\n')

        f.write('       </tbody>\n')
        f.write('       </table>\n')
        f.write('   </body>\n')
        f.write('</html>\n')

def gen_index(output_dir, db):
    with open(os.path.join(output_dir, "index.html"), 'w') as f:
        f.write('<html>\n')
        make_head(f, 'InfoPasazer Archiver')
        f.write('   <body>\n')
        f.write('       <h1>InfoPasazer Archiver</h1>\n')

        for train in db.get_trains():
            name = train.encode('utf-8')
            f.write('       <span><a href="' + escape(name) + '.html">' + name + '</a></span>\n')
            gen_train(output_dir, db, train)

        f.write('   </body>\n')
        f.write('</html>\n')

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print 'No output dir given'
        sys.exit(1)

    output_dir = sys.argv[1]

    if not os.path.isdir(output_dir):
        print 'Not a directory'
        sys.exit(2)

    db = ipa_db.Db(ipa_config.db_name)

    gen_index(output_dir, db)
