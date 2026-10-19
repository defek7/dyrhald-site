/* Dyrhald website - the few bits of script every page shares. */

/* The Discord invite every "Join the Discord" button uses. Set it to "" and those buttons show "Coming soon" instead.
   The launcher zip isn't on the website: it's pinned in the Discord's Testing channel. */
var DYRHALD = {
  discord: "https://discord.gg/HhMNbjZHPn"
};

(function () {
  // Buttons and links marked data-link="discord" get their address from DYRHALD above.
  document.querySelectorAll("[data-link]").forEach(function (el) {
    var url = DYRHALD[el.getAttribute("data-link")];
    if (url) {
      el.setAttribute("href", url);
      if (el.getAttribute("data-link") === "discord") { el.setAttribute("target", "_blank"); el.setAttribute("rel", "noopener"); }
    } else {
      el.removeAttribute("href");
      el.classList.add("disabled");
      el.setAttribute("aria-disabled", "true");
      if (el.hasAttribute("data-soon")) el.textContent = el.getAttribute("data-soon");
    }
  });

  // Phone menu
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Mark the current page in the menu
  var here = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".nav a, .site-foot nav a").forEach(function (a) {
    if (a.getAttribute("href") === here) a.setAttribute("aria-current", "page");
  });

  // Screenshot viewer on the media page
  var box = document.querySelector(".lightbox");
  if (box) {
    var big = box.querySelector("img"), cap = box.querySelector("p"), close = box.querySelector("button"), last = null;
    document.querySelectorAll(".gallery a").forEach(function (a) {
      a.addEventListener("click", function (e) {
        e.preventDefault();
        last = a;
        big.src = a.getAttribute("href");
        big.alt = a.querySelector("img").alt;
        cap.textContent = a.querySelector("figcaption") ? a.querySelector("figcaption").textContent : "";
        box.classList.add("open");
        close.focus();
      });
    });
    function shut() { box.classList.remove("open"); big.src = ""; if (last) last.focus(); }
    close.addEventListener("click", shut);
    box.addEventListener("click", function (e) { if (e.target === box) shut(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && box.classList.contains("open")) shut(); });
  }

  // A few glowing motes drifting up, like plankton
  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var m = document.createElement("div");
    m.className = "motes";
    m.setAttribute("aria-hidden", "true");
    for (var i = 0; i < 18; i++) {
      var d = document.createElement("i");
      d.style.left = Math.random() * 100 + "%";
      d.style.animationDuration = 14 + Math.random() * 18 + "s";
      d.style.animationDelay = -Math.random() * 30 + "s";
      var s = 2 + Math.random() * 3;
      d.style.width = d.style.height = s + "px";
      m.appendChild(d);
    }
    document.body.appendChild(m);
  }
})();
