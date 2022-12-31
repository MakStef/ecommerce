from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.views.generic import (
    View,
    TemplateView,
    ListView,
    DetailView,
)
from django.views.generic.base import (
    ContextMixin,
)

from store.utils import newsletter
from store.utils.utils import (
    get_random_categories,
    get_last_products,
    products_to_values_list,
)
from store.models import (
    Product,
    Subcategory,
    Category,
    Supercategory,
)

import json

# Mixins


# Class Based Views
class HomepageView(TemplateView, ContextMixin):
    template_name = "store/homepage.html"
    extra_context = {
        'bestsellers': json.dumps(products_to_values_list(Product.objects.all().order_by('sold')[:16])),
        'brandnews_1': json.dumps(products_to_values_list(Product.objects.all().order_by('created_at')[:9])),
        'brandnews_2': json.dumps(products_to_values_list(Product.objects.all().order_by('created_at')[9:18])),
        'discounted_1': json.dumps(products_to_values_list(Product.objects.all().order_by('discount')[:16])),
        'discounted_2': json.dumps(products_to_values_list(Product.objects.all().order_by('discount')[16:32])),
        'discounted_3': json.dumps(products_to_values_list(Product.objects.all().order_by('discount')[32:48])),
        'discounted_4': json.dumps(products_to_values_list(Product.objects.all().order_by('discount')[48:64])),
    }


class NewslettersView(View):
    def get(self, request, *args, **kwargs):
        if request.GET.get('action') and request.GET.get('email'):
            if request.GET.get('action') == 'sign':
                newsletter.sign(request.GET.get('email'))
            elif request.GET.get('action') == 'unsign':
                newsletter.unsign(request.GET.get('email'))
        return redirect('store:homepage')


class ProductActionView(View):
    def get(self, request, *args, **kwargs):
        if request.GET.get('action') and (request.GET.get('value') or request.GET.get('product_id')):
            action = request.GET.get('action')
        if action == 'toggle_fav':
            fav.toggle(
                fav=request.user.favourite,
                product=get_object_or_404(
                    Product, pk=request.GET.get('product_id'))
            )
        elif action == 'toggle_cart':
            cart.toggle(
                fav=request.user.favourite,
                product=get_object_or_404(
                    Product, pk=request.GET.get('product_id'))
            )
        elif action == 'rate':
            product = get_object_or_404(
                Product, pk=request.GET.get('product_id'))
            product.votes.create(
                user=request.user,
                value=request.GET.get('value'),
            )
        else:
            print('Uncorrect action on', request.get_full_path())
        return redirect('store:homepage')


class ProductsView(ListView):
    template_name = 'store/products.html'
    context_object_name = 'products'
    paginate_by = 40

    def get_queryset(self):
        cat = None
        if self.kwargs.get('subcat_slug'):
            cat = get_object_or_404(klass=Subcategory, slug=self.kwargs.get('subcat_slug'))
        elif self.kwargs.get('cat_slug'):
            cat = get_object_or_404(klass=Category, slug=self.kwargs.get('cat_slug'))
        elif self.kwargs.get('supercat_slug'):
            cat = get_object_or_404(klass=Supercategory, slug=self.kwargs.get('supercat_slug'))
        if cat:
            return cat.get_products(ordering=self.kwargs.get('order') if self.kwargs.get('order') else None)
        return Product.objects.all() if not self.kwargs.get('order') else Product.objects.all().order_by(self.kwargs.get('order'))

class ProductView(DetailView):
    pass


class SearchView(ListView):
    pass

# Function Based Views