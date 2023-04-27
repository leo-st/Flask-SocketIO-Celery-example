# Flask - SocketIO - Celery
This is an example of Flask application written with application factory pattern which uses Celery to do background tasks and notifies user in frontend when task is done through websockets using Flask-SocketIO .

### What is Flask ?
Flask is a popular web framework for Python used for building web applications. It is a lightweight and modular framework that provides a flexible way to build web applications quickly and easily.

### What is Celery and why we use it?
Celery is an asynchronous task queue/job queue library that is used to handle distributed tasks in Python applications. It is built on top of a message-broker system like RabbitMQ, Redis, or Apache Kafka, which acts as a mediator between the client and the workers.

In simple terms, Celery allows you to execute time-consuming tasks asynchronously in the background, freeing up your application to continue handling other requests while the task is being processed. This makes it useful for handling long-running or resource-intensive tasks, such as image or video processing, data analysis, sending emails or in our example case creating xlsx files.

### What is SocketIO and why we use it?
Flask-SocketIO is an extension for Flask that adds support for real-time bidirectional communication between the client and server using WebSockets.

WebSockets provide a persistent connection between the client and the server, enabling real-time communication between them. This is in contrast to traditional HTTP requests, which are stateless and require the client to initiate a new request for each interaction with the server.

### Project example
This is a Flask application which enables user to initiate long running task of creating excel file through HTTP request. Since we don't won't for user to wait till we get result we use Celery to initiate task in the background. Once the task is done we want to notify user about that. We want to avoid long pooling (continious http request from user "is the task done?") so we notify user with Web Socket message. We are using Flask-SocketIO library for this purpose. 
In this project we also introduce JWT library for authentication of the users.

### Why application factory design?
Since we want to use objects from Flask application (db from sqlaclhemy or something else) we need to create instance of flask application inside of celery application. If we don't do that then we couldn't "share" object between Flask and Celery application.

### How to run application?
For this project I prepared docker-compose file which will create 4 containers.
- Database - for managaing User auth and logging of celery tasks
- API - flask app
- Redis - nosql db which stores results and task information from celery and we use it as message channel for ws
- Celery worker - celery application

To run it execute:
```
docker-compose -f docker-compose.yml up --build -d
```

You can also stop API container and debug locally. Everything is setup in .vscode/launch.json to run it in VS Code.

### How to test this app?
You can run test.html which is small script to simulate websocket communication.
You can create 2 tabs for 2 different users.
In first form login with username:1  and in second username: 2. This will put each user 1(administrator@test.com) and  user 2 (username@test.com) in seperate rooms. Password in here is not important.
We do it in this way so that users don't get messages from another user.
![Alt text](./logging_in.png?raw=true "Initial screen")

There is a postman collection which you can import in POSTMAN.
First loging with user 1:
```
{
    "email": "administrator@test.com",
    "password": "password1"
}
```
Now initiate background task with ```/v1/create_excel_test``` endopint.
After the task is done in the background you can see only user 1 will get notification on web page.
![Alt text](./task_1.png?raw=true "Task 1")

If we now login with user 2 and initiate again task:
```
{
    "email": "username@test.com",
    "password": "password2"
}
```
You can see now that only user 2 recived message of completion.
![Alt text](./task_2.png?raw=true "Task 2")

