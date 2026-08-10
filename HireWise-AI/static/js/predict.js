const candidateForm = document.getElementById("candidate-form");


if (candidateForm) {

    candidateForm.addEventListener(
        "submit",
        function (event) {

            const age =
                Number(
                    document.getElementById("age").value
                );


            const monthlyIncome =
                Number(
                    document.getElementById(
                        "monthly-income"
                    ).value
                );


            const companiesWorked =
                Number(
                    document.getElementById(
                        "num-companies-worked"
                    ).value
                );


            // -----------------------------
            // Age validation
            // -----------------------------

            if (age < 18 || age > 70) {

                event.preventDefault();

                alert(
                    "Age must be between 18 and 70."
                );

                return;
            }


            // -----------------------------
            // Monthly income validation
            // -----------------------------

            if (monthlyIncome < 100) {

                event.preventDefault();

                alert(
                    "Please enter a valid monthly income."
                );

                return;
            }


            // -----------------------------
            // Previous companies validation
            // -----------------------------

            if (
                companiesWorked < 0 ||
                companiesWorked > 20
            ) {

                event.preventDefault();

                alert(
                    "Previous companies worked must be between 0 and 20."
                );

                return;
            }

        }
    );

}