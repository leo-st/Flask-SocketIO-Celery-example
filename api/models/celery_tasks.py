from http import HTTPStatus
from typing import Any, Union
from datetime import datetime

from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime, text
from sqlalchemy.orm import relationship
from utils.api_error import APIError
from utils.input_parsers import (parse_bool, parse_email, parse_hash_pw,
                                 parse_int, parse_language,
                                 parse_non_empty_str)

from models import db

BaseModel: DefaultMeta = db.Model

CELERY_TASK_ID_SEQ = db.Sequence('celery_tasks_id_seq')  # define sequence explicitly

class CeleryTask(BaseModel):
    __tablename__ = 'celery_tasks'

    id = Column(Integer, CELERY_TASK_ID_SEQ, primary_key=True, server_default=CELERY_TASK_ID_SEQ.next_value())
    task_id = Column(String, nullable=False, unique=True)
    user_id = Column(Integer, nullable=False)
    creation_date = Column(DateTime, nullable=False)
    task_status = Column(String, nullable=False)
    last_modified = Column(DateTime, nullable=False)

    def to_response_dict(self) -> dict:
        return {
            'id': self.id,
            'task_id': self.task_id,
            'user_id': self.user_id,
            'creation_date': self.creation_date,
            'task_status': self.task_status,
            'last_modified': self.last_modified
        }

    @staticmethod
    def create_from_dict(obj: Any, reset_pw_required: bool = True) -> Union['CeleryTask', APIError]:
        _task_id = parse_non_empty_str(obj.get("task_id"))
        if _task_id is None:
            return APIError(HTTPStatus.BAD_REQUEST, "missing or invalid _task_id attribute")
        _user_id = parse_int(obj.get("user_id"))
        if _user_id is None:
            return APIError(HTTPStatus.BAD_REQUEST, "missing or invalid _user_id attribute")
        _task_status = parse_non_empty_str(obj.get("task_status"))
        if _task_status is None:
            return APIError(HTTPStatus.BAD_REQUEST, "missing or invalid _user_id attribute")
        _creation_date = datetime.now()
        _last_modified = datetime.now()
        
        return CeleryTask(task_id = _task_id, user_id = _user_id, creation_date = _creation_date, last_modified = _last_modified, task_status = _task_status)
    

    def update_from_dict(self, obj: Any) -> None:
        _id = parse_int(obj.get("id"), self.id)
        _task_id = parse_non_empty_str(obj.get("task_id"), self.task_id)
        _user_id = parse_int(obj.get("user_id"), self.user_id)
        _task_status = parse_non_empty_str(obj.get("task_status"), self.task_status)
        _last_modified = datetime.now()

        # if there is no change in task_status there is no need to update
        if(self.task_status == _task_status):
            return

        self.id = _id
        self.task_id = _task_id
        self.user_id = _user_id
        self.task_status = _task_status
        self.last_modified = _last_modified
        return