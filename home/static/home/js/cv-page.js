$( () => {
     $('.l-content').on('displayed', (event) => {
          anime({
               targets: '.cv-left-column > *',
               translateY: ['50px', '0px'],
               opacity: [0, 1],
               easing: 'easeOutQuint',
               delay: anime.stagger(300),
          });
     
          anime({
               targets: '.cv-right-column',
               translateY: ['50px', '0px'],
               opacity: [0, 1],
               easing: 'easeOutQuint',
               delay: anime.stagger(300),
          });
     });
}); 