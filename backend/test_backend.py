"""
Test script for the FastAPI backend

This script tests all endpoints to verify the backend is working correctly.
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_health_check():
    """Test the health check endpoint."""
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print(f"✓ Health check passed: {response.json()}")
            return True
        else:
            print(f"✗ Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Health check failed: {e}")
        return False

def test_root_endpoint():
    """Test the root endpoint."""
    print("\nTesting / endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print(f"✓ Root endpoint passed: {response.json()}")
            return True
        else:
            print(f"✗ Root endpoint failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Root endpoint failed: {e}")
        return False

def test_predict_endpoint():
    """Test the predict endpoint with sample data."""
    print("\nTesting /predict endpoint...")
    
    # Sample student data
    sample_data = {
        "attendance": 85.5,
        "study_hours": 10.0,
        "assignments_completed": 8,
        "quiz_score": 75.0,
        "midterm_score": 80.0,
        "internet_access": 1,
        "past_failures": 0
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=sample_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Predict endpoint passed!")
            print(f"  Input data: {json.dumps(sample_data, indent=2)}")
            print(f"  Results:")
            print(f"    - Logistic Regression: {result.get('logistic_regression')}")
            print(f"    - Decision Tree: {result.get('decision_tree')}")
            return True
        else:
            print(f"✗ Predict endpoint failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Predict endpoint failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("FastAPI Backend Test Suite")
    print("=" * 60)
    
    # Wait a moment for server to be ready
    print("\nWaiting for server to be ready...")
    time.sleep(2)
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health_check()))
    results.append(("Root Endpoint", test_root_endpoint()))
    results.append(("Predict Endpoint", test_predict_endpoint()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Backend is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the server logs.")

if __name__ == "__main__":
    main()

