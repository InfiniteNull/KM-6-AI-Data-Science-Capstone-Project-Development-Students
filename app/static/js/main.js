// SHOW MENU
const navMenu = document.getElementById('nav-menu'),
    navToggle = document.getElementById('nav-toggle'),
    navClose = document.getElementById('nav-close');

// MENU SHOW
if (navToggle) {
    navToggle.addEventListener('click', () => {
        navMenu.classList.add('show-menu')
    });
}

// MENU HIDE
if (navClose) {
    navClose.addEventListener('click', () => {
        navMenu.classList.remove('show-menu')
    });
}

// REMOVE MENU MOBILE
const navLink = document.querySelectorAll('.nav__link');
function linkAction() {
    const navMenu = document.getElementById('nav-menu');
    navMenu.classList.remove('show-menu');
}
navLink.forEach((n) => n.addEventListener('click', linkAction));

// ACTIVE LINK
const navlink = document.querySelectorAll('.nav__link');

function activeLink() {
    navlink.forEach((a) => a.classList.remove('active-link'));
    this.classList.add('active-link');
}

navlink.forEach((a) => a.addEventListener('click', activeLink));

// BG HEADER
function scrollHeader() {
    const header = document.getElementById('header');
    // 
    if (this.scrollY >= 50) header.classList.add('scroll-header');
    else header.classList.remove('scroll-header');
}
window.addEventListener('scroll', scrollHeader);

// TESTIMONIAL

const slides = document.querySelector('.slides');
const buttons = document.querySelectorAll('.navigation button');

buttons.forEach(button => {
    button.addEventListener('click', () => {
        buttons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
        const slideIndex = button.getAttribute('data-slide');
        slides.style.transform = `translateX(-${slideIndex * 100}%)`;
    });
});


// MIXIRUP FILLTER
// let mixerProjects = mixitup('.projects__container', {
//     selectors: {
//         target: '.project__item',
//     },
//     animation: {
//         duration: 300
//     }
// });

// ACTIVE WORK
const linkWork = document.querySelectorAll('.category__btn');

function activeWork() {
    linkWork.forEach((a) => a.classList.remove('active-work'));
    this.classList.add('active-work');
}

linkWork.forEach((a) => a.addEventListener('click', activeWork));

// CONTACT FORM
const contactForm = document.getElementById('contact-form'),
    contactName = document.getElementById('contact-name'),
    contactEmail = document.getElementById('contact-email'),
    Message = document.getElementById('message'),
    contactMessage = document.getElementById('contact-message');

const sendEmail = (e) => {
    e.preventDefault();

    // CHECK FIELD HAS A VALUE
    if (contactName.value === '' || contactEmail.value === '' || Message.value === '') {
        // ADD AND REMOVE COLOR
        contactMessage.classList.remove('color-light');
        contactMessage.classList.add('color-dark');

        // SHOW MESSAGE
        contactMessage.textContent = 'Tulis Semua Kolom Input';
    }
    else {
        // SERVICE ID - TEMPLATE ID - #FORM - PUBLICKEY
        emailjs.sendForm('service_fu36s5r', 'template_c0zp9sr', '#contact-form', 'QhtVaAXM-nVm1AjEM')
            .then(() => {
                // SHOW MESSAGE COLOR
                contactMessage.classList.add('color-light');
                contactMessage.textContent = 'Pesan Terkirim ✅';

                // REMOVE MESSAGE AFTER 5 SEC
                setTimeout(() => {
                    contactMessage.textContent = '';
                }, 5000);
            }, (error) => {
                alert('OPPs! Terjadi Kesalahan', error);
            }
            );
        // CLEAR INPUT
        contactName.value = '';
        contactEmail.value = '';
        Message.value = '';
    }
};
contactForm.addEventListener('submit', sendEmail);
