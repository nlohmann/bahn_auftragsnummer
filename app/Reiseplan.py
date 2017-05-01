# coding=utf-8

########################################################################
# Licensed under the MIT License <http://opensource.org/licenses/MIT>. #
# Copyright (c) 2017 Niels Lohmann <http://nlohmann.me>.               #
########################################################################

import json
import requests
import datetime
import polyline
import urllib
from typing import Optional, Dict, Any, List


def build_map_url(coordinates):
    params = {
        'size': '640x640',
        'scale': '2',
        'maptype': 'terrain',
        'path': 'enc:{polyline}'.format(polyline=polyline.encode(coordinates)),
        'sensor': 'false',
        'language': 'de'
    }
    return 'http://maps.googleapis.com/maps/api/staticmap?' + urllib.urlencode(params)


class Coordinates(object):
    def __init__(self, payload):
        self.latitude = float(payload['y']) / 1000000.0   # type: float
        self.longitude = float(payload['x']) / 1000000.0  # type: float


class Location(object):
    def __init__(self, payload, travel_date):
        self.type = payload.get('locType')  # type: Optional[str]
        self.name = payload.get('name')     # type: Optional[str]
        self.arrival = None                 # type: Optional[datetime.datetime]
        self.departure = None               # type: Optional[datetime.datetime]

        try:
            hour, minute = payload['arr'].split(':')
            self.arrival = datetime.datetime.combine(travel_date, datetime.time(int(hour), int(minute)))
        except (ValueError, KeyError):
            pass

        try:
            hour, minute = payload['dep'].split(':')
            self.departure = datetime.datetime.combine(travel_date, datetime.time(int(hour), int(minute)))
        except (ValueError, KeyError):
            pass

        self.station_id = payload.get('evaId')   # type: Optional[str]
        self.coordinates = Coordinates(payload)  # type: Coordinates


class Leg(object):
    def __init__(self, payload, travel_date):
        self.transport = payload['icon']                                              # type: str
        self.name = ' '.join(payload['name'].split()) if 'name' in payload else None  # type: Optional[str]
        self.type = payload.get('type')                                               # type: Optional[str]

        self.product_code = None                                                      # type: Optional[int]
        try:
            self.product_code = int(payload['productcode'])
        except KeyError:
            pass

        self.train_id = payload.get('trainId')                                        # type: Optional[str]
        self.locations = [Location(loc, travel_date)
                          for loc in payload['locations'] if 'locType' in loc]        # type: List[Location]

    @property
    def coordinate_list(self):
        return [(location.coordinates.latitude, location.coordinates.longitude) for location in self.locations]

    @property
    def zugfinder_url(self):
        if self.name is not None and self.transport not in ['bus', 're', 'rb']:
            return 'http://www.zugfinder.de/zuginfo.php?zugnr={name}'.format(name=self.name.replace(' ', '_'))
        else:
            return None

    @property
    def map_url(self):
        return build_map_url(self.coordinate_list)


class Reiseplan(object):
    def __init__(self, auftragsnummer):
        self.auftragsnummer = auftragsnummer  # type: str
        self.travel_date = None               # type: datetime.date
        self.payload = None                   # type: Dict[str, Any]

        self.__download(auftragsnummer)
        if self.payload is None:
            raise ValueError

        self.legs = [Leg(section, self.travel_date)
                     for section in self.payload['sections']]  # type: List[Leg]

    @property
    def map_url(self):
        coordinates = []
        for leg in self.legs:
            coordinates += leg.coordinate_list
        return build_map_url(coordinates)

    def __download(self, auftragsnummer):
        """
        Retrieve itinerary from a given reference number
        :param auftragsnummer: Deutsche Bahn reference number (6 alphanumeric characters)
        """
        url = 'https://fahrkarten.bahn.de/privatkunde/start/start.post'
        params = {
            'lang': 'de',
            'scope': 'reiseplan',
            'atnr': auftragsnummer,
            'country': 'DEU'
        }

        response = requests.get(url, params=params)

        for line in response.text.split('\n'):
            # search for the date
            if 'activeConnectionTriggerDate' in line:
                # the date is not part of the JSON payload, so we need to get it individually
                self.travel_date = datetime.datetime.strptime(line[line.find('"') + 1:line.rfind('"')], '%d.%m.%Y').date()

            # search for the JSON payload
            if line.startswith('jsonObjC0_0'):
                # extract JSON variable
                json_text = line[line.find('=') + 1:line.rfind(';')]
                # fix JSON variable (wrong escapes)
                json_text = json_text.replace(r"\'", r'\"')
                # parse the JSON variable
                self.payload = json.loads(json_text)
                break
