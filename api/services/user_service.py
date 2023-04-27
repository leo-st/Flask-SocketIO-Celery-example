from http import HTTPStatus

from werkzeug.security import check_password_hash

from utils.api_error import APIError
from utils.input_parsers import parse_int
from models.user import User
from models.role import Role
from models.permission import Permission
from models.permission_group import PermissionGroup
from models import db


def user_login_test(request) -> User | APIError:
    # creates dictionary of form data
    user = User.query.filter_by(email=request.get("email").strip().lower()).first()
    if not user:
        return APIError(HTTPStatus.NOT_FOUND, "user does not exist")
    if check_password_hash(user.pw_hash, request.get("password").strip()):
        return user
    
    return APIError(HTTPStatus.UNAUTHORIZED, "unauthorized request")


def get_user_role(email: str) -> Role | APIError:
    user = User.query.filter_by(email=email.strip().lower()).first()
    if not user:
        return APIError(HTTPStatus.NOT_FOUND, "user does not exist")
    
    return user.role


def get_user_permissions(email: str) -> list[str] | APIError:
    user = User.query.filter_by(email=email.strip().lower()).first()
    if not user:
        return APIError(HTTPStatus.NOT_FOUND, "user does not exist")
    
    return list(user.role.permission_keys)


def get_user_by(email: str) -> User | APIError:
    user: User = User.query.filter_by(email=email.strip().lower()).first()
    if not user:
        return APIError(HTTPStatus.NOT_FOUND, "user does not exist")
    
    return user


def create_user(request_json) -> User | APIError:
    new_user = User.create_from_dict(request_json)
    if isinstance(new_user, APIError):
        return new_user
    
    existing_user = User.query.filter_by(email=new_user.email).first()
    if existing_user:
        return APIError(HTTPStatus.CONFLICT, "user with email already exist")
    
    db.session.add(new_user)
    db.session.commit()

    return new_user


def get_all_users() -> list[User]:
    all_users = User.query.order_by(User.user_id.asc()).all()
    return all_users


def get_user_with_id(user_id: int) -> User | APIError:
    user_with_id: User = User.query.filter_by(user_id=user_id).first()
    if user_with_id is None:
        return APIError(HTTPStatus.NOT_FOUND, "user does not exist")
    
    return user_with_id


def update_user_with_id(request_json, user_id: int) -> User | APIError:
    user_with_id: User = User.query.filter_by(user_id=user_id).first()
    if user_with_id is None:
        return APIError(HTTPStatus.NOT_FOUND, "user does not exist")
    
    user_with_id.update_from_dict(request_json)
    db.session.commit()

    return user_with_id


def parse_user_id(input_user_id: int, default_user: User = None) -> User | None:
    sanitized_input_user_id = parse_int(input_user_id)
    if sanitized_input_user_id is None:
        return default_user
    user_with_id = User.query.filter_by(user_id=sanitized_input_user_id).first()
    if user_with_id is None:
        return default_user
    return user_with_id
