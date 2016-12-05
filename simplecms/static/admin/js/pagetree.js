// jqtree needs jQuery in scope, we'll use the admin jQuery everywhere.
var $ = jQuery = django.jQuery;

$(function() {
  var $tree = $('#pagetree');
  var lastJqXHR = null;

  // TODO: write beforeunload handler to catch navigation away if lastJqHXR
  // isn't null

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
          // Lock the tree, display an error, reload the tree, unlock the tree
        } else {
          // Retry with exponential back-off if appropriate. Show an error
          // message if not retrying.
        }
      }
    });
  }

  function openEditModal(node, parentNode) {
    var $modal = $('#page-edit');
    $modal.data('node', node);
    $modal.data('parentNode', parentNode);
    $modal.find('input#slug').val(node ? node.name : '');
    $modal.modal();
    $modal.find('input#slug').focus();
  }

  function validateEditModal() {
    var slug = $('#page-edit input#slug').val();
    var errors = [];
    if (slug === '') {
      errors.push($('<li>Slug is required</li>'));
    }
    if (!/^[-a-z0-9_]*$/.test(slug)) {
      errors.push($(
        '<li>Invalid slug. Only numbers letters and "-" allowed.</li>'
      ));
    }
    if (errors.length > 0) {
      $('#page-edit .errorlist').html(errors);
      return null;
    }
    return {name: slug};
  }

  $('#page-edit form').submit(function(event) {
    event.preventDefault();
    var data = validateEditModal();
    if (data === null) {
      return;
    }

    $modal = $('#page-edit');
    var node = $modal.data('node');
    if (node === null) {
      // Find the parent node and add a new child.
      var parentNode = $modal.data('parentNode') || $tree.tree('getTree');
      $tree.tree('appendNode', {}, parentNode);
      $tree.tree('openNode', parentNode);
      node = parentNode.children[parentNode.children.length - 1];
    }
    $tree.tree('updateNode', node, data);
    $.modal.close();
    updateServer();
  });

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
    event.preventDefault();
    var $modal = $('#delete-confirm');
    var node = $tree.tree('getNodeByHtmlElement', event.currentTarget);
    $modal.data('node', node);
    $modal.modal();
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
