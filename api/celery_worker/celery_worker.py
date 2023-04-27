from celery import Celery
from app import create_app
import celery.states as states

application = create_app(False)

celery = Celery('tasks', broker=application.config['CELERY_BROKER_URL'], backend=application.config['CELERY_RESULT_BACKEND'])
celery.conf.update(application.config)

from services.test_service import waiting_function, create_excel_export
from services.celery_task_service import update_celery_task_with_id

@celery.task(name='app.tasks.extraction')
def extraction():
    return waiting_function()

@celery.task(name='app.tasks.create_excel')
def create_excel(arg1):
    import os
    current_path = os.getcwd()
    print("Current path:", current_path)
    contents = os.listdir(current_path)
    print("Directory contents:", contents)
    task_id = create_excel.request.id
    result = create_excel_export(arg1, task_id)
    # from app import create_app
    # application = create_app()
    with application.app_context():
        new_dict = {}
        new_dict['task_status'] = states.SUCCESS
        update_celery_task_with_id(new_dict, task_id)
    #update_celery_task_hc(arg1, task_id)
    return result