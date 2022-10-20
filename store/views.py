from django.shortcuts import render, redirect
from django.views.generic import (
    View,
    TemplateView,
)
from django.views.generic.base import (
    ContextMixin,
)

from store.utils import newsletter


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
            if request.GET.get('action') == 'unsign':
                newsletter.unsign(request.GET.get('email'))
        return redirect('store:homepage')
# Function Based Views
