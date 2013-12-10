$ ->
  console.log 'wat'
  h = 108
  w = ($ '.js-correlations-header-graph').width()
  x = d3.scale.linear().range([0, w])
  y = d3.scale.linear().range([h, 0])

  line = d3.svg.line()
    .interpolate('basis')
    .x((d) -> x(d.index))
    .y((d) -> y(d.identifier))

  area = d3.svg.area()
    .interpolate('cardinal')
    .x((d) -> x(d.index))
    .y0(h)
    .y1((d) -> y(d.identifier))

  svg = d3.select('.js-correlations-header-graph').append('svg')
    .attr('id', 'svg-chart')
    .attr('viewbox', '0 0 960' + h)
    .attr('preserveAspectRatio', 'xMinYMid')
    .attr('width', w)
    .attr('height', h)

  d3.json ($ '.js-correlations-header-graph').attr('data-url'), (data) ->
    x.domain(d3.extent(data, (d) -> d.index))
    y.domain([0, d3.max(data, (d) -> d.identifier)])

    data.forEach (d) ->
      d.identifier = d.identifier;
      d.index = d.index;

    svg.append('path')
      .datum(data)
      .attr('class', 'area')
      .attr('d', area)

    svg.append('path')
      .datum(data)
      .attr('class', 'line')
      .attr('d', line)

aspect = ($ '.js-correlations-header-graph').width() / h
chart = ($ '#svg-chart')

($ window).on 'resize', ->
  targetWidth = ($ '.js-correlations-header-graph').width()
  chart.attr('width', targetWidth)
  chart.attr('height', targetWidth / aspect)
