# Toggle the administration system.
($ document).keypress (e) ->
  ($ '.administration').toggleClass 'visible' if (e.keyCode || e.which) == 96


# "Hero" image fade-in.
window.onload = ->
  ($ '.hero-image img').animate({opacity: 1}, 300)


# NProgress-related calls.
($ document).on 'page:fetch', ->
  NProgress.start()

($ document).on 'page:change', ->
  NProgress.done()

($ document).on 'page:restore', ->
  NProgress.remove()


# A fake jQuery.ready() to handle the curveballs thrown by Turbolinks.
ready = ->
  # Search field highlighting.
  ($ '#id_q').focus ->
    ($ this).closest('.searchbar').addClass 'focus'
  ($ '#id_q').blur ->
    ($ this).closest('.searchbar').removeClass 'focus'

  # Happenings-related calls.
  ($ document).on 'click', '.happening-toggle', ->
    ($ '.happening-decade-list').toggleClass 'visible'
    ($ '.happening-toggle .ss-icon:last-child').toggleClass 'ss-navigatedown ss-navigateup'

($ document).ready ready
($ document).on 'page:load', ready
