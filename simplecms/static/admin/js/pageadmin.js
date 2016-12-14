django.jQuery(function() {
  var $ = django.jQuery;

  if (window.parent.location !== window.location) {
    window.addEventListener('unload', window.parent.handlePageSubmit)
  }
});
