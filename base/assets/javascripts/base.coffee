# "Hero" image fade-in.
($ document).ready ->
  ($ '.hero-image img').delay(1000).animate({opacity: 1}, 500)

# Search field highlighting.
($ document).ready ->
  ($ '#id_q').focus ->
    ($ this).closest('.header-search').addClass 'focus'
  ($ '#id_q').blur ->
    ($ this).closest('.header-search').removeClass 'focus'

# NProgress-related calls.
($ document).on 'page:fetch', ->
  NProgress.start()

($ document).on 'page:change', ->
  NProgress.done()

($ document).on 'page:restore', ->
  NProgress.remove()
