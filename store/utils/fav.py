def toggle(fav, product):
    if fav.products.filter(product=product).exists():
        fav.products.remove(product)
    else:
        favourite.products.add(product)
