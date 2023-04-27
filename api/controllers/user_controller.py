from http import HTTPStatus
from flask import Blueprint, request, make_response, jsonify, send_from_directory, current_app
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, set_access_cookies, unset_jwt_cookies

from utils.api_error import APIError
from services.user_service import user_login_test, get_user_by, create_user, update_user_with_id, get_all_users, get_user_with_id
from utils.enums import PermissionKey
from app import socketio

user_controller = Blueprint('user_controller', __name__)


@user_controller.route("/v1/login", methods=["POST"])
def login():
    req = request.json
    if not req or not req.get("email") or not req.get("password"):
        # returns 401 if any email or / and password is missing
        return make_response({"message": "Missing user details"}, HTTPStatus.UNAUTHORIZED.value)
    
    res = user_login_test(req)
    
    if isinstance(res, APIError):
        return res.get_response()

    access_token = create_access_token(identity=res.email)
    response = make_response({"message": "login successful"})
    set_access_cookies(response, access_token)

    return response

@user_controller.route("/v1/logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify({"message": "logout successful"})
    unset_jwt_cookies(response)
    return response


@user_controller.route("/v1/users/me", methods=["GET"])
@jwt_required()
def get_current_user():
    res = get_user_by(get_jwt_identity())
    
    if isinstance(res, APIError):
        return res.get_response()
    
    return make_response(res.to_response_dict(), HTTPStatus.OK.value)


@user_controller.route("/v1/users", methods=["POST", "GET"])
@jwt_required()
def users():
    request_user = get_user_by(get_jwt_identity())
    if isinstance(request_user, APIError):
        return res.get_response()

    if request.method == "POST":
        if PermissionKey.USERS_CAN_CREATE_USER.value in list(request_user.role.permission_keys):
            res = create_user(request.json)
            if isinstance(res, APIError):
                return res.get_response()
            
            return make_response(res.to_response_dict(), HTTPStatus.CREATED.value)

    elif request.method == "GET":
        if PermissionKey.USERS_CAN_VIEW_USER_LIST.value in list(request_user.role.permission_keys):
            res = get_all_users()
            return make_response([u.to_response_dict() for u in res], HTTPStatus.OK.value)
    
    return make_response({"message": "unauthorized request"}, HTTPStatus.UNAUTHORIZED.value)


@user_controller.route("/v1/users/<int:user_id>", methods=["PUT", "GET"])
@jwt_required()
def user_with(user_id):
    request_user = get_user_by(get_jwt_identity())
    if isinstance(request_user, APIError):
        return res.get_response()

    if request.method == "PUT":
        if user_id == request_user.user_id or PermissionKey.USERS_CAN_EDIT_OTHER_USERS.value in list(request_user.role.permission_keys):
            res = update_user_with_id(request.json, user_id)
            if isinstance(res, APIError):
                return res.get_response()
            
            return make_response(res.to_response_dict(), HTTPStatus.OK.value)
        

    elif request.method == "GET":
        if user_id == request_user.user_id or PermissionKey.USERS_CAN_VIEW_USER_LIST.value in list(request_user.role.permission_keys):
            res = get_user_with_id(user_id)
            if isinstance(res, APIError):
                return res.get_response()
            
            return make_response(res.to_response_dict(), HTTPStatus.OK.value)
    
    return make_response({"message": "Unauthorized request"}, HTTPStatus.UNAUTHORIZED.value)

@user_controller.route("/v1/room_1", methods=["GET", "POST"])
def room_1():
    print("this is a test")
    if True:
        socketio.emit("privatemsg", {'username': 'leo', 'text': 'leo'}, room='leo') 
    return make_response('finished')