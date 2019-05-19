#!/usr/bin/env python3

import http.client
import sys
from bs4 import BeautifulSoup
import ipa_config

def fetch_html(train_id):
    train_request = "/?p=train&id=" + str(train_id)

    connection = http.client.HTTPSConnection(ipa_config.domain)
    connection.request('GET', train_request)

    return connection.getresponse().read()

def format_date(date):
    [d, m, y] = date.split('.')
    return '%s-%s-%s' % (y, m, d)

def get_simple_field(columns, index):
    field = columns[index].span.string
    return field.strip() if field else ''

def get_delay_field(columns, index):
    try:
        return str(int(get_simple_field(columns, index).split()[0]))
    except:
        return ''

def get_train_name(columns):
    contents = columns[0].span.contents
    number = ' '.join(contents[0].split())
    name = contents[2].strip()
    if name != '':
        return number + ' ' + name
    else:
        return number

def get_train_date(columns):
    return format_date(get_simple_field(columns, 1))

def get_train_relation(columns):
    [start, stop] = columns[2].span.string.split(' - ')
    return start.strip() + ' - ' + stop.strip()

def get_train_stop_name(columns):
    name = columns[3].a.string
    return name.strip() if name else ''

def get_train_sched_arrive_time(columns):
    return get_simple_field(columns, 4)

def get_train_arrive_delay(columns):
    return get_delay_field(columns, 5)

def get_train_sched_dep_time(columns):
    return get_simple_field(columns, 6)

def get_train_dep_delay(columns):
    return get_delay_field(columns, 7)

def get_train(train_id):
    result = {'info': []}
    html = fetch_html(train_id)
    soup = BeautifulSoup(html, 'html.parser')

    try:
        title = soup.find_all('div', class_ = 'table-responsive')[0].find_all('div')[0].contents[0]
        result['name'] = ' '.join(title.split()[1:-2])
        result['date'] = format_date(title.split()[-1].strip('.'))
    except:
        return {'name': None, 'date': None, 'info': []}

    for tr in soup.find_all('tr')[1:]:
        tds = tr.find_all('td')
        result['info'].append({
            'name': get_train_name(tds),
            'date': get_train_date(tds),
            'relation': get_train_relation(tds),
            'stop_name': get_train_stop_name(tds),
            'arrival_time': get_train_sched_arrive_time(tds),
            'arrival_delay': get_train_arrive_delay(tds),
            'departure_time': get_train_sched_dep_time(tds),
            'departure_delay': get_train_dep_delay(tds)
        })

    return result

def print_train(rows):
    for row in rows:
        if (len(row) > 1):
            print(' | '.join([row['name'], row['date'], row['relation'], row['stop_name'],
                              row['arrival_time'], row['arrival_delay'], row['departure_time'],
                              row['departure_delay']]))
        else:
            print(row[0])

if __name__ == "__main__":
    train_id = sys.argv[1]
    train = get_train(train_id)
    print(train['name'], train['date'])
    print_train(train['info'])
