from django.conf.urls import url
from adhesive.models import Note
import adhesive.views as sv

urlpatterns = [
    url('^(?P<object_id>\w+)/json/$', sv.json_get_for_object, name='notes-get_for_object'),  # makes no sense without object type
    url('^(?P<id>\w+)/json/$', sv.json_get, name='notes-get'),
    url('^(?P<id>\w+)/json/save/$', sv.json_save, name='notes-save'),
    url('^(?P<id>\w+)/json/delete/$', sv.delete, name='notes-delete'),
]
