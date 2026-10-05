import os
from recruitment_intelligence_portal_ml.celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recruitment_intelligence_portal_ml.settings')
app = Celery('recruitment_intelligence_portal_ml')

# Reads every CELERY_* key from Django settings.py (namespace='CELERY' strips the prefix, so CELERY_BROKER_URL -> broker_url, etc.).
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discovers tasks.py inside every app listed in INSTALLED_APPS — this is why training/tasks.py needs no manual registration anywhere.
app.autodiscover_tasks()


# Simple connectivity check: run via `celery -A recruitment_intelligence_portal_ml call recruitment_intelligence_portal_ml.celery.debug_task`.
@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')