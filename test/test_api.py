import pytest
import requests
import json
import time
import subprocess
import os
import signal
import sys


class TestCalculatorAPI:
    @classmethod
    def setup_class(cls):
        """Start the REST API server before running tests"""
        cls.base_url = "http://localhost:5001"  # Using port 5001 to avoid conflicts
        cls.api_process = None
        
        # Start the REST API server
        try:
            # Change to the BE directory
            be_path = os.path.join(os.path.dirname(__file__), '..', 'BE')
            cls.api_process = subprocess.Popen([
                sys.executable, 'calculator.py', '--rest', '--port', '5001'
            ], cwd=be_path)
            
            # Wait for the server to start
            time.sleep(3)
            
            # Test if server is running
            response = requests.get(f"{cls.base_url}/", timeout=5)
            if response.status_code != 200:
                raise Exception("API server didn't start properly")
                
        except Exception as e:
            if cls.api_process:
                cls.api_process.terminate()
            raise Exception(f"Failed to start API server: {e}")
    
    @classmethod
    def teardown_class(cls):
        """Stop the REST API server after all tests"""
        if cls.api_process:
            cls.api_process.terminate()
            cls.api_process.wait()
    
    def test_api_is_running(self):
        """Test that the API is accessible"""
        response = requests.get(f"{self.base_url}/")
        assert response.status_code == 200
    
    def test_add_endpoint(self):
        """Test the add operation via API"""
        # Arrange
        payload = {
            "operand1": 5,
            "operand2": 3,
            "operation": "add"
        }
        
        # Act
        response = requests.post(
            f"{self.base_url}/calculate", 
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["result"] == 8
    
    def test_subtract_endpoint(self):
        """Test the subtract operation via API"""
        # Arrange
        payload = {
            "operand1": 10,
            "operand2": 3,
            "operation": "subtract"
        }
        
        # Act
        response = requests.post(
            f"{self.base_url}/calculate", 
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["result"] == 7
    
    def test_multiply_endpoint(self):
        """Test the multiply operation via API"""
        # Arrange
        payload = {
            "operand1": 4,
            "operand2": 5,
            "operation": "multiply"
        }
        
        # Act
        response = requests.post(
            f"{self.base_url}/calculate", 
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["result"] == 20
    
    def test_divide_endpoint(self):
        """Test the divide operation via API"""
        # Arrange
        payload = {
            "operand1": 10,
            "operand2": 2,
            "operation": "divide"
        }
        
        # Act
        response = requests.post(
            f"{self.base_url}/calculate", 
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["result"] == 5
    
    def test_divide_by_zero_error(self):
        """Test divide by zero returns error via API"""
        # Arrange
        payload = {
            "operand1": 10,
            "operand2": 0,
            "operation": "divide"
        }
        
        # Act
        response = requests.post(
            f"{self.base_url}/calculate", 
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        # Assert
        assert response.status_code == 500  # Division by zero will cause an exception
        result = response.json()
        assert "detail" in result
    
    def test_invalid_operation(self):
        """Test invalid operation returns error via API"""
        # Arrange
        payload = {
            "operand1": 10,
            "operand2": 2,
            "operation": "invalid_op"
        }
        
        # Act
        response = requests.post(
            f"{self.base_url}/calculate", 
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        # Assert
        assert response.status_code == 422  # Validation error for invalid enum value
        result = response.json()
        assert "detail" in result
    
    def test_missing_fields(self):
        """Test missing required fields returns validation error"""
        # Arrange
        payload = {
            "operand1": 10,
            # Missing operand2 and operation
        }
        
        # Act
        response = requests.post(
            f"{self.base_url}/calculate", 
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        # Assert
        assert response.status_code == 422  # Validation error
        result = response.json()
        assert "detail" in result
    
    def test_register_user(self):
        """Test user registration via API"""
        # Arrange
        payload = {
            "username": "testuser",
            "password": "testpass123"
        }
        
        # Act
        response = requests.post(
            f"{self.base_url}/register", 
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["username"] == "testuser"
    
    def test_register_duplicate_user(self):
        """Test registering a duplicate user returns error"""
        # Arrange - First register a user
        payload = {
            "username": "duplicateuser",
            "password": "testpass123"
        }
        
        # Register the user first time
        requests.post(f"{self.base_url}/register", json=payload)
        
        # Act - Try to register the same user again
        response = requests.post(
            f"{self.base_url}/register", 
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        # Assert
        assert response.status_code == 409  # Conflict - user already exists
        result = response.json()
        assert "detail" in result
    
    def test_login_user(self):
        """Test user login via API"""
        # Arrange - First register a user
        register_payload = {
            "username": "loginuser",
            "password": "loginpass123"
        }
        requests.post(f"{self.base_url}/register", json=register_payload)
        
        # Act - Login with the registered user
        login_payload = {
            "username": "loginuser",
            "password": "loginpass123"
        }
        response = requests.post(
            f"{self.base_url}/login", 
            json=login_payload,
            headers={'Content-Type': 'application/json'}
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["username"] == "loginuser"
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials returns error"""
        # Arrange
        payload = {
            "username": "nonexistent",
            "password": "wrongpass"
        }
        
        # Act
        response = requests.post(
            f"{self.base_url}/login", 
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        # Assert
        assert response.status_code == 400  # Bad request - wrong credentials
        result = response.json()
        assert "detail" in result
    
    def test_get_current_user_when_logged_in(self):
        """Test getting current user when someone is logged in"""
        # Arrange - Register and login a user
        register_payload = {
            "username": "currentuser",
            "password": "currentpass123"
        }
        requests.post(f"{self.base_url}/register", json=register_payload)
        requests.post(f"{self.base_url}/login", json=register_payload)
        
        # Act
        response = requests.get(f"{self.base_url}/users/current")
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["username"] == "currentuser"
    
    def test_logout_user(self):
        """Test user logout via API"""
        # Arrange - Register and login a user
        user_payload = {
            "username": "logoutuser",
            "password": "logoutpass123"
        }
        requests.post(f"{self.base_url}/register", json=user_payload)
        requests.post(f"{self.base_url}/login", json=user_payload)
        
        # Act - Logout
        response = requests.post(f"{self.base_url}/logout")
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["username"] == "logoutuser"
        
        # Verify user is actually logged out
        current_user_response = requests.get(f"{self.base_url}/users/current")
        assert current_user_response.status_code == 204  # No content - no user logged in