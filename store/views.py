from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.views.generic import (
    View,
    TemplateView,

)
from django.views.generic.base import (
    ContextMixin,
)

from store.utils import newsletter
from store.models import (
    Product
)

# Mixins


# Class Based Views
class HomepageView(View, ContextMixin):
    template_name = "store/homepage.html"
    extra_context = {
    }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class NewslettersView(View):
    def get(self, request, *args, **kwargs):
        if request.GET.get('action') and request.GET.get('email'):
            if request.GET.get('action') == 'sign':
                newsletter.sign(request.GET.get('email'))
            elif request.GET.get('action') == 'unsign':
                newsletter.unsign(request.GET.get('email'))
            else:
                print('Uncorrect action')
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


class ProductView(View):
    pass


class SearchView(View):
    pass


class FilterView(View):
    pass

    # Function Based Views
