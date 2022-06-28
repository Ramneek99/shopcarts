"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase

# from unittest.mock import MagicMock, patch
from service import app
from service.models import db, Shopcart, Product
from service.utils import status  # HTTP Status Codes
from tests.factories import ShopCartFactory, ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/shopcarts"
PRODUCT_URL = "/product"
######################################################################
#  T E S T   C A S E S
######################################################################


class TestShopcartService(TestCase):
    """Shop Cart Service Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Shopcart.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Runs once before test suite"""
        pass

    def setUp(self):
        """Runs before each test"""
        db.session.query(Product).delete()
        db.session.query(Shopcart).delete()  # clean up the last tests
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        """Runs once after each test case"""
        db.session.remove()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_shopcarts(self, count):
        """Factory method to create shopcarts in bulk"""
        shopcarts = []
        for _ in range(count):
            shopcart = ShopCartFactory()
            resp = self.client.post(BASE_URL, json=shopcart.serialize())
            self.assertEqual(
                resp.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Shopcart",
            )
            new_shopcart = resp.get_json()
            shopcart.id = new_shopcart["id"]
            shopcarts.append(shopcart)
        return shopcarts

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the Home Page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_shopcart(self):
        """It should Read a single Shopcart"""
        # get the id of an account
        shopcart = self._create_shopcarts(1)[0]
        resp = self.client.get(
            f"{BASE_URL}/{shopcart.id}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["customer_id"], shopcart.customer_id)

    def test_get_shopcart_not_found(self):
        """It should not Read a shopcart that is not found"""
        resp = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_shopcart(self):
        """It should Create a new Shopcart"""
        shopcart = ShopCartFactory()
        resp = self.client.post(
            BASE_URL, json=shopcart.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_shopcart = resp.get_json()
        self.assertEqual(
            new_shopcart["customer_id"], shopcart.customer_id, "Names does not match"
        )
        self.assertEqual(
            new_shopcart["products"], shopcart.products, "Address does not match"
        )

        # Check that the location header was correct by getting it
        resp = self.client.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_shopcart = resp.get_json()
        self.assertEqual(
            new_shopcart["customer_id"], shopcart.customer_id, "Names does not match"
        )
        self.assertEqual(
            new_shopcart["products"], shopcart.products, "Address does not match"
        )

    def test_create_duplicate_shopcart(self):
        """It shouldn't Create duplicate shopcarts"""
        shopcart = ShopCartFactory()
        resp = self.client.post(
            BASE_URL, json=shopcart.serialize(), content_type="application/json"
        )
        shopcart = Shopcart()
        shopcart.deserialize(resp.get_json())
        product = ProductFactory()
        product.shopcart_id = shopcart.id
        logging.info("The new product is: %s" % product.serialize())
        logging.info("The new shopcart is: %s" % shopcart.serialize())
        resp = self.client.post(
            PRODUCT_URL, json=product.serialize(), content_type="application/json"
        )
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        new_shopcart = Shopcart()
        new_shopcart.deserialize(resp.get_json())
        logging.info("The new shopcart is: %s", resp.get_json())
        self.assertEqual(
            new_shopcart.products[0].serialize(),
            product.serialize(),
            "Product does not match",
        )
        logging.info("The shopcart in response: %s", resp.get_json())
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        resp = self.client.post(
            BASE_URL, json=shopcart.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            resp.get_json()["message"],
            f"409 Conflict: Shopcart {shopcart.customer_id} already exists",
        )

    def test_404_not_found_error(self):
        "It should raise 404 not found error"
        shopcart = ShopCartFactory()
        wrong_url = "shopcarT"
        resp = self.client.post(
            wrong_url, json=shopcart.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_405_method_not_allowed(self):
        """It should raise 405 method not allowed error"""
        resp = self.client.post(f"{BASE_URL}/0")
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_415_media_not_supported(self):
        """It should raise 415 media not supported error"""
        text = "Hello World"
        resp = self.client.post(BASE_URL, data=text, content_type="text/plain")
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_500_internal_server_error(self):
        text = "Hello World"
        resp = self.client.post(
            "/test_internal_server_error", data=text, content_type="text/plain"
        )
        self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_add_product(self):
        """It should Create a new product and add it to shopcart"""
        shopcart = ShopCartFactory()
        resp = self.client.post(
            BASE_URL, json=shopcart.serialize(), content_type="application/json"
        )
        shopcart = Shopcart()
        shopcart.deserialize(resp.get_json())
        product = ProductFactory()
        product.shopcart_id = shopcart.id
        logging.info("The new product is: %s" % product.serialize())
        logging.info("The new shopcart is: %s" % shopcart.serialize())
        resp = self.client.post(
            PRODUCT_URL, json=product.serialize(), content_type="application/json"
        )
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        new_shopcart = Shopcart()
        new_shopcart.deserialize(resp.get_json())
        logging.info("The new shopcart is: %s", resp.get_json())
        self.assertEqual(
            new_shopcart.products[0].serialize(),
            product.serialize(),
            "Product does not match",
        )

    def test_get_shopcart_list(self):
        """It should Get a list of shopcarts"""
        self._create_shopcarts(5)
        resp = self.client.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_get_shopcart_by_customer_id(self):
        """It should Get a shop cart by customer id"""
        shopcarts = self._create_shopcarts(3)
        resp = self.client.get(
            BASE_URL, query_string=f"customer_id={shopcarts[1].customer_id}"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data[0]["customer_id"], shopcarts[1].customer_id)

    def test_delete_product(self):
        """It should delete product from a shopcart"""
        shopcart = ShopCartFactory()
        resp = self.client.post(
            BASE_URL, json=shopcart.serialize(), content_type="application/json"
        )
        shopcart = Shopcart()
        shopcart.deserialize(resp.get_json())
        product = ProductFactory()
        product.shopcart_id = shopcart.id
        resp = self.client.post(
            PRODUCT_URL, json=product.serialize(), content_type="application/json"
        )
        product2 = ProductFactory()
        product2.shopcart_id = shopcart.id
        resp = self.client.post(
            PRODUCT_URL, json=product2.serialize(), content_type="application/json"
        )
        resp = self.client.delete(
            PRODUCT_URL, json=product2.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT, "Failed to delete a product")
        found_shop_cart = Shopcart()
        resp = self.client.get(
            BASE_URL, query_string=f"customer_id={shopcart.customer_id}"
        )
        logging.info("The shopcart after deletion is %s", resp.get_json())
        found_shop_cart.deserialize(resp.get_json()[0])
        self.assertEqual(len(found_shop_cart.products), 1)
        self.assertEqual(found_shop_cart.products[0].serialize(), product.serialize())
