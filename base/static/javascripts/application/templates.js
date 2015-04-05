(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['autocomplete'] = template({"1":function(depth0,helpers,partials,data) {
  var helper, functionType="function", escapeExpression=this.escapeExpression;
  return "\n    <a href=\""
    + escapeExpression(((helper = helpers.url || (depth0 && depth0.url)),(typeof helper === functionType ? helper.call(depth0, {"name":"url","hash":{},"data":data}) : helper)))
    + "\">\n        <li class=\"result result-item "
    + escapeExpression(((helper = helpers.model || (depth0 && depth0.model)),(typeof helper === functionType ? helper.call(depth0, {"name":"model","hash":{},"data":data}) : helper)))
    + "\">\n            <div class=\"item-object\">\n                <span class=\"item-romanized-name\">"
    + escapeExpression(((helper = helpers.romanized_name || (depth0 && depth0.romanized_name)),(typeof helper === functionType ? helper.call(depth0, {"name":"romanized_name","hash":{},"data":data}) : helper)))
    + "</span>\n                <span class=\"item-name\">"
    + escapeExpression(((helper = helpers.name || (depth0 && depth0.name)),(typeof helper === functionType ? helper.call(depth0, {"name":"name","hash":{},"data":data}) : helper)))
    + "</span>\n            </div>\n            <span class=\"item-type\">"
    + escapeExpression(((helper = helpers.model || (depth0 && depth0.model)),(typeof helper === functionType ? helper.call(depth0, {"name":"model","hash":{},"data":data}) : helper)))
    + "</span>\n        </li>\n    </a>\n";
},"3":function(depth0,helpers,partials,data) {
  var helper, functionType="function", escapeExpression=this.escapeExpression;
  return "\n    <a href=\"/search/?q="
    + escapeExpression(((helper = helpers.query || (depth0 && depth0.query)),(typeof helper === functionType ? helper.call(depth0, {"name":"query","hash":{},"data":data}) : helper)))
    + "\">\n        <li class=\"result result-query\">Search for other \"<strong>"
    + escapeExpression(((helper = helpers.query || (depth0 && depth0.query)),(typeof helper === functionType ? helper.call(depth0, {"name":"query","hash":{},"data":data}) : helper)))
    + "</strong>\" results &rarr;</li>\n    </a>\n";
},"compiler":[5,">= 2.0.0"],"main":function(depth0,helpers,partials,data) {
  var stack1, buffer = "<ul class=\"results\">\n";
  stack1 = helpers.each.call(depth0, (depth0 && depth0.results), {"name":"each","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.query), {"name":"if","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  return buffer + "\n</ul>\n";
},"useData":true});
})();