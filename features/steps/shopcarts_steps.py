"""
Pet Steps

Steps file for shopcarts.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import requests
from behave import given
from compare import expect
import logging


@given('the following shopcarts')
def step_impl(context):
    """ Delete all shopcarts and load new ones """
    # List all of the pets and delete them one by one
    rest_endpoint = f"{context.BASE_URL}/shopcarts"
    context.resp = requests.get(rest_endpoint)
    expect(context.resp.status_code).to_equal(200)
    customer_id_set = set()
    # delete all shopcarts and products
    for shopcart in context.resp.json():
        customer_id = shopcart["id"]
        if customer_id not in customer_id_set:
            customer_id_set.add(customer_id)
            context.resp = requests.put(f"{rest_endpoint}/{customer_id}/clear", json={})
            expect(context.resp.status_code).to_equal(200)
            context.resp = requests.delete(f"{rest_endpoint}/{customer_id}")
            expect(context.resp.status_code).to_equal(204)

    # load the database with new pets
    customer_id_set = set()
    for row in context.table:
        customer_id = row["customer_id"]
        if customer_id not in customer_id_set:
            customer_id_set.add(customer_id)
            shopcart_payload = {
                "id": customer_id,
                "products": []
            }
            context.resp = requests.post(f"{rest_endpoint}/{customer_id}", json=shopcart_payload)
            expect(context.resp.status_code).to_equal(201)
        product_payload = {
            "id": row["id"],
            "name": row["name"],
            "quantity": row["quantity"],
            "price": row["price"],
            "shopcart_id": customer_id
        }
        context.resp = requests.post(f"{rest_endpoint}/{customer_id}/products", json=product_payload)
        expect(context.resp.status_code).to_equal(201)
    rest_endpoint = f"{context.BASE_URL}/shopcarts"
    context.resp = requests.get(rest_endpoint)
    for shopcart in context.resp.json():
        logging.info(shopcart)
