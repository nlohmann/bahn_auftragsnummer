# coding=utf-8

########################################################################
# Licensed under the MIT License <http://opensource.org/licenses/MIT>. #
# Copyright (c) 2017 Niels Lohmann <http://nlohmann.me>.               #
########################################################################

from flask_restplus import Resource
from app import cache, api
from app.reiseplan import reiseplan

ns = api.namespace('itineraries', description='Operations related to itineraries')

@ns.route('/<auftragsnummer>')
@api.doc(params={'auftragsnummer': 'a 6-character reference number'})
class ReferenceNumber(Resource):
    @api.doc(responses={200: 'success', 404: 'itinerary not found'})
    @cache.cached(timeout=3600)
    def get(self, auftragsnummer):
        """returns an itinerary"""
        rp = reiseplan(auftragsnummer)
        if rp:
            return rp
        else:
            api.abort(404, error='itinerary not found', referenceNumber=auftragsnummer)
