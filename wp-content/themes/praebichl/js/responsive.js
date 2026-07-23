(function () {
    'use strict';

    function isMobileView() {
        return window.innerWidth <= 960;
    }

    // Az osszes .papir vizualisan legalsobb pontjahoz igazitja a .main magassagat
    // Ez asztali es mobil nezeten is mukodik
    function shrinkMainToContent() {
        var main = document.querySelector('.main');
        if (!main) return;

        var papirs = main.querySelectorAll('.papir');
        if (papirs.length === 0) return;

        var mainTop = main.getBoundingClientRect().top + window.pageYOffset;
        var lowestBottom = 0;

        papirs.forEach(function (el) {
            var rect = el.getBoundingClientRect();
            var visualBottom = rect.bottom + window.pageYOffset;
            if (visualBottom > lowestBottom) lowestBottom = visualBottom;
        });

        var neededHeight = lowestBottom - mainTop + 30;
        if (neededHeight < main.offsetHeight) {
            main.style.minHeight = neededHeight + 'px';
        }
    }

    // Inline pozicio stílusok eltavolitasa a papir elemekrol (csak mobilon)
    function fixPapirs() {
        document.querySelectorAll('.papir').forEach(function (el) {
            el.style.position = 'static';
            el.style.top = 'auto';
            el.style.left = 'auto';
            el.style.width = '';
            el.style.height = '';
            el.style.margin = '12px auto';
        });
    }

    // Partnerek div inline stilusok
    function fixPartnerek() {
        document.querySelectorAll('.partnerek').forEach(function (el) {
            el.style.width = '';
            el.style.left = '';
            el.style.position = 'static';
            el.style.top = '';
        });
    }

    // Tablazatok inline stilusok
    function fixTables() {
        document.querySelectorAll('.papir table, .main table').forEach(function (t) {
            t.style.position = 'static';
            t.style.margin = '10px 0';
            t.removeAttribute('width');
        });
    }

    // Kepek max-width
    function fixImages() {
        document.querySelectorAll('.papir img, .main img').forEach(function (img) {
            img.style.maxWidth = '100%';
            img.style.height = 'auto';
            img.removeAttribute('width');
            img.removeAttribute('height');
        });
    }

    // Videok reszponziv wrapperbe teves
    function fixVideos() {
        document.querySelectorAll('iframe.shadow, .papir iframe').forEach(function (iframe) {
            if (iframe.parentNode.classList.contains('video-wrapper')) return;
            var wrapper = document.createElement('div');
            wrapper.className = 'video-wrapper';
            iframe.parentNode.insertBefore(wrapper, iframe);
            wrapper.appendChild(iframe);
            iframe.style.position = '';
            iframe.style.left = '';
            iframe.style.top = '';
        });
    }

    // Hamburger menu toggle
    function toggleMenu() {
        var menu = document.getElementById('mobile-menu');
        var btn = document.getElementById('hamburger-btn');
        if (!menu || !btn) return;
        var isOpen = menu.classList.toggle('open');
        btn.textContent = isOpen ? '✕ Bezár' : '☰ Menü';
    }

    // Almenü toggle
    function toggleSubmenu(subId) {
        var sub = document.getElementById(subId);
        var toggle = document.querySelector('[data-sub="' + subId + '"]');
        if (!sub || !toggle) return;
        sub.classList.toggle('open');
        toggle.classList.toggle('open');
    }

    function applyMobileFixes() {
        if (!isMobileView()) return;
        fixPapirs();
        fixPartnerek();
        fixTables();
        fixImages();
        fixVideos();
    }

    // Mobil fooldal hero slideshow
    function startMobileHeroSlideshow() {
        if (!isMobileView()) return;
        var heroBg = document.getElementById('mobile-hero-bg');
        if (!heroBg) return;

        // A meglevo nivoSlider kepek forrasa
        var sliderImgs = document.querySelectorAll('#metaslider_400 img.slider-400');
        if (sliderImgs.length === 0) return;

        var sources = Array.from(sliderImgs).map(function (img) { return img.src; });
        var current = 0;

        // Elso kep azonnal
        heroBg.style.backgroundImage = 'url(' + sources[0] + ')';

        setInterval(function () {
            // Fade ki
            heroBg.style.opacity = '0';
            setTimeout(function () {
                current = (current + 1) % sources.length;
                heroBg.style.backgroundImage = 'url(' + sources[current] + ')';
                // Fade be
                heroBg.style.opacity = '1';
            }, 900);
        }, 4000); // 4 masodpercenkent valt
    }

    document.addEventListener('DOMContentLoaded', function () {
        // Mobilon: inline stilusok eltavolitasa
        applyMobileFixes();

        // Mobil hero slideshow inditasa
        startMobileHeroSlideshow();

        // Minden nezeten: felesleges ures ter vagasa
        shrinkMainToContent();

        // Hamburger gomb
        var btn = document.getElementById('hamburger-btn');
        if (btn) btn.addEventListener('click', toggleMenu);

        // Almenük
        document.querySelectorAll('.sub-toggle').forEach(function (toggle) {
            toggle.addEventListener('click', function () {
                toggleSubmenu(this.getAttribute('data-sub'));
            });
        });
    });

    window.addEventListener('resize', function () {
        applyMobileFixes();
        shrinkMainToContent();
    });
}());
