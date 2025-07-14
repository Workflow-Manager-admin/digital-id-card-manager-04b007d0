from flask_smorest import Blueprint
from flask import request, jsonify
from flask.views import MethodView
from ..db import get_db_connection
from ..auth import jwt_required

blp = Blueprint("idcards", __name__, url_prefix="/idcards", description="ID Card operations")

# PUBLIC_INTERFACE
@blp.route("")
class IDCardList(MethodView):
    """List and create ID cards (authentication required)"""

    @jwt_required()
    def get(self):
        """List all ID cards"""
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, holder_id, unique_number FROM idcards")
        cards = [
            {"id": row[0], "holder_id": row[1], "unique_number": row[2]}
            for row in cur.fetchall()
        ]
        conn.close()
        return jsonify(cards)

    @jwt_required()
    def post(self):
        """Create new unique number, optionally link holder"""
        data = request.json
        holder_id = data.get("holder_id")
        unique_number = data.get("unique_number")
        if not unique_number:
            return jsonify({"message": "Missing unique_number"}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        if holder_id:
            cur.execute("SELECT id FROM holders WHERE id=%s", (holder_id,))
            if not cur.fetchone():
                conn.close()
                return jsonify({"message": "Holder not found"}), 404

        cur.execute(
            "INSERT INTO idcards (holder_id, unique_number) VALUES (%s, %s) RETURNING id",
            (holder_id, unique_number)
        )
        card_id = cur.fetchone()[0]
        conn.commit()
        conn.close()
        return jsonify({"id": card_id})

# PUBLIC_INTERFACE
@blp.route("/<int:idcard_id>")
class IDCardItem(MethodView):
    """Get/update/delete a single ID card (authentication required)"""

    @jwt_required()
    def get(self, idcard_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, holder_id, unique_number FROM idcards WHERE id=%s", (idcard_id,)
        )
        row = cur.fetchone()
        conn.close()
        if not row:
            return jsonify({"message": "ID card not found"}), 404
        return jsonify({"id": row[0], "holder_id": row[1], "unique_number": row[2]})

    @jwt_required()
    def put(self, idcard_id):
        data = request.json
        holder_id = data.get("holder_id")
        unique_number = data.get("unique_number")

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE idcards SET holder_id=%s, unique_number=%s WHERE id=%s RETURNING id",
            (holder_id, unique_number, idcard_id)
        )
        if not cur.fetchone():
            conn.close()
            return jsonify({"message": "ID card not found"}), 404
        conn.commit()
        conn.close()
        return jsonify({"id": idcard_id})

    @jwt_required()
    def delete(self, idcard_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM idcards WHERE id=%s RETURNING id", (idcard_id,))
        if not cur.fetchone():
            conn.close()
            return jsonify({"message": "ID card not found"}), 404
        conn.commit()
        conn.close()
        return jsonify({"message": "Deleted"})

# PUBLIC_INTERFACE
@blp.route("/link", methods=["POST"])
class IDCardLink(MethodView):
    """Link a unique number to a holder (authentication required)"""

    @jwt_required()
    def post(self):
        data = request.json
        idcard_id = data.get("idcard_id")
        holder_id = data.get("holder_id")
        if not idcard_id or not holder_id:
            return jsonify({"message": "Missing fields"}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM idcards WHERE id=%s", (idcard_id,))
        if not cur.fetchone():
            conn.close()
            return jsonify({"message": "ID card not found"}), 404

        cur.execute("SELECT id FROM holders WHERE id=%s", (holder_id,))
        if not cur.fetchone():
            conn.close()
            return jsonify({"message": "Holder not found"}), 404

        cur.execute("UPDATE idcards SET holder_id=%s WHERE id=%s RETURNING id",
                    (holder_id, idcard_id))
        if not cur.fetchone():
            conn.close()
            return jsonify({"message": "Linking failed"}), 400
        conn.commit()
        conn.close()
        return jsonify({"message": "Linked"})
