from flask import Blueprint, jsonify, session
from app.user.services.user_service import get_user_by_id

profile_bp = Blueprint('profile_bp', __name__)

@profile_bp.route('/user/profile', methods=['GET'])
def get_profile():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Nie jesteś zalogowany'}), 401

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'Użytkownik nie istnieje'}), 404

    return jsonify(user.to_dict()), 200
