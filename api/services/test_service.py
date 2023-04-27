import time
import os
import io
import xlsxwriter
import base64

def  waiting_function():
    print('i entered here')
    start_time = time.time()
    time.sleep(20)
    return "The time required to extract information: " + str(time.time() - start_time) + " seconds"

def create_excel_export(arg1, task_id):
    print("----------------------TEST_SERVICE-------------")
    print(os.path.dirname(os.path.abspath(__file__)))
    time.sleep(2)
    output = io.BytesIO()

    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, 'Hello, world!')

    workbook.close()

    output.seek(0)

    base64EncodedStr = base64.b64encode(output.read()).decode()
    #print(f"THIS IS A PRINT MESSAGE ................{arg1}, {task_id}" )
    # new_dict = {}
    # new_dict['task_status'] = states.SUCCESS
    # update_celery_task_with_id(new_dict, task_id)
    from flask_socketio import SocketIO
    socketio = SocketIO(cors_allowed_origins='*', message_queue='redis://:super-secret@redis_cache:6381/0')
    #from sockets import socketio
    socketio.emit("privatemsg", {'username': 'leo', 'text': str(task_id)}, room=str(arg1))
    return base64EncodedStr