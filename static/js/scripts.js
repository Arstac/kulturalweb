/*!
* Start Bootstrap - Agency v7.0.12 (https://startbootstrap.com/theme/agency)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-agency/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {
    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    //  Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});



function preparePlayer(songId, audioUrl, title, artist, imageUrl) {
    // Configura la información de la canción en el reproductor fijo
    document.getElementById('songTitle').innerText = title;
    document.getElementById('songArtist').innerText = artist;
    document.getElementById('albumImage').src = imageUrl;

    // Configura el audio source
    var audioPlayer = document.getElementById('fixedAudioPlayer');
    audioPlayer.src = audioUrl;
    
    // Opcional: Si quieres reproducir automáticamente la canción al cargarla
    // audioPlayer.play();
}



//Regula la opacitat del navbar
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar'); // Cambia a tu selector de navbar específico
    const maxOpacity = 0.6;
    const scrollRange = 500; // Ajusta este valor según la altura a partir de la cual la opacidad debe llegar a 0.3
    let scrollY = window.scrollY || window.pageYOffset;
    let opacity = scrollY / scrollRange * maxOpacity;
    opacity = Math.min(maxOpacity, opacity); // Asegura que la opacidad no exceda de 0.3
  
    navbar.style.backgroundColor = `rgba(0, 0, 0, ${opacity})`;
  });




//PAGINA DEL EVENTO -- EVENTOS RELACIONATS (PERMET ARRASTRAR I SCROLLEJAR DES DE QUALSEVOL PUNT DE)
// Selector del contenedor que quieres que sea desplazable
document.addEventListener('DOMContentLoaded', function() {
    const slider = document.querySelector('.row-scrollable');
    let isDown = false;
    let startX;
    let scrollLeft;
  
    slider.addEventListener('mousedown', (e) => {
      isDown = true;
      slider.classList.add('grabbing');
      startX = e.pageX - slider.offsetLeft;
      scrollLeft = slider.scrollLeft;
    });
  
    slider.addEventListener('mouseleave', () => {
      isDown = false;
      slider.classList.remove('grabbing');
    });
  
    slider.addEventListener('mouseup', () => {
      isDown = false;
      slider.classList.remove('grabbing');
    });
  
    slider.addEventListener('mousemove', (e) => {
      if (!isDown) return;
      e.preventDefault();
      const x = e.pageX - slider.offsetLeft;
      const walk = (x - startX); // Controla la velocidad del arrastre
      slider.scrollLeft = scrollLeft - walk;
    });
  });



  //VINILS FLOTANTS
// Espera a que el DOM esté listo
document.addEventListener('DOMContentLoaded', function () {
    const vinyls = document.querySelectorAll('.floating-vinyl');
  
    // Función constructora para crear vinilos con propiedades de movimiento
    function Vinyl(vinylElement) {
        this.vx = Math.random() * 2 - 1; // Velocidad horizontal
        this.vy = Math.random() * 2 - 1; // Velocidad vertical
        this.element = vinylElement;
        this.friction = 0.9998; // La fricción reduce la velocidad en cada fotograma

        this.move = function() {
        const rect = this.element.getBoundingClientRect();
        if (rect.left <= 0 || rect.right >= window.innerWidth) this.vx *= -1;
        if (rect.top <= 0 || rect.bottom >= window.innerHeight) this.vy *= -1;

        // Aplica fricción para reducir la velocidad
        this.vx *= this.friction;
        this.vy *= this.friction;

        // Detiene el movimiento si la velocidad es muy baja
        if (Math.abs(this.vx) < 0.01 && Math.abs(this.vy) < 0.01) {
            this.vx = 0;
            this.vy = 0;
        }

        this.element.style.left = rect.left + this.vx + 'px';
        this.element.style.top = rect.top + this.vy + 'px';
        };
    }
  
    // Crea una instancia de Vinyl para cada vinilo
    const vinylObjects = Array.from(vinyls, vinyl => new Vinyl(vinyl));
  
    // Función de animación recurrente
    function animate() {
      vinylObjects.forEach(vinyl => vinyl.move());
      requestAnimationFrame(animate); // Siguiente ciclo de animación
    }
  
    // Iniciar la animación
    animate();
  
    // Evento del movimiento del ratón
    document.addEventListener('mousemove', event => {
      const mouseX = event.clientX;
      const mouseY = event.clientY;
  
      vinylObjects.forEach(vinyl => {
        const rect = vinyl.element.getBoundingClientRect();
        const dx = mouseX - (rect.left + rect.width / 2);
        const dy = mouseY - (rect.top + rect.height / 2);
        const distance = Math.sqrt(dx * dx + dy * dy);
  
        if (distance < 150) {
          // Calcula el ángulo entre el vinilo y el ratón
          const angle = Math.atan2(dy, dx);
          // Mueve el vinilo en dirección opuesta al ratón
          vinyl.vx = -Math.cos(angle) * 5;
          vinyl.vy = -Math.sin(angle) * 5;
        }
      });
    });
  });


//OBRIR EL MODAL DE TALLES EN EL PRODUCTE
document.addEventListener('DOMContentLoaded', function() {
  var modal = document.getElementById('modalTallas'); // Asegúrate de que el ID corresponde al de tu modal
  var btn = document.getElementById('abrirModal'); // El botón que abre el modal
  var span = document.querySelector('.close'); // El botón o elemento que cierra el modal

  // Evento para abrir el modal
  btn.onclick = function() {
      modal.style.display = "block";
  }

  // Evento para cerrar el modal al hacer clic en el botón de cerrar
  span.onclick = function() {
      modal.style.display = "none";
  }

  // Evento para cerrar el modal al hacer clic fuera de él
  window.onclick = function(event) {
      if (event.target == modal) {
          modal.style.display = "none";
      }
  }
});


//ACTUALITZAR SUBTOTAL DEL CARRITO
document.addEventListener('DOMContentLoaded', function () {
  const quantityInputs = document.querySelectorAll('.quantity-input');
  
  quantityInputs.forEach(input => {
      input.addEventListener('change', function () {
          const itemId = this.getAttribute('data-item-id');
          const productId = this.getAttribute('data-product-id');
          const quantity = this.value;
          updateSubtotal(itemId, productId, quantity);
      });
  });
  
  function updateSubtotal(itemId, productId, quantity) {
      fetch(`/carrito/update/${itemId}/${productId}/${quantity}/`)
          .then(response => response.json())
          .then(data => {
              document.querySelector(`.subtotal[data-item-id="${itemId}"]`).textContent = `${data.subtotal} €`;
              document.querySelector('.total-carrito').textContent = `${data.total_carrito} €`;
              document.querySelector('.total-items').textContent = `(${data.total_items}) artículos`;
          })
          .catch(error => console.error('Error:', error));
  }
});
