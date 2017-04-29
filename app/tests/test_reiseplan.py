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
