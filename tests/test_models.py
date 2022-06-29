"""
Test cases for YourResourceModel Model

"""
import logging
import os
import unittest

# from sqlalchemy import null
# from werkzeug.exceptions import NotFound
from service.models import DataValidationError
from service.models import Product, Shopcart, db
from service import app
from tests.factories import ShopCartFactory, ProductFactory

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
        db.session.query(Product).delete()
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

    def test_add_a_shopcart(self):
        """It should Create a shopcart and add it to the database"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])
        shopcart = ShopCartFactory()
        shopcart.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(shopcart.id)
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)

    def test_read_shopcart(self):
        """It should Read an shopcart"""
        shopcart = ShopCartFactory()
        shopcart.create()

        # Read it back
        found_shopcart = Shopcart.find(shopcart.id)
        self.assertEqual(found_shopcart.id, shopcart.id)
        self.assertEqual(found_shopcart.customer_id, shopcart.customer_id)
        self.assertEqual(found_shopcart.products, [])

    def test_delete_an_shopcart(self):
        """It should Delete an shopcart from the database"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])
        shopcart = ShopCartFactory()
        shopcart.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(shopcart.id)
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)
        shopcart = shopcarts[0]
        shopcart.delete()
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 0)

    def test_list_all_shopcarts(self):
        """It should List all Shopcarts in the database"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])
        for _ in range(5):
            shopcart = ShopCartFactory()
            shopcart.create()
        # Assert that there are now 5 shopcarts in the database
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 5)

    def test_find_by_customer_id(self):
        """It should Find an Shopcart by customer id"""
        shopcart = ShopCartFactory()
        shopcart.create()

        # Fetch it back by name
        same_shopcart = Shopcart.find_by_customer_id(shopcart.customer_id)
        self.assertEqual(same_shopcart.id, shopcart.id)
        self.assertEqual(same_shopcart.customer_id, shopcart.customer_id)

    def test_serialize_a_shopcart(self):
        """It should Serialize a shopcart"""
        shopcart = ShopCartFactory()
        product = ProductFactory()
        shopcart.products.append(product)
        serial_shopcart = shopcart.serialize()
        self.assertEqual(serial_shopcart["id"], shopcart.id)
        self.assertEqual(serial_shopcart["customer_id"], shopcart.customer_id)
        self.assertEqual(len(serial_shopcart["products"]), 1)
        products = serial_shopcart["products"]
        self.assertEqual(products[0]["id"], product.id)
        self.assertEqual(products[0]["shopcart_id"], product.shopcart_id)
        self.assertEqual(products[0]["name"], product.name)
        self.assertEqual(products[0]["price"], product.price)
        self.assertEqual(products[0]["quantity"], product.quantity)

    def test_deserialize_a_shopcart(self):
        """It should Deserialize a shopcart"""
        shopcart = ShopCartFactory()
        shopcart.products.append(ProductFactory())
        shopcart.create()
        serial_shopcart = shopcart.serialize()
        new_shopcart = Shopcart()
        new_shopcart.deserialize(serial_shopcart)
        self.assertEqual(new_shopcart.customer_id, shopcart.customer_id)

    def test_deserialize_with_key_error(self):
        """It should not Deserialize an account with a KeyError"""
        shopcart = Shopcart()
        self.assertRaises(DataValidationError, shopcart.deserialize, {})

    def test_deserialize_with_type_error(self):
        """It should not Deserialize an account with a TypeError"""
        shopcart = Shopcart()
        self.assertRaises(DataValidationError, shopcart.deserialize, [])

    def test_deserialize_address_key_error(self):
        """It should not Deserialize an address with a KeyError"""
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, {})

    def test_deserialize_address_type_error(self):
        """It should not Deserialize an address with a TypeError"""
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, [])

    def test_add_shopcart_product(self):
        """It should Create a shopcart with a product and add it to the database"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])
        shopcart = ShopCartFactory()
        product = ProductFactory(shopcart=shopcart)
        shopcart.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(shopcart.id)
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)

        new_shopcart = Shopcart.find_by_customer_id(shopcart.customer_id)
        self.assertEqual(new_shopcart.products[0].name, product.name)

        product2 = ProductFactory()
        shopcart.products.append(product2)
        shopcart.update()

        new_shopcart = Shopcart.find_by_customer_id(shopcart.customer_id)
        self.assertEqual(len(new_shopcart.products), 2)
        self.assertEqual(new_shopcart.products[1].name, product2.name)

    def test_update_shopcart_product(self):
        """It should Update a shopcart's product"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])

        shopcart = ShopCartFactory()
        product = ProductFactory(shopcart=shopcart)
        shopcart.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(shopcart.id)
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)

        # Fetch it back
        shopcart = Shopcart.find_by_customer_id(shopcart.customer_id)
        old_product = shopcart.products[0]
        print("%r", old_product)
        self.assertEqual(old_product.quantity, product.quantity)
        # Change the city
        old_product.quantity = 40
        shopcart.update()

        # Fetch it back again
        shopcart = Shopcart.find_by_customer_id(shopcart.customer_id)
        product = shopcart.products[0]
        self.assertEqual(product.quantity, 40)

    def test_delete_shopcart_product(self):
        """It should Delete a shopcart's product"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])

        shopcart = ShopCartFactory()
        product = ProductFactory(shopcart=shopcart)
        shopcart.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(shopcart.id)
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)

        # Fetch it back
        shopcart = shopcart.find_by_customer_id(shopcart.customer_id)
        product = shopcart.products[0]
        product.delete()
        shopcart.update()

        # Fetch it back again
        shopcart = Shopcart.find_by_customer_id(shopcart.customer_id)
        self.assertEqual(len(shopcart.products), 0)
