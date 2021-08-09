import requests
from html.parser import unescape
from helper_functs import sorted_schedule, event_timeint
from datetime import datetime
from variables import WebApiURL


def get_groups() -> map:
    url = WebApiURL.DOMAIN + WebApiURL.GROUPS
    params = {'searchTerm': '_', 'pageSize': '10000', 'resType': '103'}
    r = requests.get(url, params=params)
    j = r.json()
    return map(lambda e: e['id'], j['results'])


def format_description(event: dict) -> filter:
    return filter(None, map(
        unescape,
        event['description']
        .replace('\r', '')
        .replace('<br />', '')
        .split('\n')
    ))


def is_staff(field: str) -> bool:
    return all(map(lambda x: x.isupper() or x.istitle(), field.split()))


def is_room(field: str) -> bool:
    return '/' in field


def get_calendar(group: str):
    data = {
        'start': '2021-09-03',
        'end': '2021-12-17',
        'resType': '103',
        'calView': 'agendaDay',
        'federationIds[]': group,
    }
    url = WebApiURL.DOMAIN + WebApiURL.CALENDARDATA
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    r = requests.post(url, data=data, headers=headers)
    j = r.json()
    return {event['id']: event for event in j}


def parse_event(event: dict) -> dict:
    parsed_event = {
        'id':        event['id'],
        'day':       0,
        'date':      tuple(map(int, event['start'].split('T')[0].split('-'))),
        'starttime': event['start'].split('T')[1],
        'endtime':   event['end']  .split('T')[1],
        'startint':  event_timeint(event, 'start'),
        'endint':    event_timeint(event, 'end'),
        'timeint':   event_timeint(event),
        'module':    event['modules'] and event['modules'][0],
        'category':  event['eventCategory'],
        'groups':    [],
        'room':      None,
        'staff':     None,
        'notes':     None,
    }
    parsed_event['day'] = datetime(*parsed_event['date']).weekday()
    for field in format_description(event):
        if field in (parsed_event['module'], parsed_event['category']):
            continue
        elif is_room(field):
            parsed_event['room'] = field
        elif is_staff(field):
            parsed_event['staff'] = [field]
        else:
            if parsed_event['notes']:
                parsed_event['notes'] += field
            else:
                parsed_event['notes'] = field
    return parsed_event


def get_combined_schedule(groups: list) -> list:
    sche_id_dict = {}
    for group in groups:
        id_cal = get_calendar(group)
        for id, event in id_cal.items():
            if event['eventCategory'] != 'Vacances':
                if id not in sche_id_dict:
                    sche_id_dict[id] = parse_event(event)
                sche_id_dict[id]['groups'].append(group)
    return sorted_schedule(sche_id_dict.values())


if __name__ == '__main__':
    from variables import MI_groups
    sche = get_combined_schedule(MI_groups)
