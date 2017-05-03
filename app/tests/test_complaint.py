# coding=utf-8

########################################################################
# Licensed under the MIT License <http://opensource.org/licenses/MIT>. #
# Copyright (c) 2017 Niels Lohmann <http://nlohmann.me>.               #
########################################################################

from unittest import TestCase
import os.path
from app.Complaint import Complaint


class TestComplaint(TestCase):
    def test_empty(self):
        c = Complaint()
        f = c.create_pdf()
        self.assertTrue(os.path.isfile(f))

    def test_payload(self):
        payload = {
            "firstName": "Max",
            "compensation": "transfer",
            "phone": "030/5554422",
            "endStation": u"Köln Hbf",
            "iban": "DE89 3704 0044 0532 0130 00",
            "email": "m.mustermann@t-online.de",
            "gender": "Herr",
            "startStationPlannedArrival": "2017-05-01T17:09:00",
            "lastName": "Mustermann",
            "marketingResearch": False,
            "stationLastChange": "Hannover Hbf",
            "trainFirstDelayedPlannedDeparture": "2017-05-01T14:31:00",
            "city": "Berlin",
            "street": u"Musterstraße",
            "houseNumber": "23",
            "dateOfBirth": "1981-05-10",
            "travelEndDate": "2017-05-01",
            "stationTripSuspended": "Hannover Hbf",
            "company": "ACME",
            "numberBahncard100": "7081411012345678",
            "startStationPlannedDeparture": "2017-05-01T13:01:00",
            "travelStartDate": "2017-05-01",
            "stationMissedTrain": "Hannover Hbf",
            "startStationActualArrival": "2017-05-01T21:09:00",
            "trainArrived": "ICE 554",
            "accountHolder": "Mustermann, Max",
            "state": "NL",
            "stationTripAborted": "Hannover Hbf",
            "postcode": "12345",
            "co": "Norbert Nachname",
            "title": "Dr.",
            "numberSeasonTicket": "7081411012345678",
            "trainFirstDelayed": "ICE 558",
            "bic": "PBNKDEFF",
            "startStation": "Hamburg Hbf"
        }
        c = Complaint()
        c.fill(payload)
        f = c.create_pdf()
        self.assertTrue(os.path.isfile(f))

    def test_empty_fill(self):
        c = Complaint()
        c.fill({})
        f = c.create_pdf()
        self.assertTrue(os.path.isfile(f))

    def test_additional_cases(self):
        c = Complaint()
        c.fill({
            "gender": "Frau",
            "marketingResearch": True,
            "compensation": "voucher"
        })
        f = c.create_pdf()
        self.assertTrue(os.path.isfile(f))

    def test_value_error(self):
        c = Complaint()
        c.geschlecht = "foobar"
        with self.assertRaises(ValueError):
            c.create_pdf()
