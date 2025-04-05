/*!
* Start Bootstrap - Agency v7.0.12 (https://startbootstrap.com/theme/agency)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-agency/blob/master/LICENSE)
*/

window.addEventListener('DOMContentLoaded', event => {
    // Navbar shrink function
    const navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) return;
        
        navbarCollapsible.classList.toggle('navbar-shrink', window.scrollY !== 0);
    };

    // Initial shrink
    navbarShrink();
    
    // Shrink on scroll
    document.addEventListener('scroll', navbarShrink);

    // Bootstrap ScrollSpy
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    }

    // Collapse responsive navbar
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    if (navbarToggler) {
        const responsiveNavItems = [].slice.call(
            document.querySelectorAll('#navbarResponsive .nav-link')
        );
        
        responsiveNavItems.forEach(responsiveNavItem => {
            responsiveNavItem.addEventListener('click', () => {
                if (window.getComputedStyle(navbarToggler).display !== 'none') {
                    navbarToggler.click();
                }
            });
        });
    }

    // Actualizar subtotal del carrito
    const quantityInputs = document.querySelectorAll('.quantity-input');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function () {
            const itemId = this.getAttribute('data-item-id');
            const productId = this.getAttribute('data-product-id');
            const quantity = this.value;
            updateSubtotal(itemId, productId, quantity);
        });
    });

    // Inicializar reproductor de música
    initializeMusicPlayer();
});

// Función para actualizar subtotal
function updateSubtotal(itemId, productId, quantity) {
    fetch(`/carrito/update/${itemId}/${productId}/${quantity}/`)
        .then(response => response.json())
        .then(data => {
            const updateElement = (selector, text) => {
                const element = document.querySelector(selector);
                if (element) element.textContent = text;
            };
            
            updateElement(`.subtotal[data-item-id="${itemId}"]`, `${data.subtotal} €`);
            updateElement('.total-carrito', `${data.total_carrito} €`);
            updateElement('.total-items', `(${data.total_items}) artículos`);
        })
        .catch(error => console.error('Error:', error));
}

// Control de opacidad del navbar
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    const maxOpacity = 0.6;
    const scrollRange = 500;
    const scrollY = window.scrollY || window.pageYOffset;
    const opacity = Math.min(maxOpacity, (scrollY / scrollRange) * maxOpacity);
  
    navbar.style.backgroundColor = `rgba(0, 0, 0, ${opacity})`;
});

// Reproductor de música
function initializeMusicPlayer() {
    const playButtons = document.querySelectorAll('.play-button');
    if (!playButtons.length) return;

    let currentAudio = null;
    let currentButton = null;

    const toggleIcon = (element, play = true) => {
        if (!element) return;
        element.classList.toggle('fa-play', play);
        element.classList.toggle('fa-pause', !play);
    };

    playButtons.forEach(button => {
        button.addEventListener('click', function() {
            const cancionId = this.dataset.cancionId;
            const audio = document.getElementById(`audio-${cancionId}`);
            const icon = this.querySelector('i');
            
            if (!audio || !icon) return;

            // Pausar audio actual
            if (currentAudio && currentAudio !== audio) {
                currentAudio.pause();
                currentAudio.currentTime = 0;
                if (currentButton) {
                    toggleIcon(currentButton.querySelector('i'), true);
                }
            }

            // Controlar reproducción
            if (audio.paused) {
                audio.play()
                    .then(() => {
                        toggleIcon(icon, false);
                        currentAudio = audio;
                        currentButton = this;
                    })
                    .catch(error => console.error('Error al reproducir:', error));
            } else {
                audio.pause();
                toggleIcon(icon, true);
                currentAudio = null;
                currentButton = null;
            }

            // Manejar finalización
            audio.onended = () => {
                toggleIcon(icon, true);
                currentAudio = null;
                currentButton = null;
            };
        });
    });

    // Clic fuera
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.play-button') && currentAudio) {
            currentAudio.pause();
            currentAudio.currentTime = 0;
            toggleIcon(currentButton?.querySelector('i'), true);
            currentAudio = null;
            currentButton = null;
        }
    });
}

// Función para preparar reproductor fijo (si es necesario)
function preparePlayer(songId, audioUrl, title, artist, imageUrl) {
    const setElementContent = (id, content) => {
        const element = document.getElementById(id);
        if (element) element.textContent = content;
    };

    setElementContent('songTitle', title);
    setElementContent('songArtist', artist);
    
    const albumImage = document.getElementById('albumImage');
    if (albumImage) albumImage.src = imageUrl;

    const audioPlayer = document.getElementById('fixedAudioPlayer');
    if (audioPlayer) audioPlayer.src = audioUrl;
}