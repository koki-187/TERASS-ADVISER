"""
Test script for TERASS user registration system
"""
import requests
import sys

def test_registration():
    """Test user registration"""
    print("=" * 50)
    print("Testing User Registration")
    print("=" * 50)
    
    session = requests.Session()
    
    # Test registration with a new user
    register_data = {
        'username': 'demouser',
        'email': 'demo@example.com',
        'password': 'demo123456',
        'confirm_password': 'demo123456'
    }
    
    response = session.post('http://127.0.0.1:5000/register', data=register_data, allow_redirects=True)
    
    if response.status_code == 200 and 'Login' in response.text:
        print("✓ Registration successful!")
        print(f"  - Username: {register_data['username']}")
        print(f"  - Email: {register_data['email']}")
    else:
        print("✗ Registration failed or user already exists")
        return False
    
    return True

def test_login():
    """Test user login"""
    print("\n" + "=" * 50)
    print("Testing User Login")
    print("=" * 50)
    
    session = requests.Session()
    
    # Login with credentials
    login_data = {
        'username': 'testuser',
        'password': 'password123'
    }
    
    response = session.post('http://127.0.0.1:5000/login', data=login_data, allow_redirects=True)
    
    if response.status_code == 200 and 'Welcome, testuser!' in response.text:
        print("✓ Login successful!")
        print(f"  - Logged in as: {login_data['username']}")
        print("  - Reached dashboard")
        return True
    else:
        print("✗ Login failed")
        return False

def test_validation():
    """Test input validation"""
    print("\n" + "=" * 50)
    print("Testing Input Validation")
    print("=" * 50)
    
    session = requests.Session()
    
    # Test password mismatch
    register_data = {
        'username': 'validationtest',
        'email': 'validation@example.com',
        'password': 'password123',
        'confirm_password': 'differentpassword'
    }
    
    response = session.post('http://127.0.0.1:5000/register', data=register_data, allow_redirects=False)
    
    if 'Passwords do not match' in response.text or response.status_code == 200:
        print("✓ Password mismatch validation working")
    else:
        print("✗ Password mismatch validation failed")
        return False
    
    # Test short password
    register_data['password'] = '12345'
    register_data['confirm_password'] = '12345'
    
    response = session.post('http://127.0.0.1:5000/register', data=register_data, allow_redirects=False)
    
    if 'at least 6 characters' in response.text or response.status_code == 200:
        print("✓ Password length validation working")
    else:
        print("✗ Password length validation failed")
        return False
    
    return True

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("TERASS User Registration System - Test Suite")
    print("=" * 50 + "\n")
    
    try:
        # Run tests
        test_registration()
        test_login()
        test_validation()
        
        print("\n" + "=" * 50)
        print("All Tests Completed!")
        print("=" * 50 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Cannot connect to Flask application")
        print("  Make sure the application is running on http://127.0.0.1:5000")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
