// jqtree needs jQuery in scope, we'll use the admin jQuery everywhere.
var $ = jQuery = django.jQuery;

$(function() {
  var $tree = $('#pagetree');
  var lastJqXHR = null;

  window.onbeforeunload = function(e)
  {
    if (lastJqXHR !== null) {
      return true;
    }
  };

  function lockAndReload() {
    // TODO: Lock the tree before reloading, unlock on the callback
    $tree.tree('reload', function() {
      console.log('Data reloaded');
    });
  }

  function handlePageSubmit() {
    $.modal.close();
    $('#pageAdmin').removeAttr('src');
    lockAndReload();
  }
  window.handlePageSubmit = handlePageSubmit;

  function updateServer() {
    lastJqXHR = $.post(
      $tree.data('url'),
      {tree: $tree.tree('toJson')}
    ).done(function(data, textStatus, jqXHR) {
      if (jqXHR === lastJqXHR) {
        // Update the tree with data from the server. This shouldn't change the
        // visible tree structure if nothing went wrong.
        $tree.tree('loadData', data);
        lastJqXHR = null;
      }
    }).fail(function(jqXHR, textStatus, errorThrown) {
      console.log('Request failed: ' + textStatus);
      if (jqXHR === lastJqXHR) {
        // if there's a newer pending request, lets wait and see.
        // TODO: Handle error cases.
        if (jqXHR.status == 401) {
          // Redirect to login
        } else if (jqXHR.status == 409) {
          lockAndReload();
        } else {
          // Retry with exponential back-off if appropriate. Show an error
          // message if not retrying, and clear the jqXHR.
        }
      }
    });
  }

  function openEditModal(node, parentNode) {
    function doit() {
      var $modal = $('#pageAdmin');
      if (node === null) {
        var url = $modal.data('add-url') + '?_popup=1';
        if (parentNode !== null) {
          url += '&parent=' + parentNode.id;
        }
      }
      else {
        var url = $modal.data('change-url').replace('0', node.id) + '?_popup=1';
      }
      url += '&cmssite=1';
      $modal.attr('src', url);
      $modal.modal();
      $modal.focus();
    }

    if (lastJqXHR !== null) {
      lastJqXHR.done(
        doit
      ).fail(function(jqXHR, textStatus, errorThrown) {
        // TODO: Do something smarter here.
        console.log("Pending request failed");
      });
    } else {
      doit();
    }
  }

  $('#delete-confirm form').submit(function(event) {
    event.preventDefault();
    var $modal = $('#delete-confirm');
    $tree.tree('removeNode', $modal.data('node'));
    $.modal.close();
    updateServer();
  });

  $tree.bind('tree.move', function(event) {
    event.preventDefault();
    event.move_info.do_move();
    updateServer();
  });

  $tree.add('#root-node-add').on('click', '.node-add', function(event) {
    event.preventDefault();
    var parentNode = $tree.tree('getNodeByHtmlElement', event.currentTarget);
    openEditModal(null, parentNode);
  });

  $tree.on('click', '.node-edit', function(event) {
    event.preventDefault();
    openEditModal(
      $tree.tree('getNodeByHtmlElement', event.currentTarget)
    );
  });

  $tree.on('click', '.node-delete', function(event) {
    console.log('Foo');
    event.preventDefault();
    var $modal = $('#delete-confirm');
    var node = $tree.tree('getNodeByHtmlElement', event.currentTarget);
    $modal.data('node', node);
    $modal.modal();
  });

  $('#pageAdmin').on('load', function(event) {
    this.style.height = this.contentWindow.document.body.scrollHeight + 'px';
  });

  $tree.tree({
    autoOpen: true,
    dragAndDrop: true,
    onCreateLi: function(node, $li) {
      $links = [
        $('#node-edit-template').clone(),
        $('#node-add-template').clone(),
        $('#node-delete-template').clone(),
      ].reduce($.merge);
      $links.removeAttr('id');
      $links.show();
      $li.find('.jqtree-title').after($links);
    },
  });
});
