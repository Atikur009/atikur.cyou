/* Atikur Rahman — portfolio interactions (index.html only). */
(function () {
  "use strict";

  /* ---------- theme toggle (persisted) ---------- */
  var root = document.documentElement;
  var themeBtn = document.getElementById("themeToggle");
  function paintThemeBtn() {
    themeBtn.textContent = root.getAttribute("data-theme") === "light" ? "🌙" : "☀️";
  }
  paintThemeBtn();
  themeBtn.addEventListener("click", function () {
    var next = root.getAttribute("data-theme") === "light" ? "dark" : "light";
    root.setAttribute("data-theme", next);
    try { localStorage.setItem("atikur-theme", next); } catch (e) {}
    paintThemeBtn();
  });

  /* ---------- mobile menu ---------- */
  var menuBtn = document.getElementById("menuBtn");
  var mobileMenu = document.getElementById("mobileMenu");
  menuBtn.addEventListener("click", function () {
    var open = mobileMenu.classList.toggle("open");
    menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    menuBtn.textContent = open ? "✕" : "☰";
  });
  mobileMenu.querySelectorAll("a").forEach(function (a) {
    a.addEventListener("click", function () {
      mobileMenu.classList.remove("open");
      menuBtn.setAttribute("aria-expanded", "false");
      menuBtn.textContent = "☰";
    });
  });

  /* ---------- typing effect ---------- */
  var roles = [
    "Digital Marketing Expert",
    "Social Media Marketer",
    "Creative Designer",
    "YouTube SEO Expert",
    "Lead Generation Specialist"
  ];
  var typedEl = document.getElementById("typedText");
  var roleIdx = 0, charIdx = 0, deleting = false;
  function tick() {
    var role = roles[roleIdx];
    if (!deleting) {
      charIdx++;
      typedEl.textContent = role.slice(0, charIdx);
      if (charIdx === role.length) { deleting = true; setTimeout(tick, 1700); return; }
      setTimeout(tick, 55);
    } else {
      charIdx--;
      typedEl.textContent = role.slice(0, charIdx);
      if (charIdx === 0) { deleting = false; roleIdx = (roleIdx + 1) % roles.length; setTimeout(tick, 350); return; }
      setTimeout(tick, 28);
    }
  }
  tick();

  /* ---------- scroll reveal ---------- */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- scrollspy ---------- */
  var sections = ["home", "about", "skills", "projects", "experience", "services", "pricing", "contact"]
    .map(function (id) { return document.getElementById(id); })
    .filter(Boolean);
  var navAnchors = document.querySelectorAll(".navlinks a");
  function onScroll() {
    var pos = window.scrollY + 120, current = "home";
    sections.forEach(function (s) { if (s.offsetTop <= pos) current = s.id; });
    navAnchors.forEach(function (a) {
      a.classList.toggle("active", a.getAttribute("href") === "#" + current);
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- project filter ---------- */
  var filterBtns = document.querySelectorAll(".filter-btn");
  var cards = document.querySelectorAll(".project-card");
  filterBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      filterBtns.forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");
      var f = btn.getAttribute("data-filter");
      cards.forEach(function (c) {
        c.classList.toggle("hide", f !== "all" && c.getAttribute("data-cat") !== f);
      });
    });
  });

  /* ---------- download counts (same endpoints as before) ---------- */
  function loadCount(elId, url) {
    var el = document.getElementById(elId);
    if (!el) return;
    fetch(url).then(function (r) { return r.json(); }).then(function (d) {
      var n = parseInt(d.count, 10) || 0;
      el.textContent = "⬇ " + n.toLocaleString("en-US") + " downloads";
    }).catch(function () {});
  }
  loadCount("apk-download-count", "/api/download-count");
  loadCount("avd-download-count", "/api/avd-download-count");
  loadCount("pesticide-download-count", "/api/pesticide-download-count");
})();
