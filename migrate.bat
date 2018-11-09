#自动重建数据库
start cmd /k "activate django&&title wxmanage&&python manage.py makemigrations&&python manage.py migrate&&exit"
