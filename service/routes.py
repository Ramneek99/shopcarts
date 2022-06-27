"""
My Service

Describe what your service does here
"""

from flask import jsonify, request, url_for, abort, make_response

# , Flask
from .utils import status  # HTTP Status Codes
from service.models import Shopcart, Product

# Import Flask application
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Shop Cart REST API Service",
            version="1.0",
            paths=url_for("create_shopcarts", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
# RETRIEVE AN ACCOUNT
######################################################################
@app.route("/shopcarts/<int:shopcart_id>", methods=["GET"])
def get_shopcarts(shopcart_id):
    """
    Retrieve a shopcart of a customer
    This endpoint will return a shopcart based on it's id
    """
    app.logger.info("Request for Shopcart with id: %s", shopcart_id)
    shopcart = Shopcart.find(shopcart_id)
    if not shopcart:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Shopcart with id '{shopcart_id}' could not be found.",
        )

    return make_response(jsonify(shopcart.serialize()), status.HTTP_200_OK)


######################################################################
# CREATE A NEW SHOPCART
######################################################################
@app.route("/shopcarts", methods=["POST"])
def create_shopcarts():
    """
    Creates a Shopcart
    This endpoint will create a Shop Cart based the data in the body that is posted
    """
    app.logger.info("Request to create a Shop Cart")
    check_content_type("application/json")
    shopcart = Shopcart()
    shopcart.deserialize(request.get_json())
    shopcart.create()
    message = shopcart.serialize()
    location_url = url_for("get_shopcarts", shopcart_id=shopcart.id, _external=True)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# ADD A NEW PRODUCT
######################################################################
@app.route("/product", methods=["POST"])
def add_product():
    """
    Add a Product to a existed Shopcart
    This endpoint will add a product to a given shopcart based on the posted data in the body
    """
    app.logger.info("Request to add a Product to a Shop Cart")
    check_content_type("application/json")
    product = Product()
    product.deserialize(request.get_json())
    Shopcart.add_product(product.shopcart_id, product)
    shopCart = Shopcart.find(product.shopcart_id)
    message = shopcart.serialize()
    location_url = url_for("add_product", shopcart_id=shopcart.id, _external=True)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )


def init_db():
    """Initializes the SQLAlchemy app"""
    global app
    Shopcart.init_db(app)
