/**
 * Receitas da Família — UI interactions
 */
(function () {
  "use strict";

  function getCsrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta && meta.content) return meta.content;
    const input = document.querySelector("[name=csrfmiddlewaretoken]");
    if (input) return input.value;
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : "";
  }

  /* Mobile navigation */
  const navToggle = document.getElementById("navToggle");
  const mobileMenu = document.getElementById("mobileMenu");

  if (navToggle && mobileMenu) {
    navToggle.addEventListener("click", function () {
      const isOpen = mobileMenu.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });

    document.addEventListener("click", function (e) {
      if (
        mobileMenu.classList.contains("is-open") &&
        !mobileMenu.contains(e.target) &&
        !navToggle.contains(e.target)
      ) {
        mobileMenu.classList.remove("is-open");
        navToggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* Auto-dismiss alerts */
  document.querySelectorAll(".alert-app[data-auto-dismiss]").forEach(function (alert) {
    setTimeout(function () {
      alert.style.opacity = "0";
      alert.style.transform = "translateY(-8px)";
      alert.style.transition = "0.3s ease";
      setTimeout(function () {
        alert.remove();
      }, 300);
    }, 5000);
  });

  /* Favorite buttons (feed) */
  document.querySelectorAll(".btn-favoritar").forEach(function (btn) {
    btn.addEventListener("click", function () {
      const url = this.dataset.url;
      const button = this;
      const iconOn = button.dataset.iconOn || "♥";
      const iconOff = button.dataset.iconOff || "♡";

      fetch(url, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCsrfToken(),
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then(function (res) {
          return res.json();
        })
        .then(function (data) {
          if (data.favoritado) {
            button.textContent = iconOn;
            button.classList.add("is-favorited");
            button.dataset.favoritado = "true";
            button.setAttribute("aria-pressed", "true");
          } else {
            button.textContent = iconOff;
            button.classList.remove("is-favorited");
            button.dataset.favoritado = "false";
            button.setAttribute("aria-pressed", "false");
          }
        })
        .catch(function () {
          console.error("Erro ao favoritar receita.");
        });
    });
  });

  /* Avaliação por estrelas */
  var starGroup = document.getElementById("starRatingGroup");
  if (starGroup) {
    var hintEl = document.getElementById("starRatingHint");
    var previewEl = document.getElementById("starRatingPreview");
    var feedbackEl = document.getElementById("starRatingFeedback");
    var inputs = starGroup.querySelectorAll(".star-rating__input");
    var labels = starGroup.querySelectorAll(".star-rating__btn");

    var messages = {
      1: { title: "1 estrela", sub: "Não curti muito" },
      2: { title: "2 estrelas", sub: "Razoável" },
      3: { title: "3 estrelas", sub: "Bom!" },
      4: { title: "4 estrelas", sub: "Muito bom" },
      5: { title: "5 estrelas", sub: "Excelente!" },
    };

    var starPath =
      "M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z";

    function renderPreviewIcons(count) {
      if (!previewEl) return;
      var html = "";
      for (var i = 1; i <= 5; i++) {
        var cls = i <= count ? "on" : "off";
        html +=
          '<svg class="star-rating-feedback__svg ' +
          cls +
          '" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
          '<path fill="currentColor" d="' +
          starPath +
          '"/></svg>';
      }
      previewEl.innerHTML = html;
    }

    function showFeedback(value, isHover) {
      if (!hintEl || !feedbackEl) return;
      if (!value) {
        feedbackEl.classList.remove("is-active");
        starGroup.classList.remove("is-preview");
        labels.forEach(function (l) {
          l.classList.remove("is-lit");
        });
        var selected = 0;
        inputs.forEach(function (inp) {
          if (inp.checked) selected = parseInt(inp.value, 10);
        });
        if (selected) {
          showFeedback(selected, false);
        } else {
          hintEl.innerHTML = "Passe o mouse ou clique para avaliar";
          if (previewEl) previewEl.innerHTML = "";
        }
        return;
      }
      var msg = messages[value];
      feedbackEl.classList.add("is-active");
      hintEl.innerHTML =
        msg.title + '<em>' + msg.sub + "</em>";
      renderPreviewIcons(value);
      if (isHover) {
        starGroup.classList.add("is-preview");
        labels.forEach(function (l) {
          var n = parseInt(l.dataset.star, 10);
          l.classList.toggle("is-lit", n <= value);
        });
      } else {
        starGroup.classList.remove("is-preview");
        labels.forEach(function (l) {
          l.classList.remove("is-lit");
        });
      }
    }

    labels.forEach(function (label) {
      var value = parseInt(label.dataset.star, 10);
      label.addEventListener("mouseenter", function () {
        showFeedback(value, true);
      });
    });

    starGroup.addEventListener("mouseleave", function () {
      showFeedback(0, false);
    });

    inputs.forEach(function (inp) {
      inp.addEventListener("change", function () {
        showFeedback(parseInt(inp.value, 10), false);
      });
    });

    var initial = 0;
    inputs.forEach(function (inp) {
      if (inp.checked) initial = parseInt(inp.value, 10);
    });
    if (initial) showFeedback(initial, false);
  }

  /* Confirm destructive actions (links e formulários) */
  document.querySelectorAll("[data-confirm]").forEach(function (el) {
    if (el.tagName === "FORM") {
      el.addEventListener("submit", function (e) {
        const msg = this.dataset.confirm || "Tem certeza?";
        if (!window.confirm(msg)) {
          e.preventDefault();
        }
      });
      return;
    }
    el.addEventListener("click", function (e) {
      const msg = this.dataset.confirm || "Tem certeza?";
      if (!window.confirm(msg)) {
        e.preventDefault();
      }
    });
  });
})();
