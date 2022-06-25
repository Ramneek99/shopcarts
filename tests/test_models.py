"""
Test cases for YourResourceModel Model

"""
import logging
import os
import unittest
# from sqlalchemy import null
# from werkzeug.exceptions import NotFound
# from service.models import DataValidationError
from service.models import Shopcart, db
from service import app
from tests.factories import ShopCartFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  S H O P C A R T   M O D E L   T E S T   C A S E S
######################################################################
class TestShopCart(unittest.TestCase):
    """Test Cases for ShopCart Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Shopcart.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        pass

    def setUp(self):
        """This runs before each test"""
        db.session.query(Shopcart).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################
    def test_create_a_shopcart(self):
        """It should Create an Shopcart and assert that it exists"""
        fake_shopcart = ShopCartFactory()
        shopcart = Shopcart(
            customer_id=fake_shopcart.customer_id,
        )
        self.assertIsNotNone(shopcart)
        self.assertEqual(shopcart.id, None)

    ''' def test_create_a_shopcart(self):
        """It should Create a pet and assert that it exists"""
        pet = ShopCart(customer_id=0, product_id=2, product_name="apple", price=3.99)
        self.assertEqual(str(pet), "customer_id: 0, items: apple")
        self.assertTrue(pet is not None)
        self.assertEqual(pet.id, None)
        self.assertEqual(pet.name, "Fido")
        self.assertEqual(pet.category, "dog")
        self.assertEqual(pet.available, True)
        self.assertEqual(pet.gender, Gender.MALE)
        pet = Pet(name="Fido", category="dog", available=False, gender=Gender.FEMALE)
        self.assertEqual(pet.available, False)
        self.assertEqual(pet.gender, Gender.FEMALE)

    def test_add_a_pet(self):
        """It should Create a pet and add it to the database"""
        pets = Pet.all()
        self.assertEqual(pets, [])
        pet = Pet(name="Fido", category="dog", available=True, gender=Gender.MALE)
        self.assertTrue(pet is not None)
        self.assertEqual(pet.id, None)
        pet.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(pet.id)
        pets = Pet.all()
        self.assertEqual(len(pets), 1)'''

    '''def test_createShopCart(self):
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
        self.assertTrue(shopCartFound.price==shopCart.price)'''

    def test_XXXX(self):
        """It should always be true"""

        self.assertTrue(True)
