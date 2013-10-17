# Toggle the administration system.
($ document).keypress (e) ->
  ($ '.administration').toggleClass 'visible' if (e.keyCode || e.which) == 96

# "Hero" image fade-in.
window.onload = ->
  ($ '.hero-image img').animate({opacity: 1}, 300)

# Search field highlighting.
($ document).ready ->
  ($ '#id_q').focus ->
    ($ this).closest('.searchbar').addClass 'focus'
  ($ '#id_q').blur ->
    ($ this).closest('.searchbar').removeClass 'focus'

# NProgress-related calls.
($ document).on 'page:fetch', ->
  NProgress.start()

($ document).on 'page:change', ->
  NProgress.done()

($ document).on 'page:restore', ->
  NProgress.remove()
