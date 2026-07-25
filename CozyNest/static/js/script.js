// =============================
// Auto Scroll to Prediction Result
// =============================

window.onload = function () {

    const result = document.querySelector(".result-card");

    if (result) {

        result.scrollIntoView({

            behavior: "smooth"

        });

    }

};


// =============================
// Loading Animation
// =============================

const form = document.getElementById("predictionForm");

if (form) {

    form.addEventListener("submit", function () {

        const button = document.getElementById("predictButton");

        const text = document.getElementById("buttonText");

        const spinner = document.getElementById("loadingSpinner");

        button.disabled = true;

        text.textContent = "Predicting...";

        spinner.style.display = "inline-block";

    });

}

// =============================
// Scroll Reveal Animation
// =============================

const revealElements = document.querySelectorAll(".reveal");

function revealOnScroll() {

    revealElements.forEach(element => {

        const windowHeight = window.innerHeight;

        const elementTop = element.getBoundingClientRect().top;

        if (elementTop < windowHeight - 100) {

            element.classList.add("active");

        }

    });

}

window.addEventListener("scroll", revealOnScroll);

revealOnScroll();