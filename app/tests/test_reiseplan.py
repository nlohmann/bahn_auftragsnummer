# coding=utf-8

########################################################################
# Licensed under the MIT License <http://opensource.org/licenses/MIT>. #
# Copyright (c) 2017 Niels Lohmann <http://nlohmann.me>.               #
########################################################################

from unittest import TestCase
from app.Reiseplan import Reiseplan
import datetime


class TestReiseplan(TestCase):
    def test_complete(self):
        r = Reiseplan('TYFMQE')
        self.assertEqual(r.auftragsnummer, 'TYFMQE')
        self.assertEqual(r.travel_date, datetime.date(2016, 12, 25))
        self.assertEqual(len(r.legs), 1)
        self.assertEqual(r.legs[0].transport, 'ic')
        self.assertEqual(r.legs[0].name, 'IC 2216')
        self.assertEqual(r.legs[0].zugfinder_url, 'http://www.zugfinder.de/zuginfo.php?zugnr=IC_2216')
        self.assertEqual(r.legs[0].type, 'JOURNEY')
