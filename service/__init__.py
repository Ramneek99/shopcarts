# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# spell: ignore Rofrano restx gunicorn
"""
Microservice module

This module contains the microservice code for
    service
    models
"""
import sys
from flask import Flask
from flask_restx import Api
from service.utils import log_handlers
from service import config

# NOTE: Do not change the order of this code
# The Flask app must be created
# BEFORE you import modules that depend on it !!!

# Create the Flask app
app = Flask(__name__)
app.config.from_object(config)

app.url_map.strict_slashes = False

######################################################################
# Configure Swagger before initializing it
######################################################################
api = Api(
    app,
    version="1.0.0",
    title="Shop Cart Demo REST API Service",
    description="This is a sample server Shop Cart server.",
    default="shopcarts",
    default_label="Shop Cart shop operations",
    doc="/apidocs",  # default also could use doc='/apidocs/'
    prefix="/api",
    format_checker=("str")
)

# Import the routes After the Flask app is created
from service import routes  # noqa: E402, E261
from .utils import error_handlers, cli_commands  # noqa: F401 E402


# Set up logging for production
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  S H O P C A R T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")
try:
    routes.init_db()  # make our SQLAlchemy tables
except Exception as error:
    app.logger.critical("%s: Cannot continue", error)
    # gunicorn requires exit code 4 to stop spawning workers when they die
    sys.exit(4)
app.logger.info("Service initialized!")
