from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column, Integer, Text, text
from sqlalchemy.orm import relationship

from models import db


BaseModel: DefaultMeta = db.Model


PERMISSION_GROUP_ID_SEQ = db.Sequence('app_permission_group_id_seq')  # define sequence explicitly


class PermissionGroup(BaseModel):
    __tablename__ = 'app_permission_group'

    permission_group_id = Column(Integer, PERMISSION_GROUP_ID_SEQ, primary_key=True, server_default=PERMISSION_GROUP_ID_SEQ.next_value())
    permission_group_name = Column(Text, nullable=False, unique=True, server_default=text("'permission_group_x'::text"))

    permissions = relationship('Permission', back_populates='permission_group', lazy='select')

    def to_response_dict(self):
        return {
            "permission_group_name": self.permission_group_name,
            "permissions": [per.to_response_dict() for per in self.permissions]
        }
    