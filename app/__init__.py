# coding=utf-8

########################################################################
# Licensed under the MIT License <http://opensource.org/licenses/MIT>. #
# Copyright (c) 2017 Niels Lohmann <http://nlohmann.me>.               #
########################################################################

from flask import Flask
from flask_compress import Compress
from flask_cache import Cache

# create Flask app
app = Flask(__name__)

# add compression
Compress(app)
# add caching
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# load views
from app import views
