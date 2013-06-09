from django.views.generic import ListView, DetailView, TemplateView

from .models import Shop


class GoodsBrowseView(TemplateView):
    template_name = 'goods/goods-browse.html'


class ShopListView(ListView):
    queryset = Shop.objects.all()
    template_name = 'goods/shop-list.html'


class ShopDetailView(DetailView):
    queryset = Shop.objects.all()
    template_name = 'goods/shop-detail.html'
