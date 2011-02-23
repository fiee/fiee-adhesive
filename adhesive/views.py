#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from dorsale.forms import ModelFormFactory
from dorsale.json import JSONResponse
from models import Note

def check_request(request):
    data = {'info': '', 'error': None}
    if request.user.is_anonymous():
        data['error'] = 'not authorized'
        return JSONResponse(data, status=401)
    if request.method != 'POST':
        data['error'] = 'invalid request method'
        return JSONResponse(data, status=400)
    return data

def json_get_for_object(request, object_id):
    """
    AJAX query - not yet usable
    """
    data = {}
    try:
        pass
    except Exception, e:
        return JSONResponse(e, status=404)
    return JSONResponse(data)

def json_get(request, id):
    """
    AJAX query
    """
    data = {'info': ''}
    try:
        if request.user.has_perm('adhesive.view_note'):
            note = Note.objects.get(id=id)
            data['info'] = note.info_text()
            data['note'] = note.note
            data['placement'] = note.placement
    except Exception, e:
        return JSONResponse(e, status=404)
    return JSONResponse(data)

def json_save(request, id):
    """
    AJAX query
    """
    data = check_request(request)
    try:
        note = Note.objects.get(id=id)
        if not request.user.has_perm('adhesive.change_note'):
            return JSONResponse(data, status=401)
        form = ModelFormFactory(Note, request.POST, user=request.user, instance=note)
        data['is_new'] = False
    except (ValueError, ObjectDoesNotExist):
        if not request.user.has_perm('adhesive.add_note'):
            return JSONResponse(data, status=401)
        form = ModelFormFactory(Note, request.POST, user=request.user) 
        form.id = None
        data['is_new'] = True
    if form.is_valid():
        note = form.save()
        data['id'] = note.id
        data['placement'] = note.placement
        data['info'] = note.info_text()
    else:
        data['error'] = form.errors
        return JSONResponse(data, status=400)
    return JSONResponse(data)

def delete(request, id):
    """
    AJAX query
    """
    data = check_request(request)
    try:
        if request.user.has_perm('adhesive.delete_note'):
            Note.objects.get(id=id).delete()
        else:
            return JSONResponse(data, status=401)
    except Exception, e:
        return JSONResponse(e, status=404)
    return JSONResponse(data)
