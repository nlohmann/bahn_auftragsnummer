# coding=utf-8

########################################################################
# Licensed under the MIT License <http://opensource.org/licenses/MIT>. #
# Copyright (c) 2017 Niels Lohmann <http://nlohmann.me>.               #
########################################################################

from flask_restplus import Resource, fields
from app import cache, api
from app.reiseplan import Reiseplan
from app.buchung import Buchung

########################################################################
# namespaces
########################################################################

ns_itineraries = api.namespace('itineraries', description='Operations related to itineraries')
ns_bookings = api.namespace('bookings', description='Operations related to bookings')

########################################################################
# models
########################################################################

m_location = api.model('Location', {
    'coordinates': fields.Nested(
        api.model('Coordinates', {
            'latitude': fields.Float(min=-90, max=90, example=54.078242, required=True),
            'longitude': fields.Float(min=-180, max=180, example=12.131078, required=True)
        })
    ),
    'arrival': fields.DateTime(description='date and time of the arrival'),
    'departure': fields.DateTime(description='date and time of the departure'),
    'stationId': fields.String(example='8000044', description='station id'),
    'type': fields.String(example='STATION', description='location type', required=True),
    'name': fields.String(example='Bonn Hbf', description='location name', required=True)
})

m_leg = api.model('Leg', {
    'mapUrl': fields.Url(description='map with the leg\'s route', example='http://maps.googleapis.com/maps/api/staticmap?size=800x800&scale=2&maptype=terrain&path=enc:}{q_IufrpAov@br`@c{eEjdnR&sensor=false&language=de', required=True),
    'type': fields.String(example='JOURNEY', required=True),
    'name': fields.String(example='IC  2216', description='train name'),
    'transport': fields.String(example='ic', description='type of the current transportation', required=True),
    'trainId': fields.String(example='628083/400978/773460/177369/80', description='internal id of the train'),
    'productCode': fields.Integer(example=1),
    'locations': fields.List(fields.Nested(m_location), description='list of intermediate locations', required=True),
    'zugfinderUrl': fields.Url(example='http://www.zugfinder.de/zuginfo.php?zugnr=IC_2376', description='more information on the train')
})

m_itinerary = api.model('Itinerary', {
    'travelDate': fields.Date(description="start date", required=True),
    'mapUrl': fields.Url(description='map with the complete route', example='http://maps.googleapis.com/maps/api/staticmap?size=800x800&scale=2&maptype=terrain&path=enc:}{q_IufrpAov@br`@c{eEjdnR??q_OmppG{of@akrB_bn@q}X&sensor=false&language=de', required=True),
    'referenceNumber': fields.String(example='TYFMQE', description='reference number', minLength=6, pattern='^[A-Z0-9]{6}$', required=True),
    'legs': fields.List(fields.Nested(m_leg), description='legs of the travel', required=True)
})

m_bookingrequest = api.model('BookingRequest', {
    'referenceNumber': fields.String(description='reference number of the booking ("Auftragsnummer")', minLength=6, pattern='^[A-Z0-9]{6}$', required=True),
    'lastName': fields.String(description='the last name of the booker', required=True)
})

m_booking_entry = api.model('BookingEntry', {
    'entryType': fields.String(description='type of the booking entry; values can be "Fahrschein" or "Reservierung"', example="Fahrschein", attribute='type', required=True),
    'travelDate': fields.Date(description='travel date', example='2017-05-01', attribute='travel_date', required=True),
    'description': fields.String(description='descriptive text for the booking entry', example='Einfache Fahrt, Flexpreis, 2. Kl., 2 Erw., BC 50', required=True),
    'voucherNumber': fields.Integer(description='voucher number of the booking entry', example=75133739, attribute='voucher_number', required=True),
    'price': fields.Float(min=0.0, description='price of the booking entry in EUR', example=39.90, required=True)
})

m_booking = api.model('Booking', {
    'referenceNumber': fields.String(description='reference number', example='TYFMQE', attribute='reference_number', required=True),
    'bookingDate': fields.Date(description='booking date', example='2017-04-20', attribute='booking_date', required=True),
    'booker': fields.String(description='name of the booker', example='Mustermann', required=True),
    'traveler': fields.String(description='name of the traveler', example='Mustermann', required=True),
    'state': fields.String(description='state of the booking; values can be "bearbeitet"', example="bearbeitet", required=True),
    'entries': fields.List(fields.Nested(m_booking_entry), description='entries of the booking', required=True)
})

########################################################################
# routes
########################################################################

@ns_itineraries.route('/<auftragsnummer>')
@api.doc(params={'auftragsnummer': 'a 6-character reference number'})
class ReferenceNumber(Resource):
    @api.response(200, 'success', m_itinerary)
    @api.response(404, 'itinerary not found')
    @cache.cached(timeout=3600)
    def get(self, auftragsnummer):
        """
        returns an itinerary
        
        [terms of use](https://www.bahn.de/p/view/home/agb/nutzungsbedingungen.shtml)
        """
        rp = Reiseplan(auftragsnummer)
        if rp.valid:
            return dict(rp)
        else:
            api.abort(404, error='itinerary not found', referenceNumber=auftragsnummer)

@ns_bookings.route('/')
class Bookin(Resource):
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
