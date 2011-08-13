#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from dorsale.models import DorsaleBaseModel
from django.db import models
import logging
#logger = logging.getLogger(__name__)
from django.conf import settings
logger = logging.getLogger(settings.PROJECT_NAME) 

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
    try:
        int(sender.pk)
    except TypeError, e:
        logger.warning(e) # exception would stop
        logger.warning(u'%s was deleted, but its PK is not an integer. Cannot look for and delete attached notes.' % sender)
    else:
        sender_type = ContentType.objects.get_for_model(sender)
        Note.objects.filter(content_type__pk=sender_type.pk, object_id=int(sender.pk)).delete()

post_delete.connect(delete_related_Notes)
