# coding=utf-8

########################################################################
# Licensed under the MIT License <http://opensource.org/licenses/MIT>. #
# Copyright (c) 2017 Niels Lohmann <http://nlohmann.me>.               #
########################################################################

import datetime
from unittest import TestCase
from app.Buchung import Buchung


class TestBuchung(TestCase):
    def test_complete(self):
        b = Buchung('TYFMQE', 'Lohmann')
        self.assertEqual(b.reference_number, 'TYFMQE')
        self.assertEqual(b.booker, 'Niels Lohmann')
        self.assertEqual(b.traveler, 'Niels Lohmann')
        self.assertEqual(b.state, 'bearbeitet')
        self.assertEqual(b.booking_date, datetime.date(2016, 11, 8))
        self.assertEqual(len(b.entries), 2)
        self.assertTrue(b.valid)

    def test_incomplete(self):
        b = Buchung('TYFMQE', '')
        self.assertIsNone(b.reference_number)
        self.assertIsNone(b.booker)
        self.assertIsNone(b.traveler)
        self.assertIsNone(b.state)
        self.assertIsNone(b.booking_date)
        self.assertEqual(len(b.entries), 0)
        self.assertFalse(b.valid)

    def test_invalid_name(self):
        b = Buchung('TYFMQE', 'Mustermann')
        self.assertIsNone(b.reference_number)
        self.assertIsNone(b.booker)
        self.assertIsNone(b.traveler)
        self.assertIsNone(b.state)
        self.assertIsNone(b.booking_date)
        self.assertEqual(len(b.entries), 0)
        self.assertFalse(b.valid)

    def test_invalid_reference(self):
        b = Buchung('TQFMQE', 'Lohmann')
        self.assertIsNone(b.reference_number)
        self.assertIsNone(b.booker)
        self.assertIsNone(b.traveler)
        self.assertIsNone(b.state)
        self.assertIsNone(b.booking_date)
        self.assertEqual(len(b.entries), 0)
        self.assertFalse(b.valid)
