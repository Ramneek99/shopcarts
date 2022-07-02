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

import logging


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
            paths=url_for("list_shopcarts", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
# RETRIEVE A SHOP CART
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
            status.HTTP_400_BAD_REQUEST,
            f"Shopcart with id '{shopcart_id}' could not be found.",
        )

    return make_response(jsonify(shopcart.serialize()), status.HTTP_200_OK)


######################################################################
# UPDATE AN EXISTING SHOPCART
######################################################################
@app.route("/shopcarts/<int:customer_id>", methods=["PUT"])
def update_shopcarts(customer_id):
    """
    Update a Shopcart
    This endpoint will update an Account based the body that is posted
    """
    app.logger.info("Request to update shopcart with id: %s", customer_id)
    check_content_type("application/json")
    shopcart = Shopcart.find_by_customer_id(customer_id)
    if not shopcart:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Shopcart with id '{customer_id}' was not found.",
        )

    shopcart.deserialize(request.get_json())
    shopcart.customer_id = customer_id
    shopcart.update()
    return make_response(jsonify(shopcart.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE A SHOPCART
######################################################################
@app.route("/shopcarts/<int:customer_id>", methods=["DELETE"])
def delete_shopcarts(customer_id):
    """
    Delete a Shopcart
    This endpoint will delete a Shopcart based the id specified in the path
    """
    app.logger.info("Request to delete shopcart with id: %s", customer_id)
    shopcart = Shopcart.find_by_customer_id(customer_id)
    if shopcart:
        shopcart.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
# CREATE A NEW SHOP CART
######################################################################
@app.route("/shopcarts/<int:customer_id>", methods=["POST"])
def create_shopcarts(customer_id):
    """
    Creates a Shopcart
    This endpoint will create a Shop Cart based the data in the body that is posted
    """
    app.logger.info("Request to create a Shop Cart")
    check_content_type("application/json")
    shopcart = Shopcart()
    shopcart.deserialize(request.get_json())
    found_shop_cart = Shopcart.find_by_customer_id(shopcart.customer_id)
    logging.info("To create shopcart with customer_id: %d", shopcart.customer_id)
    if found_shop_cart is not None:
        logging.info("Found shopcart: %s", type(found_shop_cart))
        abort(
            status.HTTP_409_CONFLICT, f"Shopcart {shopcart.customer_id} already exists"
        )
    shopcart.create()
    shopcart.customer_id = customer_id
    message = Shopcart.find_by_customer_id(shopcart.customer_id).serialize()
    location_url = url_for("get_shopcarts", shopcart_id=shopcart.id, _external=True)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


######################################################################
# LIST ALL PRODUCTS OF A GIVEN SHOP CART
######################################################################
@app.route("/shopcarts/<int:customer_id>/products", methods=["GET"])
def list_products(customer_id):
    """Return all of products of a given shopcart"""
    app.logger.info("Request for reading items of a given shop cart")
    shopcart = Shopcart().find_by_customer_id(customer_id)
    # If the shopcart does not exist, return 400 BAD REQUEST ERROR
    if not shopcart:
        abort(
            status.HTTP_400_BAD_REQUEST,
            f"Shopcart with id '{customer_id}' could not be found.",
        )
    results = [product.serialize() for product in shopcart.products]
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# RETRIEVE AN PRODUCT FROM SHOPCART
######################################################################
@app.route("/shopcarts/<int:customer_id>/products/<int:product_id>", methods=["GET"])
def get_products(customer_id, product_id):
    """
    Get an Address
    This endpoint returns just an address
    """
    app.logger.info(
        "Request to retrieve Product %s for CUSTOMER id: %s", (product_id, customer_id)
    )

    product = Product.find(product_id)
    if not product:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Shopcart with id '{product_id}' could not be found.",
        )

    return make_response(jsonify(product.serialize()), status.HTTP_200_OK)


######################################################################
# ADD A Product TO A shopcart
######################################################################
@app.route("/shopcarts/<int:customer_id>/products", methods=["POST"])
def add_products(customer_id):
    """
    Create a Product on a Shopcart
    This endpoint will add a product to a shopcart
    """
    app.logger.info(
        "Request to create a Products for Shopcart with id: %s", customer_id
    )
    check_content_type("application/json")

    shopcart = Shopcart().find_by_customer_id(customer_id)
    if not shopcart:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Shopcart with id '{customer_id}' could not be found.",
        )

    product = Product()
    product.deserialize(request.get_json())
    shopcart.products.append(product)
    shopcart.update()
    message = product.serialize()
    return make_response(jsonify(message), status.HTTP_201_CREATED)


######################################################################
# DELETE A Product
######################################################################
@app.route("/shopcarts/<int:customer_id>/products/<int:product_id>", methods=["DELETE"])
def delete_products(customer_id, product_id):
    """
    Delete a Product
    This endpoint will delete a Product based the id specified in the path
    """
    app.logger.info(
        "Request to delete Product %s for Customer id: %s", (product_id, customer_id)
    )

    product = Product().find(product_id)
    if product:
        product.delete()

    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
# UPDATE A Product
######################################################################
@app.route(
    "/shopcarts/<int:customer_id>/products/<int:product_id>",
    methods=["PUT"],
)
def update_products(customer_id, product_id):
    """
    Update a Product
    This endpoint will update a product based the body that is posted
    """
    app.logger.info(
        "Request to update product %s for customer id: %s", (product_id, customer_id)
    )
    check_content_type("application/json")

    product = Product.find(product_id)
    if not product:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Shopcart with id '{product_id}' could not be found.",
        )

    product.deserialize(request.get_json())
    product.id = product_id
    product.update()
    return make_response(jsonify(product.serialize()), status.HTTP_200_OK)


######################################################################
# LIST ALL SHOP CARTS
######################################################################
@app.route("/shopcarts", methods=["GET"])
def list_shopcarts():
    """Returns all of the Shopcarts"""
    app.logger.info("Request for Shop Cart list")
    customer_id = request.args.get("customer_id")
    results = []
    if customer_id:
        shopcarts = Shopcart.find_by_customer_id(customer_id)
        results = [shopcarts.serialize()]
    else:
        shopcarts = Shopcart.all()
        results = [shopcart.serialize() for shopcart in shopcarts]
    return make_response(jsonify(results), status.HTTP_200_OK)


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
