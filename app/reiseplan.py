# coding=utf-8

import json
import requests


def reiseplan(auftragsnummer):
    """
    Retrieve itinerary from a given reference number
    :param auftragsnummer: Deutsche Bahn reference number (6 alphanumeric characters)
    :return: itinerary as dictionary or None
    """
    url = 'https://fahrkarten.bahn.de/privatkunde/start/start.post'
    params = {
        'lang': 'de',
        'scope': 'reiseplan',
        'atnr': auftragsnummer,
        'country': 'DEU'
    }

    res = requests.get(url, params=params).text

    date_str = None
    for line in res.split('\n'):
        # search for the date
        if 'activeConnectionTriggerDate' in line:
            # the date is not part of the JSON payload, so we need to get it individually
            date_str = line[line.find('"') + 1:line.rfind('"')]

        # search for the JSON payload
        if line.startswith('jsonObjC0_0'):
            # parse the JSON variable
            result = json.loads(line[line.find('=') + 1:line.rfind(';')])

            # add the date and the reference number
            result['date'] = date_str
            result['referenceNumber'] = auftragsnummer
            return result

    return None
