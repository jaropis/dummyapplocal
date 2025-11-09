#!/bin/bash

# DummyAPI Test Script
# This script tests the Flask API endpoints

BASE_URL="http://localhost:5000/data/v1"
APP_ID="0JyYiOQXQQr5H9OEn21312"

echo "================================"
echo "DummyAPI Test Script"
echo "================================"
echo ""

# Test 1: Get list of users
echo "1. Getting list of users..."
curl -s -H "app-id: $APP_ID" "$BASE_URL/user?page=0&limit=5" | python3 -m json.tool
echo ""
echo "---"
echo ""

# Test 2: Get specific user
echo "2. Getting user by ID..."
curl -s -H "app-id: $APP_ID" "$BASE_URL/user/60d0fe4f5311236168a109ca" | python3 -m json.tool
echo ""
echo "---"
echo ""

# Test 3: Get list of posts
echo "3. Getting list of posts..."
curl -s -H "app-id: $APP_ID" "$BASE_URL/post?page=0&limit=5" | python3 -m json.tool
echo ""
echo "---"
echo ""

# Test 4: Get posts by tag
echo "4. Getting posts by tag 'nature'..."
curl -s -H "app-id: $APP_ID" "$BASE_URL/tag/nature/post" | python3 -m json.tool
echo ""
echo "---"
echo ""

# Test 5: Get comments
echo "5. Getting list of comments..."
curl -s -H "app-id: $APP_ID" "$BASE_URL/comment?limit=5" | python3 -m json.tool
echo ""
echo "---"
echo ""

# Test 6: Get tags
echo "6. Getting list of tags..."
curl -s -H "app-id: $APP_ID" "$BASE_URL/tag" | python3 -m json.tool
echo ""
echo "---"
echo ""

# Test 7: Create a new user
echo "7. Creating a new user..."
curl -s -X POST -H "app-id: $APP_ID" -H "Content-Type: application/json" \
  -d '{
    "firstName": "Test",
    "lastName": "User",
    "email": "test.user@example.com",
    "title": "mr",
    "gender": "male",
    "phone": "555-0000"
  }' \
  "$BASE_URL/user/create" | python3 -m json.tool
echo ""
echo "---"
echo ""

# Test 8: Test error - missing app-id
echo "8. Testing error handling (missing app-id)..."
curl -s "$BASE_URL/user" | python3 -m json.tool
echo ""
echo "---"
echo ""

echo "================================"
echo "Tests completed!"
echo "================================"
