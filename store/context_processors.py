from .models import Supercategory


def get_supercategories_to_context(request):
    return {
        'supercategories': Supercategory.objects.all(),
    }
