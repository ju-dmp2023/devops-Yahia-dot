import pytest
from test_base import TestBase


class TestCalculatorHelper(TestBase):
    def test_add_positive_numbers(self):
        # Arrange
        a = 3
        b = 5
        expected = 8
        
        # Act
        result = self.calculator.add(a, b)
        
        # Assert
        assert result == expected
    
    def test_add_negative_numbers(self):
        # Arrange
        a = -3
        b = -5
        expected = -8
        
        # Act
        result = self.calculator.add(a, b)
        
        # Assert
        assert result == expected
    
    def test_subtract_positive_numbers(self):
        # Arrange
        a = 10
        b = 3
        expected = 7
        
        # Act
        result = self.calculator.subtract(a, b)
        
        # Assert
        assert result == expected
    
    def test_multiply_positive_numbers(self):
        # Arrange
        a = 4
        b = 5
        expected = 20
        
        # Act
        result = self.calculator.multiply(a, b)
        
        # Assert
        assert result == expected
    
    def test_divide_positive_numbers(self):
        # Arrange
        a = 10
        b = 2
        expected = 5
        
        # Act
        result = self.calculator.divide(a, b)
        
        # Assert
        assert result == expected
    
    def test_divide_by_zero_raises_exception(self):
        # Arrange
        a = 10
        b = 0
        
        # Act & Assert
        with pytest.raises(ZeroDivisionError):
            self.calculator.divide(a, b)

    @pytest.mark.parametrize("a,b,expected", [
        (3, 3, 6),
        (3, -3, 0),
        (-3, -3, -6),
        (0, 5, 5),
        (10, 0, 10)
    ])
    def test_add_with_various_inputs(self, a, b, expected):
        # Act
        result = self.calculator.add(a, b)
        
        # Assert
        assert result == expected
    
    @pytest.mark.parametrize("a,b,expected", [
        (10, 5, 2),
        (15, 3, 5),
        (-10, -2, 5),
        (0, 1, 0)
    ])
    def test_divide_with_various_inputs(self, a, b, expected):
        # Act
        result = self.calculator.divide(a, b)
        
        # Assert
        assert result == expected
    
    @pytest.mark.parametrize("a,b,expected", [
        (5, 3, 2),
        (10, 7, 3),
        (-5, -3, -2),
        (0, 5, -5)
    ])
    def test_subtract_with_various_inputs(self, a, b, expected):
        # Act
        result = self.calculator.subtract(a, b)
        
        # Assert
        assert result == expected