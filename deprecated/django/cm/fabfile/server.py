import fabric

@task
def start():
    local("python manage.py runserver")
