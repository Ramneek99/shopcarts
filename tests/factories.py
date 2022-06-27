# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test Factory to make fake objects for testing
"""
import factory
import random
from factory.fuzzy import FuzzyChoice
from service.models import Product, Shopcart


class ProductFactory(factory.Factory):
    """Creates fake products"""

    class Meta:
        model = Product

    id = factory.Sequence(lambda n: n)
    shopcart_id = None 
    name = FuzzyChoice(choices=["apple", "peach", "banana", "pear", "cake"])
    quantity = FuzzyChoice(choices=[0, 1, 2, 3, 4])
    price = FuzzyChoice(choices=[0.99, 1.99, 2.99, 3.99, 4.99])

class ShopCartFactory(factory.Factory):
    """Creates fake shopCarts"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Shopcart

    # MIN_PRICE = 10.0
    # MAX_PRICE = 1000.0

    id = factory.Sequence(lambda n: n)
    customer_id = factory.Sequence(lambda n: n)
    products = []
