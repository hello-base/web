from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views import generic

from . import forms
from . import models


class GoodsBrowseView(generic.TemplateView):
    template_name = 'goods/goods-browse.html'

    def get_context_data(self, **kwargs):
        context = super(GoodsBrowseView, self).get_context_data(**kwargs)
        context['event_goods'] = models.Good.objects.filter(event__isnull=False)
        context['shop_goods'] = models.Good.objects.filter(shop__isnull=False)
        return context


class ShopListView(generic.ListView):
    model = models.Shop
    template_name = 'goods/shop-list.html'


class ShopDetailView(generic.DetailView):
    model = models.Shop
    template_name = 'goods/shop-detail.html'


class ShopCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = forms.ShopForm
    model = models.Shop
    success_url = reverse_lazy('shop-detail')


class ShopUpdateView(LoginRequiredMixin, generic.CreateView):
    form_class = forms.ShopForm
    model = models.Shop
    success_url = reverse_lazy('shop-detail')


class GoodCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = forms.GoodForm
    model = models.Good
    success_url = reverse_lazy('goods-browse')
    template_name = 'goods/goods-form.html'


class GoodUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.GoodForm
    model = models.Good
    success_url = reverse_lazy('goods-browse')


class SetCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = forms.SetForm
    model = models.Set
    success_url = reverse_lazy('goods-browse')


class SetUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.SetForm
    model = models.Set
    success_url = reverse_lazy('goods-browse')


class SuperSetCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = forms.SuperSetForm
    model = models.SuperSet
    success_url = reverse_lazy('goods-browse')


class SuperSetUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.SuperSetForm
    model = models.SuperSet
    success_url = reverse_lazy('goods-browse')

# See if we can change success_url from 'goods-browse' good permalink?
