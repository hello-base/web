from django.core.urlresolvers import reverse_lazy
from django.views import generic

from .models import Shop


class GoodsBrowseView(generic.TemplateView):
    template_name = 'goods/good_browse.html'


class ShopListView(generic.ListView):
    model = Shop
    template_name = 'goods/shop_list.html'


class ShopDetailView(generic.DetailView):
    model = Shop
    template_name = 'goods/shop_detail.html'
