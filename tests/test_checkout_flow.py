from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CheckOutPage

def test_user_checkout(page):
    # Set up page objects
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    checkout_page = CheckOutPage(page)

    # UI
    login_page.navigate()
    # User logins in, adds item to cart, clicks on cart icon
    login_page.login("standard_user", "secret_sauce")
    inventory_page.add_backpack_to_cart()
    inventory_page.shopping_cart_badge.click()
    # User in cart page
    checkout_page.click_checkout_button()
    # User in checkout page
    checkout_page.checkout("John", "Doe", "55555")
    checkout_page.click_finish_button()

    # Test
    assert checkout_page.get_success_message() == "Thank you for your order!"