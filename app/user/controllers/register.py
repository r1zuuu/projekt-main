from flask import Blueprint, request, jsonify
from app.user.services.user_service import create_user

register_bp = Blueprint('register_bp', __name__)

@register_bp.route('/user/register', methods=['POST'])
def register_user():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    user, error = create_user(username, password)
    if error:
        return jsonify({'error': error}), 400

    return jsonify({
        'message': 'Zarejestrowano pomyślnie',
        'user': user.to_dict()
    }), 201
