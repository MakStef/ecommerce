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
const setStars = (rating, cardRating) => {
    const fillSpan = (from, to) => {
        const floatPart = (rating - Math.floor(rating))

        const span = Object.values(cardRating.children).slice(from, to)
        span.forEach(
            star => star.querySelector('img').src = `/static/store/images/icons/star-icon.svg`
        )
        if (to !== -1) {
            Object.values(cardRating.children).slice(to).forEach(
                star => changeStar(star.querySelector('img'), 'empty')
            )
        }
        if (0.3 < floatPart) {
            changeStar(cardRating.children[to].querySelector('.rating-star'), 'half')
        }
        if (0.6 < floatPart) {
            changeStar(cardRating.children[to].querySelector('.rating-star'), 'fill')
        }
    }
    // If rating is n.3-...-n.7, we fill n stars, half fill 1 star and the rest remain empty
    switch (Math.floor(rating)) {
        case 1:
            fillSpan(from=0, to=1)
            break;
        case 2:
            fillSpan(from=0, to=2)
            break;
        case 3:
            fillSpan(from=0, to=3)

            break;
        case 4:
            fillSpan(from=0, to=4)

            break;
        case 5:
            fillSpan(from=0, to=5)
            break
        default:
            break;
    }
}
const rate = (rating, cardRating, cardId) => {
    authenticated === true ? async () => {
        const response = await fetch(`${window.location.host}/product/rate`, {
            method: 'POST',
            headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            },
            body: `{
            "product_id": ${cardId.value},
            "rating" : ${rating},
            }`,
        });
            let personalRating = cardId.parentElement.querySelector('.product-card__personal-rating')
            if (cardId.parentNode.contains(personalRating) === true) {
                personalRating.value = rating
            } else {
                personalRating = document.createElement('input')
                personalRating.type = 'hidden';
                personalRating.value = rating;
                personalRating.classList.add('product-card__personal-rating');
                cardId.parentNode.appendChild(personalRating);
            }
        setStars(rating, cardRating);
    
    } : alert('You are not authenticated');
    // let personalRating = cardId.parentElement.querySelector('.product-card__personal-rating')
    //     if (cardId.parentNode.contains(personalRating) === true) {
    //         personalRating.value = rating
    //     } else {
    //         personalRating = document.createElement('input')
    //         personalRating.type = 'hidden';
    //         personalRating.value = rating;
    //         personalRating.classList.add('product-card__personal-rating');
    //         cardId.parentNode.appendChild(personalRating);
    //     }
    // setStars(rating, cardRating);
}
function appendProductCard(container, product) {
    let template = document.querySelector('#product-card-template').content.cloneNode(true);
    // Define card and it's parts
    let card = template.querySelector('.product-card'),
    cardId = template.querySelector('.product-card__id'),
    cardImage = template.querySelector('.product-card__image img'),
    cardTitle = template.querySelector('.product-card__row_title h2'),
    cardSize = template.querySelector('.product-card__size h3'),
    cardMaterials = template.querySelector('.product-card__materials h3'),
    cardRating = template.querySelector('.product-card__rating'),
    cardPersonalRating = template.querySelector('.product-card__personal-rating'),
    cardRateCount = template.querySelector('.product-card__rate-count h3'),
    cardPrice = template.querySelector('.product-card__price h3');
    // Fill card's parts
    cardId.attributes['value'] = product['rating']
    cardImage.attributes.src = window.location.host+'/media/'+product['image_source']
    cardTitle.innerText = product["title"]
    cardSize.innerText = product["size"]
    cardMaterials.innerText = product["materials"]
    product['personal_rating'] ? cardPersonalRating.value = product['personal_rating'] : null
    cardRateCount.innerText = product["rate_count"] + " votes"
    cardPrice.innerText = product["price"] + "$"

    cardPersonalRating.value != 0 ? setStars(product['personal_rating'], cardRating) : setStars(product['rating'], cardRating)

    container.appendChild(card)
}
let maCont = document.querySelector('.content')
let maObj = {
    'image_source' : "store/images/example.png",
    'title' : "Example",
    'size' : "24x7x5",
    'materials' : "Material",
    'personal_rating' : 0,
    'rating' : 2.5,
    'rate_count' : 20,
    'price' : 128.99,
}

appendProductCard(maCont, maObj)