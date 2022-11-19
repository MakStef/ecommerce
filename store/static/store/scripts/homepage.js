import * as base from './base.js';

let maCont = document.querySelector('.content')
let maObj = {
    'image_source': "store/images/products/example.png",
    'title': "Example",
    'size': "24x7x5",
    'materials': "Material",
    'personal_rating': 0,
    'rating': 2.5,
    'rate_count': 20,
    'price': 128.99,
}

base.appendProductCard(maCont, maObj);