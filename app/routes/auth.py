from flask_jwt_extended import get_jwt_identity


def current_user_id() -> int:
    """JWT identities are stored as strings; convert once so services compare ints."""
    return int(get_jwt_identity())
