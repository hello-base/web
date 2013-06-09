from django.views.generic import ListView, DetailView, TemplateView
from django.core.urlresolvers import reverse_lazy

from .models import Shop, Good, Set, SuperSet


class GoodsBrowseView(TemplateView):
    template_name = 'goods/goods-browse.html'


class ShopListView(ListView):
    queryset = Shop.objects.all()
    template_name = 'goods/shop-list.html'


class ShopDetailView(DetailView):
    queryset = Shop.objects.all()
    template_name = 'goods/shop-detail.html'


class ShopCreateForm(CreateForm):
    model = Shop
    success_url = reverse_lazy('shop-detail')
    form_class = ShopForm


class ShopUpdateForm(CreateForm):
    model = Shop
    success_url = reverse_lazy('shop-detail')
    form_class = ShopForm


class GoodCreateForm(CreateForm):
    model = Good
    success_url = reverse_lazy('goods-browse')
    form_class = GoodForm


class GoodUpdateForm(UpdateForm):
    model = Good
    success_url = reverse_lazy('goods-browse')
    form_class = GoodForm


class SetCreateForm(CreateForm):
    model = Set
    success_url = reverse_lazy('goods-browse')
    form_class = SetForm


class SetUpdateForm(UpdateForm):
    model = Set
    success_url = reverse_lazy('goods-browse')
    form_class = SetForm


class SuperSetCreateForm(CreateForm):
    model = SuperSet
    success_url = reverse_lazy('goods-browse')
    form_class = SuperSetForm


class SuperSetUpdateForm(UpdateForm):
    model = SuperSet
    success_url = reverse_lazy('goods-browse')
    form_class = SuperSetForm

# See if we can change success_url from 'goods-browse' good permalink?