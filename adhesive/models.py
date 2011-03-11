#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from dorsale.models import DorsaleBaseModel
from django.db import models

class Note(DorsaleBaseModel):
    """
    A generic model for adding simple, arbitrary notes to other models.
    """
    note = models.TextField(_(u'Note'))
    placement = models.CommaSeparatedIntegerField(verbose_name=_(u'Placement'), max_length=23, default='600,100,100,60', blank=True, help_text=_(u'x,y,width,height [px]'))

    content_type = models.ForeignKey(ContentType, verbose_name=_(u'content type'))
    object_id = models.PositiveIntegerField(_(u'object id'))
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _('note')
        verbose_name_plural = _('notes')
        permissions = (
            ('view_note', _(u'Can view note')),
        )

    def __unicode__(self):
        return self.note
    
    def info_text(self):
        return render_to_string('adhesive/info.txt', {'note':self})


class DorsaleAnnotatedBaseModel(DorsaleBaseModel):
        
    notes = generic.GenericRelation(Note)
    
    class Meta:
        abstract = True

def delete_related_Notes(sender, **kwargs):
    """
    If an objects gets deleted, delete also all Notes on it
    """
    Note.objects.filter(content_object=sender).delete()

post_delete.connect(delete_related_Notes)
