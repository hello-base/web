// Generated by CoffeeScript 1.8.0
(function() {
  var ready;

  ($(document)).keypress(function(e) {
    if ((e.keyCode || e.which) === 96) {
      return ($('.administration')).toggleClass('visible');
    }
  });

  window.onload = function() {
    return ($('.hero-image img')).animate({
      opacity: 1
    }, 300);
  };

  ($(document)).on('page:fetch', function() {
    return NProgress.start();
  });

  ($(document)).on('page:change', function() {
    return NProgress.done();
  });

  ($(document)).on('page:restore', function() {
    return NProgress.remove();
  });

  ready = function() {
    ($('#id_q')).focus(function() {
      return ($(this)).closest('.searchbar').addClass('focus');
    });
    ($('#id_q')).blur(function() {
      return ($(this)).closest('.searchbar').removeClass('focus');
    });
    return ($(document)).on('click', '.happening-toggle', function() {
      ($('.happening-decade-list')).toggleClass('visible');
      return ($('.happening-toggle .ss-icon:last-child')).toggleClass('ss-navigatedown ss-navigateup');
    });
  };

  ($(document)).ready(ready);

  ($(document)).on('page:load', ready);

}).call(this);