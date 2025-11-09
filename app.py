from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime
from functools import wraps
import time

app = Flask(__name__)
CORS(app)

# Base URL prefix
BASE_URL = '/data/v1'

# Response delay in seconds (set to 0 for no delay)
RESPONSE_DELAY = 2

# Data file paths
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
POSTS_FILE = os.path.join(DATA_DIR, 'posts.json')
COMMENTS_FILE = os.path.join(DATA_DIR, 'comments.json')
TAGS_FILE = os.path.join(DATA_DIR, 'tags.json')


# Helper functions for data management
def load_json(filename):
    """Load data from JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_json(filename, data):
    """Save data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


def get_user_preview(user_id):
    """Get user preview data by ID"""
    users = load_json(USERS_FILE)
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return {
            'id': user['id'],
            'title': user['title'],
            'firstName': user['firstName'],
            'lastName': user['lastName'],
            'picture': user['picture']
        }
    return None


def paginate(data, page, limit):
    """Paginate data and return in list format"""
    start = page * limit
    end = start + limit
    return {
        'data': data[start:end],
        'total': len(data),
        'page': page,
        'limit': limit
    }


# Error response functions
def error_response(error_type, status_code):
    """Return error response"""
    errors = {
        'APP_ID_MISSING': 'app-id header is missing',
        'APP_ID_NOT_EXIST': 'app-id header is invalid',
        'PARAMS_NOT_VALID': 'URL parameters are not valid',
        'BODY_NOT_VALID': 'Request body is not valid',
        'RESOURCE_NOT_FOUND': 'Resource not found',
        'PATH_NOT_FOUND': 'Path not found',
        'SERVER_ERROR': 'Server error'
    }
    return jsonify({'error': error_type, 'message': errors.get(error_type, 'Unknown error')}), status_code


# Middleware for app-id validation
def require_app_id(f):
    """Decorator to check for app-id header"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        app_id = request.headers.get('app-id')
        if not app_id:
            return error_response('APP_ID_MISSING', 403)
        # For simplicity, we accept any non-empty app-id
        # In a real app, you would validate against a database
        
        # Apply response delay
        if RESPONSE_DELAY > 0:
            time.sleep(RESPONSE_DELAY)
        
        return f(*args, **kwargs)
    return decorated_function


# ============================================================================
# USER CONTROLLER
# ============================================================================

@app.route(f'{BASE_URL}/user', methods=['GET'])
@require_app_id
def get_users():
    """Get list of users"""
    try:
        page = int(request.args.get('page', 0))
        limit = int(request.args.get('limit', 20))
        created = request.args.get('created', '0')
        
        # Validate pagination params
        if not (0 <= page <= 999):
            return error_response('PARAMS_NOT_VALID', 400)
        if not (5 <= limit <= 50):
            return error_response('PARAMS_NOT_VALID', 400)
        
        users = load_json(USERS_FILE)
        
        # Convert to preview format
        users_preview = [{
            'id': u['id'],
            'title': u['title'],
            'firstName': u['firstName'],
            'lastName': u['lastName'],
            'picture': u['picture']
        } for u in users]
        
        return jsonify(paginate(users_preview, page, limit))
    except Exception as e:
        return error_response('SERVER_ERROR', 500)


@app.route(f'{BASE_URL}/user/<user_id>', methods=['GET'])
@require_app_id
def get_user(user_id):
    """Get user by id"""
    try:
        users = load_json(USERS_FILE)
        user = next((u for u in users if u['id'] == user_id), None)
        
        if not user:
            return error_response('RESOURCE_NOT_FOUND', 404)
        
        return jsonify(user)
    except Exception as e:
        return error_response('SERVER_ERROR', 500)


@app.route(f'{BASE_URL}/user/create', methods=['POST'])
@require_app_id
def create_user():
    """Create new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not all(k in data for k in ['firstName', 'lastName', 'email']):
            return error_response('BODY_NOT_VALID', 400)
        
        users = load_json(USERS_FILE)
        
        # Generate new ID (simple incremental)
        import random
        new_id = f"60d0fe4f5311236168a109{random.randint(1000, 9999)}"
        
        new_user = {
            'id': new_id,
            'title': data.get('title', ''),
            'firstName': data['firstName'],
            'lastName': data['lastName'],
            'gender': data.get('gender', ''),
            'email': data['email'],
            'dateOfBirth': data.get('dateOfBirth', ''),
            'registerDate': datetime.utcnow().isoformat() + 'Z',
            'phone': data.get('phone', ''),
            'picture': data.get('picture', ''),
            'location': data.get('location', {
                'street': '',
                'city': '',
                'state': '',
                'country': '',
                'timezone': ''
            })
        }
        
        users.append(new_user)
        save_json(USERS_FILE, users)
        
        return jsonify(new_user), 201
    except Exception as e:
        return error_response('SERVER_ERROR', 500)


