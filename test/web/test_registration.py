from test.web.test_base import WebBase
from test.web.pages.login_page import LoginPage
from test.web.pages.register_page import RegisterPage
from test.web.pages.calculator_page import CalculatorPage
from playwright.sync_api import expect
import pytest
import time

class TestRegistration(WebBase):
    def test_register_new_user(self):
        """Test registering a new user"""
        # Start at login page
        self.page.goto(f"{self.app_url}/login.html")
        
        login_page = LoginPage(self.page)
        register_page = RegisterPage(self.page)
        
        # Go to register page
        login_page.go_to_register()
        
        # Wait for register page to load
        expect(self.page).to_have_url(f"{self.app_url}/register.html")
        
        # Register new user with unique username
        username = f"testuser_{int(time.time())}"
        password = "testpass123"
        
        register_page.register_user(username, password)
        
        # After successful registration, should redirect to main calculator
        # Wait for redirect and check we're on the main page
        expect(self.page).to_have_url(f"{self.app_url}/index.html")
        
        # Verify we can see the calculator interface
        calculator_page = CalculatorPage(self.page)
        expect(calculator_page.element("screen")).to_be_visible()

    def test_register_password_mismatch(self):
        """Test registration with mismatched passwords"""
        self.page.goto(f"{self.app_url}/register.html")
        
        register_page = RegisterPage(self.page)
        
        # Try to register with mismatched passwords
        register_page.element("username").fill("testuser")
        register_page.element("password1").fill("password1")
        register_page.element("password2").fill("password2")  # Different password
        register_page.element("register_button").click()
        
        # Should show error message
        expect(register_page.element("error_message")).to_be_visible()
        error_text = register_page.get_error_message()
        assert "not match" in error_text.lower()

    def test_register_existing_user(self):
        """Test registering with existing username"""
        self.page.goto(f"{self.app_url}/register.html")
        
        register_page = RegisterPage(self.page)
        
        # Try to register with admin user (assuming it exists)
        register_page.register_user("admin", "testpass123")
        
        # Should show error message about user already existing
        expect(register_page.element("error_message")).to_be_visible()
        error_text = register_page.get_error_message()
        assert "already exists" in error_text.lower()