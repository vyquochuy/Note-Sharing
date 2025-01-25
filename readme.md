tạo môi trường ảo (virtual Environment)
Windows CMD:
```
python -m venv venv
```
Linux
```
python3 -m venv venv
```
kích hoạt môi trường ảo:
Windows CMD:
```
venv\Scripts\activate
```
Linux
```
.venv\bin\activate
```


2. Tải thư viện cần thiết:
```
pip install -r requirements.txt
```
Trong folder server:

1. cd vào folder server
2. initialize database:
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


Chạy main.py để chạy client.
