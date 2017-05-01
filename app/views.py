# coding=utf-8

########################################################################
# Licensed under the MIT License <http://opensource.org/licenses/MIT>. #
# Copyright (c) 2017 Niels Lohmann <http://nlohmann.me>.               #
########################################################################

from flask import send_from_directory
from flask_restplus import Resource
from app import cache, api
from app.Buchung import Buchung
from app.models import m_itinerary, m_bookingrequest, m_booking, m_form_request
from app.Reiseplan import Reiseplan
from app.Complaint import Complaint
from os.path import basename, dirname

########################################################################
# namespaces
########################################################################

ns_itineraries = api.namespace('itineraries', description='Operations related to itineraries')
ns_bookings = api.namespace('bookings', description='Operations related to bookings')
ns_form = api.namespace('forms', description='Operations related to Fahrgastrechte forms')


########################################################################
# routes
########################################################################

@ns_itineraries.route('/<auftragsnummer>')
@api.doc(params={'auftragsnummer': 'a 6-character reference number'})
class ReferenceNumber(Resource):
    @api.response(404, 'itinerary not found')
    @ns_itineraries.marshal_with(m_itinerary)
    @cache.cached(timeout=3600)
    def get(self, auftragsnummer):
        """
        returns an itinerary
        
        [terms of use](https://www.bahn.de/p/view/home/agb/nutzungsbedingungen.shtml)
        """
        try:
            return Reiseplan(auftragsnummer)
        except ValueError:
            api.abort(404, error='itinerary not found', referenceNumber=auftragsnummer)


@ns_bookings.route('/')
class Booking(Resource):
    @api.response(404, 'booking not found')
    @ns_bookings.marshal_with(m_booking)
    @ns_bookings.expect(m_bookingrequest)
    def post(self):
        """
        returns a booking

        [terms of use](https://www.bahn.de/p/view/home/agb/nutzungsbedingungen.shtml)
        """
        booking = Buchung(api.payload.get('referenceNumber'), api.payload.get('lastName'))
        if booking.valid:
            return booking
        else:
            api.abort(404, error='booking not found', payload=api.payload)


@ns_form.route('/')
class Form(Resource):
    @ns_form.expect(m_form_request)
    @api.response(400, 'input validation failure')
    @api.representation('application/pdf')
    def post(self):
        """
        returns a filled form
        """
        complaint = Complaint()
        complaint.fill(api.payload)
        filled_form = complaint.create_pdf()
        return send_from_directory(dirname(filled_form), basename(filled_form))
