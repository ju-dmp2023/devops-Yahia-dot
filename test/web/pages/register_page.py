from playwright.sync_api import Page
from test.web.pages.page_base import PageBase

class RegisterPage(PageBase):
    def __init__(self, page: Page) -> None:
        super().__init__(page, elements={
            # Navigation
            "register_link": "#register",  # From login page
            
            # Form fields
            "username": "#username",
            "password1": "#password1", 
            "password2": "#password2",
            "register_button": "#register",  # Register button on register page
            
            # Messages
            "error_message": "#errormsg",
            "spinner": "#spinner"
        })

    def go_to_register_from_login(self):
        """Click register link from login page"""
        self.element("register_link").click()

    def register_user(self, username: str, password: str):
        """Register a new user"""
        self.element("username").fill(username)
        self.element("password1").fill(password)
        self.element("password2").fill(password)
        self.element("register_button").click()

    def get_error_message(self) -> str:
        """Get error message text if visible"""
        if self.element("error_message").is_visible():
            return self.element("error_message").text_content()
        return ""

    def is_spinner_visible(self) -> bool:
        """Check if loading spinner is visible"""
        return self.element("spinner").is_visible()