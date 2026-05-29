$(() => {
    $('.l-content').on('displayed', (event) => {
        anime({
            targets: '.portfolio-item-wrp',
            translateY: ['50px', '0px'],
            opacity: [0, 1],
            easing: 'easeOutExpo',
            delay: anime.stagger(300),
        });
    });
});
