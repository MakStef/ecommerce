import * as base from './base.js';

let scene = document.querySelector('.welcome-section__sheath > .image-container');
const sheathParallax = new Parallax(scene);


let nlButtons = document.querySelectorAll('.newsletter-toggler');
for (const toggler of nlButtons) {
    toggler.onclick = () => base.toggleNewsletter(toggler);
}
nlButtons = document.querySelectorAll('.newsletter-button_sign')
for (const signButton of nlButtons) {
    signButton.onclick = () => base.signNewsletter();
}
nlButtons = document.querySelectorAll('.newsletter-button_unsign')
for (const unsignButton of nlButtons) {
    unsignButton.onclick = () => base.unsignNewsletter(toggler);
}

let bestsellerProducts = JSON.parse(JSON.parse(document.querySelector('#brandnew-products').textContent))

const brandnewSwiper = new Swiper('.bestsellers-section .swiper', {
    // Optional parameters
    loop: true,
    spaceBetween: 1024,

    // If we need pagination
    pagination: {
        el: '.swiper-pagination',
    },
});
let fillBestsellerSwiper = (products) => {
    var slides = []
    var cond;
    if (window.matchMedia('(min-width:0px)').matches) {
        cond = 1;
    }
    if (window.matchMedia('(min-width:768px)').matches) {
        cond = 2;
    }
    if (window.matchMedia('(min-width:1440px)').matches) {
        cond = 4;
    }

    for (const [index, product] of products.entries()) {
        if (index === 0 || index % cond === 0) {
            var slide = document.createElement('div');
            var container = document.createElement('div');
            slide.classList.add('swiper-slide')
            container.classList.add('products-row')
            slide.append(container)
            slides.push(slide);
        }
        base.appendProductCard(container, product);
    }
    brandnewSwiper.appendSlide(slides);
}
fillBestsellerSwiper(bestsellerProducts);
