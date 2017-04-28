# coding=utf-8

########################################################################
# Licensed under the MIT License <http://opensource.org/licenses/MIT>. #
# Copyright (c) 2017 Niels Lohmann <http://nlohmann.me>.               #
########################################################################

from flask_restplus import fields
from app import api

m_location = api.model('Location', {
    'coordinates': fields.Nested(
        api.model('Coordinates', {
            'latitude': fields.Float(min=-90, max=90, example=54.078242, required=True),
            'longitude': fields.Float(min=-180, max=180, example=12.131078, required=True)
        })
    ),
    'arrival': fields.DateTime(description='date and time of the arrival', example='2017-01-06'),
    'departure': fields.DateTime(description='date and time of the departure', example='2017-01-06'),
    'stationId': fields.String(description='station id', example='8000044'),
    'type': fields.String(description='location type', example='STATION', required=True),
    'name': fields.String(description='location name', example='Bonn Hbf', required=True)
})

m_leg = api.model('Leg', {
    'mapUrl': fields.Url(description='map with the leg\'s route',
                         example='http://maps.googleapis.com/maps/api/staticmap?size=800x800&scale=2&maptype=terrain&path=enc:}{q_IufrpAov@br`@c{eEjdnR&sensor=false&language=de',
                         required=True),
    'type': fields.String(example='JOURNEY', required=True),
    'name': fields.String(description='train name', example='IC  2216'),
    'transport': fields.String(description='type of the current transportation', example='ic', required=True),
    'trainId': fields.String(description='internal id of the train', example='628083/400978/773460/177369/80'),
    'productCode': fields.Integer(example=1),
    'locations': fields.List(fields.Nested(m_location), description='list of intermediate locations', required=True),
    'zugfinderUrl': fields.Url(description='more information on the train',
                               example='http://www.zugfinder.de/zuginfo.php?zugnr=IC_2376')
})

m_itinerary = api.model('Itinerary', {
    'travelDate': fields.Date(description="start date", example='2017-02-23', required=True),
    'mapUrl': fields.Url(description='map with the complete route',
                         example='http://maps.googleapis.com/maps/api/staticmap?size=800x800&scale=2&maptype=terrain&path=enc:}{q_IufrpAov@br`@c{eEjdnR??q_OmppG{of@akrB_bn@q}X&sensor=false&language=de',
                         required=True),
    'referenceNumber': fields.String(description='reference number', example='TYFMQE', minLength=6,
                                     pattern='^[A-HK-Z1-46-9]{6}$', required=True),
    'legs': fields.List(fields.Nested(m_leg), description='legs of the travel', required=True)
})

m_bookingrequest = api.model('BookingRequest', {
    'referenceNumber': fields.String(description='reference number of the booking ("Auftragsnummer")', example='TYFMQE',
                                     minLength=6, pattern='^[A-HK-Z1-46-9]{6}$', required=True),
    'lastName': fields.String(description='the last name of the booker', example='Mustermann', required=True)
})

m_booking_entry = api.model('BookingEntry', {
    'entryType': fields.String(description='type of the booking entry; values can be "Fahrschein" or "Reservierung"',
                               example="Fahrschein", attribute='type', required=True),
    'travelDate': fields.Date(description='travel date', example='2017-05-01', attribute='travel_date', required=True),
    'description': fields.String(description='descriptive text for the booking entry',
                                 example='Einfache Fahrt, Flexpreis, 2. Kl., 2 Erw., BC 50', required=True),
    'voucherNumber': fields.Integer(description='voucher number of the booking entry', example=75133739,
                                    attribute='voucher_number', required=True),
    'price': fields.Float(min=0.0, description='price of the booking entry in EUR', example=39.90, required=True)
})

m_booking = api.model('Booking', {
    'referenceNumber': fields.String(description='reference number', example='TYFMQE', attribute='reference_number',
                                     pattern='^[A-HK-Z1-46-9]{6}$', required=True),
    'bookingDate': fields.Date(description='booking date', example='2017-04-20', attribute='booking_date',
                               required=True),
    'booker': fields.String(description='name of the booker', example='Mustermann', required=True),
    'traveler': fields.String(description='name of the traveler', example='Mustermann', required=True),
    'state': fields.String(description='state of the booking; values can be "bearbeitet"', example="bearbeitet",
                           required=True),
    'entries': fields.List(fields.Nested(m_booking_entry), description='entries of the booking', required=True)
})

m_form_request = api.model('FormRequest', {
    'travelStartDate': fields.Date(description='travel start date', example='2017-05-01'),
    'startStation': fields.String(description='start station', example='Hamburg Hbf'),
    'startStationPlannedDeparture': fields.DateTime(description='planned departure at start station',
                                                    example='2017-05-01T13:01:00'),
    'travelEndDate': fields.Date(description='travel end date', example='2017-05-01'),
    'endStation': fields.String(description='end station', default=u'Köln Hbf'),
    'startStationPlannedArrival': fields.DateTime(description='planned arrival at end station',
                                                  example='2017-05-01T17:09:00'),
    'startStationActualArrival': fields.DateTime(description='actual arrival at end station',
                                                 example='2017-05-01T21:09:00'),
    'trainArrived': fields.String(description='last used train', example='ICE 554', pattern=r'^[A-Z]+ [0-9]+$'),
    'trainFirstDelayed': fields.String(description='first delayed train', example='ICE 558', pattern=r'^[A-Z]+ [0-9]+$'),
    'trainFirstDelayedPlannedDeparture': fields.DateTime(description='planned departure time of the first delayed train',
                                                         example='2017-05-01T14:31:00'),
    'stationMissedTrain': fields.String(description='station where a train was missed', example='Hannover Hbf'),
    'stationLastChange': fields.String(description='station where trains where last changed', example='Hannover Hbf'),
    'stationTripAborted': fields.String(description='station where the trip was aborted', example='Hannover Hbf'),
    'stationTripSuspended': fields.String(description='station where the trip was suspended', example='Hannover Hbf'),
    'gender': fields.String(description='gender', enum=['Herr', 'Frau']),
    'title': fields.String(description='title', example='Dr.'),
    'company': fields.String(description='company', example='ACME'),
    'firstName': fields.String(description='first name', example='Max'),
    'lastName': fields.String(description='last name', example='Mustermann'),
    'co': fields.String(description='c/o', example='Norbert Nachname'),
    'phone': fields.String(description='phone number for further inquiries', example='030/5554422'),
    'street': fields.String(description='street name', example=u'Musterstraße'),
    'houseNumber': fields.String(description='house number', example='23'),
    'state': fields.String(description='state (unless D)', example='NL'),
    'postcode': fields.String(description='postcode', example='12345'),
    'city': fields.String(description='place of residence', example='Berlin'),
    'numberBahncard100': fields.String('number of BahnCard 100', example='7081411012345678'),
    'numberSeasonTicket': fields.String('number of a season ticket', example='7081411012345678'),
    'dateOfBirth': fields.Date(description='date of birth (needed when BahnCard 100 number is given)',
                               example='1981-05-10'),
    'email': fields.String(description='email address (for marketing purposes)', example='m.mustermann@t-online.de'),
    'marketingResearch': fields.Boolean(description='whether marketing research is allowed', example=False),
    'compensation': fields.String(description='how compensation should be made', enum=['transfer', 'voucher'],
                                  example='transfer'),
    'accountHolder': fields.String(description='last name/first name of the account holder', example='Mustermann, Max'),
    'iban': fields.String(description='IBAN', example='DE89 3704 0044 0532 0130 00'),
    'bic': fields.String(description='BIC', example='PBNKDEFF')
})
