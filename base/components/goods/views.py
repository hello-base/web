from django.views.generic import (ListView, DetailView, TemplateView, 
   CreateView, UpdateView)
from django.core.urlresolvers import reverse_lazy

from .forms import ShopForm, GoodForm, SetForm, SuperSetForm
from .models import Shop, Good, Set, SuperSet


class GoodsBrowseView(TemplateView):
    template_name = 'goods/goods-browse.html'


class ShopListView(ListView):
    queryset = Shop.objects.all()
    template_name = 'goods/shop-list.html'


class ShopDetailView(DetailView):
    queryset = Shop.objects.all()
    template_name = 'goods/shop-detail.html'


class ShopCreateView(CreateView):
    model = Shop
    success_url = reverse_lazy('shop-detail')
    form_class = ShopForm


class ShopUpdateView(CreateView):
    model = Shop
    success_url = reverse_lazy('shop-detail')
    form_class = ShopForm


class GoodCreateView(CreateView):
    model = Good
    success_url = reverse_lazy('goods-browse')
    form_class = GoodForm


class GoodUpdateView(UpdateView):
    model = Good
    success_url = reverse_lazy('goods-browse')
    form_class = GoodForm


class SetCreateView(CreateView):
    model = Set
    success_url = reverse_lazy('goods-browse')
    form_class = SetForm


class SetUpdateView(UpdateView):
    model = Set
    success_url = reverse_lazy('goods-browse')
    form_class = SetForm


class SuperSetCreateView(CreateView):
    model = SuperSet
    success_url = reverse_lazy('goods-browse')
    form_class = SuperSetForm


class SuperSetUpdateView(UpdateView):
    model = SuperSet
    success_url = reverse_lazy('goods-browse')
    form_class = SuperSetForm

# See if we can change success_url from 'goods-browse' good permalink?