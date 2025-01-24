Trong folder server:
1. cd vào folder server
2.initialize database:
For Windows Command Prompt:
```
set FLASK_APP=app.py
flask init-db
```

For Windows PowerShell:
```
$env:FLASK_APP = "app.py"
flask init-db
```

For Unix-based systems (Linux, macOS):
```
export FLASK_APP=app.py
flask init-db
```
3.chạy app.py để chạy server
-----------------------------
Trong thư mục chứa dự án:
1. CD vào thư mục chứa dự án.
2. Tải thư viện cần thiết:
```
pip install -r requirements.txt
```

Chạy main.py để chạy client.
