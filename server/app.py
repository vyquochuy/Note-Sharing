import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from db import init_app, close_db  # Import init_app and close_db from db.py

# Modules
from modules.PingPong import PingPong
from modules.Register import Register
from modules.Login import Login
from modules.Logout import Logout
from modules.Uploadfiles import UploadFiles
from modules.Downloadfiles import DownloadFiles
from modules.Sharing import Sharing

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # File SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DATABASE'] = 'data.db'  # Set the DATABASE configuration key

    # Ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize the database module
    init_app(app)  # Call init_app to register the init-db command

    # Connect SQLAlchemy
    db.init_app(app)

    # Define the model for the table
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(80), nullable=False)
        public_key = db.Column(db.String(200), nullable=False)
        key_length = db.Column(db.String(200), nullable=False)
        api_token = db.Column(db.String(200), nullable=True)
        verify_token = db.Column(db.String(200), nullable=True)

    # Create the database and tables if they don't exist
    with app.app_context():
        db.create_all()

    # Route to get all tasks
    @app.route("/tasks", methods=["GET"])
    def get_tasks():
        tasks = Task.query.all()
        result = [{"id": task.id, "title": task.title, "description": task.description} for task in tasks]
        return jsonify(result)

    # Route to add a new task
    @app.route("/tasks", methods=["POST"])
    def add_task():
        data = request.json
        new_task = Task(title=data['title'], description=data.get('description', ''))
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"message": "Task created successfully!"}), 201

    # Route to delete a task
    @app.route("/tasks/<int:id>", methods=["DELETE"])
    def delete_task(id):
        task = Task.query.get(id)
        if not task:
            return jsonify({"error": "Task not found"}), 404
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully!"})

    @app.route("/", methods=["GET"])
    def home():
        return jsonify({"message": "Welcome to the Task API!"})

    # API initializing
    api = Api(app)
    api.add_resource(PingPong, '/ping')
    api.add_resource(Register, '/register')
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/logout')
    api.add_resource(UploadFiles, '/upload')
    api.add_resource(
        DownloadFiles,
        '/viewall',
        endpoint='viewall',
        methods=['POST']
    )
    api.add_resource(
        DownloadFiles,
        '/passphrase',
        endpoint='passphrase',
        methods=['POST']
    )
    api.add_resource(
        DownloadFiles,
        '/download',
        endpoint='download',
        methods=['POST']
    )
    api.add_resource(
        DownloadFiles,
        '/checksum',
        endpoint='checksum',
        methods=['POST']
    )
    api.add_resource(
        Sharing,
        '/publickey',
        endpoint='publickey',
        methods=['POST']
    )
    api.add_resource(
        Sharing,
        '/share',
        endpoint='share',
        methods=['POST']
    )
    return app

# Create Flask instance and configure database
app = create_app()

@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)

# Start the server
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)