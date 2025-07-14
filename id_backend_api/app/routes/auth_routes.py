from flask import Blueprint, request, jsonify
from flask.views import MethodView
from werkzeug.security import generate_password_hash, check_password_hash
from ..db import get_db_connection
from ..auth import encode_auth_token

blp = Blueprint("auth", __name__, url_prefix="/auth", description="Authentication routes")

# PUBLIC_INTERFACE
@blp.route("/signup")
class SignUp(MethodView):
    """Register a new user (role-agnostic)"""

    def post(self):
        data = request.json
        username = data.get("username")
        password = data.get("password")
        if not all([username, password]):
            return jsonify({"message": "Missing fields"}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cur.fetchone():
            conn.close()
            return jsonify({"message": "Username already exists"}), 409

        password_hash = generate_password_hash(password)
        cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id",
                    (username, password_hash))
        user_id = cur.fetchone()[0]
        conn.commit()
        conn.close()
        token = encode_auth_token(user_id)
        return jsonify({"user_id": user_id, "token": token})

# PUBLIC_INTERFACE
@blp.route("/login")
class Login(MethodView):
    """Login for registered users (returns JWT, role-agnostic)"""

    def post(self):
        data = request.json
        username = data.get("username")
        password = data.get("password")
        if not all([username, password]):
            return jsonify({"message": "Missing username or password"}), 400
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
        row = cur.fetchone()
        if not row or not check_password_hash(row[1], password):
            conn.close()
            return jsonify({"message": "Invalid credentials"}), 401
        user_id, _ = row
        conn.close()
        token = encode_auth_token(user_id)
        return jsonify({"user_id": user_id, "token": token})
