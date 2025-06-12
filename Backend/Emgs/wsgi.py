

import os

from django.core.wsgi import get_wsgi_application
settins_module='Emgs.Deployement' if 'WEPSITE_HOSTNAME'in os.environ else'Emgs.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settins_module)

application = get_wsgi_application()
