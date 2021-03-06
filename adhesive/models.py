# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.contrib.sessions.models import Session
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import validate_comma_separated_integer_list
from siteprofile.models import DorsaleBaseModel
from django.db import models
import logging
# logger = logging.getLogger(__name__)
from django.conf import settings
logger = logging.getLogger(settings.PROJECT_NAME)


@python_2_unicode_compatible
class Note(DorsaleBaseModel):
    """
    A generic model for adding simple, arbitrary notes to other models.
    """
    note = models.TextField(_('Note'))
    placement = models.CharField(
        verbose_name=_('Placement'),
        max_length=23,
        default='600,100,100,60',
        blank=True,
        help_text=_('x,y,width,height [px]'),
        validators=[validate_comma_separated_integer_list])

    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'))
    object_id = models.PositiveIntegerField(_('object id'))
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _('note')
        verbose_name_plural = _('notes')
        permissions = (
            ('view_note', _('Can view note')),
        )

    def __str__(self):
        return self.note

    def info_text(self):
        return render_to_string('adhesive/info.txt', {'note':self})


class NotesMixin(models.Model):
    notes = GenericRelation(Note)

    class Meta:
        abstract = True


class DorsaleAnnotatedBaseModel(NotesMixin, DorsaleBaseModel):
    class Meta:
        abstract = True


def delete_related_Notes(sender, **kwargs):
    """
    If an objects gets deleted, delete also all Notes on it
    """
    if 'django.contrib.sessions.models.Session' in str(sender):
        # most common source of warnings are deleted Sessions
        # but their type is ModelBase, even if their class is as above??
        return
    try:
        int(sender.pk)
    except TypeError as e:
        logger.warning(
            'fiee adhesive: %s: %s was deleted, but its PK is not an integer. Cannot look for and delete attached notes.', e, sender)
    else:
        sender_type = ContentType.objects.get_for_model(sender)
        Note.objects.filter(
            content_type__pk=sender_type.pk,
            object_id=int(sender.pk)).delete()

post_delete.connect(delete_related_Notes)
