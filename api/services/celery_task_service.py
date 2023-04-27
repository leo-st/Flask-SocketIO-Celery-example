from http import HTTPStatus

from utils.api_error import APIError
from models.celery_tasks import CeleryTask
from models import db
import redis
import os

def create_celery_task(request_dict) -> CeleryTask:
    new_celery_task: CeleryTask = CeleryTask.create_from_dict(request_dict)
    if isinstance(new_celery_task, APIError):
        return new_celery_task

    db.session.add(new_celery_task)
    db.session.commit()

    return new_celery_task

def update_celery_task_with_id(request_json, task_id: int) -> CeleryTask | APIError:
    celery_task_with_id: CeleryTask = CeleryTask.query.filter_by(task_id=task_id).first()
    if celery_task_with_id is None:
        return APIError(HTTPStatus.NOT_FOUND, "celery task does not exist")
    
    celery_task_with_id.update_from_dict(request_json)
    db.session.commit()

    return celery_task_with_id

def get_list_of_celery_tasks():
    REDIS_URL = os.environ.get('CELERY_RESULT_BACKEND', 'redis://:super-secret@localhost:6381/0')
    redis_client = redis.from_url(REDIS_URL)

    keys = redis_client.keys('*celery-task-meta-*')
    new_string_list = []
    for k in keys:
        string_key = str(k)
        new_string = string_key.replace('celery-task-meta-', '')
        new_string = new_string[2:-1]
        new_string_list.append(new_string)
        
    return new_string_list

def query_only_for_user(user_id, celery_tasks):
    return CeleryTask.query.filter_by(user_id=user_id).filter(CeleryTask.task_id.in_(celery_tasks)).all()
    