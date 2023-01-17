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
from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator

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

import api
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


class ProductsView(ListView, ContextMixin):
    template_name = 'store/products.html'
    context_object_name = 'products'
    model = Product
    paginate_by = 24
    extra_context = {
        'filter_cats': Category.objects.all()[:4],
        'max_price': Product.objects.all().order_by('-price')[0].price,
        'min_price': Product.objects.all().order_by('price')[0].price,
    }
    
    def get_queryset(self):
        queryset = Product.objects.all()
        request = self.request

        if request.GET.get('subcategory_id'):
            queryset = queryset.filter(subcat_id=request.GET.get('subcategory_id'))
        elif request.GET.get('category_id'):
            queryset = queryset.filter(cat_id=request.GET.get('category_id'))
        elif request.GET.get('supercategory_id'):
            queryset = queryset.filter(supercat_id=request.GET.get('supercategory_id'))
        
        if request.GET.get('ordering'):
            queryset = queryset.order_by(request.GET.get('ordering'))
        
        if request.GET.get('count'):
            lim = int(request.GET.get('count'))
            queryset = queryset[:lim]

        if request.GET.get('price_span'):
            cheapest, expensiest = request.GET.get('price_span').split('_')
            queryset = queryset.filter(price__lte=int(cheapest), price__gte=int(expensiest))
        return queryset

    def get(self, request, *args, **kwargs):
        if request.GET.get('subcategory_id'):
            self.extra_context.update({
                'prods_cat': Subcategory.objects.get(id=int(request.GET.get('subcategory_id')))
            })
        elif request.GET.get('category_id'):
            self.extra_context.update({
                'prods_cat': Category.objects.get(id=int(request.GET.get('category_id')))
            })
        elif request.GET.get('supercategory_id'):
            self.extra_context.update({
                'prods_cat': Supercategory.objects.get(id=int(request.GET.get('supercategory_id')))
            })
        return super().get(request, *args, **kwargs)


class ProductView(DetailView):
    template_name = "store/product.html"



class SearchView(ListView):
    pass

# Function Based Views