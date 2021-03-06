#!/usr/bin/env python3

import requests
import datetime
from requests.auth import HTTPBasicAuth
import pickle
import matplotlib.pyplot as plt
from random import randint

api = pickle.load(open('api.p', 'rb'))

internal = False


def get_data():
    url = 'https://api.theprintful.com/orders'
    user = api['user']
    pass_w = api['passw']
    data = [requests.get(url, auth=HTTPBasicAuth(user, pass_w))]
    order_count = data[0].json()['paging']['total']
    loops = 1
    while order_count > (loops * 20):
        data.append(requests.get(url + '?offset=' + str(loops * 20), auth=HTTPBasicAuth(user, pass_w)))
        loops += 1
    return data


def compile_patterns(data):
    patterns = {
        'Winter Sun': 0,
        'Soothing Wave': 0,
        'Natural Explosion': 0,
        'Ripples in Time': 0,
        'Cooling Core': 0,
        'Feathered Breath': 0,
        'GL!TCH': 0,
        'Parallax Shift': 0,
        'Digital Twilight': 0,
        'Mahogany Stone': 0
    }
    save_data(extract_orders(data, patterns), 'patterns')


def compile_sex(data):
    sex = {
        'Men': 0,
        'Women': 0
    }
    save_data(extract_orders(data, sex), 'sex')


def compile_states(data):
    states = {}
    for slot in data:
        info = slot.json()['result']
        for order in info:
            if order['external_id'] or internal:
                states[order['recipient']['state_name']] = states.get(order['recipient']['state_name'], 0) \
                                                       + len(order['items'])
    save_data(states, 'states')


def compile_styles(data):
    styles = {
        'Tank': 0,
        'Shirt': 0,
        'Socks': 0,
        'Leggings': 0
    }
    save_data(extract_orders(data, styles), 'styles')


def extract_orders(data, metric):
    for slot in data:
        info = slot.json()['result']
        for order in info:
            if order['external_id'] or internal:
                metric = analyze_items(order['items'], metric)
    return metric


def analyze_items(items, info):
    for item in items:
        for key in info:
            if key in item['name']:
                info[key] += 1
    return info


def compile_data(data, type):
    return{
        'patterns': compile_patterns,
        'states': compile_states,
        'styles': compile_styles,
        'sex': compile_sex
    }[type](data)


def save_data(data, type):
    with open(type + str(datetime.datetime.now().strftime('%Y%b%d')) + '.txt', 'w+') as f:
        for key in data:
            f.write(key + ': ' + str(data[key]) + '\n')
    print('Data saved.')
    print()

    if input('Would you like to create a pie chart? (y to select)\n') == 'y':
        draw_pie(data)


def draw_pie(data):
    labels = [x for x in data.keys()]
    sizes = [x for x in data.values()]
    colors = []
    for x in range(0, len(sizes)):
        colors.append(get_color(x))
    explode = [0 for x in data.values()]
    explode[randint(0, len(explode) - 1)] = 0.1
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')
    plt.show()


def get_color(num):
    li = ['yellowgreen', 'gold', 'blue', 'lightcoral', 'red', 'green', 'orange',
          'purple', 'pink', 'violet']
    return li[num]


def choose_report():
    report_list = ['patterns', 'states', 'styles', 'sex', 'quit']
    print('Report types:')
    for report in report_list:
        print(report)
    print()
    choice = input('Which report would you like to run? (Enter "quit" to exit)\n')
    while choice not in report_list:
        choice = input('Which report would you like to run? (Enter "quit" to exit)\n')
    print()
    return choice


def decide_internal():
    global internal
    c = input('Count internal orders? (y/n)\n')
    print()
    internal = (c == 'y')


def main():
    data = get_data()
    report = choose_report()
    while report != 'quit':
        decide_internal()
        compile_data(data, report)
        report = choose_report()

if __name__ == '__main__':
    main()
