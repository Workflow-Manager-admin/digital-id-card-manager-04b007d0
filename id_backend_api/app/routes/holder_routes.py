from flask_smorest import Blueprint
from flask import request, jsonify
from flask.views import MethodView
from ..db import get_db_connection
from ..auth import jwt_required

blp = Blueprint("holders", __name__, url_prefix="/holders", description="Digital ID card Holders")

# PUBLIC_INTERFACE
@blp.route("")
class HolderList(MethodView):
    """Create a Holder or list all holders (authentication required)"""

    @jwt_required()
    def get(self):
        """List all digital ID holders"""
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, phone, address FROM holders")
        holders = [
            {"id": row[0], "name": row[1], "email": row[2], "phone": row[3], "address": row[4]}
            for row in cur.fetchall()
        ]
        conn.close()
        return jsonify(holders)

    @jwt_required()
    def post(self):
        """Create a new holder's digital ID profile"""
        data = request.json
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        address = data.get("address")
        if not all([name, email, phone, address]):
            return jsonify({"message": "Missing fields"}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO holders (name, email, phone, address) VALUES (%s, %s, %s, %s) RETURNING id",
            (name, email, phone, address)
        )
        holder_id = cur.fetchone()[0]
        conn.commit()
        conn.close()
        return jsonify({"holder_id": holder_id})

# PUBLIC_INTERFACE
@blp.route("/<int:holder_id>")
class HolderItem(MethodView):
    """Get, update, or delete holder profile (authentication required)"""

    @jwt_required()
    def get(self, holder_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, phone, address FROM holders WHERE id=%s", (holder_id,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return jsonify({"message": "Holder not found"}), 404
        return jsonify({"id": row[0], "name": row[1], "email": row[2], "phone": row[3], "address": row[4]})

    @jwt_required()
    def put(self, holder_id):
        data = request.json
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        address = data.get("address")

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE holders SET name=%s, email=%s, phone=%s, address=%s WHERE id=%s RETURNING id",
            (name, email, phone, address, holder_id)
        )
        if not cur.fetchone():
            conn.close()
            return jsonify({"message": "Holder not found"}), 404
        conn.commit()
        conn.close()
        return jsonify({"holder_id": holder_id})

    @jwt_required()
    def delete(self, holder_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM holders WHERE id=%s RETURNING id", (holder_id,))
        if not cur.fetchone():
            conn.close()
            return jsonify({"message": "Holder not found"}), 404
        conn.commit()
        conn.close()
        return jsonify({"message": "Deleted"})
