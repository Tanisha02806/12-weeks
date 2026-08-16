/*
 * HireWise AI — Prediction Form Validation
 * 5.11.4
 */

const candidateForm =
    document.getElementById("candidate-form");


if (candidateForm) {

    const ageInput =
        document.getElementById("age");

    const monthlyIncomeInput =
        document.getElementById(
            "monthly-income"
        );

    const companiesWorkedInput =
        document.getElementById(
            "num-companies-worked"
        );


    // ========================================================
    // VALIDATION HELPERS
    // ========================================================

    function clearFieldError(input) {

        if (!input) {
            return;
        }

        input.classList.remove(
            "input-error"
        );

        input.removeAttribute(
            "aria-invalid"
        );

        const error =
            input.parentElement.querySelector(
                ".field-error"
            );

        if (error) {
            error.remove();
        }
    }


    function showFieldError(
        input,
        message
    ) {

        if (!input) {
            return;
        }

        clearFieldError(input);

        input.classList.add(
            "input-error"
        );

        input.setAttribute(
            "aria-invalid",
            "true"
        );

        const error =
            document.createElement(
                "small"
            );

        error.className =
            "field-error";

        error.textContent =
            message;

        input.parentElement.appendChild(
            error
        );
    }


    function clearAllErrors() {

        candidateForm
            .querySelectorAll(
                ".field-error"
            )
            .forEach(
                error => error.remove()
            );

        candidateForm
            .querySelectorAll(
                ".input-error"
            )
            .forEach(
                input => {

                    input.classList.remove(
                        "input-error"
                    );

                    input.removeAttribute(
                        "aria-invalid"
                    );

                }
            );

        const formError =
            candidateForm.querySelector(
                ".form-error"
            );

        if (formError) {
            formError.remove();
        }
    }


    function showFormError(
        message
    ) {

        const error =
            document.createElement(
                "div"
            );

        error.className =
            "form-error";

        error.setAttribute(
            "role",
            "alert"
        );

        error.textContent =
            message;

        candidateForm.prepend(
            error
        );
    }


    // ========================================================
    // FORM VALIDATION
    // ========================================================

    function validateForm() {

        clearAllErrors();

        let isValid = true;

        let firstInvalidField = null;


        // ----------------------------------------------------
        // AGE
        // ----------------------------------------------------

        if (
            ageInput.value.trim() === ""
        ) {

            showFieldError(
                ageInput,
                "Age is required."
            );

            isValid = false;

            firstInvalidField =
                firstInvalidField ||
                ageInput;

        }

        else {

            const age =
                Number(
                    ageInput.value
                );


            if (
                !Number.isFinite(age) ||
                age < 18 ||
                age > 70
            ) {

                showFieldError(
                    ageInput,
                    "Age must be between 18 and 70."
                );

                isValid = false;

                firstInvalidField =
                    firstInvalidField ||
                    ageInput;
            }
        }


        // ----------------------------------------------------
        // MONTHLY INCOME
        // ----------------------------------------------------

        if (
            monthlyIncomeInput.value.trim() === ""
        ) {

            showFieldError(
                monthlyIncomeInput,
                "Monthly income is required."
            );

            isValid = false;

            firstInvalidField =
                firstInvalidField ||
                monthlyIncomeInput;

        }

        else {

            const monthlyIncome =
                Number(
                    monthlyIncomeInput.value
                );


            if (
                !Number.isFinite(
                    monthlyIncome
                ) ||
                monthlyIncome < 100
            ) {

                showFieldError(
                    monthlyIncomeInput,
                    "Monthly income must be at least 100."
                );

                isValid = false;

                firstInvalidField =
                    firstInvalidField ||
                    monthlyIncomeInput;
            }
        }


        // ----------------------------------------------------
        // PREVIOUS COMPANIES
        // ----------------------------------------------------

        if (
            companiesWorkedInput.value.trim() === ""
        ) {

            showFieldError(
                companiesWorkedInput,
                "Previous companies worked is required."
            );

            isValid = false;

            firstInvalidField =
                firstInvalidField ||
                companiesWorkedInput;

        }

        else {

            const companiesWorked =
                Number(
                    companiesWorkedInput.value
                );


            if (
                !Number.isInteger(
                    companiesWorked
                ) ||
                companiesWorked < 0 ||
                companiesWorked > 20
            ) {

                showFieldError(
                    companiesWorkedInput,
                    "Previous companies worked must be between 0 and 20."
                );

                isValid = false;

                firstInvalidField =
                    firstInvalidField ||
                    companiesWorkedInput;
            }
        }


        // ----------------------------------------------------
        // REQUIRED SELECTS
        // ----------------------------------------------------

        const requiredSelects =
            candidateForm.querySelectorAll(
                "select[required]"
            );


        requiredSelects.forEach(
            select => {

                if (
                    select.value.trim() === ""
                ) {

                    showFieldError(
                        select,
                        "Please select an option."
                    );

                    isValid = false;

                    firstInvalidField =
                        firstInvalidField ||
                        select;
                }

            }
        );


        // ----------------------------------------------------
        // SHOW FORM ERROR
        // ----------------------------------------------------

        if (!isValid) {

            showFormError(
                "Please correct the highlighted fields before continuing."
            );


            if (firstInvalidField) {

                firstInvalidField.focus();

                firstInvalidField.scrollIntoView({
                    behavior: "smooth",
                    block: "center"
                });

            }

        }


        return isValid;
    }


    // ========================================================
    // CLEAR ERRORS WHEN USER CORRECTS INPUT
    // ========================================================

    candidateForm
        .querySelectorAll(
            "input, select"
        )
        .forEach(
            field => {

                field.addEventListener(
                    "input",
                    function () {

                        clearFieldError(
                            this
                        );

                    }
                );


                field.addEventListener(
                    "change",
                    function () {

                        clearFieldError(
                            this
                        );

                    }
                );

            }
        );


    // ========================================================
    // FORM SUBMISSION
    // ========================================================

    candidateForm.addEventListener(
        "submit",
        function (event) {

            if (
                !validateForm()
            ) {

                event.preventDefault();

                return;
            }


            // ------------------------------------------------
            // LOADING STATE
            // ------------------------------------------------

            const submitButton =
                candidateForm.querySelector(
                    'button[type="submit"]'
                );


            if (submitButton) {

                // Prevent double submission.
                submitButton.disabled =
                    true;


                // Add loading styling.
                submitButton.classList.add(
                    "is-loading"
                );


                // Save original button text.
                submitButton.dataset.originalText =
                    submitButton.textContent.trim();


                // Show spinner + loading text.
                submitButton.innerHTML =
                    '<span class="submit-spinner" aria-hidden="true"></span>' +
                    '<span>Analyzing...</span>';


                // Accessibility state.
                submitButton.setAttribute(
                    "aria-busy",
                    "true"
                );


                candidateForm.classList.add(
                    "form-submitting"
                );

            }

        }
    );

}


/*
 * ============================================================
 * RESTORE BUTTON AFTER BROWSER BACK/FORWARD
 * ============================================================
 */

window.addEventListener(
    "pageshow",
    function () {

        const form =
            document.getElementById(
                "candidate-form"
            );


        if (!form) {
            return;
        }


        const submitButton =
            form.querySelector(
                'button[type="submit"]'
            );


        if (submitButton) {

            submitButton.disabled =
                false;


            submitButton.classList.remove(
                "is-loading"
            );


            submitButton.removeAttribute(
                "aria-busy"
            );


            const originalText =
                submitButton.dataset.originalText;


            if (originalText) {

                submitButton.textContent =
                    originalText;

            }

        }


        form.classList.remove(
            "form-submitting"
        );

    }
);