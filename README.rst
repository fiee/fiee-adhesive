=============
fiëé adhésive
=============

Sticky notes for your Django_ models.

This pluggable Django application adds sticky notes to arbitrary models.

Its own Notes model is based on `fiëé dorsâle`_, but your models don’t need to use dorsale themselves.


Dependencies
------------

* Django_ 1.8+ with included contributions
* django-registration_ (or compatible)
* fiee-dorsale_ 0.1.0+
* jQuery_ 1.x
* js.cookie_ 2.1.0+ (included)


How to use
----------

* Add 'adhesive' to your ``INSTALLED_APPS``.
* You *can* use `adhesive.models.NotesMixin`_ to add a generic relation 'notes' to your models,
  it makes notes retrieval easier, but it’s not necessary.
* Use staticfiles_ to include adhésive’s media.
* Setup adhésive’s urls::

    url(r'^notes/', include('adhesive.urls')),

* Load jQuery_ in your template head.
* Include "adhesive/head.html" within your template head (loads CSS and JS from ``STATIC_URL/adhesive/css|js/``).
* Include "adhesive/notes.html" within your detail-view template, where you’d like the notes icons to appear (e.g in a sidebar).
* ``notes.html`` expects 'notes', 'item' and 'item_type' in the context::

    {
      item: your_object,
      notes: item.notes.all(), # with 'NotesMixin'
      item_type: ContentType.objects.get_for_model(item),
    }

Now, if you open a detail view on one of your models, you should see a “new note” icon.
Click on it to create a note. Type some text in it. Move it around.

As soon as you created a note, there’s another icon to hide/show all notes.

Text and position of the note get saved silently as soon as it loses focus, at least if you click anywhere else or press “tab”.
Mouse over the tiny note icon in the note’s title bar and you see some management data like change date (or a "not yet saved" message).

You can change the note’s size at the lower right corner. You can delete the note by clicking on the cross icon in its titlebar.

Go to another view, come back, and your note(s) should appear again.

If you delete an item, its attached notes get automatically deleted, too.
I.e. they get marked as deleted and won’t show up again, since `fiëé dorsâle`_ models aren’t really deletable.


Hints
-----

* Don’t use class ``adhesive`` in your templates.
* Don’t use a ``notes`` field in a model that you want to use with adhésive.
* Don’t use ``notes``, ``item``, ``item_type`` in a notes-enabled template 
  for anything else than adhésive notes, the currently displayed object 
  and its ContentType.

* You can override ``adhesive/info.txt`` template for different management info 
  in mouseover.


Known Issues
------------

* path ‘/notes/’ is hardcoded in JS
* names of context variables ``item``, ``item_type`` and ``notes`` 
  are hardcoded in template
* notes not always saved on lost focus (add some indicator?)
* incomplete permission checks
* probably more dependencies
* no tests, no demo


License
-------

BSD, see LICENSE_

famfamfam_ icons appear under Creative Commons Attribution license (CC BY 3.0)

js.cookie_ is MIT licensed.


Author(s)
---------

* fiëé visuëlle, Henning Hraban Ramm, <hraban@fiee.net>, http://www.fiee.net
* contains code from the Django_ project and other sources (as indicated in the code)
* contains famfamfam_ silk icons by Mark James
* contains js.cookie_ by Klaus Hartl et.al.

.. _LICENSE: ./fiee-adhesive/raw/master/LICENSE
.. _fiee-dorsale: https://github.com/fiee/fiee-dorsale
.. _`fiëé dorsâle`: https://github.com/fiee/fiee-dorsale
.. _Django: http://www.djangoproject.com
.. _staticfiles: https://docs.djangoproject.com/en/1.6/ref/contrib/staticfiles/
.. _django-registration: https://bitbucket.org/ubernostrum/django-registration/
.. _jQuery: http://docs.jquery.com/
.. _js.cookie: https://github.com/js-cookie/js-cookie/tree/v2.1.0
.. _famfamfam: http://www.famfamfam.com/lab/icons/silk/
