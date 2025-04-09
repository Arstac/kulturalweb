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





// Función para el apartado especial con el scroll DE HOME.HTML

import { Pane } from 'https://cdn.skypack.dev/tweakpane@4.0.4'
import gsap from 'https://cdn.skypack.dev/gsap@3.12.0'
import ScrollTrigger from 'https://cdn.skypack.dev/gsap@3.12.0/ScrollTrigger'

const config = {
  theme: 'dark',
  animate: true,
  snap: true,
  start: gsap.utils.random(0, 100, 1),
  end: gsap.utils.random(900, 1000, 1),
  scroll: true,
  debug: false,
}

const ctrl = new Pane({
  title: 'Config',
  expanded: false,
})

let items
let scrollerScrub
let dimmerScrub
let chromaEntry
let chromaExit

const update = () => {
  document.documentElement.dataset.theme = config.theme
  document.documentElement.dataset.syncScrollbar = config.scroll
  document.documentElement.dataset.animate = config.animate
  document.documentElement.dataset.snap = config.snap
  document.documentElement.dataset.debug = config.debug
  document.documentElement.style.setProperty('--start', config.start)
  document.documentElement.style.setProperty('--hue', config.start)
  document.documentElement.style.setProperty('--end', config.end)

  if (!config.animate) {
    chromaEntry?.scrollTrigger.disable(true, false)
    chromaExit?.scrollTrigger.disable(true, false)
    dimmerScrub?.disable(true, false)
    scrollerScrub?.disable(true, false)
    gsap.set(items, { opacity: 1 })
    gsap.set(document.documentElement, { '--chroma': 0 })
  } else {
    gsap.set(items, { opacity: (i) => (i !== 0 ? 0.2 : 1) })
    dimmerScrub.enable(true, true)
    scrollerScrub.enable(true, true)
    chromaEntry.scrollTrigger.enable(true, true)
    chromaExit.scrollTrigger.enable(true, true)
  }
}

const sync = (event) => {
  if (
    !document.startViewTransition ||
    event.target.controller.view.labelElement.innerText !== 'Theme'
  )
    return update()
  document.startViewTransition(() => update())
}
ctrl.addBinding(config, 'animate', {
  label: 'Animate',
})
ctrl.addBinding(config, 'snap', {
  label: 'Snap',
})
ctrl.addBinding(config, 'start', {
  label: 'Hue Start',
  min: 0,
  max: 1000,
  step: 1,
})
ctrl.addBinding(config, 'end', {
  label: 'Hue End',
  min: 0,
  max: 1000,
  step: 1,
})
ctrl.addBinding(config, 'scroll', {
  label: 'Scrollbar',
})
ctrl.addBinding(config, 'debug', {
  label: 'Debug',
})

ctrl.addBinding(config, 'theme', {
  label: 'Theme',
  options: {
    System: 'system',
    Light: 'light',
    Dark: 'dark',
  },
})

ctrl.on('change', sync)

// backfill the scroll functionality with GSAP
if (
  !CSS.supports('(animation-timeline: scroll()) and (animation-range: 0% 100%)')
) {
  gsap.registerPlugin(ScrollTrigger)

  // animate the items with GSAP if there's no CSS support
  items = gsap.utils.toArray('ul li')

  gsap.set(items, { opacity: (i) => (i !== 0 ? 0.2 : 1) })

  const dimmer = gsap
    .timeline()
    .to(items.slice(1), {
      opacity: 1,
      stagger: 0.5,
    })
    .to(
      items.slice(0, items.length - 1),
      {
        opacity: 0.2,
        stagger: 0.5,
      },
      0
    )

  dimmerScrub = ScrollTrigger.create({
    trigger: items[0],
    endTrigger: items[items.length - 1],
    start: 'center center',
    end: 'center center',
    animation: dimmer,
    scrub: 0.2,
  })

  // register scrollbar changer
  const scroller = gsap.timeline().fromTo(
    document.documentElement,
    {
      '--hue': config.start,
    },
    {
      '--hue': config.end,
      ease: 'none',
    }
  )

  scrollerScrub = ScrollTrigger.create({
    trigger: items[0],
    endTrigger: items[items.length - 1],
    start: 'center center',
    end: 'center center',
    animation: scroller,
    scrub: 0.2,
  })

  chromaEntry = gsap.fromTo(
    document.documentElement,
    {
      '--chroma': 0,
    },
    {
      '--chroma': 0.3,
      ease: 'none',
      scrollTrigger: {
        scrub: 0.2,
        trigger: items[0],
        start: 'center center+=40',
        end: 'center center',
      },
    }
  )
  chromaExit = gsap.fromTo(
    document.documentElement,
    {
      '--chroma': 0.3,
    },
    {
      '--chroma': 0,
      ease: 'none',
      scrollTrigger: {
        scrub: 0.2,
        trigger: items[items.length - 2],
        start: 'center center',
        end: 'center center-=40',
      },
    }
  )
}
// run it
update()