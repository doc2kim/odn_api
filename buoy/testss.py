import os ,sys
import django
from django.conf import settings
sys.path.append("../")
sys.path.append("/var/app/current/buoy")
sys.path.append("/var/app/venv/staging-LQM1lest/lib/python3.8/site-packages")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
print(settings.DATABASES["default"]['ENGINE'])
settings.DATABASES["default"]['HOST'] = "11"
print(settings.DATABASES["default"]['HOST'])