import pytest
from products import Product, NonStockedProduct, LimitedProduct
from store import Store


@pytest.fixture
def best_buy_store():
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),
        LimitedProduct("Shipping", price=10, quantity=250, maximum=1),
    ]
    return Store(product_list)


def test_store_total_quantity(best_buy_store):
    # 100 + 500 + 250 + 0 + 250 = 1100
    assert best_buy_store.get_total_quantity() == 1100


def test_store_get_all_products_excludes_inactive(best_buy_store):
    all_active = best_buy_store.get_all_products()
    assert len(all_active) == 5

    # Deactivate MacBook Air M2 by buying all 100 units
    macbook = all_active[0]
    macbook.buy(100)

    updated_active = best_buy_store.get_all_products()
    assert len(updated_active) == 4
    assert macbook not in updated_active


def test_store_order_mixed_products(best_buy_store):
    macbook, earbuds, pixel, windows, shipping = best_buy_store.get_all_products()

    total = best_buy_store.order([
        (macbook, 1),
        (windows, 2),
        (shipping, 1),
    ])

    assert total == 1450 + 250 + 10
    assert macbook.get_quantity() == 99
    assert windows.get_quantity() == 0
    assert windows.is_active() is True
    assert shipping.get_quantity() == 249


def test_store_order_exceeding_limited_product_raises(best_buy_store):
    shipping = best_buy_store.get_all_products()[-1]
    with pytest.raises(ValueError):
        best_buy_store.order([(shipping, 2)])


def test_store_order_unlisted_product_raises(best_buy_store):
    unlisted = Product("iPad Pro", price=999, quantity=10)
    with pytest.raises(ValueError):
        best_buy_store.order([(unlisted, 1)])