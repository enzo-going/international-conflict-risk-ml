document.addEventListener("DOMContentLoaded", () => {
  const sections = Array.from(document.querySelectorAll("main section[id]"));
  const navLinks = Array.from(document.querySelectorAll(".topbar a[href^='#']"));

  if ("IntersectionObserver" in window && sections.length > 0) {
    const observer = new IntersectionObserver(
      (entries) => {
        const active = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

        if (!active) {
          return;
        }

        navLinks.forEach((link) => {
          link.classList.toggle("is-active", link.getAttribute("href") === `#${active.target.id}`);
        });
      },
      { threshold: [0.28, 0.5, 0.75] }
    );

    sections.forEach((section) => observer.observe(section));
  }

  const lightbox = document.getElementById("chartLightbox");
  const lightboxImage = document.getElementById("chartLightboxImage");
  const lightboxTitle = document.getElementById("chartLightboxTitle");
  const closeButton = lightbox ? lightbox.querySelector(".chart-lightbox-close") : null;
  const chartCards = Array.from(document.querySelectorAll("[data-chart-src]"));

  if (!lightbox || !lightboxImage || !lightboxTitle || chartCards.length === 0) {
    return;
  }

  function openLightbox(card) {
    const src = card.getAttribute("data-chart-src");
    const title = card.getAttribute("data-chart-title") || "Gráfico preditivo";

    if (!src) {
      return;
    }

    lightboxImage.src = src;
    lightboxImage.alt = title;
    lightboxTitle.textContent = title;
    lightbox.classList.add("is-open");
    lightbox.setAttribute("aria-hidden", "false");
    document.body.classList.add("chart-lightbox-open");
  }

  function closeLightbox() {
    lightbox.classList.remove("is-open");
    lightbox.setAttribute("aria-hidden", "true");
    document.body.classList.remove("chart-lightbox-open");
    lightboxImage.removeAttribute("src");
    lightboxImage.alt = "";
    lightboxTitle.textContent = "";
  }

  chartCards.forEach((card) => {
    card.tabIndex = 0;
    card.addEventListener("click", () => openLightbox(card));
    card.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        openLightbox(card);
      }
    });
  });

  if (closeButton) {
    closeButton.addEventListener("click", closeLightbox);
  }

  lightbox.addEventListener("click", (event) => {
    if (event.target && event.target.getAttribute("data-chart-close") === "true") {
      closeLightbox();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && lightbox.classList.contains("is-open")) {
      closeLightbox();
    }
  });
});
