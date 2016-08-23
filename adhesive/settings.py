# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
This is just for 'django-admin makemessages -a'
"""
_ = lambda s: s

DEBUG = True
TEMPLATE_DEBUG = DEBUG

TIME_ZONE = 'Europe/Berlin'
LANGUAGE_CODE = 'de'
LANGUAGES = (('de', _('German')),
             ('en', _('English')),
             )

USE_I18N = True
USE_L10N = True
