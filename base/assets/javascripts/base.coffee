($ document).ready ->
  ($ '#id_q').focus ->
    ($ this).closest('.header-search').addClass 'focus'
  ($ '#id_q').blur ->
    ($ this).closest('.header-search').removeClass 'focus'

($ document).on 'page:fetch', ->
  NProgress.start()

($ document).on 'page:change', ->
  NProgress.done()

($ document).on 'page:restore', ->
  NProgress.remove()
