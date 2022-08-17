"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase

from mockito import when
from mockito import mock
import requests

# from unittest.mock import MagicMock, patch
from service import app, routes
from service.models import db, Shopcart, Product
from service.utils import status  # HTTP Status Codes
from tests.factories import ShopCartFactory, ProductFactory
from urllib.parse import quote_plus
from flask import Flask
logging.disable(logging.CRITICAL)

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)

BASE_URL = "api/shopcarts"
PRODUCT_URL = "/product"

CONTENT_TYPE_JSON = "application/json"
######################################################################
#  T E S T   C A S E S
######################################################################


class CustomFlask(Flask):
    """Custom Flask app for test"""
    def test_request_context(self, *args, **kwargs):
        headers = kwargs.setdefault("headers", {})
        headers.setdefault("Content-Type", CONTENT_TYPE_JSON)
        return super().test_request_context(*args, **kwargs)


class TestShopcartService(TestCase):
    """Shop Cart Service Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        routes.init_db()

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

    def _create_shopcarts(self, count: int = 1) -> list:
        """Factory method to create shopcarts in bulk"""
        shopcarts = []
        for _ in range(count):
            shopcart = ShopCartFactory()
            resp = self.client.post(
                f"{BASE_URL}/{shopcart.id}",
                json=shopcart.serialize(),
                content_type=CONTENT_TYPE_JSON,
            )
            self.assertEqual(
                resp.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Shopcart",
            )
            new_shopcart = resp.get_json()
            shopcart.id = new_shopcart["id"]
            shopcarts.append(shopcart)
        return shopcarts

    def _find_shopcarts(self, shopcarts):
        """Factory method to find shopcarts in bulk"""
        rst = []
        for shopcart in shopcarts:
            resp = self.client.get(
                f"{BASE_URL}/{shopcart.id}", content_type="application/json"
            )
            rst.append(shopcart.deserialize(resp.get_json()))
        return rst

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the Home Page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_shopcart(self):
        """It should Read a single Shopcart"""
        # get the id of an shopcart
        shopcart = self._create_shopcarts(1)[0]
        resp = self.client.get(
            f"{BASE_URL}/{shopcart.id}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["id"], shopcart.id)

    def test_get_shopcart_not_found(self):
        """It should not Read a shopcart that is not found"""
        resp = self.client.get(f"{BASE_URL}/0", content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_product_with_no_id(self):
        """Create a product without a name"""
        """It should Add a product to a shopcart"""
        shopcart = self._create_shopcarts(1)[0]
        product = ProductFactory()
        new_product = product.serialize()
        del new_product["name"]
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id}/products",
            json=new_product,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_shopcart(self):
        """It should Create a new Shopcart"""
        shopcart = ShopCartFactory()
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id}",
            json=shopcart.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_shopcart = resp.get_json()
        self.assertEqual(new_shopcart["id"], shopcart.id, "Names does not match")
        self.assertEqual(
            new_shopcart["products"], shopcart.products, "Product does not match"
        )

        # Check that the location header was correct by getting it
        resp = self.client.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_shopcart = resp.get_json()
        self.assertEqual(new_shopcart["id"], shopcart.id, "Names does not match")
        self.assertEqual(
            new_shopcart["products"], shopcart.products, "Address does not match"
        )
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id}",
            json=shopcart.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_409_CONFLICT)

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
        resp = self.client.post(f"{BASE_URL}")
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    '''
    def test_415_media_not_supported(self):
        """It should raise 415 media not supported error"""
        text = "Hello World"
        resp = self.client.post(f"{BASE_URL}/0", data=text, content_type="text/plain")
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    '''

    def test_500_error_handler(self):
        """It should return 500 error"""
        response = mock(
            {
                "status_code": 500,
            },
            spec=requests.Response,
        )
        when(requests).get(f"{BASE_URL}/886").thenReturn(response)
        app.config["TESTING"] = False
        response = requests.get(f"{BASE_URL}/886")
        app.config["TESTING"] = True
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_add_product(self):
        """It should Add a product to a shopcart"""
        shopcart = self._create_shopcarts(1)[0]
        product = ProductFactory()
        resp = self.client.post(
            f"{BASE_URL}/123/products",
            json=product.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id}/products",
            json=product.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["shopcart_id"], shopcart.id)
        self.assertEqual(data["name"], product.name)
        self.assertEqual(data["quantity"], product.quantity)
        self.assertEqual(data["price"], product.price)

    def test_get_shopcart_list(self):
        """It should Get a list of shopcarts"""
        self._create_shopcarts(5)
        resp = self.client.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)
        resp = self.client.get(f"{BASE_URL}?id={data[0]['id']}")

    def test_get_shopcart_by_id(self):
        """It should Get a shop cart by customer id"""
        shopcarts = self._create_shopcarts(3)
        resp = self.client.get(f"{BASE_URL}/{shopcarts[1].id}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["id"], shopcarts[1].id)

    def test_read_items(self):
        """It should read all the items from a given shopcart"""
        shopcart = self._create_shopcarts(1)[0]
        product_list = ProductFactory.create_batch(2)
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id}/products",
            json=product_list[0].serialize(),
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id}/products",
            json=product_list[1].serialize(),
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        resp = self.client.get(f"{BASE_URL}/123/products")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        resp = self.client.get(f"{BASE_URL}/{shopcart.id}/products")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        self.assertEqual(len(data), 2)

    def test_delete_product(self):
        """It should Delete a Product"""
        shopcart = self._create_shopcarts(1)[0]
        product = ProductFactory()
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id}/products",
            json=product.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data["id"])
        product_id = data["id"]

        # send delete request
        resp = self.client.delete(
            f"{BASE_URL}/{shopcart.id}/products/{product_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        # retrieve it back and make sure product is not there
        resp = self.client.get(
            f"{BASE_URL}/{shopcart.id}/products/{product_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_shopcart(self):
        """It should Delete a Shopcart"""
        # get the id of an account
        shopcart = self._create_shopcarts(1)[0]
        resp = self.client.delete(f"{BASE_URL}/{shopcart.id}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_clear_shopcart(self):
        """It should clear an existing shopcart's products"""
        # create a Shopcart to clear
        test_shopcart = self._create_shopcarts(1)[0]
        product = ProductFactory()
        resp = self.client.post(
            f"{BASE_URL}/{test_shopcart.id}/products",
            json=product.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        product2 = ProductFactory()

        resp = self.client.post(
            f"{BASE_URL}/{test_shopcart.id}/products",
            json=product2.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        resp = self.client.get(f"{BASE_URL}/{test_shopcart.id}/products")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 2)
        # clear the shopcart
        resp = self.client.put(
            f"{BASE_URL}/{test_shopcart.id}/clear",
            json=test_shopcart.serialize(),
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_shopcart = resp.get_json()
        self.assertEqual(updated_shopcart["products"], [])
        resp = self.client.put(f"{BASE_URL}/123/clear", json=test_shopcart.serialize())
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_product(self):
        """It should Get a product from a shopcart"""
        # create a known product
        shopcart = self._create_shopcarts(1)[0]
        product = ProductFactory()
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id}/products",
            json=product.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.get_json()
        logging.debug(data)
        product_id = data["id"]

        # retrieve it back
        resp = self.client.get(
            f"{BASE_URL}/{shopcart.id}/products/{product_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["shopcart_id"], shopcart.id)
        self.assertEqual(data["name"], product.name)
        self.assertEqual(data["quantity"], product.quantity)
        self.assertEqual(data["price"], product.price)

    def test_update_product(self):
        """It should Update a product on a shopcart"""
        # create a known product
        shopcart = self._create_shopcarts(1)[0]
        product = ProductFactory()
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id}/products",
            json=product.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.get_json()
        logging.debug(data)
        product_id = data["id"]
        data["quantity"] = 123
        data["price"] = 123

        # send the update back
        resp = self.client.put(
            f"{BASE_URL}/{shopcart.id}/products/{product_id}",
            json=data,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # retrieve it back
        resp = self.client.get(
            f"{BASE_URL}/{shopcart.id}/products/{product_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["id"], product_id)
        self.assertEqual(data["shopcart_id"], shopcart.id)
        self.assertEqual(data["quantity"], 123)
        self.assertEqual(data["price"], 123)
        resp = self.client.put(
            f"{BASE_URL}/{shopcart.id}/products/125",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_shopcarts_by_product_name(self):
        """It should Filter Shop Carts by product name"""
        shopcarts = self._create_shopcarts(3)
        product = ProductFactory()
        name = product.name
        for i in range(2):
            product = ProductFactory()
            product.name = name
            product.shopcart_id = shopcarts[i].id
            resp = self.client.post(
                f"{BASE_URL}/{shopcarts[i].id}/products",
                json=product.serialize(),
                content_type="application/json",
            )
        shopcarts = self._find_shopcarts(shopcarts)
        resp = self.client.get(
            BASE_URL, query_string=f"name={quote_plus(product.name)}"
        )
        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["id"], shopcarts[0].id)
        self.assertEqual(data[1]["id"], shopcarts[1].id)

    def test_update_shopcart(self):
        """It should Update an existing shopcart"""
        # create an Account to update
        shopcart_id = 1234
        products = ProductFactory.create_batch(3)
        shopcart = ShopCartFactory(products=products)
        shopcart.id = shopcart_id
        logging.debug(f"innitial Shopcart = {shopcart.serialize()}")
        resp = self.client.post(f"{BASE_URL}/{shopcart.id}", json=shopcart.serialize())
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        resp = self.client.get(f"{BASE_URL}/{shopcart.id}")
        returned_shopcart = resp.get_json()
        logging.debug(f"Returned Shopcat = {returned_shopcart}")
        self.assertEqual(len(returned_shopcart["products"]), 3)
        product = ProductFactory()
        returned_shopcart["products"] = [product.serialize()]
        resp = self.client.put(f"{BASE_URL}/{shopcart.id}", json=returned_shopcart)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_shopcart = resp.get_json()
        self.assertEqual(len(updated_shopcart["products"]), 1)
        resp = self.client.put(f"{BASE_URL}/{shopcart.id+100}", json=returned_shopcart)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_check_content_type(self):
        customApp = CustomFlask(import_name="Test App")
        with customApp.test_request_context():
            routes.check_content_type(CONTENT_TYPE_JSON)
