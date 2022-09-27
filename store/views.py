from django.shortcuts import render
from django.views.generic import (
    View,
    TemplateView,
)
from django.views.generic.base import (
    ContextMixin,
)

# Mixins


# Create your views here.
class HomepageView(View, ContextMixin):
    template_name = "store/homepage.html"
    extra_context = {
    }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
