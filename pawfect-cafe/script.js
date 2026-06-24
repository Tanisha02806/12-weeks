// =========================
// MOBILE NAVBAR TOGGLE
// =========================
const menuToggle = document.getElementById("menuToggle");
const navWrapper = document.getElementById("navWrapper");

if (menuToggle && navWrapper) {
  menuToggle.addEventListener("click", () => {
    menuToggle.classList.toggle("active");
    navWrapper.classList.toggle("show");
  });

  // close menu when clicking any nav link
  const navLinks = navWrapper.querySelectorAll("a");
  navLinks.forEach(link => {
    link.addEventListener("click", () => {
      menuToggle.classList.remove("active");
      navWrapper.classList.remove("show");
    });
  });
}

// =========================
// FAKE FORM SUBMIT FOR UI DEMO
// =========================
const reservationForm = document.querySelector(".reservation-form");

if (reservationForm) {
  reservationForm.addEventListener("submit", function (e) {
    e.preventDefault();

    alert("Your reservation request has been sent to Pawfect Café! 🐾☕");
    reservationForm.reset();
  });
}