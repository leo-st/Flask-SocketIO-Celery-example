import os

current_path = os.getcwd()
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,os.path.join(parentdir, 'api'))

from flask import Flask
from datetime import datetime, timedelta, timezone
from flask_socketio import SocketIO, emit, join_room
from sockets import socketio

#from celery_worker import celery

def create_app(bool=True):
    app = Flask(__name__)    
    from utils.config import Config
    app.config.from_object(os.getenv("CONFIG_CLASS", Config))
    
    from models import db
    db.init_app(app)

    if(bool):
        socketio.init_app(app,cors_allowed_origins='*', message_queue=app.config['CELERY_BROKER_URL'] )
        @socketio.on('connect')
        def test_connect():
            socketio.emit('message', {'text': 'Connected to server successfully'})
            print("connected")

        @socketio.on('message')
        def handle_message(message): # Should it take an argument ?
            socketio.emit('message', {'text': 'this is response from server'})
            print("Message recieved" + message)


        @socketio.on('login')
        def on_join(data):
            username = data['username']
            channel = data['channel']
            join_room(channel)
            print("succesfull joined")
            #socketio.emit('message', {'text': 'Connected to room!'})

    with app.app_context():
        # creates tables
        from models.user import User
        from models.role import Role
        from models.permission_group import PermissionGroup
        from models.permission import Permission
        # Import blueprints
        from controllers.user_controller import user_controller
        from controllers.test_controller import test_controller

        # Register blueprints
        app.register_blueprint(user_controller)
        app.register_blueprint(test_controller)

        # Create database tables
        db.create_all()
    from flask_jwt_extended import JWTManager, set_access_cookies, create_access_token, get_jwt, get_jwt_identity
    jwt = JWTManager(app)
    @app.after_request
    def refresh_expiring_jwts(response):
        # make sure all return content-types are application/json
        response.headers['Content-Type'] = 'application/json'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the original response
            return response
    
    from flask_cors import CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])

    #celery.conf.update(app.config)
    app.config.update(
    CELERY_BROKER_URL='redis://:super-secret@redis_cache:6381/0',
    CELERY_RESULT_BACKEND='redis://:super-secret@redis_cache:6381/0'
    )

    
    return app

if __name__ == "__main__":
    application = create_app(True)
    socketio.run(application)