import products
import promotions
import store


def print_menu():
    print("\tStore Menu\n\t----------")
    print("1. List all products in store")
    print("2. Show total amount in store")
    print("3. Make an order")
    print("4. Quit")


def make_order(best_buy):
    prods = best_buy.get_all_products()
    order = []

    for i, product in enumerate(prods, start=1):
        print(f"{i}. ", end="")
        product.show()

    while True:
        menu_choice = input("Select # of product (or press Enter to finish): ")
        if not menu_choice:
            break
        try:
            prod_index = int(menu_choice)
            if not (0 < prod_index <= len(prods)):
                print("Error: Product number out of range.")
                continue

            selected_product = prods[prod_index - 1]
            quantity = int(input("Enter amount: "))

            if quantity <= 0:
                print("Error: quantity must be greater than zero")
                continue

            if (
                not isinstance(selected_product, products.NonStockedProduct)
                and quantity >= selected_product.quantity
                and selected_product.active
            ):
                quantity = selected_product.quantity
                print("Stock is empty. Adjusting to remaining stock.")
                subtotal = selected_product.buy(quantity)
                order.append((selected_product, quantity, subtotal))

            elif selected_product.active:
                subtotal = selected_product.buy(quantity)
                order.append((selected_product, quantity, subtotal))
                print(f"Added {selected_product.name}, quantity: {quantity}")

            else:
                print("Product sold out")

        except ValueError as e:
            print(f"Error: {e}")

    if order:
        print("---ORDER SUMMARY---")
        total_cost = 0.0
        for item, qty, subtotal in order:
            print(f"Item: {item.name}, Quantity: {qty}, Subtotal: ${subtotal:.2f}")
            total_cost += subtotal
        print(f"Total order cost: ${total_cost:.2f}")


def main():
    # setup initial stock of inventory
    product_list = [
        products.Product("MacBook Air M2", price=1450, quantity=100),
        products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        products.Product("Google Pixel 7", price=500, quantity=250),
        products.NonStockedProduct("Windows License", price=125),
        products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1),
    ]

    # Create promotion catalog
    second_half_price = promotions.SecondHalfPrice("Second Half price!")
    third_one_free = promotions.ThirdOneFree("Third One Free!")
    thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

    # Add promotions to products
    product_list[0].set_promotion(second_half_price)
    product_list[1].set_promotion(third_one_free)
    product_list[3].set_promotion(thirty_percent)

    best_buy = store.Store(product_list)

    while True:
        print_menu()
        try:
            menu_choice = int(input("Please choose a number: "))
            if menu_choice == 1:
                print("------")
                for product in best_buy.get_all_products():
                    product.show()
                print("------")

            elif menu_choice == 2:
                print(best_buy.get_total_quantity())

            elif menu_choice == 3:
                make_order(best_buy)

            elif menu_choice == 4:
                print("bye bye!!!")
                break

            else:
                print("number must be in menu")
        except ValueError:
            print("Value Error: Type a number")


if __name__ == "__main__":
    main()