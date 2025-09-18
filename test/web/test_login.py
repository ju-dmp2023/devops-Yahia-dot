from test.web.test_base import WebBase
from test.web.pages.login_page import LoginPage
from test.web.pages.calculator_page import CalculatorPage
from playwright.sync_api import expect
import pytest

class TestLogin(WebBase):
    def test_successful_login(self):
        """Test successful login with correct credentials"""
        self.page.goto(f"{self.app_url}/login.html")
        
        login_page = LoginPage(self.page)
        login_page.login("admin", "test1234")
        
        # Should redirect to calculator page
        expect(self.page).to_have_url(f"{self.app_url}/index.html")
        
        # Verify calculator interface is visible
        calculator_page = CalculatorPage(self.page)
        expect(calculator_page.element("screen")).to_be_visible()
        expect(calculator_page.element("username")).to_have_text("admin")

    def test_failed_login(self):
        """Test login with incorrect credentials"""
        self.page.goto(f"{self.app_url}/login.html")
        
        login_page = LoginPage(self.page)
        login_page.login("wronguser", "wrongpass")
        
        # Should show error message
        expect(login_page.element("error_message")).to_be_visible()
        error_text = login_page.get_error_message()
        assert "wrong" in error_text.lower() or "password" in error_text.lower()
        
        # Should remain on login page
        expect(self.page).to_have_url(f"{self.app_url}/login.html")

    def test_navigate_to_register(self):
        """Test navigation from login to register page"""
        self.page.goto(f"{self.app_url}/login.html")
        
        login_page = LoginPage(self.page)
        login_page.go_to_register()
        
        # Should navigate to register page
        expect(self.page).to_have_url(f"{self.app_url}/register.html")