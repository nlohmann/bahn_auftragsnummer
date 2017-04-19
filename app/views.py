# coding=utf-8

########################################################################
# Licensed under the MIT License <http://opensource.org/licenses/MIT>. #
# Copyright (c) 2017 Niels Lohmann <http://nlohmann.me>.               #
########################################################################

from flask_restplus import Resource, fields
from app import cache, api
from app.reiseplan import reiseplan

ns = api.namespace('itineraries', description='Operations related to itineraries')

m_location = api.model('Location', {
    'x': fields.String(example='7097136', description='longitude'),
    'y': fields.String(example='50732008', description='latitude'),
    'evaId': fields.String(example='8000044', description='station id'),
    'locType': fields.String(example='STATION', description='location type'),
    'count': fields.String(example='0', description='location index'),
    'name': fields.String(example='Bonn Hbf', description='location name'),
    'icon': fields.String(example='ic', description='icon type of the current transport'),
    'disabled': fields.String(example=''),
    'dep': fields.String(example='10:46', description='departure time'),
    'arr': fields.String(example='10:44', description='arrival time'),
    'infocontent': fields.String(example="<div class='bold pointer' onclick='setActiveStation(0, 8000044,\"10:46\",\"no\")'>Bonn Hbf</div>IC  2216 ab 10:46, Gleis 2 ")
})

m_section = api.model('Section', {
    'type': fields.String(example='JOURNEY'),
    'name': fields.String(example='IC  2216', description='train name'),
    'icon': fields.String(example='ic', description='icon type of the current transportation'),
    'trainId': fields.String(example='628083/400978/773460/177369/80'),
    'productcode': fields.String(example='1'),
    'locations': fields.List(fields.Nested(m_location), description='list of intermediate locations')

})

m_itinerary = api.model('Itinerary', {
    'name': fields.String(example='C0-0'),
    'date': fields.String(example='25.12.2016', description='start date'),
    'referenceNumner': fields.String('TYFMQE', description='reference number'),
    'sections': fields.List(fields.Nested(m_section), description='legs of the travel')
})

@ns.route('/<auftragsnummer>')
@api.doc(params={'auftragsnummer': 'a 6-character reference number'})
class ReferenceNumber(Resource):
    @api.response(200, 'success', m_itinerary)
    @api.response(404, 'itinerary not found')
    @cache.cached(timeout=3600)
    def get(self, auftragsnummer):
        """returns an itinerary"""
        rp = reiseplan(auftragsnummer)
        if rp:
            return rp
        else:
            api.abort(404, error='itinerary not found', referenceNumber=auftragsnummer)
