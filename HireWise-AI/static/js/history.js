// ============================================================
// PREDICTION HISTORY
// SEARCH + FILTER + SORT
// ============================================================


// ============================================================
// ELEMENTS
// ============================================================

const historySearch =
    document.getElementById("historySearch");

const riskFilter =
    document.getElementById("riskFilter");

const probabilitySort =
    document.getElementById(
        "probabilitySort"
    );

const historyTable =
    document.querySelector(
        ".history-table"
    );

const historyBody =
    document.querySelector(
        ".history-table tbody"
    );

const visiblePredictionCount =
    document.getElementById(
        "visiblePredictionCount"
    );


// ============================================================
// STORE ORIGINAL ROW ORDER
// ============================================================

let historyRows = Array.from(
    document.querySelectorAll(
        ".history-table tbody tr"
    )
);


// ============================================================
// FILTER HISTORY
// ============================================================

function filterHistory() {

    const searchValue =
        historySearch.value
            .trim()
            .toLowerCase();


    const selectedRisk =
        riskFilter.value;


    let visibleRows = [];


    historyRows.forEach(
        function (row) {

            const jobRole =
                row.children[1]
                    .textContent
                    .trim()
                    .toLowerCase();


            const prediction =
                row.children[2]
                    .textContent
                    .trim()
                    .toLowerCase();


            // ------------------------------
            // SEARCH
            // ------------------------------

            const matchesSearch =
                jobRole.includes(
                    searchValue
                );


            // ------------------------------
            // RISK FILTER
            // ------------------------------

            let matchesRisk = true;


            if (
                selectedRisk === "high"
            ) {

                matchesRisk =
                    prediction.includes(
                        "high attrition risk"
                    );

            }


            if (
                selectedRisk === "low"
            ) {

                matchesRisk =
                    prediction.includes(
                        "low attrition risk"
                    );

            }


            // ------------------------------
            // FINAL FILTER
            // ------------------------------

            if (
                matchesSearch &&
                matchesRisk
            ) {

                row.style.display = "";

                visibleRows.push(
                    row
                );

            } else {

                row.style.display =
                    "none";

            }

        }
    );


    sortHistory(
        visibleRows
    );


    updateEmptyMessage(
        visibleRows.length
    );


    updateResultCount(
        visibleRows.length
    );

}


// ============================================================
// SORT HISTORY
// ============================================================

function sortHistory(
    visibleRows
) {

    const sortType =
        probabilitySort.value;


    // ----------------------------------------
    // NEWEST FIRST
    // ----------------------------------------

    if (
        sortType === "newest"
    ) {

        visibleRows.sort(
            function (a, b) {

                const dateA =
                    new Date(
                        a.children[0]
                            .textContent
                            .trim()
                    );

                const dateB =
                    new Date(
                        b.children[0]
                            .textContent
                            .trim()
                    );


                return dateB - dateA;

            }
        );

    }


    // ----------------------------------------
    // HIGHEST RISK
    // ----------------------------------------

    if (
        sortType === "highest"
    ) {

        visibleRows.sort(
            function (a, b) {

                const probabilityA =
                    parseFloat(
                        a.children[3]
                            .textContent
                            .replace(
                                "%",
                                ""
                            )
                            .trim()
                    );


                const probabilityB =
                    parseFloat(
                        b.children[3]
                            .textContent
                            .replace(
                                "%",
                                ""
                            )
                            .trim()
                    );


                return (
                    probabilityB -
                    probabilityA
                );

            }
        );

    }


    // ----------------------------------------
    // LOWEST RISK
    // ----------------------------------------

    if (
        sortType === "lowest"
    ) {

        visibleRows.sort(
            function (a, b) {

                const probabilityA =
                    parseFloat(
                        a.children[3]
                            .textContent
                            .replace(
                                "%",
                                ""
                            )
                            .trim()
                    );


                const probabilityB =
                    parseFloat(
                        b.children[3]
                            .textContent
                            .replace(
                                "%",
                                ""
                            )
                            .trim()
                    );


                return (
                    probabilityA -
                    probabilityB
                );

            }
        );

    }


    // ----------------------------------------
    // REBUILD TABLE
    // ----------------------------------------

    visibleRows.forEach(
        function (row) {

            historyBody.appendChild(
                row
            );

        }
    );

}


// ============================================================
// EMPTY RESULT MESSAGE
// ============================================================

function updateEmptyMessage(
    visibleRows
) {

    let message =
        document.getElementById(
            "historyEmptyMessage"
        );


    if (
        visibleRows === 0
    ) {

        if (!message) {

            message =
                document.createElement(
                    "div"
                );

            message.id =
                "historyEmptyMessage";

            message.className =
                "history-filter-empty";


            message.innerHTML = `
                <div class="filter-empty-icon">
                    No matches
                </div>

                <h3>
                    No predictions found
                </h3>

                <p>
                    Try changing the search term
                    or risk filter.
                </p>
            `;


            historyTable
                .parentElement
                .parentElement
                .appendChild(
                    message
                );

        }

    } else {

        if (message) {

            message.remove();

        }

    }

}

// ============================================================
// RESULT COUNT
// ============================================================

function updateResultCount(
    visibleRows
) {

    if (!visiblePredictionCount) {

        return;

    }


    visiblePredictionCount.textContent =
        visibleRows;

}

// ============================================================
// EVENT LISTENERS
// ============================================================

if (historySearch) {

    historySearch.addEventListener(
        "input",
        filterHistory
    );

}


if (riskFilter) {

    riskFilter.addEventListener(
        "change",
        filterHistory
    );

}


if (probabilitySort) {

    probabilitySort.addEventListener(
        "change",
        filterHistory
    );

}


// ============================================================
// INITIAL SORT
// ============================================================

filterHistory();