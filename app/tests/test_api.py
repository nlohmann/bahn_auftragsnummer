# coding=utf-8

########################################################################
# Licensed under the MIT License <http://opensource.org/licenses/MIT>. #
# Copyright (c) 2017 Niels Lohmann <http://nlohmann.me>.               #
########################################################################

from unittest import TestCase
from app import app


class ApiTest(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_auftragsnummer_empty(self):
        rv = self.app.get('/api/itineraries/')
        self.assertEqual(rv.status_code, 404)

    def test_get_auftragsnummer_invalid(self):
        rv = self.app.get('/api/itineraries/123456')
        self.assertEqual(rv.status_code, 404)

    def test_post_booking_empty(self):
        rv = self.app.post('/api/bookings/', data='{}', content_type='application/json')
        self.assertEqual(rv.status_code, 400)

    def test_post_booking_invalid(self):
        rv = self.app.post('/api/bookings/', data='{"lastName": "Mustermann", "referenceNumber": "TYFMQE"}',
                           content_type='application/json')
        self.assertEqual(rv.status_code, 404)

    def test_post_forms_empty(self):
        rv = self.app.post('/api/forms/', data='{}', content_type='application/json')
        self.assertEqual(rv.status_code, 200)
