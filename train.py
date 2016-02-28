#!/usr/bin/env python

import httplib
import sys
from bs4 import BeautifulSoup
import ipa_config

def fetch_html(train_id):
    train_request = "/?p=train&id=" + str(train_id)

    connection = httplib.HTTPConnection(ipa_config.domain)
    connection.request('GET', train_request)

    return connection.getresponse().read()

def get_simple_field(columns, index):
    field = columns[index].span.string
    return field.strip() if field else ''

def get_train_number(columns):
    contents = columns[0].span.contents
    number =  ' '.join(contents[0].split())
    name = contents[2].strip()
    if name != '':
        return number + ' ' + name
    else:
        return number

def get_train_date(columns):
    return get_simple_field(columns, 1)

def get_train_relation(columns):
    [start, stop] = columns[2].span.string.split('-')
    return start.strip() + ' - ' + stop.strip()

def get_train_stop_name(columns):
    name = columns[3].a.string
    return name.strip() if name else ''

def get_train_sched_arrive_time(columns):
    return get_simple_field(columns, 4)

def get_train_arrive_delay(columns):
    return get_simple_field(columns, 5)

def get_train_sched_dep_time(columns):
    return get_simple_field(columns, 6)

def get_train_dep_delay(columns):
    return get_simple_field(columns, 7)

def get_train(train_id):
    result = []
    html = fetch_html(train_id)
    soup = BeautifulSoup(html, 'html.parser')

    for tr in soup.find_all('tr')[1:]:
        tds = tr.find_all('td')
        result.append({
            'number': get_train_number(tds),
            'date': get_train_date(tds),
            'relation': get_train_relation(tds),
            'stop_name': get_train_stop_name(tds),
            'sched_arrive_time': get_train_sched_arrive_time(tds),
            'arrive_delay': get_train_arrive_delay(tds),
            'sched_dep_time': get_train_sched_dep_time(tds),
            'dep_delay': get_train_dep_delay(tds)
        })

    return result

def print_train(rows):
    for row in rows:
        if (len(row) > 1):
            print ' | '.join([row['number'], row['date'], row['relation'], row['stop_name'],
                              row['sched_arrive_time'], row['arrive_delay'], row['sched_dep_time'],
                              row['dep_delay']])
        else:
            print row[0]

if __name__ == "__main__":
    train_id = sys.argv[1]
    train = get_train(train_id)
    print_train(train)
