# 项目/settings和wsgi.py的同目录下创建asgi.py
"""
ASGI入口点，运行Django，然后运行在settings.py ASGI_APPLICATION 中定义的应用程序
安装：pip install daphne
运行：daphne -p 8001 BMS.asgi:application
"""

import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BMS.settings")
django.setup()
application = get_default_application()