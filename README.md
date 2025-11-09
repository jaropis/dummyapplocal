# DummyAPI Flask Implementation

A Flask-based API that mimics the DummyAPI.io structure. I made it because I needed it for my educational activitiesa and dummyapi seems to be down a lot or you can't log in. Now you can use it locally.

## Installation

```bash
pip install -r requirements.txt
```

## Running the API

```bash
python app.py
```

The API will be available at `http://localhost:5000/data/v1/`

## Configuration

### Response Delay

You can simulate network latency by setting the `RESPONSE_DELAY` variable in `app.py`. This will delay all API responses by the specified number of seconds.

- Set to `0` (default) for no delay
- Set to `2` for a 2-second delay on all responses
- Useful for testing loading states and async behavior in your frontend

To configure the delay, edit line 16 in `app.py`:

```python
RESPONSE_DELAY = 2  # Delay all responses by 2 seconds
```

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

# dummyapplocal
