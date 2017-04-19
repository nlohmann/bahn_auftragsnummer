# coding=utf-8

########################################################################
# Licensed under the MIT License <http://opensource.org/licenses/MIT>. #
# Copyright (c) 2017 Niels Lohmann <http://nlohmann.me>.               #
########################################################################

from flask_restplus import Resource, fields
from app import cache, api
from app.reiseplan import Reiseplan

ns = api.namespace('itineraries', description='Operations related to itineraries')

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
    'referenceNumber': fields.String(example='TYFMQE', description='reference number', minLength=6, pattern='^[A-F0-9]{6}$', required=True),
    'legs': fields.List(fields.Nested(m_leg), description='legs of the travel', required=True)
})

@ns.route('/<auftragsnummer>')
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
