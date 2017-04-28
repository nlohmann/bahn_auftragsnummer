# coding=utf-8

########################################################################
# Licensed under the MIT License <http://opensource.org/licenses/MIT>. #
# Copyright (c) 2017 Niels Lohmann <http://nlohmann.me>.               #
########################################################################

import requests
from bs4 import BeautifulSoup
import datetime
from typing import List


class Buchungseintrag(object):
    def __init__(self):
        self.type = None            # type: str
        self.travel_date = None     # type: datetime.date
        self.description = None     # type: str
        self.voucher_number = None  # type: str
        self.price = None           # type: float


class Buchung(object):
    def __init__(self, auftragsnummer, nachname):
        self.auftragsnummer = auftragsnummer  # type: str
        self.nachname = nachname              # type: str

        self.reference_number = None          # type: str
        self.booking_date = None              # type: datetime.date
        self.booker = None                    # type: str
        self.traveler = None                  # type: str
        self.state = None                     # type: str
        self.entries = []                     # type: List[Buchungseintrag]

        self.__download()

    @property
    def valid(self):
        return self.reference_number is not None

    def __download(self):
        url = 'https://fahrkarten.bahn.de/privatkunde/start/start.post'
        params = {
            'dbkanal_007': 'L01_S01_D001_KIN0014_qf-buchungenauftrag_LZ08'
        }
        payload = {
            'scope': 'bahnatsuche',
            'search': 1,
            'country': 'DEU',
            'lang': 'de',
            'auftragsnr': self.auftragsnummer,
            'reisenderNachname': self.nachname
        }

        page = requests.post(url, params=params, data=payload)
        soup = BeautifulSoup(page.content, 'html.parser')

        headers = soup.find_all('table',
                                {'class': 'form brsDetailsTable brsDetailsKopfzeileTable bottommargin-big spanall'})
        try:
            header_entries = headers[0].find_all('td')
        except IndexError:
            return

        self.reference_number = header_entries[0].text.strip()
        self.booking_date = datetime.datetime.strptime(header_entries[1].text.strip(), '%d.%m.%Y').date()
        self.booker = header_entries[2].text.strip()
        self.traveler = header_entries[3].text.strip()
        self.state = header_entries[5].text.strip()

        details = soup.find_all('table', {'class': 'form brsDetailsTable spanall'})
        for tr in details[0].find_all('tr'):
            try:
                detail_entries = tr.find_all('td')
                entry = Buchungseintrag()
                entry.type = detail_entries[0].text.strip()
                entry.travel_date = datetime.datetime.strptime(detail_entries[1].text.strip(), '%d.%m.%Y').date()
                entry.description = detail_entries[2].text.strip()
                entry.voucher_number = int(detail_entries[3].text.strip())
                entry.price = float(detail_entries[5].text.strip().replace(' EUR', '').replace(',', '.'))
                self.entries.append(entry)
            except IndexError:
                pass
