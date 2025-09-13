import sys
import os

# Add the BE directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'BE'))

from calculator_helper import CalculatorHelper

class TestBase:
    def setup_method(self):
        """Setup method called before each test"""
        self.calculator = CalculatorHelper()
    
    def teardown_method(self):
        """Teardown method called after each test"""
        self.calculator = None