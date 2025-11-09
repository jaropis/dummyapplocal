# DummyAPI Flask Implementation

A Flask-based API that mimics the DummyAPI.io structure.

## Installation

```bash
pip install -r requirements.txt
```

## Running the API

```bash
python app.py
```

The API will be available at `http://localhost:5000/data/v1/`

## Usage

All requests require the `app-id` header:

```bash
curl -H "app-id: 0JyYiOQXQQr5H9OEn21312" http://localhost:5000/data/v1/user
```

## Endpoints

### User Controller

- GET `/data/v1/user` - Get list of users
- GET `/data/v1/user/:id` - Get user by id
- POST `/data/v1/user/create` - Create new user
- PUT `/data/v1/user/:id` - Update user
- DELETE `/data/v1/user/:id` - Delete user

### Post Controller

- GET `/data/v1/post` - Get list of posts
- GET `/data/v1/user/:id/post` - Get posts by user
- GET `/data/v1/tag/:id/post` - Get posts by tag
- GET `/data/v1/post/:id` - Get post by id
- POST `/data/v1/post/create` - Create new post
- PUT `/data/v1/post/:id` - Update post
- DELETE `/data/v1/post/:id` - Delete post

### Comment Controller

- GET `/data/v1/comment` - Get list of comments
- GET `/data/v1/post/:id/comment` - Get comments by post
- GET `/data/v1/user/:id/comment` - Get comments by user
- POST `/data/v1/comment/create` - Create new comment
- DELETE `/data/v1/comment/:id` - Delete comment

### Tag Controller

- GET `/data/v1/tag` - Get list of tags
# dummyapplocal
