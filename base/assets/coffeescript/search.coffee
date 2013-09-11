$(document).on 'focusin', '.js-search', ->
  new Results this
  return

class Results
  constructor: (field) ->
    @$field = $ field
    @$form = $ field.form
    @$field.on 'keydown.results', @onFieldKeyDown
    @$field.on 'input.results', @onFieldInput
    @$field.on 'focusout.results', @teardown
    @$form.on 'submit.results', @teardown

    @$template = $ '#js-search-results-template'
    @$results = $ '.js-search-results'

  teardown: =>
    @$field.off '.results'
    @$form.off '.results'
    @$results.removeClass 'active'

  onFieldKeyDown: (event) =>
    if event.hotkey is 'esc'
      @$results.removeClass 'active'

  onFieldInput: =>
    @$results.toggleClass 'active', @$field.val() isnt ""

    $.ajax
      url: "/search/autocomplete/"
      data:
        q: @$field.val()
      success: (data) =>
        template = Handlebars.templates["autocomplete"]
        @$results.html(template(data))

$(document).on 'click', '.result-item', ->
  $('.js-search').val("")
  return
