"""
Models for ShopCart

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""

    pass


class PersistentBase:
    """Base class added persistent methods"""

    def create(self):
        """
        Creates a Shopcart to the database
        """
        logger.info("Creating %s", self.customer_id)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Shopcart to the database
        """
        logger.info("Updating %s", self.id)
        db.session.commit()

    @classmethod
    def init_db(cls, app):
        """Initializes the database session"""
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """Returns all of the records in the database"""
        logger.info("Processing all records")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a record by it's ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    def delete(self):
        """Removes a Shopcart from the data store"""
        logger.info("Deleting %s", self.id)
        deletedCnt = db.session.delete(self)
        db.session.commit()
        return deletedCnt


######################################################################
#  P R O D U C T   M O D E L
######################################################################
class Product(db.Model, PersistentBase):
    """
    Class that represents an Product
    """

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(260), nullable=False)  
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    shopcart_id = db.Column(db.Integer, db.ForeignKey("shopcart.id"), nullable=False)

    def __repr__(self):
        return "<Product %r id=[%s] shopcart[%s]>" % (
            self.name,
            self.id,
            self.shopcart_id,
        )

    def __str__(self):
        return "%s: %s, %s" % (
            self.name,
            self.quantity,
            self.price,
        )

    def serialize(self):
        """Serializes a Product into a dictionary"""
        return {
            "id": self.id,
            "shopcart_id": self.shopcart_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
        }

    def deserialize(self, data: dict):
        """
        Deserializes a Product from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.shopcart_id = data["shopcart_id"]
            self.name = data["name"]
            self.price = data["price"]
            self.quantity = data["quantity"]
            self.id = data["id"]
        except KeyError as error:
            raise DataValidationError("Invalid Product: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Product: body of request contained "
                "bad or no data " + error.args[0]
            )
        return self


######################################################################
#  S H O P C A R T   M O D E L
######################################################################
class Shopcart(db.Model, PersistentBase):
    """
    Class that represents an Shopcart
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    products = db.relationship("Product", backref="shopcart", passive_deletes=True)

    def __repr__(self):
        return "<Shopcart %r id=[%s]>" % (self.id, self.customer_id)

    def serialize(self):
        """Serializes a Shopcart into a dictionary"""
        shopcart = {
            "id": self.id,
            "customer_id": self.customer_id,
            "products": [],
        }
        for product in self.products:
            shopcart["products"].append(product.serialize())
        return shopcart

    def deserialize(self, data):
        """
        Deserializes a Shopcart from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.id = data["id"]
            self.customer_id = data["customer_id"]
            # handle inner list of products
            product_list = data.get("products")
            for json_product in product_list:
                product = Product()
                product.deserialize(json_product)
                self.products.append(product)
        except KeyError as error:
            raise DataValidationError("Invalid Shopcart: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Shopcart: body of request contained "
                "bad or no data - " + error.args[0]
            )
        return self

    @classmethod
    def find_by_customer_id(cls, customer_id):
        """Returns the Shopcart with the given customer id
        Args:
            customer_id (Integer): the id of the customer you want to match
        """
        logger.info("Processing id query for %s ...", customer_id)
        return cls.query.filter(cls.customer_id == customer_id).first()
