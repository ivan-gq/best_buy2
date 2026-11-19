import pytest
from products import Product, NonStockedProduct, LimitedProduct


def test_create_normal_product():
    product = Product("MacBook Air M2", price=1450, quantity=100)
    assert product.name == "MacBook Air M2"
    assert product.price == 1450
    assert product.quantity == 100
    assert product.is_active() is True


def test_create_invalid_product():
    with pytest.raises(ValueError):
        Product("", price=1450, quantity=100)

    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=-10, quantity=100)


def test_product_becomes_inactive_at_zero_quantity():
    product = Product("MacBook Air M2", price=1450, quantity=10)
    product.buy(10)
    assert product.get_quantity() == 0
    assert product.is_active() is False


def test_product_purchase_modifies_quantity_and_returns_total():
    product = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    total_price = product.buy(3)
    assert product.get_quantity() == 497
    assert total_price == 750


def test_buy_larger_quantity_than_exists_raises_exception():
    product = Product("MacBook Air M2", price=1450, quantity=5)
    with pytest.raises(ValueError):
        product.buy(10)

def test_non_stocked_product_stays_at_zero_and_active():
    license_prod = NonStockedProduct("Windows License", price=125)
    assert license_prod.get_quantity() == 0
    assert license_prod.is_active() is True

    total = license_prod.buy(3)
    assert total == 375.0
    assert license_prod.get_quantity() == 0
    assert license_prod.is_active() is True


def test_limited_product_enforces_maximum_per_order():
    shipping = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    assert shipping.buy(1) == 10.0
    assert shipping.get_quantity() == 249

    with pytest.raises(ValueError):
        shipping.buy(2)