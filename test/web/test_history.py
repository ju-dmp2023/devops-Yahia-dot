from test.web.test_base import WebBase
from test.web.pages.login_page import LoginPage
from test.web.pages.calculator_page import CalculatorPage
from playwright.sync_api import expect
import pytest

class TestHistory(WebBase):
    def setup_method(self):
        """Setup for each test - login first"""
        super().setup_method()
        # Go to login page and login
        self.page.goto(f"{self.app_url}/login.html")
        LoginPage(self.page).login(username="admin", password="test1234")
        
        # Wait for redirect to calculator
        expect(self.page).to_have_url(f"{self.app_url}/index.html")
        self.calculator = CalculatorPage(self.page)

    def test_history_toggle(self):
        """Test that history panel can be opened and closed"""
        # Initially history should be hidden (right: -320px)
        assert not self.calculator.is_history_visible()
        
        # Open history
        self.calculator.toggle_history()
        self.page.wait_for_timeout(500)  # Wait for animation
        
        # History should now be visible
        assert self.calculator.is_history_visible()
        
        # Close history
        self.calculator.toggle_history()
        self.page.wait_for_timeout(500)  # Wait for animation
        
        # History should be hidden again
        assert not self.calculator.is_history_visible()

    def test_calculation_history_tracking(self):
        """Test that calculations are logged in history"""
        # Clear history first
        self.calculator.clear_history()
        
        # Perform some calculations
        self.calculator.perform_calculation("5", "+", "3")
        self.calculator.perform_calculation("10", "-", "2")
        self.calculator.perform_calculation("6", "*", "4")
        
        # Open history
        if not self.calculator.is_history_visible():
            self.calculator.toggle_history()
        
        # Get history content
        history_content = self.calculator.get_history_content()
        
        # Verify calculations appear in history
        # Based on the logToTextWindow function, history should contain operations and results
        assert "5" in history_content
        assert "+" in history_content
        assert "3" in history_content
        assert "=8" in history_content
        
        assert "10" in history_content
        assert "-" in history_content
        assert "2" in history_content
        assert "=8" in history_content
        
        assert "6" in history_content
        assert "*" in history_content
        assert "4" in history_content
        assert "=24" in history_content

    def test_clear_history_function(self):
        """Test clearing the history"""
        # Perform a calculation to create history
        self.calculator.perform_calculation("7", "+", "8")
        
        # Open history and verify it has content
        if not self.calculator.is_history_visible():
            self.calculator.toggle_history()
        
        history_before = self.calculator.get_history_content()
        assert history_before != ""  # Should have content
        
        # Clear history
        self.calculator.clear_history()
        
        # Verify history is empty
        history_after = self.calculator.get_history_content()
        assert history_after == ""

    def test_history_button_text_changes(self):
        """Test that the history button text changes when toggled"""
        toggle_button = self.calculator.element("toggle_button")
        
        # Initially should show '>>'
        initial_text = toggle_button.text_content()
        assert initial_text == ">>"
        
        # Click to open history
        self.calculator.toggle_history()
        self.page.wait_for_timeout(500)
        
        # Should now show '<<'
        opened_text = toggle_button.text_content()
        assert opened_text == "<<"
        
        # Click to close history
        self.calculator.toggle_history()
        self.page.wait_for_timeout(500)
        
        # Should be back to '>>'
        closed_text = toggle_button.text_content()
        assert closed_text == ">>"