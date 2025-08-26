#!/usr/bin/env python3
"""
Simple test script to verify the FastAPI endpoints are working
"""

import requests

API_BASE_URL = "http://localhost:8000"


def test_api():
    print("🧪 Testing FastAPI Task Management API")
    print("=" * 50)

    try:
        # Test root endpoint
        print("1. Testing root endpoint...")
        response = requests.get(f"{API_BASE_URL}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")

        # Test get all tasks
        print("\n2. Testing get all tasks...")
        response = requests.get(f"{API_BASE_URL}/tasks")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Found {len(data['tasks'])} tasks")

        # Test create task
        print("\n3. Testing create task...")
        new_task = {
            "id": 999,
            "title": "Test Task",
            "description": "This is a test task",
            "completed": False,
        }
        response = requests.post(f"{API_BASE_URL}/tasks", json=new_task)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            print("   ✅ Task created successfully!")
        else:
            print(f"   ❌ Error: {response.json()}")

        # Test get specific task
        print("\n4. Testing get specific task...")
        response = requests.get(f"{API_BASE_URL}/tasks/999")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Task retrieved successfully!")

        # Test delete task
        print("\n5. Testing delete task...")
        response = requests.delete(f"{API_BASE_URL}/tasks/999")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Task deleted successfully!")

        print("\n🎉 All tests completed!")

    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("   Make sure the server is running with:")
        print("   fastapi dev main.py")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    test_api()
