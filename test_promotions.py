import pytest
from products import Product, NonStockedProduct, LimitedProduct
from promotions import Promotion, PercentDiscount, SecondHalfPrice, ThirdOneFree
from store import Store


def test_cannot_instantiate_abstract_promotion():
    with pytest.raises(TypeError):
        Promotion("Generic Promo")


def test_invalid_promotion_inputs_raise_errors():
    with pytest.raises(ValueError):
        PercentDiscount("", percent=20)

    with pytest.raises(ValueError):
        PercentDiscount("Invalid High", percent=110)

    with pytest.raises(ValueError):
        PercentDiscount("Invalid Negative", percent=-5)


def test_percent_discount_calculation():
    mac = Product("MacBook Air M2", price=1450, quantity=10)
    promo = PercentDiscount("20% off!", percent=20)
    mac.set_promotion(promo)

    assert mac.buy(2) == 2320.0
    assert mac.quantity == 8


def test_second_half_price_odd_and_even_quantities():
    mac = Product("MacBook Air M2", price=1450, quantity=10)
    mac.set_promotion(SecondHalfPrice("Second Half price!"))

    assert mac.buy(1) == 1450.0
    assert mac.buy(2) == 2175.0
    assert mac.buy(3) == 3625.0
    assert mac.quantity == 4


def test_third_one_free_boundary_quantities():
    earbuds = Product("Bose QuietComfort Earbuds", price=250, quantity=20)
    earbuds.set_promotion(ThirdOneFree("Third One Free!"))

    assert earbuds.buy(2) == 500.0
    assert earbuds.buy(3) == 500.0
    assert earbuds.buy(4) == 750.0
    assert earbuds.quantity == 11


def test_set_swap_and_remove_promotion():
    pixel = Product("Google Pixel 7", price=500, quantity=10)
    assert pixel.get_promotion() is None

    promo_10 = PercentDiscount("10% off!", percent=10)
    pixel.set_promotion(promo_10)
    assert pixel.get_promotion() is promo_10

    pixel.set_promotion(None)
    assert pixel.get_promotion() is None
    assert pixel.buy(1) == 500.0

    with pytest.raises(TypeError):
        pixel.set_promotion("10% off!")


def test_non_stocked_product_with_promotion():
    windows = NonStockedProduct("Windows License", price=125)
    windows.set_promotion(PercentDiscount("30% off!", percent=30))

    total = windows.buy(2)
    assert total == 175.0
    assert windows.quantity == 0
    assert windows.is_active() is True


def test_show_displays_and_hides_promotion(capsys):
    windows = NonStockedProduct("Windows License", price=125)
    windows.set_promotion(PercentDiscount("30% off!", percent=30))

    windows.show()
    captured_with_promo = capsys.readouterr().out
    assert "30% off!" in captured_with_promo

    windows.set_promotion(None)
    windows.show()
    captured_without_promo = capsys.readouterr().out
    assert "30% off!" not in captured_without_promo


def test_store_order_with_full_promotion_catalog():
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),
        LimitedProduct("Shipping", price=10, quantity=250, maximum=1),
    ]

    product_list[0].set_promotion(SecondHalfPrice("Second Half price!"))
    product_list[1].set_promotion(ThirdOneFree("Third One Free!"))
    product_list[3].set_promotion(PercentDiscount("30% off!", percent=30))

    best_buy = Store(product_list)

    total_order = best_buy.order([
        (product_list[0], 2),
        (product_list[1], 3),
        (product_list[2], 1),
        (product_list[3], 2),
        (product_list[4], 1),
    ])

    assert total_order == 3360.0