#!/usr/bin/env python3
""" SessionAuth module for flask routes
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, Flask
from models.user import User
from flask import session
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=True)
def auth_session():
    """ Handles all routes for the Session authentication. """

    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    password_check = user[0].is_valid_password(password)
    if not password_check:
        return jsonify({"error": "wrong password"}), 401
    try:
        from api.v1.app import auth

        session_id = auth.create_session(user[0].id)
        session_name = getenv('SESSION_NAME')
        out = jsonify(user[0].to_json())
        out.set_cookie(session_name, session_id)
    except Exception as e:
        print(e)
    return out


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=True)
def logout_session():
    """ Deletes the user session / logout
    """
    from api.v1.app import auth

    if auth.destroy_session(request):
        return jsonify({}), 200
    else:
        abort(404)
