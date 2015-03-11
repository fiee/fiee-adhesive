# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes import generic
from dorsale.admin import DorsaleBaseAdmin
from models import Note


class NoteAdmin(DorsaleBaseAdmin):
    list_display = ('note', 'createdon')


class NoteInline(generic.GenericTabularInline):
    model = Note
    extra = 1


admin.site.register(Note, NoteAdmin)
