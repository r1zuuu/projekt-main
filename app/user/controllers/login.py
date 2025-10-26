from flask import Blueprint, request, jsonify, session
from app.user.services.user_service import authenticate_user

login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/user/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user, error = authenticate_user(username, password)
    if error:
        return jsonify({'error': error}), 401

    session['user_id'] = user.id
    return jsonify({
        'message': f'Zalogowano jako {username}',
        'user': user.to_dict()
    }), 200


@login_bp.route('/user/logout', methods=['GET'])
def logout_user():
    session.pop('user_id', None)
    return jsonify({'message': 'Wylogowano pomyślnie'}), 200
