#!/usr/bin/env python

import httplib
import sys
from bs4 import BeautifulSoup
import ipa_config

def fetch_html(train_id):
    train_request = "/?p=train&id=" + train_id

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
        result.append([
            get_train_number(tds),
            get_train_date(tds),
            get_train_relation(tds),
            get_train_stop_name(tds),
            get_train_sched_arrive_time(tds),
            get_train_arrive_delay(tds),
            get_train_sched_dep_time(tds),
            get_train_dep_delay(tds)
        ])

    return result

def print_train(rows):
    for row in rows:
        if (len(row) > 1):
            print ' | '.join(row)
        else:
            print row[0]

if __name__ == "__main__":
    train_id = sys.argv[1]
    train = get_train(train_id)
    print_train(train)
