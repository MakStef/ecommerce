window.onload = ()=> {
    document.querySelector('.load').classList.add('invisible', 'hidden');
    document.querySelector('.wrapper').classList.remove('invisible');
}
const signNewsletter = () => {
    const email = document.querySelector('#newsletter-email');
    window.location.href = `/newsletters?action=sign&email=${email.value}`
}
const unsignNewsletter = () => {
    const email = document.querySelector('#newsletter-email');
    window.location.href = `/newsletters?action=unsign&email=${email.value}`
}
const toggleNewsletter = (toggler) => {
    const sign = toggler.parentNode.querySelector('.newsletter-button_sign'),
    unsign = toggler.parentNode.querySelector('.newsletter-button_unsign');
    sign.classList.toggle('toggled');
    unsign.classList.toggle('toggled');
    
    let toChange = (toggler.parentNode.parentNode.parentNode.querySelector('.page-footer__item-link a')) ? toggler.parentNode.parentNode.parentNode.querySelector('.page-footer__item-link a') : undefined;
    if (unsign.classList.contains('toggled')) {
        toChange.innerText = 'Sign up now!'
    }
    else {
        toChange.innerText = 'Unsign newsletter.'
    }
}