@app.route(f'{BASE_URL}/user/<user_id>', methods=['PUT'])
@require_app_id
def update_user(user_id):
    """Update user by id"""
    try:
        data = request.get_json()
        
        if not data:
            return error_response('BODY_NOT_VALID', 400)
        
        # Email cannot be updated
        if 'email' in data:
            return error_response('BODY_NOT_VALID', 400)
        
        users = load_json(USERS_FILE)
        user_index = next((i for i, u in enumerate(users) if u['id'] == user_id), None)
        
        if user_index is None:
            return error_response('RESOURCE_NOT_FOUND', 404)
        
        # Update user fields
        for key, value in data.items():
            if key in users[user_index] and key != 'id' and key != 'registerDate':
                users[user_index][key] = value
        
        save_json(USERS_FILE, users)
        
        return jsonify(users[user_index])
    except Exception as e:
        return error_response('SERVER_ERROR', 500)


@app.route(f'{BASE_URL}/user/<user_id>', methods=['DELETE'])
@require_app_id
def delete_user(user_id):
    """Delete user by id"""
    try:
        users = load_json(USERS_FILE)
        user_index = next((i for i, u in enumerate(users) if u['id'] == user_id), None)
        
        if user_index is None:
            return error_response('RESOURCE_NOT_FOUND', 404)
        
        users.pop(user_index)
        save_json(USERS_FILE, users)
        
        return jsonify(user_id)
    except Exception as e:
        return error_response('SERVER_ERROR', 500)


# ============================================================================
# POST CONTROLLER
# ============================================================================

@app.route(f'{BASE_URL}/post', methods=['GET'])
@require_app_id
def get_posts():
    """Get list of posts"""
    try:
        page = int(request.args.get('page', 0))
        limit = int(request.args.get('limit', 20))
        
        if not (0 <= page <= 999):
            return error_response('PARAMS_NOT_VALID', 400)
        if not (5 <= limit <= 50):
            return error_response('PARAMS_NOT_VALID', 400)
        
        posts = load_json(POSTS_FILE)
        
        # Add owner preview to each post
        posts_with_owner = []
        for post in posts:
            owner_preview = get_user_preview(post['owner'])
            if owner_preview:
                post_copy = post.copy()
                post_copy['owner'] = owner_preview
                posts_with_owner.append(post_copy)
        
        return jsonify(paginate(posts_with_owner, page, limit))
    except Exception as e:
        return error_response('SERVER_ERROR', 500)


@app.route(f'{BASE_URL}/user/<user_id>/post', methods=['GET'])
@require_app_id
def get_posts_by_user(user_id):
    """Get posts by user"""
    try:
        page = int(request.args.get('page', 0))
        limit = int(request.args.get('limit', 20))
        
        if not (0 <= page <= 999):
            return error_response('PARAMS_NOT_VALID', 400)
        if not (5 <= limit <= 50):
            return error_response('PARAMS_NOT_VALID', 400)
        
        posts = load_json(POSTS_FILE)
        user_posts = [p for p in posts if p['owner'] == user_id]
        
        # Add owner preview
        posts_with_owner = []
        for post in user_posts:
            owner_preview = get_user_preview(post['owner'])
            if owner_preview:
                post_copy = post.copy()
                post_copy['owner'] = owner_preview
                posts_with_owner.append(post_copy)
        
        return jsonify(paginate(posts_with_owner, page, limit))
    except Exception as e:
        return error_response('SERVER_ERROR', 500)


@app.route(f'{BASE_URL}/tag/<tag>/post', methods=['GET'])
@require_app_id
def get_posts_by_tag(tag):
    """Get posts by tag"""
    try:
        page = int(request.args.get('page', 0))
        limit = int(request.args.get('limit', 20))
        
        if not (0 <= page <= 999):
            return error_response('PARAMS_NOT_VALID', 400)
        if not (5 <= limit <= 50):
            return error_response('PARAMS_NOT_VALID', 400)
        
        posts = load_json(POSTS_FILE)
        tag_posts = [p for p in posts if tag in p.get('tags', [])]
        
        # Add owner preview
        posts_with_owner = []
        for post in tag_posts:
            owner_preview = get_user_preview(post['owner'])
            if owner_preview:
                post_copy = post.copy()
                post_copy['owner'] = owner_preview
                posts_with_owner.append(post_copy)
        
        return jsonify(paginate(posts_with_owner, page, limit))
    except Exception as e:
        return error_response('SERVER_ERROR', 500)


