# coding=utf-8

########################################################################
# Licensed under the MIT License <http://opensource.org/licenses/MIT>. #
# Copyright (c) 2017 Niels Lohmann <http://nlohmann.me>.               #
########################################################################

from unittest import TestCase
from app.Reiseplan import Reiseplan, build_map_url
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


class TestBuildMapUrl(TestCase):
    def test_empty(self):
        with self.assertRaises(IndexError):
            build_map_url([])

    def test_filled(self):
        m = build_map_url([(52, 13), (52.1, 13.1)])
        self.assertEqual(m, 'http://maps.googleapis.com/maps/api/staticmap?scale=2&language=de&maptype=terrain&path=enc%3A_gk%7CH_ajnA_pR_pR&sensor=false&size=640x640')
