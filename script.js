const menuToggle = document.getElementById("menuToggle");
const navMenu = document.getElementById("navMenu");

// Defensive checks in case elements are missing
if (menuToggle && navMenu) {
  const setMenuState = (open) => {
    menuToggle.setAttribute("aria-expanded", open ? "true" : "false");
    navMenu.setAttribute("aria-hidden", open ? "false" : "true");
    if (open) navMenu.classList.add("active");
    else navMenu.classList.remove("active");
  };

  menuToggle.addEventListener("click", () => {
    const isOpen = navMenu.classList.toggle("active");
    setMenuState(isOpen);
  });

  document.querySelectorAll("#navMenu a").forEach((link) => {
    link.addEventListener("click", () => {
      setMenuState(false);
    });
  });

  // Close menu with Escape key for keyboard users
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" || e.key === "Esc") {
      setMenuState(false);
    }
  });

  // Ensure initial ARIA state matches visual state
  setMenuState(navMenu.classList.contains("active"));
}

// Update year in footer if the element exists
const yearEl = document.getElementById("year");
if (yearEl) yearEl.textContent = new Date().getFullYear();

// Intersection observer for reveal animations
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1";
        entry.target.style.transform = "translateY(0)";
      }
    });
  },
  {
    threshold: 0.15
  }
);

// Elements to observe
const revealElements = document.querySelectorAll(
  ".feature-card, .about-image, .about-content, .cta-inner"
);

revealElements.forEach((element) => {
  element.style.opacity = "0";
  element.style.transform = "translateY(25px)";
  element.style.transition = "opacity 0.8s ease, transform 0.8s ease";

  observer.observe(element);
});
