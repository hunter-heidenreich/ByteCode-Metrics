import requests
import datetime
from requests.auth import HTTPBasicAuth
import pickle

api = pickle.load(open('api.p', 'rb'))

def getData():
    url = 'https://api.theprintful.com/orders'
    user = api['user']
    passw = api['passw']
    data = [requests.get(url, auth=HTTPBasicAuth(user, passw))]
    orderCount = data[0].json()['paging']['total']
    loops = 1
    while orderCount > (loops * 20):
        data.append(requests.get(url + '?offset=' + str(loops * 20), auth=HTTPBasicAuth(user, passw)))
        loops += 1
    return data


def compilePatterns(data):
    patterns = {
        'Winter Sun': 0,
        'Soothing Wave': 0,
        'Natural Explosion': 0,
        'Ripples in Time': 0,
        'Cooling Core': 0
    }
    for slot in data:
        info = slot.json()['result']
        for order in info:
            for item in order['items']:
                for key in patterns:
                    if key in item['name']:
                        patterns[key] += 1
    saveData(patterns, 'patterns')


def compileGenders(data):
    genders = {
        'Men': 0,
        'Women': 0
    }
    for slot in data:
        info = slot.json()['result']
        for order in info:
            for item in order['items']:
                for key in genders:
                    if key in item['name']:
                        genders[key] += 1
    saveData(genders, 'genders')


def compileStates(data):
    states = {}
    for slot in data:
        info = slot.json()['result']
        for order in info:
            states[order['recipient']['state_name']] = states.get(order['recipient']['state_name'], 0) \
                                                       + len(order['items'])
    saveData(states, 'states')


def compileStyles(data):
    styles = {
        'Tank': 0,
        'Shirt': 0,
        'Socks': 0,
        'Leggings': 0
    }
    for slot in data:
        info = slot.json()['result']
        for order in info:
            for item in order['items']:
                for key in styles:
                    if key in item['name']:
                        styles[key] += 1
    saveData(styles, 'styles')


def compileData(data, type):
    return{
        'patterns': compilePatterns,
        'states': compileStates,
        'styles': compileStyles,
        'genders': compileGenders
    }[type](data)


def saveData(data, type):
    with open(type + str(datetime.datetime.now().strftime('%Y%b%d')) + '.txt', 'w+') as f:
        for key in data:
            f.write(key + ': ' + str(data[key]) + '\n')
    print('Data saved.')
    print()


def chooseReport():
    reportList = ['patterns', 'states', 'styles', 'genders', 'quit']
    print('Report types:')
    for report in reportList:
        print(report)
    print()
    choice = input('Which report would you like to run? (Enter "quit" to exit)\n')
    while choice not in reportList:
        choice = input('Which report would you like to run? (Enter "quit" to exit)\n')
    print()
    return choice


def main():
    data = getData()
    report = chooseReport()
    while report != 'quit':
        compileData(data, report)
        report = chooseReport()

main()
