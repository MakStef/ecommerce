function appendProductCard(container, product) {
    let template = document.querySelector('#product-card-template').content.cloneNode(true);

    let cardImage = template.querySelector('.product-card__image');
    let cardTitle = template.querySelector('.product-card__title');
}