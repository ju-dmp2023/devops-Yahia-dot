from test.web.test_base import WebBase
from test.web.pages.login_page import LoginPage
from test.web.pages.calculator_page import CalculatorPage
from playwright.sync_api import expect
import pytest

class TestFullWorkflow(WebBase):
    def test_complete_user_session(self):
        """Test a complete user session from login to logout"""
        # Start at login page
        self.page.goto(f"{self.app_url}/login.html")
        
        # Login
        login_page = LoginPage(self.page)
        login_page.login("admin", "test1234")
        
        # Verify we're on calculator page
        expect(self.page).to_have_url(f"{self.app_url}/index.html")
        calculator_page = CalculatorPage(self.page)
        
        # Perform some calculations
        result1 = calculator_page.perform_calculation("15", "+", "25")
        assert result1 == "40"
        
        result2 = calculator_page.perform_calculation("100", "/", "4")
        assert result2 == "25"
        
        # Check history
        calculator_page.toggle_history()
        history = calculator_page.get_history_content()
        assert "15" in history and "+25" in history and "=40" in history
        assert "100" in history and "/4" in history and "=25" in history
        
        # Toggle remote service
        initial_remote_state = calculator_page.is_remote_service_enabled()
        calculator_page.toggle_remote_service()
        assert calculator_page.is_remote_service_enabled() != initial_remote_state
        
        # Perform calculation with different service
        result3 = calculator_page.perform_calculation("8", "*", "9")
        assert result3 == "72"
        
        # Logout
        calculator_page.logout()
        
        # Should redirect back to login page
        expect(self.page).to_have_url(f"{self.app_url}/login.html")