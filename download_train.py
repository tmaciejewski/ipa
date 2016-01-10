#!/usr/bin/env python

import httplib
import sys
from bs4 import BeautifulSoup
import ipa_config

train_id = sys.argv[1]

def fetch_html(train_id):
    train_request = "/?p=train&id=" + train_id

    connection = httplib.HTTPConnection(ipa_config.domain)
    connection.request('GET', train_request)

    return connection.getresponse().read()

def get_train_number(columns):
    number = columns[0].span.contents[0]
    return ' '.join(number.split())

def get_train_name(columns):
    return columns[0].span.contents[2].strip()

def get_train_date(columns):
    return columns[1].span.string

def get_train_relation(columns):
    [start, stop] = columns[2].span.string.split('-')
    return start.strip() + ' - ' + stop.strip()

def get_train_stop_name(columns):
    return columns[3].a.string.strip()

def get_train_sched_arrive_time(columns):
    time = columns[4].span.string
    if time:
        return time
    else:
        return ''

def get_train_arrive_delay(columns):
    time = columns[5].span.string
    if time:
        return time
    else:
        return ''

def get_train_sched_dep_time(columns):
    time = columns[6].span.string
    if time:
        return time
    else:
        return ''

def get_train_dep_delay(columns):
    time = columns[7].span.string
    if time:
        return time
    else:
        return ''

def parse_html(html):
    result = []
    soup = BeautifulSoup(html, 'html.parser')

    for tr in soup.find_all('tr')[1:]:
        tds = tr.find_all('td')
        result.append([
            get_train_number(tds),
            get_train_name(tds),
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


html = fetch_html(train_id)

rows = parse_html(html)

print_train(rows)
