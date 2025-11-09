"""
Example script demonstrating how to use the DummyAPI with Python requests
"""

import requests
import json

BASE_URL = "http://localhost:5000/data/v1"
APP_ID = "0JyYiOQXQQr5H9OEn21312"

headers = {
    "app-id": APP_ID
}


def print_response(response):
    """Pretty print the response"""
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print("-" * 60)


def main():
    print("=" * 60)
    print("DummyAPI Python Example")
    print("=" * 60)
    
    # 1. Get list of users
    print("\n1. Getting list of users (page 0, limit 5)...")
    response = requests.get(f"{BASE_URL}/user?page=0&limit=5", headers=headers)
    print_response(response)
    
    # 2. Get specific user
    print("\n2. Getting user by ID...")
    response = requests.get(f"{BASE_URL}/user/60d0fe4f5311236168a109ca", headers=headers)
    print_response(response)
    
    # 3. Create a new user
    print("\n3. Creating a new user...")
    new_user = {
        "firstName": "Jane",
        "lastName": "Smith",
        "email": "jane.smith@example.com",
        "title": "ms",
        "gender": "female",
        "phone": "555-1234"
    }
    response = requests.post(f"{BASE_URL}/user/create", headers=headers, json=new_user)
    print_response(response)
    created_user_id = response.json()['id'] if response.status_code == 201 else None
    
    # 4. Update the user
    if created_user_id:
        print(f"\n4. Updating user {created_user_id}...")
        update_data = {
            "firstName": "Jane",
            "lastName": "Doe"
        }
        response = requests.put(f"{BASE_URL}/user/{created_user_id}", headers=headers, json=update_data)
        print_response(response)
    
    # 5. Get list of posts
    print("\n5. Getting list of posts...")
    response = requests.get(f"{BASE_URL}/post?limit=3", headers=headers)
    print_response(response)
    
    # 6. Get posts by tag
    print("\n6. Getting posts by tag 'nature'...")
    response = requests.get(f"{BASE_URL}/tag/nature/post", headers=headers)
    print_response(response)
    
    # 7. Create a new post
    print("\n7. Creating a new post...")
    new_post = {
        "text": "This is a test post created via Python!",
        "image": "https://example.com/image.jpg",
        "likes": 0,
        "tags": ["test", "python", "api"],
        "owner": "60d0fe4f5311236168a109ca"
    }
    response = requests.post(f"{BASE_URL}/post/create", headers=headers, json=new_post)
    print_response(response)
    
    # 8. Get comments
    print("\n8. Getting comments...")
    response = requests.get(f"{BASE_URL}/comment?limit=3", headers=headers)
    print_response(response)
    
    # 9. Get tags
    print("\n9. Getting all tags...")
    response = requests.get(f"{BASE_URL}/tag", headers=headers)
    print_response(response)
    
    # 10. Test error handling (missing app-id)
    print("\n10. Testing error handling (missing app-id)...")
    response = requests.get(f"{BASE_URL}/user")
    print_response(response)
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API.")
        print("Make sure the Flask server is running (python app.py)")
    except Exception as e:
        print(f"Error: {e}")
