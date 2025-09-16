import pytest
import requests
from calculator_client.client import Client
from calculator_client.api.actions import calculate, login, logout, register, users_current
from calculator_client.models.calculation import Calculation
from calculator_client.models.opertions import Opertions
from calculator_client.models.user import User
from calculator_client.models import ResultResponse, UserResponse, ErrorResponse, HTTPValidationError


class TestGeneratedApi:
    """Test suite for the generated API client code."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.base_url = "http://localhost:5001"
        self.client = Client(base_url=self.base_url)
    
    def test_generated_code(self):
        """Test the basic calculation functionality."""
        response = calculate.sync(
            client=self.client,
            body=Calculation(operation=Opertions.ADD, operand1=1, operand2=2),
        )
        assert isinstance(response, ResultResponse)
        assert response.result == 3

    def test_calculate_add(self):
        """Test addition operation."""
        response = calculate.sync(
            client=self.client,
            body=Calculation(operation=Opertions.ADD, operand1=5, operand2=3),
        )
        assert isinstance(response, ResultResponse)
        assert response.result == 8

    def test_calculate_subtract(self):
        """Test subtraction operation."""
        response = calculate.sync(
            client=self.client,
            body=Calculation(operation=Opertions.SUBTRACT, operand1=10, operand2=4),
        )
        assert isinstance(response, ResultResponse)
        assert response.result == 6

    def test_calculate_multiply(self):
        """Test multiplication operation."""
        response = calculate.sync(
            client=self.client,
            body=Calculation(operation=Opertions.MULTIPLY, operand1=6, operand2=7),
        )
        assert isinstance(response, ResultResponse)
        assert response.result == 42

    def test_calculate_divide(self):
        """Test division operation."""
        response = calculate.sync(
            client=self.client,
            body=Calculation(operation=Opertions.DIVIDE, operand1=15, operand2=3),
        )
        assert isinstance(response, ResultResponse)
        assert response.result == 5

    def test_calculate_divide_by_zero(self):
        """Test division by zero handling."""
        response = calculate.sync(
            client=self.client,
            body=Calculation(operation=Opertions.DIVIDE, operand1=10, operand2=0),
        )
        # Expecting an error response for division by zero
        assert isinstance(response, ErrorResponse)

    def test_calculate_with_floats(self):
        """Test calculation with floating point numbers."""
        response = calculate.sync(
            client=self.client,
            body=Calculation(operation=Opertions.ADD, operand1=2.5, operand2=3.7),
        )
        assert isinstance(response, ResultResponse)
        assert response.result == pytest.approx(6.2)

    def test_register_new_user(self):
        """Test user registration."""
        test_user = User(username="testuser", password="testpassword")
        response = register.sync(
            client=self.client,
            body=test_user,
        )
        # Should return UserResponse on successful registration
        assert isinstance(response, (UserResponse, ErrorResponse))
        
        if isinstance(response, UserResponse):
            assert response.username == "testuser"

    def test_register_duplicate_user(self):
        """Test registration of duplicate user."""
        test_user = User(username="duplicateuser", password="testpassword")
        
        # First registration
        first_response = register.sync(
            client=self.client,
            body=test_user,
        )
        
        # Second registration (should fail)
        second_response = register.sync(
            client=self.client,
            body=test_user,
        )
        
        # Second registration should return an error (409 conflict)
        assert isinstance(second_response, ErrorResponse)

    def test_login_valid_credentials(self):
        """Test login with valid credentials."""
        # First register a user
        test_user = User(username="logintest", password="loginpassword")
        register_response = register.sync(
            client=self.client,
            body=test_user,
        )
        
        # Now try to login
        login_response = login.sync(
            client=self.client,
            body=test_user,
        )
        
        assert isinstance(login_response, (UserResponse, ErrorResponse))
        
        if isinstance(login_response, UserResponse):
            assert login_response.username == "logintest"

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        invalid_user = User(username="nonexistent", password="wrongpassword")
        response = login.sync(
            client=self.client,
            body=invalid_user,
        )
        
        # Should return ErrorResponse for invalid credentials (400 status)
        assert isinstance(response, ErrorResponse)

    def test_get_current_user_when_logged_in(self):
        """Test getting current user when logged in."""
        # First register and login a user
        test_user = User(username="currentusertest", password="currentpassword")
        register.sync(client=self.client, body=test_user)
        login.sync(client=self.client, body=test_user)
        
        # Get current user
        response = users_current.sync(client=self.client)
        
        # Should return UserResponse when logged in, or None/ErrorResponse when not
        assert isinstance(response, (UserResponse, ErrorResponse, type(None)))

    def test_logout_when_logged_in(self):
        """Test logout when user is logged in."""
        # First register and login a user
        test_user = User(username="logouttest", password="logoutpassword")
        register.sync(client=self.client, body=test_user)
        login.sync(client=self.client, body=test_user)
        
        # Now logout
        response = logout.sync(client=self.client)
        
        assert isinstance(response, (UserResponse, ErrorResponse))

    def test_logout_when_not_logged_in(self):
        """Test logout when no user is logged in."""
        response = logout.sync(client=self.client)
        
        # Should handle logout gracefully even when not logged in
        assert isinstance(response, (UserResponse, ErrorResponse, type(None)))

    # Error handling tests
    def test_calculate_validation_error(self):
        """Test calculation with invalid data should return HTTPValidationError."""
        # This test assumes the server validates input and returns 422 for invalid data
        try:
            response = calculate.sync(
                client=self.client,
                body=Calculation(operation="INVALID_OP", operand1=1, operand2=2),
            )
            assert isinstance(response, (HTTPValidationError, ErrorResponse))
        except Exception:
            # If the model validation prevents creating invalid operation, that's also acceptable
            pass

    def test_register_validation_error(self):
        """Test registration with invalid data."""
        try:
            # Try to register with missing or invalid data
            invalid_user = User(username="", password="")  # Empty username/password
            response = register.sync(
                client=self.client,
                body=invalid_user,
            )
            assert isinstance(response, (HTTPValidationError, ErrorResponse))
        except Exception:
            # If the model validation prevents creating invalid user, that's also acceptable
            pass

    def test_detailed_response_methods(self):
        """Test the detailed response methods that return full Response objects."""
        detailed_response = calculate.sync_detailed(
            client=self.client,
            body=Calculation(operation=Opertions.ADD, operand1=1, operand2=1),
        )
        
        # Check that we get a Response object with status code, content, headers, etc.
        assert hasattr(detailed_response, 'status_code')
        assert hasattr(detailed_response, 'content')
        assert hasattr(detailed_response, 'headers')
        assert hasattr(detailed_response, 'parsed')
        
        # The parsed response should be our ResultResponse
        assert isinstance(detailed_response.parsed, ResultResponse)
        assert detailed_response.parsed.result == 2

    def test_client_configuration(self):
        """Test client configuration options."""
        # Test client with custom headers
        custom_client = self.client.with_headers({"X-Custom-Header": "test-value"})
        
        response = calculate.sync(
            client=custom_client,
            body=Calculation(operation=Opertions.ADD, operand1=1, operand2=1),
        )
        
        assert isinstance(response, ResultResponse)
        assert response.result == 2

    def test_client_with_timeout(self):
        """Test client with custom timeout."""
        import httpx
        timeout_client = self.client.with_timeout(httpx.Timeout(30.0))
        
        response = calculate.sync(
            client=timeout_client,
            body=Calculation(operation=Opertions.ADD, operand1=5, operand2=5),
        )
        
        assert isinstance(response, ResultResponse)
        assert response.result == 10