@app.route(f'{BASE_URL}/post/<post_id>', methods=['GET'])
@require_app_id
def get_post(post_id):
    """Get post by id"""
    try:
        posts = load_json(POSTS_FILE)
        post = next((p for p in posts if p['id'] == post_id), None)
        
        if not post:
            return error_response('RESOURCE_NOT_FOUND', 404)
        
        # Add owner preview
        owner_preview = get_user_preview(post['owner'])
        if owner_preview:
            post = post.copy()
            post['owner'] = owner_preview
        
        return jsonify(post)
    except Exception as e:
        return error_response('SERVER_ERROR', 500)


@app.route(f'{BASE_URL}/post/create', methods=['POST'])
@require_app_id
def create_post():
    """Create new post"""
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['text', 'owner']):
            return error_response('BODY_NOT_VALID', 400)
        
        posts = load_json(POSTS_FILE)
        
        # Generate new ID
        import random
        new_id = f"60d21b4667d0d8992e610{random.randint(1000, 9999)}"
        
        new_post = {
            'id': new_id,
            'text': data['text'],
            'image': data.get('image', ''),
            'likes': data.get('likes', 0),
            'tags': data.get('tags', []),
            'publishDate': datetime.utcnow().isoformat() + 'Z',
            'owner': data['owner']
        }
        
        posts.append(new_post)
        save_json(POSTS_FILE, posts)
        
        # Add owner preview
        owner_preview = get_user_preview(new_post['owner'])
        if owner_preview:
            new_post_response = new_post.copy()
            new_post_response['owner'] = owner_preview
            return jsonify(new_post_response), 201
        
        return jsonify(new_post), 201
    except Exception as e:
        return error_response('SERVER_ERROR', 500)


@app.route(f'{BASE_URL}/post/<post_id>', methods=['PUT'])
@require_app_id
def update_post(post_id):
    """Update post by id"""
    try:
        data = request.get_json()
        
        if not data:
            return error_response('BODY_NOT_VALID', 400)
        
        # Owner cannot be updated
        if 'owner' in data:
            return error_response('BODY_NOT_VALID', 400)
        
        posts = load_json(POSTS_FILE)
        post_index = next((i for i, p in enumerate(posts) if p['id'] == post_id), None)
        
        if post_index is None:
            return error_response('RESOURCE_NOT_FOUND', 404)
        
        # Update post fields
        for key, value in data.items():
            if key in posts[post_index] and key != 'id' and key != 'publishDate':
                posts[post_index][key] = value
        
        save_json(POSTS_FILE, posts)
        
        # Add owner preview
        owner_preview = get_user_preview(posts[post_index]['owner'])
        post_response = posts[post_index].copy()
        if owner_preview:
            post_response['owner'] = owner_preview
        
        return jsonify(post_response)
    except Exception as e:
        return error_response('SERVER_ERROR', 500)


@app.route(f'{BASE_URL}/post/<post_id>', methods=['DELETE'])
@require_app_id
def delete_post(post_id):
    """Delete post by id"""
    try:
        posts = load_json(POSTS_FILE)
        post_index = next((i for i, p in enumerate(posts) if p['id'] == post_id), None)
        
        if post_index is None:
            return error_response('RESOURCE_NOT_FOUND', 404)
        
        posts.pop(post_index)
        save_json(POSTS_FILE, posts)
        
        return jsonify(post_id)
    except Exception as e:
        return error_response('SERVER_ERROR', 500)


# ============================================================================
# COMMENT CONTROLLER
# ============================================================================

@app.route(f'{BASE_URL}/comment', methods=['GET'])
@require_app_id
def get_comments():
    """Get list of comments"""
    try:
        page = int(request.args.get('page', 0))
        limit = int(request.args.get('limit', 20))
        
        if not (0 <= page <= 999):
            return error_response('PARAMS_NOT_VALID', 400)
        if not (5 <= limit <= 50):
            return error_response('PARAMS_NOT_VALID', 400)
        
        comments = load_json(COMMENTS_FILE)
        
        # Add owner preview
        comments_with_owner = []
        for comment in comments:
            owner_preview = get_user_preview(comment['owner'])
            if owner_preview:
                comment_copy = comment.copy()
                comment_copy['owner'] = owner_preview
                comments_with_owner.append(comment_copy)
        
        return jsonify(paginate(comments_with_owner, page, limit))
    except Exception as e:
        return error_response('SERVER_ERROR', 500)


