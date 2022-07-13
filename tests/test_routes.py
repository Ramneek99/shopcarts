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
            resp = self.client.post(
                f"{BASE_URL}/{shopcart.customer_id}", json=shopcart.serialize()
            )
            self.assertEqual(
                resp.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Shopcart",
            )
            new_shopcart = resp.get_json()
            shopcart.customer_id = new_shopcart["customer_id"]
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
        # get the id of an shopcart
        shopcart = self._create_shopcarts(1)[0]
        resp = self.client.get(
            f"{BASE_URL}/{shopcart.customer_id}", content_type="application/json"
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
            f"{BASE_URL}/{shopcart.customer_id}",
            json=shopcart.serialize(),
            content_type="application/json",
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
            new_shopcart["products"], shopcart.products, "Product does not match"
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
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.customer_id}",
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

    def test_415_media_not_supported(self):
        """It should raise 415 media not supported error"""
        text = "Hello World"
        resp = self.client.post(f"{BASE_URL}/0", data=text, content_type="text/plain")
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_500_error_handler(self):
        """It should return 500 error"""
        response = mock({
            'status_code': 500,
        }, spec=requests.Response)
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
            f"{BASE_URL}/{shopcart.customer_id}/products",
            json=product.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["shopcart_id"], shopcart.customer_id)
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

    def test_get_shopcart_by_customer_id(self):
        """It should Get a shop cart by customer id"""
        shopcarts = self._create_shopcarts(3)
        resp = self.client.get(
            BASE_URL, query_string=f"customer_id={shopcarts[1].customer_id}"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data[0]["customer_id"], shopcarts[1].customer_id)

    def test_read_items(self):
        """It should read all the items from a given shopcart"""
        shopcart = self._create_shopcarts(1)[0]
        product_list = ProductFactory.create_batch(2)
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.customer_id}/products",
            json=product_list[0].serialize(),
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        resp = self.client.post(
            f"{BASE_URL}/{shopcart.customer_id}/products",
            json=product_list[1].serialize(),
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        resp = self.client.get(f"{BASE_URL}/123/products")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        resp = self.client.get(f"{BASE_URL}/{shopcart.customer_id}/products")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        self.assertEqual(len(data), 2)

    def test_delete_product(self):
        """It should Delete a Product"""
        shopcart = self._create_shopcarts(1)[0]
        product = ProductFactory()
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.customer_id}/products",
            json=product.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data)
        product_id = data["id"]

        # send delete request
        resp = self.client.delete(
            f"{BASE_URL}/{shopcart.customer_id}/products/{product_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        # retrieve it back and make sure product is not there
        resp = self.client.get(
            f"{BASE_URL}/{shopcart.customer_id}/products/{product_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_shopcart(self):
        """It should Delete a Shopcart"""
        # get the id of an account
        shopcart = self._create_shopcarts(1)[0]
        resp = self.client.delete(f"{BASE_URL}/{shopcart.customer_id}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_shopcart(self):
        """It should Update an existing shopcart"""
        # create a Shopcart to update
        test_shopcart = ShopCartFactory()
        resp = self.client.post(
            f"{BASE_URL}/{test_shopcart.customer_id}", json=test_shopcart.serialize()
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the shopcart
        new_shopcart = resp.get_json()
        new_shopcart["products"] = []
        new_shopcart_id = new_shopcart["customer_id"]
        resp = self.client.put(f"{BASE_URL}/{new_shopcart_id}", json=new_shopcart)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_shopcart = resp.get_json()
        self.assertEqual(updated_shopcart["products"], [])
        resp = self.client.put(f"{BASE_URL}/123", json=test_shopcart.serialize())
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_product(self):
        """It should Get a product from a shopcart"""
        # create a known product
        shopcart = self._create_shopcarts(1)[0]
        product = ProductFactory()
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.customer_id}/products",
            json=product.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.get_json()
        logging.debug(data)
        product_id = data["id"]

        # retrieve it back
        resp = self.client.get(
            f"{BASE_URL}/{shopcart.customer_id}/products/{product_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["shopcart_id"], shopcart.customer_id)
        self.assertEqual(data["name"], product.name)
        self.assertEqual(data["quantity"], product.quantity)
        self.assertEqual(data["price"], product.price)

    def test_update_product(self):
        """It should Update a product on a shopcart"""
        # create a known product
        shopcart = self._create_shopcarts(1)[0]
        product = ProductFactory()
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.customer_id}/products",
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
            f"{BASE_URL}/{shopcart.customer_id}/products/{product_id}",
            json=data,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # retrieve it back
        resp = self.client.get(
            f"{BASE_URL}/{shopcart.customer_id}/products/{product_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["id"], product_id)
        self.assertEqual(data["shopcart_id"], shopcart.customer_id)
        self.assertEqual(data["quantity"], 123)
        self.assertEqual(data["price"], 123)
        resp = self.client.put(
            f"{BASE_URL}/{shopcart.customer_id}/products/125",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
