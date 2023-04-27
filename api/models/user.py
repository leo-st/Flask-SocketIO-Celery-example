from http import HTTPStatus
from typing import Any, Union

from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from utils.api_error import APIError
from utils.input_parsers import (parse_bool, parse_email, parse_hash_pw,
                                 parse_int, parse_language,
                                 parse_non_empty_str)

from models import db


BaseModel: DefaultMeta = db.Model


USER_ID_SEQ = db.Sequence('app_user_id_seq')  # define sequence explicitly


DEFAULT_ROLE_ID = 2


class User(BaseModel):
    __tablename__ = 'app_user'

    user_id = Column(Integer, USER_ID_SEQ, primary_key=True, server_default=USER_ID_SEQ.next_value())
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    enabled = Column(Boolean, nullable=False, server_default=text("true"))
    language = Column(String, server_default=text("'DE'::character varying"))
    pw_hash = Column(String, nullable=False)
    pw_reset_required = Column(Boolean, nullable=False, server_default=text("true"))
    
    # a user has only one role -> uselist=False
    # otherwise role would be a list of one role
    role_id = Column(Integer, ForeignKey("app_role.role_id"))
    role = relationship('Role', backref='app_role', lazy='select', uselist=False)

    def to_response_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'email': self.email,
            'first_name': self.first_name,
            'enabled': self.enabled,
            'language': self.language,
            'last_name': self.last_name,
            'role_name': str(self.role.role_name),
            'permission_keys': list(self.role.permission_keys)
        }
    
    def to_minimal_response_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "user_name": f"{self.first_name} {self.last_name}"
        }
    

    @staticmethod
    def create_from_dict(obj: Any, reset_pw_required: bool = True) -> Union['User', APIError]:
        _email = parse_email(obj.get("email"))
        if _email is None:
            return APIError(HTTPStatus.BAD_REQUEST, "missing or invalid email attribute")
        _first_name = parse_non_empty_str(obj.get("first_name"))
        if _first_name is None:
            return APIError(HTTPStatus.BAD_REQUEST, "missing or invalid first_name attribute")
        _last_name = parse_non_empty_str(obj.get("last_name"))
        if _last_name is None:
            return APIError(HTTPStatus.BAD_REQUEST, "missing or invalid last_name attribute")
        _enabled = parse_bool(obj.get("enabled"))
        _language = parse_language(obj.get("language"))
        _password = parse_hash_pw(obj.get("password"))
        if _password is None:
            return APIError(HTTPStatus.BAD_REQUEST, "missing or invalid password attribute")
        _pw_reset_required = reset_pw_required
        _role_id = parse_int(obj.get("role_id"), DEFAULT_ROLE_ID)
        
        return User(email = _email, first_name = _first_name, last_name = _last_name, enabled = _enabled, language = _language, pw_hash = _password, pw_reset_required = _pw_reset_required, role_id = _role_id)
    

    def update_from_dict(self, obj: Any, reset_pw_required: bool = True) -> None:
        _email = parse_email(obj.get("email"), self.email)
        _first_name = parse_non_empty_str(obj.get("first_name"), self.first_name)
        _last_name = parse_non_empty_str(obj.get("last_name"), self.last_name)
        _enabled = parse_bool(obj.get("enabled"))
        _language = parse_language(obj.get("language"), self.language)
        _password = parse_hash_pw(obj.get("password"), self.pw_hash)
        _pw_reset_required = reset_pw_required
        _role_id = parse_int(obj.get("role_id"), DEFAULT_ROLE_ID)

        self.email = _email
        self.first_name = _first_name
        self.last_name = _last_name
        self.enabled = _enabled
        self.language = _language
        self.pw_hash = _password
        self.pw_reset_required = _pw_reset_required
        self.role_id = _role_id

        return
