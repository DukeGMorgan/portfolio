/* ============================================================
   Duke Morgan — portfolio behaviour
   No dependencies. Degrades cleanly if JS is unavailable.
   ============================================================ */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- footer year ---------- */
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  /* ---------- scroll progress + sticky nav ---------- */
  var bar = document.querySelector('.scroll-progress span');
  var nav = document.getElementById('nav');
  var ticking = false;

  function onScroll() {
    var y = window.scrollY || document.documentElement.scrollTop;
    var max = document.documentElement.scrollHeight - window.innerHeight;

    if (bar) {
      var pct = max > 0 ? Math.min(y / max, 1) : 0;
      bar.style.transform = 'scaleX(' + pct + ')';
    }
    if (nav) nav.classList.toggle('is-stuck', y > 12);

    ticking = false;
  }

  window.addEventListener('scroll', function () {
    if (!ticking) {
      window.requestAnimationFrame(onScroll);
      ticking = true;
    }
  }, { passive: true });
  onScroll();

  /* ---------- mobile nav ---------- */
  var toggle = document.querySelector('.nav__toggle');
  var links = document.querySelector('.nav__links');

  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      links.classList.toggle('is-open', !open);
    });

    links.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        toggle.setAttribute('aria-expanded', 'false');
        links.classList.remove('is-open');
      }
    });
  }

  /* ---------- reveal on scroll ---------- */
  var revealables = document.querySelectorAll('.reveal');

  if (reduceMotion || !('IntersectionObserver' in window)) {
    Array.prototype.forEach.call(revealables, function (el) {
      el.classList.add('is-in');
    });
  } else {
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

    Array.prototype.forEach.call(revealables, function (el) {
      revealObserver.observe(el);
    });
  }

  /* ---------- animated stat counters ---------- */
  var stats = document.querySelectorAll('.stat__num[data-count]');

  function formatNumber(n) {
    return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  }

  function runCounter(el) {
    var target = parseFloat(el.getAttribute('data-count'));
    var prefix = el.getAttribute('data-prefix') || '';
    var suffix = el.getAttribute('data-suffix') || '';
    var duration = 1400;
    var start = null;

    function step(ts) {
      if (start === null) start = ts;
      var p = Math.min((ts - start) / duration, 1);
      // ease-out cubic
      var eased = 1 - Math.pow(1 - p, 3);
      var value = Math.round(target * eased);
      el.textContent = prefix + formatNumber(value) + suffix;
      if (p < 1) window.requestAnimationFrame(step);
    }

    window.requestAnimationFrame(step);
  }

  if (!reduceMotion && 'IntersectionObserver' in window && stats.length) {
    var statObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          runCounter(entry.target);
          statObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.55 });

    Array.prototype.forEach.call(stats, function (el) {
      statObserver.observe(el);
    });
  }

  /* ---------- active section in nav ---------- */
  var sections = document.querySelectorAll('main section[id]');
  var navLinks = document.querySelectorAll('.nav__links a[href^="#"]');

  if ('IntersectionObserver' in window && sections.length) {
    var sectionObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var id = entry.target.getAttribute('id');
        Array.prototype.forEach.call(navLinks, function (a) {
          a.classList.toggle('is-active', a.getAttribute('href') === '#' + id);
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });

    Array.prototype.forEach.call(sections, function (s) {
      sectionObserver.observe(s);
    });
  }

  /* ---------- email, assembled client-side to slow down scrapers ---------- */
  var emailLink = document.getElementById('email-link');
  var emailText = document.getElementById('email-text');

  if (emailLink && emailText) {
    var user = ['Duke', 'isrn'].join('');
    var domain = ['me', 'com'].join('.');
    var address = user + String.fromCharCode(64) + domain;
    var revealed = false;

    emailLink.addEventListener('click', function (e) {
      if (revealed) return;              // second click follows the mailto
      e.preventDefault();
      revealed = true;
      emailText.textContent = address;
      emailLink.setAttribute('href', 'mailto:' + address);
    });
  }

})();
