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
from typing import List, Dict, Any


class Reiseplan(object):
    def __init__(self, auftragsnummer):
        self.auftragsnummer = auftragsnummer  # type: str
        self.travel_date = None               # type: datetime.date
        self.payload = None                   # type: Dict[str, Any]

        self.__download(auftragsnummer)

    def __download(self, auftragsnummer):
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

        response = requests.get(url, params=params)

        for line in response.text.split('\n'):
            # search for the date
            if 'activeConnectionTriggerDate' in line:
                # the date is not part of the JSON payload, so we need to get it individually
                try:
                    self.travel_date = datetime.datetime.strptime(line[line.find('"') + 1:line.rfind('"')], '%d.%m.%Y').date()
                except ValueError:
                    break

            # search for the JSON payload
            if line.startswith('jsonObjC0_0'):
                # extract JSON variable
                json_text = line[line.find('=') + 1:line.rfind(';')]
                # fix JSON variable (wrong escapes)
                json_text = json_text.replace(r"\'", r'\"')
                # parse the JSON variable
                self.payload = json.loads(json_text)
                break

    @property
    def valid(self):
        return self.payload is not None

    @staticmethod
    def map_url(coordinates):
        params = {
            'size': '640x640',
            'scale': '2',
            'maptype': 'terrain',
            'path': 'enc:{polyline}'.format(polyline=polyline.encode(coordinates)),
            'sensor': 'false',
            'language': 'de'
        }
        return 'http://maps.googleapis.com/maps/api/staticmap?' + urllib.urlencode(params)

    def __iter__(self):
        legs = []

        all_coordinates = []
        for leg in self.payload['sections']:
            try:
                name = ' '.join(leg['name'].split())
                zugfinder_url = 'http://www.zugfinder.de/zuginfo.php?zugnr={name}'.format(name=name.replace(' ', '_'))
            except KeyError:
                name = None
                zugfinder_url = None

            leg_entry = {
                'transport': leg['icon'],
                'name': name,
                'type': leg.get('type'),
                'productCode': int(leg['productcode']) if 'productcode' in leg else None,
                'trainId': leg.get('trainId'),
                'locations': [],
                'zugfinderUrl': zugfinder_url
            }

            leg_coordinates = []
            for location in leg['locations']:
                latitude = float(location["y"]) / 1000000.0
                longitude = float(location["x"]) / 1000000.0

                leg_coordinates.append((latitude, longitude))

                try:
                    hour, minute = location['arr'].split(':')
                    arrival = datetime.datetime.combine(self.travel_date, datetime.time(int(hour), int(minute)))
                except (ValueError, KeyError):
                    arrival = None

                try:
                    hour, minute = location['dep'].split(':')
                    departure = datetime.datetime.combine(self.travel_date, datetime.time(int(hour), int(minute)))
                except (ValueError, KeyError):
                    departure = None

                location_entry = {
                    'type': location.get('locType'),
                    'name': location.get('name'),
                    'arrival': arrival.isoformat() if arrival else arrival,
                    'departure': departure.isoformat() if departure else departure,
                    'stationId': location.get('evaId'),
                    'coordinates': {
                        'latitude': latitude,
                        'longitude': longitude
                    }
                }
                leg_entry['locations'].append(location_entry)
            leg_entry['mapUrl'] = self.map_url(leg_coordinates)
            all_coordinates += leg_coordinates

            legs.append(leg_entry)

        yield 'referenceNumber', self.auftragsnummer,
        yield 'travelDate', self.travel_date.isoformat(),
        yield 'legs', legs
        yield 'mapUrl', self.map_url(all_coordinates)
