import pytest

from app import ProductModel, OrderModel


@pytest.fixture(scope='module')
def product():
    product = ProductModel("desk", 12)
    return product

@pytest.fixture(scope='module')
def order():
    order = OrderModel("Order 1: T-shirt", 1)
    return order

def properly_product(product):
    assert product.name == ("desk",)
    assert product.amount == 12

def properly_order(order):
    assert order.name == ("Order1",)
    assert order.product_id == 1

def not_proper_amount_of_product(product):
    assert product.name == ("desk",)
    assert not product.amount == 10


def not_proper_name_of_order(order):
    assert not order.name == ("xyz",)
    assert order.product_id == 1



