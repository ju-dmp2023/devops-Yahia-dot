from playwright.sync_api import Page
from test.web.pages.page_base import PageBase

class CalculatorPage(PageBase):
    def __init__(self, page: Page) -> None:
        super().__init__(page, elements={
            # User info
            "username": "#user-name",
            
            # Calculator screen
            "screen": "#calculator-screen",
            
            # Number buttons (using exact IDs from HTML)
            "key_0": "#key-0",
            "key_1": "#key-1", 
            "key_2": "#key-2",
            "key_3": "#key-3",
            "key_4": "#key-4",
            "key_5": "#key-5",
            "key_6": "#key-6",
            "key_7": "#key-7",
            "key_8": "#key-8",
            "key_9": "#key-9",
            "key_decimal": "#key-decimal",
            
            # Operation buttons
            "key_add": "#key-add",
            "key_subtract": "#key-subtract",
            "key_multiply": "#key-multiply",
            "key_divide": "#key-divide",
            "key_equals": "#key-equals",
            "key_clear": "#key-clear",
            
            # Control buttons
            "toggle_button": "#toggle-button",  # History toggle '>>'
            "logout_button": "#logout-button",
            "remote_toggle": "#remote-toggle",
            "clear_history": "#clear-history",
            
            # History/text window
            "text_window": "#text-window",
            "history": "#history"
        })

    def click_number(self, number: str):
        """Click a number button"""
        self.element(f"key_{number}").click()

    def click_operation(self, operation: str):
        """Click an operation button"""
        operations = {
            "+": "key_add",
            "-": "key_subtract", 
            "*": "key_multiply",
            "/": "key_divide",
            "=": "key_equals"
        }
        if operation in operations:
            self.element(operations[operation]).click()
        else:
            raise ValueError(f"Unknown operation: {operation}")

    def get_screen_value(self) -> str:
        """Get the current calculator screen value"""
        return self.element("screen").input_value()

    def clear_calculator(self):
        """Clear the calculator screen"""
        self.element("key_clear").click()

    def perform_calculation(self, num1: str, operation: str, num2: str):
        """Perform a complete calculation"""
        # Clear first
        self.clear_calculator()
        
        # Enter first number (digit by digit)
        for digit in num1:
            if digit == '.':
                self.element("key_decimal").click()
            else:
                self.click_number(digit)
        
        # Click operation
        self.click_operation(operation)
        
        # Enter second number (digit by digit)
        for digit in num2:
            if digit == '.':
                self.element("key_decimal").click()
            else:
                self.click_number(digit)
        
        # Get result
        self.click_operation("=")
        
        # Wait a moment for calculation (especially remote service)
        self.page.wait_for_timeout(500)
        
        return self.get_screen_value()

    def toggle_history(self):
        """Toggle the history panel"""
        self.element("toggle_button").click()

    def get_history_content(self) -> str:
        """Get all history content from textarea"""
        return self.element("history").input_value()

    def clear_history(self):
        """Clear the history"""
        # First open history if not visible
        if not self.is_history_visible():
            self.toggle_history()
        self.element("clear_history").click()

    def is_history_visible(self) -> bool:
        """Check if history panel is visible"""
        # The text window slides in from right: -320px to 0px
        text_window = self.element("text_window")
        style = text_window.get_attribute("style")
        return "right: 0px" in style if style else False

    def get_username(self) -> str:
        """Get the displayed username"""
        return self.element("username").text_content()

    def logout(self):
        """Click logout button"""
        self.element("logout_button").click()

    def toggle_remote_service(self):
        """Toggle remote service on/off"""
        self.element("remote_toggle").click()

    def is_remote_service_enabled(self) -> bool:
        """Check if remote service is enabled (green button)"""
        button = self.element("remote_toggle")
        return "enabled" in button.get_attribute("class")