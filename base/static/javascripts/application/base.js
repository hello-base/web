// Generated by CoffeeScript 1.6.3
(function() {
  $(document).on('page:fetch', function() {
    return NProgress.start();
  });

  $(document).on('page:change', function() {
    return NProgress.done();
  });

  $(document).on('page:restore', function() {
    return NProgress.remove();
  });

}).call(this);
