# coding=utf-8

########################################################################
# Licensed under the MIT License <http://opensource.org/licenses/MIT>. #
# Copyright (c) 2017 Niels Lohmann <http://nlohmann.me>.               #
########################################################################

from flask import Flask
from flask_compress import Compress
from flask_cache import Cache
from flask_restplus import Api

# create Flask app
app = Flask(__name__)

# add compression
Compress(app)
# add caching
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# create a Flask-RESTPlus API
api = Api(app, version='0.0.7', catch_all_404s=True, prefix='/api', validate=True,
          title='Deutsche Bahn Reiseplan', description='API for the itineraries of the Deutsche Bahn',
          terms_url='https://www.bahn.de/p/view/home/agb/nutzungsbedingungen.shtml',
          contact='Niels Lohmann', contact_email='mail@nlohmann.me',
          contact_url='https://github.com/nlohmann/bahn_auftragsnummer')

# initial UI expansion state
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'

# load views
from app import views
