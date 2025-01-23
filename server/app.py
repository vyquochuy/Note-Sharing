import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from db import init_app

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # File SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Đảm bảo thư mục instance tồn tại
    os.makedirs(app.instance_path, exist_ok=True)

    # Khởi tạo module database
    init_app(app)

    # Kết nối SQLAlchemy
    db.init_app(app)

    # Tạo model cho bảng lưu dữ liệu
    class Task(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(80), nullable=False)
        description = db.Column(db.String(200), nullable=True)

    # Tạo database và bảng nếu chưa có
    with app.app_context():
        db.create_all()

    # Route để lấy tất cả công việc
    @app.route("/tasks", methods=["GET"])
    def get_tasks():
        tasks = Task.query.all()
        result = [{"id": task.id, "title": task.title, "description": task.description} for task in tasks]
        return jsonify(result)

    # Route để thêm công việc mới
    @app.route("/tasks", methods=["POST"])
    def add_task():
        data = request.json
        new_task = Task(title=data['title'], description=data.get('description', ''))
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"message": "Task created successfully!"}), 201

    # Route để xóa công việc
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

    return app


# Tạo instance Flask và cấu hình database
app = create_app()

# Khởi động server
if __name__ == "__main__":
    app.run(debug=True)
