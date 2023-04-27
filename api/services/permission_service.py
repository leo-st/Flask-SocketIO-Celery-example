from http import HTTPStatus

from utils.api_error import APIError
from utils.enums import PermissionKey
from models.permission import Permission

def get_all_permissions() -> list[Permission]:
    all_permissions = Permission.query.all()
    return all_permissions


def get_permission_by_key(permission_key: str) -> Permission:
    permission_with_key = Permission.query.filter_by(permission_key=permission_key).first()
    if permission_with_key is None:
        return APIError(HTTPStatus.NOT_FOUND, "permission does not exist")
    return permission_with_key


def get_permissions_by_keys(permission_keys: list[str]) -> list[Permission]:
    permissions_with_keys = Permission.query.filter(Permission.permission_key.in_(permission_keys)).all()
    return permissions_with_keys


def get_permissions_by_ids(permission_ids: list[str]) -> list[Permission]:
    permissions_with_keys = Permission.query.filter(Permission.permission_id.in_(permission_ids)).all()
    return permissions_with_keys


def parse_permissions_keys(input_permission_keys: list[str], default_permissions: list[Permission] = []) -> list[Permission]:
    if input_permission_keys is None:
        return default_permissions
    try:
        some_object_iterator = iter(input_permission_keys)
    except TypeError as te:
        input_permission_keys = [input_permission_keys]
    
    sanitized_input_permission_keys = set(input_permission_keys)
    sanitized_input_permission_keys = list(sanitized_input_permission_keys.intersection(set(PermissionKey.value_list())))
    sanitized_input_permission_keys = get_permissions_by_keys(sanitized_input_permission_keys)
    return sanitized_input_permission_keys


def parse_permission_ids(input_permission_ids: list[int], default_permissions: list[Permission] = []) -> list[Permission]:
    if input_permission_ids is None:
        return default_permissions
    try:
        some_object_iterator = iter(input_permission_ids)
    except TypeError as te:
        input_permission_ids = [input_permission_ids]
    
    sanitized_input_permission_ids = []
    for ipk in input_permission_ids:
        try:
            sanitized_input_permission_ids.append(int(ipk))
        except:
            continue
    
    if len(sanitized_input_permission_ids) == 0:
        return sanitized_input_permission_ids
    
    sanitized_input_permission_ids = get_permissions_by_ids(sanitized_input_permission_ids)
    return sanitized_input_permission_ids
