"""
Test cases for YourResourceModel Model

"""
import logging
import os
import unittest
from datetime import date
from sqlalchemy import null
from werkzeug.exceptions import NotFound
from service.models import DataValidationError, ShopCart, db
from service import app
from tests.factories import ShopCartFactory 

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)

######################################################################
#  <your resource name>   M O D E L   T E S T   C A S E S
######################################################################


class TestYourResourceModel(unittest.TestCase):
    """Test Cases for YourResourceModel Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        ShopCart.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(ShopCart).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################
    def test_createShopCart(self):
        """This test will test the function to create a shopCart"""
        shopCart = ShopCartFactory()
        ShopCart.create(
            customer_id=shopCart.customer_id,
            product_id=shopCart.product_id,
            product_name=shopCart.product_name,
            quantity=shopCart.quantity,
            price=shopCart.price
        )
        shopCartFound = ShopCart.find(customer_id=shopCart.customer_id, product_id=shopCart.product_id)
        self.assertTrue(shopCartFound!=null)
        self.assertTrue(shopCartFound.customer_id==shopCart.customer_id)
        self.assertTrue(shopCartFound.product_id==shopCart.product_id)
        self.assertTrue(shopCartFound.product_name==shopCart.product_name)
        self.assertTrue(shopCartFound.quantity==shopCart.quantity)
        self.assertTrue(shopCartFound.price==shopCart.price)



    def test_XXXX(self):
        """It should always be true"""
        
        self.assertTrue(True)
