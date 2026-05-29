$( () => {
    anime({
        targets: '.l-intro__credentials > *',
        translateY: ['50px', '0px'],
        opacity: [0, 1],
        easing: 'easeOutQuint',
        delay: anime.stagger(300),
    });

    setTimeout(() => {

        anime({
            targets: '.l-intro__scroll-icon',
            opacity: [0, 1],
            easing: 'linear',
            duration: 500,
        });

        anime({
            targets: '.l-intro__scroll-icon',
            translateY: -20,
            direction: 'alternate',
            loop: true,
            easing: 'easeInOutSine',
        });

    }, 800);

    
    var toastEl = $('#construction-toast');
    if (toastEl.length > 0) {
        var toast = new bootstrap.Toast(toastEl);
        toast.show();
    }


    function subscribeIntersectionEvent(targetElementQuery, intersectionOptions, callback) {
        const targetElements = document.querySelectorAll(targetElementQuery);
        if (!targetElements.length) return;

        const observerCallback = (entries, observer) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    callback(entry, observer);
                }
            });
        }

        const observer = new IntersectionObserver(observerCallback, intersectionOptions);
        targetElements.forEach(element => observer.observe(element));
    }

    if($('.l-intro').length){
        const rootIntersectionOptions = {
            root: null,
            rootMargin: '0px 0px -99.9% 0px', 
            threshold: 0,
        };

        subscribeIntersectionEvent('.l-content', rootIntersectionOptions, (entry, observer) => {
            observer.unobserve(entry.target);
            anime({
                targets: '.l-content__header',
                translateY: ['50px', '0px'],
                opacity: [0, 1],
                easing: 'easeOutQuint',
            });

            setTimeout(() => {
                $(entry.target).trigger('displayed');
            }, 200);
        });

    } else {
        $('.l-content__header').css('opacity', '1');
        $(document).on('app-ready', () => {
            $('.l-content').trigger('displayed');
        });
    }
});