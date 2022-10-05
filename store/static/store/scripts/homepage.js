function appendProductCard(container, product) {
    let template = document.querySelector('#product-card-template').content.cloneNode(true);
    // Define card and it's parts
    let card = template.querySelector('.product-card'),
    cardImage = template.querySelector('.product-card__image img'),
    cardTitle = template.querySelector('.product-card__row_title h2'),
    cardSize = template.querySelector('.product-card__size h3'),
    cardMaterials = template.querySelector('.product-card__materials h3'),
    cardRating = template.querySelector('.product-card__rating'),
    cardRateCount = template.querySelector('.product-card__rate-count h3'),
    cardPrice = template.querySelector('.product-card__price h3');
    // Fill card's parts
    cardImage.attributes.src = window.location.host+'/media/'+product['image_source']
    cardTitle.innerText = product["title"]
    cardSize.innerText = product["size"]
    cardMaterials.innerText = product["materials"]
    cardRateCount.innerText = product["rate_count"] + " votes"
    cardPrice.innerText = product["price"] + "$"

    const changeStar = (image, type='fill') => {
        let path = '/static/store/images/icons/';
        switch (type) {
            case 'empty':
                image.src = path + 'emptystar-icon.svg'
                break;
            case 'half':
                image.src = path + 'halfstar-icon.svg'
                break;
            default:
                image.src = path + 'star-icon.svg'
                break
        }
    }
    // If rating is 0.3-...-3.7, we fill 3 stars, half fill 1 star and the last one is unfilled
    const floatPart = (product['rating'] - Math.floor(product['rating']))
    switch (Math.floor(product['rating'])) {
        case 1:
            for (let i = 0; i <= 0; i++) {
                const star = cardRating.children[i].querySelector('.rating-star');
                changeStar(star, 'fill');
            }
            if (0.3 < floatPart) {
                changeStar(cardRating.children[1].querySelector('.rating-star'), 'half')
            }
            if (0.6 < floatPart) {
                changeStar(cardRating.children[1].querySelector('.rating-star'), 'fill')
            }
            break;
        case 2:
            for (let i = 0; i <= 1; i++) {
                const star = cardRating.children[i].querySelector('.rating-star');
                changeStar(star, 'fill');
            }
            if (0.3 < floatPart) {
                changeStar(cardRating.children[2].querySelector('.rating-star'), 'half')
            }
            if (0.6 < floatPart) {
                changeStar(cardRating.children[2].querySelector('.rating-star'), 'fill')
            }
            break;
        case 3:
            for (let i = 0; i <= 2; i++) {
                const star = cardRating.children[i].querySelector('.rating-star');
                changeStar(star, 'fill');
            }
            if (0.3 < floatPart) {
                changeStar(cardRating.children[3].querySelector('.rating-star'), 'half')
            }
            if (0.6 < floatPart) {
                changeStar(cardRating.children[3].querySelector('.rating-star'), 'fill')
            }
            break;
        case 4:
            for (let i = 0; i <= 3; i++) {
                const star = cardRating.children[i].querySelector('.rating-star');
                changeStar(star, 'fill');
            }
            if (0.3 < floatPart) {
                changeStar(cardRating.children[4].querySelector('.rating-star'), 'half')
            }
            if (0.6 < floatPart) {
                changeStar(cardRating.children[4].querySelector('.rating-star'), 'fill')
            }
            break;
        case 5:
            for (let i = 0; i <= 4; i++) {
                const star = cardRating.children[i].querySelector('.rating-star');
                changeStar(star, 'fill');
            }
        default:
            break;
    }

    container.appendChild(card)
}
let maCont = document.querySelector('.content > .row')
let maObj = {
    'image_source' : "store/images/example.png",
    'title' : "Example",
    'size' : "24x7x5",
    'materials' : "Material",
    'rating' : 5,
    'rate_count' : 20,
    'price' : 128.99,
}

// appendProductCard(maCont, maObj)