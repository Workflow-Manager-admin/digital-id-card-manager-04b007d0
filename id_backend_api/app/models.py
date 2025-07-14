from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# PUBLIC_INTERFACE
class User:
    """User model representing users of Digital ID Card system.

    All users are considered generic. There is no role or RBAC logic.
    """
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.created_at = datetime.utcnow()

    def check_password(self, password):
        """Check supplied password for match."""
        return check_password_hash(self.password_hash, password)

# PUBLIC_INTERFACE
class Holder:
    """Holder model representing a person's digital ID profile."""
    def __init__(self, id, name, email, phone, address):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.created_at = datetime.utcnow()

# PUBLIC_INTERFACE
class IDCard:
    """ID Card model containing unique number and mapped Holder profile."""
    def __init__(self, id, holder_id, unique_number):
        self.id = id
        self.holder_id = holder_id  # FK to Holder
        self.unique_number = unique_number
        self.created_at = datetime.utcnow()
