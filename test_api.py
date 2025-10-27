#!/usr/bin/env python3
"""
Test script for TERASS Adviser API
Tests all major endpoints to ensure they work correctly
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
API_TOKEN = "terass-api-token-2025"
HEADERS = {"X-API-Token": API_TOKEN, "Content-Type": "application/json"}


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def test_health_check():
    """Test health check endpoint"""
    print_section("Testing Health Check")
    
    response = requests.get(f"{BASE_URL}/api/v1/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200, "Health check failed"
    print("✓ Health check passed")


def test_api_info():
    """Test API info endpoint"""
    print_section("Testing API Info")
    
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200, "API info failed"
    print("✓ API info passed")


def test_reward_calculation():
    """Test reward calculation endpoint"""
    print_section("Testing Reward Calculation")
    
    # Test single self-discovered deal
    payload = {
        "deals": [
            {
                "tax_excluded_fee": 5000000,
                "source": "self",
                "date": "2025-04-01"
            }
        ]
    }
    
    print("Request payload:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    
    response = requests.post(
        f"{BASE_URL}/api/v1/reward/calculate",
        headers=HEADERS,
        json=payload
    )
    
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200, "Reward calculation failed"
    data = response.json()
    assert "total_reward" in data, "Missing total_reward in response"
    assert data["total_reward"] == 3750000, f"Expected 3750000 but got {data['total_reward']}"
    print("✓ Reward calculation passed")
    
    # Test multiple deals with bonus stage
    print("\nTesting multiple deals with bonus stage:")
    payload_multi = {
        "deals": [
            {
                "tax_excluded_fee": 15000000,
                "source": "self",
                "date": "2025-04-01"
            },
            {
                "tax_excluded_fee": 10000000,
                "source": "self",
                "date": "2025-05-01"
            }
        ]
    }
    
    print("Request payload:")
    print(json.dumps(payload_multi, indent=2, ensure_ascii=False))
    
    response = requests.post(
        f"{BASE_URL}/api/v1/reward/calculate",
        headers=HEADERS,
        json=payload_multi
    )
    
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200, "Multi-deal calculation failed"
    data = response.json()
    # First deal: 15M * 0.75 = 11.25M
    # Second deal: 10M * 0.75 = 7.5M (no bonus stage yet, both in same period)
    # Total: 18.75M
    # Note: Bonus stage activates from next month, not immediately
    expected_total = 18750000
    assert data["total_reward"] == expected_total, f"Expected {expected_total} but got {data['total_reward']}"
    print("✓ Multi-deal calculation with bonus stage passed")


def test_agent_class():
    """Test agent class determination endpoint"""
    print_section("Testing Agent Class Determination")
    
    # Test Senior class (capital region)
    payload = {
        "region": "capital",
        "period_sales": 12000000,
        "cumulative_cases": 5
    }
    
    print("Request payload:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    
    response = requests.post(
        f"{BASE_URL}/api/v1/agent/class",
        headers=HEADERS,
        json=payload
    )
    
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200, "Agent class determination failed"
    data = response.json()
    assert "class" in data, "Missing class in response"
    assert data["class"] == "Senior", f"Expected Senior but got {data['class']}"
    print("✓ Agent class determination passed")


def test_feedback_submission():
    """Test feedback submission endpoint"""
    print_section("Testing Feedback Submission")
    
    payload = {
        "user_id": "test_agent_001",
        "category": "feature_request",
        "message": "モバイルアプリがあると便利です",
        "context": {
            "platform": "test",
            "timestamp": datetime.now().isoformat()
        }
    }
    
    print("Request payload:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    
    response = requests.post(
        f"{BASE_URL}/api/v1/feedback",
        headers=HEADERS,
        json=payload
    )
    
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200, "Feedback submission failed"
    data = response.json()
    assert data["success"] == True, "Feedback submission not successful"
    assert "feedback_id" in data, "Missing feedback_id in response"
    print("✓ Feedback submission passed")


def test_feedback_listing():
    """Test feedback listing endpoint"""
    print_section("Testing Feedback Listing")
    
    response = requests.get(
        f"{BASE_URL}/api/v1/feedback",
        headers=HEADERS
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200, "Feedback listing failed"
    data = response.json()
    assert "feedback" in data, "Missing feedback in response"
    assert "count" in data, "Missing count in response"
    print("✓ Feedback listing passed")


def test_authentication():
    """Test authentication requirement"""
    print_section("Testing Authentication")
    
    # Test without token
    response = requests.post(
        f"{BASE_URL}/api/v1/reward/calculate",
        headers={"Content-Type": "application/json"},
        json={"deals": [{"tax_excluded_fee": 1000000, "source": "self"}]}
    )
    
    print(f"Request without token - Status: {response.status_code}")
    assert response.status_code == 401, "Should return 401 without token"
    print("✓ Authentication check passed (401 without token)")
    
    # Test with wrong token
    response = requests.post(
        f"{BASE_URL}/api/v1/reward/calculate",
        headers={"X-API-Token": "wrong-token", "Content-Type": "application/json"},
        json={"deals": [{"tax_excluded_fee": 1000000, "source": "self"}]}
    )
    
    print(f"Request with wrong token - Status: {response.status_code}")
    assert response.status_code == 401, "Should return 401 with wrong token"
    print("✓ Authentication check passed (401 with wrong token)")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  TERASS Adviser API Test Suite")
    print("="*60)
    print(f"Target: {BASE_URL}")
    print(f"Time: {datetime.now().isoformat()}")
    
    try:
        test_api_info()
        test_health_check()
        test_authentication()
        test_reward_calculation()
        test_agent_class()
        test_feedback_submission()
        test_feedback_listing()
        
        print_section("All Tests Passed ✓")
        print("API is working correctly!")
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except requests.exceptions.ConnectionError:
        print(f"\n✗ Connection failed: Could not connect to {BASE_URL}")
        print("Make sure the API server is running:")
        print("  python api_server.py")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