@app.route(f'{BASE_URL}/post/<post_id>/comment', methods=['GET'])
@require_app_id
def get_comments_by_post(post_id):
    """Get comments by post"""
    try:
        page = int(request.args.get('page', 0))
        limit = int(request.args.get('limit', 20))
        
        if not (0 <= page <= 999):
            return error_response('PARAMS_NOT_VALID', 400)
        if not (5 <= limit <= 50):
            return error_response('PARAMS_NOT_VALID', 400)
        
        comments = load_json(COMMENTS_FILE)
        post_comments = [c for c in comments if c['post'] == post_id]
        
        # Add owner preview
        comments_with_owner = []
        for comment in post_comments:
            owner_preview = get_user_preview(comment['owner'])
            if owner_preview:
                comment_copy = comment.copy()
                comment_copy['owner'] = owner_preview
                comments_with_owner.append(comment_copy)
        
        return jsonify(paginate(comments_with_owner, page, limit))
    except Exception as e:
        return error_response('SERVER_ERROR', 500)


@app.route(f'{BASE_URL}/user/<user_id>/comment', methods=['GET'])
@require_app_id
def get_comments_by_user(user_id):
    """Get comments by user"""
    try:
        page = int(request.args.get('page', 0))
        limit = int(request.args.get('limit', 20))
        
        if not (0 <= page <= 999):
            return error_response('PARAMS_NOT_VALID', 400)
        if not (5 <= limit <= 50):
            return error_response('PARAMS_NOT_VALID', 400)
        
        comments = load_json(COMMENTS_FILE)
        user_comments = [c for c in comments if c['owner'] == user_id]
        
        # Add owner preview
        comments_with_owner = []
        for comment in user_comments:
            owner_preview = get_user_preview(comment['owner'])
            if owner_preview:
                comment_copy = comment.copy()
                comment_copy['owner'] = owner_preview
                comments_with_owner.append(comment_copy)
        
        return jsonify(paginate(comments_with_owner, page, limit))
    except Exception as e:
        return error_response('SERVER_ERROR', 500)


@app.route(f'{BASE_URL}/comment/create', methods=['POST'])
@require_app_id
def create_comment():
    """Create new comment"""
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['message', 'owner', 'post']):
            return error_response('BODY_NOT_VALID', 400)
        
        comments = load_json(COMMENTS_FILE)
        
        # Generate new ID
        import random
        new_id = f"60d21b9967d0d8992e610{random.randint(1000, 9999)}"
        
        new_comment = {
            'id': new_id,
            'message': data['message'],
            'owner': data['owner'],
            'post': data['post'],
            'publishDate': datetime.utcnow().isoformat() + 'Z'
        }
        
        comments.append(new_comment)
        save_json(COMMENTS_FILE, comments)
        
        # Add owner preview
        owner_preview = get_user_preview(new_comment['owner'])
        if owner_preview:
            new_comment_response = new_comment.copy()
            new_comment_response['owner'] = owner_preview
            return jsonify(new_comment_response), 201
        
        return jsonify(new_comment), 201
    except Exception as e:
        return error_response('SERVER_ERROR', 500)


@app.route(f'{BASE_URL}/comment/<comment_id>', methods=['DELETE'])
@require_app_id
def delete_comment(comment_id):
    """Delete comment by id"""
    try:
        comments = load_json(COMMENTS_FILE)
        comment_index = next((i for i, c in enumerate(comments) if c['id'] == comment_id), None)
        
        if comment_index is None:
            return error_response('RESOURCE_NOT_FOUND', 404)
        
        comments.pop(comment_index)
        save_json(COMMENTS_FILE, comments)
        
        return jsonify(comment_id)
    except Exception as e:
        return error_response('SERVER_ERROR', 500)


# ============================================================================
# TAG CONTROLLER
# ============================================================================

@app.route(f'{BASE_URL}/tag', methods=['GET'])
@require_app_id
def get_tags():
    """Get list of tags"""
    try:
        tags = load_json(TAGS_FILE)
        return jsonify({'data': tags})
    except Exception as e:
        return error_response('SERVER_ERROR', 500)


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return error_response('PATH_NOT_FOUND', 404)


@app.errorhandler(500)
def internal_error(error):
    return error_response('SERVER_ERROR', 500)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Create data directory if it doesn't exist
    os.makedirs(DATA_DIR, exist_ok=True)
    
    print("=" * 60)
    print("DummyAPI Flask Server")
    print("=" * 60)
    print(f"Base URL: http://localhost:5000{BASE_URL}")
    print("Required header: app-id: <your-app-id>")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
