function init_adhesive(obj) {
  /* Initialize one sticky note */
  var placement = $(obj).find('input[name|=placement]').val().split(',');
  var id = $(obj).attr('id').replace('adhesive_', '');
  
  $(obj).show()
  /* make Stickies movable */
  .draggable({
    handle: '.adhesive_head',
    stop: function(event, ui){ /* set values of hidden fields */
      var placement = $(obj).find('input[name|=placement]').val().split(',');
      $(this).find('input[name|=placement]').val(ui.position.left+','+ui.position.top+','+placement[2]+','+placement[3]);
      $(this).find('input[name|=is_changed]').val(1);
      save_adhesive(id);
    }
  })
  /* make Stickies resizable */
  .resizable({
    autoHide: true,
    minHeight: 60,
    minWidth: 100,
    resize: function(event, ui){ /* resize also contained textarea */
      $(this).find('textarea').height(ui.size.height - 20);
    },
    stop: function(event, ui){ /* set values of hidden fields */
      var placement = $(obj).find('input[name|=placement]').val().split(',');
      $(this).find('input[name|=placement]').val(placement[0]+','+placement[1]+','+ui.size.width+','+ui.size.height);
      $(this).find('input[name|=is_changed]').val(1);
      save_adhesive(id);
    },
  })
  /* Placement and size at startup */
  .css('left', placement[0]+'px')
  .css('top', placement[1]+'px')
  .width(placement[2]+'px')
  .height(placement[3]+'px')
  /* Handle events in notes */
  .find('textarea')
  .attr('readonly', false)
  .height($(obj).height() - 20)
  .keyup(function(){
    $(this).siblings('input[name|=is_changed]').val(1);
  })
  .focusout(function(){ /* save */
    save_adhesive(id);
  });
  $(obj).find('input').attr('readonly', false);
  
  /* Delete note on close */
  $(obj).find('.adhesive_close').click(function(){
    delete_adhesive(id);
  });
  
  /* Management info dialog */
  $(obj).find('.adhesive_info').click(function(){
    $('#adhesive_info_dialog')
    .html('<p>'+$(this)[0].title.replace(/\n/g, '<br />')+'</p>')
    .dialog()
    .removeClass('hidden');
  });
}

function new_adhesive() {
  var adhesive = $('div.adhesive_template').clone();
  adhesive.attr('id', 'adhesive_new');
  adhesive.find('textarea').attr('id', 'id_adhesive_new_note');
  adhesive.removeClass('adhesive_template hidden').appendTo('#adhesive_start');
  init_adhesive(adhesive);
  $('#adhesive_toggle').removeClass('hidden');
  return adhesive;
}

function save_adhesive(id) {
  /* id = pure numerical id */
  var adhesive = $('#adhesive_'+id);
  var ta = adhesive.find('textarea');
  if (ta.val() && (ta.siblings('input[name|=is_changed]').val()=="1")) {
    ta.siblings('input[name|=is_changed]').val(0); /* otherwise we get double saves */

    $.post('/notes/'+id+'/json/save/', 
    {
      'note': ta.val(),
      'placement': ta.siblings('input[name|=placement]').val(),
      'id': ta.siblings('input[name|=id]').val(),
      'object_id': ta.siblings('input[name|=object_id]').val(),
      'content_type': ta.siblings('input[name|=content_type]').val(),
    }, 
    function(data){
      /* update management info */
      if (data['is_new']) { 
        var adhesive = $('#adhesive_new');
        adhesive.attr('id', 'adhesive_'+data['id'])
        .find('input[name|=id]').val(data['id'])
        .siblings('textarea').attr('id', 'id_adhesive_'+data['id']+'_note');
      }
      $('#adhesive_'+data['id']+' .adhesive_head .adhesive_info').attr('title', data['info']);
    }, 'json');

  }
}

function delete_adhesive(id) {
  /* id = pure numerical id */
  var adhesive = $('#adhesive_'+id);
  if ((adhesive.find('textarea').val()=='')||(id=='new')) {
    adhesive.remove();
  } else {
    $('#adhesive_delete_dialog')
    .dialog(
    {
      modal: true,
      buttons: {
        "Ok": function() {
          $(this).dialog("close");
          $.post('/notes/'+id+'/json/delete/', {
            'id': adhesive.find('input[name|=id]').val(),
            'object_id': adhesive.find('input[name|=object_id]').val(),
            'content_type': adhesive.find('input[name|=content_type]').val(),
          });
          adhesive.remove();
        }, 
        "Cancel": function() { 
          $(this).dialog("close"); 
        } 
      }
    });
  }
}

$(function(){
  $.ajaxSetup({ cache: false });
  /* use Django's CSRF tokens in AJAX queries
   * requires jquery.cookie
   */ 
  $('html').ajaxSend(function(event, xhr, settings) {
      function getCookie(name) {
          var cookieValue = null;
          if (document.cookie && document.cookie != '') {
              var cookies = document.cookie.split(';');
              for (var i = 0; i < cookies.length; i++) {
                  var cookie = jQuery.trim(cookies[i]);
                  // Does this cookie string begin with the name we want?
                  if (cookie.substring(0, name.length + 1) == (name + '=')) {
                      cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                      break;
                  }
              }
          }
          return cookieValue;
      }
      if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
          // Only send the token to relative URLs i.e. locally.
          xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      }
  });

  /* Initialize all notes */
  $('div.adhesive:not(.adhesive_template)').each(function(index){ init_adhesive(this); });
  
  /* Show/hide notes */
  $('#adhesive_toggle').click(function(){
    $('div.adhesive').toggle();
  });
  
  /* New note */
  $('#adhesive_add').click(function(){
    new_adhesive(); 
  });
});
