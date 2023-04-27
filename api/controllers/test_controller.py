from http import HTTPStatus
from flask import Blueprint, request, make_response, Response, jsonify
import celery.states as states

from flask_jwt_extended import jwt_required
from datetime import datetime 
import mimetypes
from werkzeug.datastructures import Headers
from flask_socketio import emit, join_room, leave_room
from flask import session
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, set_access_cookies, unset_jwt_cookies
from services.user_service import user_login_test, get_user_by
import os
from services.celery_task_service import create_celery_task, update_celery_task_with_id
test_controller = Blueprint('test_controller', __name__)


@test_controller.route('/v1/initiate_extraction', methods=["POST"])
@jwt_required()
def initiate_extraction() -> str:
    from celery_worker.celery_worker import celery
    task = celery.send_task('app.tasks.extraction')
    response = f"task_id : {task.id}"
    return response

@test_controller.route('/v1/get_extraction_result', methods=["GET"])
@jwt_required()
def get_extraction_result() -> str:
    req = request.json
    task_id = req.get('task_id')
    from celery_worker.celery_worker import celery
    res = celery.AsyncResult(task_id)
    if(res.state==states.SUCCESS):
        return str(res.result)
    else:
        return make_response("task not finished or not even started", 404)
    
@test_controller.route('/v1/check_task', methods=["POST"])
@jwt_required()
def check_task() -> str:
    req = request.json
    task_id = req.get('task_id')
    from celery_worker.celery_worker import celery
    res = celery.AsyncResult(task_id)
    if res.state == states.STARTED or res.state==states.SUCCESS:
        return res.state
    if res.state == states.PENDING:
        return make_response('this should not happen: PENDING - only if you ask for un existing process', 404)
    else:
        return make_response(f"unexpected state: {res.state}", 404)
    
@test_controller.route('/v1/create_excel_test', methods=["GET"])
@jwt_required()
def create_excel():
    print("----------------------TEST_CONTROLLER-------------")
    print(os.path.dirname(os.path.abspath(__file__)))
    request_user = get_user_by(get_jwt_identity())
    arg1 = request_user.user_id
    from celery_worker.celery_worker import celery
    task = celery.send_task('app.tasks.create_excel',args=[arg1])
    
    response = f"task_id : {task.id}"
    new_dict = {}
    
    new_dict['user_id'] = arg1
    new_dict['task_id'] = task.id
    new_dict['task_status'] = task.status
    print(new_dict)
    res = create_celery_task(new_dict)
    return response

@test_controller.route('/v1/get_excel_export', methods=["GET"])
@jwt_required()
def get_excel_export():
    req = request.json
    task_id = req.get('task_id')
    from celery_worker.celery_worker import celery
    res = celery.AsyncResult(task_id)
    if(res.state==states.SUCCESS):
        #first update table celery_tasks
        new_dict = {}
        new_dict['task_status'] = res.state
        update_celery_task_with_id(new_dict, task_id)

        response = Response()
        import base64 
        base64_message  = res.result
        response.data = base64.b64decode(base64_message)

        # Set filname and mimetype
        file_name = f'export_monthly_{datetime.now()}.xlsx'
        mimetype_tuple = mimetypes.guess_type(file_name)

        # HTTP headers for forcing file download
        response_headers = Headers({
                'Pragma': "public",  # required,
                'Expires': '0',
                'Cache-Control': 'must-revalidate, post-check=0, pre-check=0',
                'Cache-Control': 'private',  # required for certain browsers,
                'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'Content-Disposition': 'attachment; filename=\"%s\";' % file_name,
                'Content-Transfer-Encoding': 'binary',
                'Content-Length': len(response.data)
            })

        if not mimetype_tuple[1] is None:
            response.update({
                    'Content-Encoding': mimetype_tuple[1]
                })

        # Add headers
        response.headers = response_headers

        #jquery.fileDownload.js requirements
        response.set_cookie('fileDownload', 'true', path='/')

        # Return the response
        return response
    else:
        return make_response("task not finished or not even started", 404)