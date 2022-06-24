"""
Test cases for YourResourceModel Model

"""
import unittest
from datetime import date
from sqlalchemy import null
from werkzeug.exceptions import NotFound
from service.models import Pet, Gender, DataValidationError, ShopCart, Shopcart, db
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
        db.session.query(Pet).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################
    def test_createItem(self):
        """This test will test the function to create a shopCart"""
        customer_id = 0
        product_id = 123
        product_name = "iPhone13"
        quantity = 1
        price = 80.0
        ShopCart.create(
            customer_id=customer_id,
            product_id=product_id,
            product_name=product_name,
            quantity=quantity,
            price=price
        )
        shopCart = ShopCart.find(customer_id=customer_id, product_id=product_id)
        self.assertTrue(shopCart!=null)
        self.assertTrue(shopCart.customer_id==customer_id)
        self.assertTrue(shopCart.product_id==product_id)
        self.assertTrue(shopCart.product_name==product_name)
        self.assertTrue(shopCart.quantity==quantity)
        self.assertTrue(shopCart.price==price)



    def test_XXXX(self):
        """It should always be true"""
        
        self.assertTrue(True)
