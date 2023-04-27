from http import HTTPStatus
from typing import Any, Union

from flask_sqlalchemy.model import DefaultMeta
from services.permission_service import parse_permission_ids
from sqlalchemy import (Boolean, Column, ForeignKey, Integer, Sequence, Table,
                        Text, text)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from utils.api_error import APIError
from utils.input_parsers import parse_non_empty_str

from models import db


BaseModel: DefaultMeta = db.Model


ROLE_ID_SEQ = Sequence('app_role_id_seq')  # define sequence explicitly


class Role(BaseModel):
    __tablename__ = 'app_role'

    role_id = Column(Integer, ROLE_ID_SEQ, primary_key=True,
                     server_default=ROLE_ID_SEQ.next_value())
    role_name = Column(Text, nullable=False,
                       server_default=text("'Neuer Benutzertyp'::text"))
    locked = Column(Boolean, nullable=False, server_default=text("true"))

    permissions = relationship('Permission', secondary='app_roles_permissions')

    # allows direct read/write to the actual permission keys
    # e.g. instead of Role.permissions[0].permission_key (if element 0 exists)
    # we can access/modify the permissions directly like Role.permission_keys
    # which would return a (modifiable) list of all permission keys
    permission_keys = association_proxy('permissions', 'permission_key')
    permission_groups = association_proxy('permissions', 'permission_group')

    def to_response_dict(self) -> dict:
        return {
            "role_id": self.role_id,
            "role_name": self.role_name,
            "locked": self.locked,
            "permission_groups": [
                {
                    "permission_group_name": pg.permission_group_name,
                    "permissions": [p.to_response_dict() for p in self.permissions if p.permission_group.permission_group_name == pg.permission_group_name]
                }
                for pg in set(self.permission_groups)
            ]
        }
    
    @staticmethod
    def create_from_dict(obj: Any) -> Union['Role', APIError]:
        _role_name = parse_non_empty_str(obj.get("role_name"))
        if _role_name is None:
            return APIError(HTTPStatus.BAD_REQUEST, "missing or invalid role_name attribute")

        _permissions = parse_permission_ids(obj.get("permission_ids"))

        return Role(role_name=_role_name, permissions=_permissions)

    def update_from_dict(self, obj: Any) -> Union[None, APIError]:
        _role_name = parse_non_empty_str(obj.get("role_name"), self.role_name)
        if _role_name is None:
            return APIError(HTTPStatus.BAD_REQUEST, "missing or invalid role_name attribute")

        _permissions = parse_permission_ids(
            obj.get("permission_ids"), self.permissions)

        self.role_name = _role_name
        self.permissions = _permissions

        return


t_roles_permissions = Table(
    'app_roles_permissions', db.metadata,
    Column('role_id', ForeignKey('app_role.role_id',
           ondelete='CASCADE'), nullable=False),
    Column('permission_id', ForeignKey(
        'app_permission.permission_id', ondelete='CASCADE'), nullable=False)
)
