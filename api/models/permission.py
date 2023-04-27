from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column, ForeignKey, Integer, Text, text
from sqlalchemy.orm import relationship

from models import db


BaseModel: DefaultMeta = db.Model


PERMISSION_ID_SEQ = db.Sequence('app_permission_id_seq')  # define sequence explicitly


class Permission(BaseModel):
    __tablename__ = 'app_permission'

    permission_id = Column(Integer, PERMISSION_ID_SEQ, primary_key=True, server_default=PERMISSION_ID_SEQ.next_value())
    permission_key = Column(Text, nullable=False, unique=True, server_default=text("'can_do_x'::text"))

    permission_group_id = Column(Integer, ForeignKey("app_permission_group.permission_group_id"))

    permission_group = relationship('PermissionGroup', back_populates='permissions', lazy='select')

    def to_response_dict(self):
        return {
            "permission_id": self.permission_id,
            "permission_key": self.permission_key,
            "permission_group_name": self.permission_group.permission_group_name
        }
