"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_wsgi_application()

# class Config:
#     username = None
#     admin = None
#     survey = None
#     question = None
#
#     # def __init__(self):
#     #     self.username = None
#     #     self.admin = None
#     #     self.survey = None
#     #     self.question = None
#
# configs = Config()
