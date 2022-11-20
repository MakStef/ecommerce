from .models import ProductSupercategory


def get_supercategories_to_context(request):
    return {
        'supercategories': ProductSupercategory.objects.all(),
    }
