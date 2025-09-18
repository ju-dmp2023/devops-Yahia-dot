from test.web.test_base import WebBase
from test.web.pages.login_page import LoginPage
from test.web.pages.calculator_page import CalculatorPage
from playwright.sync_api import expect
import pytest

class TestCalculations(WebBase):
    def setup_method(self):
        """Setup for each test - login first"""
        super().setup_method()
        # Go to login page and login
        self.page.goto(f"{self.app_url}/login.html")
        LoginPage(self.page).login(username="admin", password="test1234")
        
        # Wait for redirect to calculator
        expect(self.page).to_have_url(f"{self.app_url}/index.html")
        self.calculator = CalculatorPage(self.page)

    def test_addition(self):
        """Test addition operation: 5 + 3 = 8"""
        result = self.calculator.perform_calculation("5", "+", "3")
        assert result == "8"

    def test_subtraction(self):
        """Test subtraction operation: 10 - 4 = 6"""  
        result = self.calculator.perform_calculation("10", "-", "4")
        assert result == "6"

    def test_multiplication(self):
        """Test multiplication operation: 6 * 7 = 42"""
        result = self.calculator.perform_calculation("6", "*", "7")
        assert result == "42"

    def test_division(self):
        """Test division operation: 15 / 3 = 5"""
        result = self.calculator.perform_calculation("15", "/", "3")
        assert result == "5"

    def test_decimal_calculation(self):
        """Test calculation with decimals: 2.5 + 1.5 = 4"""
        # Clear first
        self.calculator.clear_calculator()
        
        # Enter 2.5
        self.calculator.click_number("2")
        self.calculator.element("key_decimal").click()
        self.calculator.click_number("5")
        
        # Add operation
        self.calculator.click_operation("+")
        
        # Enter 1.5
        self.calculator.click_number("1")
        self.calculator.element("key_decimal").click()
        self.calculator.click_number("5")
        
        # Calculate
        self.calculator.click_operation("=")
        self.page.wait_for_timeout(500)
        
        result = self.calculator.get_screen_value()
        assert result == "4"

    def test_multiple_operations(self):
        """Test performing multiple calculations in sequence"""
        # First calculation: 2 + 3 = 5
        result1 = self.calculator.perform_calculation("2", "+", "3")
        assert result1 == "5"
        
        # Second calculation: 4 * 5 = 20
        result2 = self.calculator.perform_calculation("4", "*", "5")
        assert result2 == "20"
        
        # Third calculation: 10 - 2 = 8
        result3 = self.calculator.perform_calculation("10", "-", "2")
        assert result3 == "8"

    def test_clear_function(self):
        """Test the clear functionality"""
        # Enter some numbers
        self.calculator.click_number("1")
        self.calculator.click_number("2")
        self.calculator.click_number("3")
        
        # Verify numbers are displayed
        assert self.calculator.get_screen_value() == "123"
        
        # Clear
        self.calculator.clear_calculator()
        
        # Verify screen is cleared
        assert self.calculator.get_screen_value() == ""

    def test_remote_service_toggle(self):
        """Test toggling between remote and local calculation"""
        # Ensure remote service is enabled initially
        if not self.calculator.is_remote_service_enabled():
            self.calculator.toggle_remote_service()
        
        # Test calculation with remote service
        result_remote = self.calculator.perform_calculation("7", "+", "8")
        assert result_remote == "15"
        
        # Toggle to local service
        self.calculator.toggle_remote_service()
        assert not self.calculator.is_remote_service_enabled()
        
        # Test calculation with local service
        result_local = self.calculator.perform_calculation("9", "+", "6")
        assert result_local == "15"