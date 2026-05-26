document.addEventListener("DOMContentLoaded", () => {
  const sections = Array.from(document.querySelectorAll("section")).filter((section) =>
    section.querySelector("h2")
  );

  if (sections.length === 0) {
    return;
  }

  const createSlug = (text) =>
    text
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "");

  sections.forEach((section) => {
    const heading = section.querySelector("h2");

    if (!section.id) {
      section.id = createSlug(heading.textContent);
    }
  });

  const nav = document.createElement("nav");
  nav.className = "dashboard-nav";
  nav.setAttribute("aria-label", "Navegação rápida do dashboard");

  const title = document.createElement("div");
  title.className = "dashboard-nav-title";
  title.textContent = "Navegação rápida";

  const list = document.createElement("div");
  list.className = "dashboard-nav-list";

  sections.forEach((section) => {
    const heading = section.querySelector("h2");

    const button = document.createElement("button");
    button.type = "button";
    button.className = "dashboard-nav-button";
    button.textContent = heading.textContent;
    button.dataset.target = section.id;

    button.addEventListener("click", () => {
      section.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    });

    list.appendChild(button);
  });

  nav.appendChild(title);
  nav.appendChild(list);

  const firstSection = document.querySelector("section");

  if (firstSection) {
    firstSection.parentNode.insertBefore(nav, firstSection);
  } else {
    document.body.prepend(nav);
  }

  const navButtons = Array.from(nav.querySelectorAll(".dashboard-nav-button"));

  const setActiveButton = (sectionId) => {
    navButtons.forEach((button) => {
      button.classList.toggle("active", button.dataset.target === sectionId);
    });
  };

  const observer = new IntersectionObserver(
    (entries) => {
      const visibleEntries = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio);

      if (visibleEntries.length > 0) {
        setActiveButton(visibleEntries[0].target.id);
      }
    },
    {
      root: null,
      threshold: [0.25, 0.5, 0.75],
    }
  );

  sections.forEach((section) => observer.observe(section));
});

// Predictive chart lightbox
(function () {
  const lightbox = document.getElementById("chartLightbox");
  const lightboxImage = document.getElementById("chartLightboxImage");
  const lightboxTitle = document.getElementById("chartLightboxTitle");

  if (!lightbox || !lightboxImage || !lightboxTitle) {
    return;
  }

  const closeButton = lightbox.querySelector(".chart-lightbox-close");
  const cards = document.querySelectorAll(".predictive-chart-card");

  function openLightbox(card) {
    const src = card.getAttribute("data-chart-src");
    const title = card.getAttribute("data-chart-title") || "Gráfico preditivo";

    if (!src) {
      return;
    }

    lightboxImage.setAttribute("src", src);
    lightboxImage.setAttribute("alt", title);
    lightboxTitle.textContent = title;
    lightbox.classList.add("is-open");
    lightbox.setAttribute("aria-hidden", "false");
    document.body.classList.add("chart-lightbox-open");
  }

  function closeLightbox() {
    lightbox.classList.remove("is-open");
    lightbox.setAttribute("aria-hidden", "true");
    document.body.classList.remove("chart-lightbox-open");
    lightboxImage.setAttribute("src", "");
    lightboxImage.setAttribute("alt", "");
    lightboxTitle.textContent = "";
  }

  cards.forEach((card) => {
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
    const target = event.target;
    if (target && target.getAttribute("data-chart-close") === "true") {
      closeLightbox();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && lightbox.classList.contains("is-open")) {
      closeLightbox();
    }
  });
})();
