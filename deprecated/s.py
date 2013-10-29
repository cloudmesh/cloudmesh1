# celery worker --app=simple -l info

from simple.tasks import add
from simple.celery import celery
print add(2, 2)

r = add.delay(4, 4)

print r.get()
