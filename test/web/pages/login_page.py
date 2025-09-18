from playwright.sync_api import Page
from test.web.pages.page_base import PageBase

class LoginPage(PageBase):
    def __init__(self, page: Page) -> None:
        super().__init__(page, elements={
            "username": "#username",
            "password": "#password", 
            "login_button": "#login",
            "register_button": "#register",
            "error_message": "#errormsg",
            "spinner": "#spinner"
        })

    def login(self, username: str, password: str):
        """Login with username and password"""
        self.element("username").fill(username)
        self.element("password").fill(password)
        self.element("login_button").click()

    def go_to_register(self):
        """Navigate to register page"""
        self.element("register_button").click()

    def get_error_message(self) -> str:
        """Get error message text if visible"""
        if self.element("error_message").is_visible():
            return self.element("error_message").text_content()
        return ""

    def is_spinner_visible(self) -> bool:
        """Check if loading spinner is visible"""
        return self.element("spinner").is_visible()