#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is just for 'manage.py makemessages -a'
"""
_ = lambda s: s

DEBUG = True
TEMPLATE_DEBUG = DEBUG

TIME_ZONE = 'Europe/Berlin'
LANGUAGE_CODE = 'de'
LANGUAGES = (('de', _(u'German')),
             ('en', _(u'English')),
             )

USE_I18N = True
USE_L10N = True
