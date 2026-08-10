// ============================================================
// HIREWISE ANALYTICS
// ============================================================


// ============================================================
// PREDICTION DISTRIBUTION DATA
// ============================================================

const predictionChartData =
    {{ prediction_chart_data | tojson }};


// ============================================================
// GET CHART ELEMENT
// ============================================================

const predictionChartElement =
    document.getElementById(
        "predictionChart"
    );

showEmptyChartMessage(
    predictionChartElement,
    predictionChartData.values.some(
        function (value) {
            return value > 0;
        }
    )
);


// ============================================================
// CREATE PREDICTION CHART
// ============================================================

if (predictionChartElement) {

    // ============================================================
    // PREDICTION DISTRIBUTION CHART
    // ============================================================

    const predictionChartData =
        {{ prediction_chart_data | tojson }};


    const predictionChartElement =
        document.getElementById(
            "predictionChart"
        );


    if (predictionChartElement) {

        const predictionTotal =
            predictionChartData.values.reduce(
                function (total, value) {

                    return total + value;

                },
                0
            );


        new Chart(
            predictionChartElement,
            {

                type: "doughnut",

                data: {

                    labels:
                        predictionChartData.labels,

                    datasets: [

                        {

                            data:
                                predictionChartData.values,

                            borderWidth: 0

                        }

                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    cutout: "65%",

                    plugins: {

                        legend: {

                            position: "bottom",

                            labels: {

                                padding: 18,

                                usePointStyle: true

                            }

                        },

                        tooltip: {

                            callbacks: {

                                label:
                                    function (
                                        context
                                    ) {

                                        const value =
                                            context.raw;


                                        let percentage =
                                            0;


                                        if (
                                            predictionTotal > 0
                                        ) {

                                            percentage =
                                                (
                                                    value /
                                                    predictionTotal
                                                ) * 100;

                                        }


                                        return (
                                            context.label +
                                            ": " +
                                            value +
                                            " (" +
                                            percentage.toFixed(
                                                1
                                            ) +
                                            "%)"
                                        );

                                    }

                            }

                        }

                    }

                }

            }
        );

    }

}

// ============================================================
// PROBABILITY DISTRIBUTION
// ============================================================

const probabilityChartData =
    {{ probability_distribution_data | tojson }};


const probabilityChartElement =
    document.getElementById(
        "probabilityChart"
    );

showEmptyChartMessage(
    probabilityChartElement,
    probabilityChartData.values.some(
        function (value) {
            return value > 0;
        }
    )
);


if (probabilityChartElement) {

    // ============================================================
    // PROBABILITY DISTRIBUTION CHART
    // ============================================================

    const probabilityChartData =
        {{ probability_distribution_data | tojson }};


    const probabilityChartElement =
        document.getElementById(
            "probabilityChart"
        );


    if (probabilityChartElement) {

        new Chart(
            probabilityChartElement,
            {

                type: "bar",

                data: {

                    labels:
                        probabilityChartData.labels,

                    datasets: [

                        {

                            label:
                                "Predictions",

                            data:
                                probabilityChartData.values,

                            borderWidth: 0,

                            borderRadius: 6

                        }

                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    scales: {

                        x: {

                            title: {

                                display: true,

                                text:
                                    "Attrition Probability"

                            }

                        },

                        y: {

                            beginAtZero: true,

                            ticks: {

                                precision: 0

                            },

                            title: {

                                display: true,

                                text:
                                    "Number of Predictions"

                            }

                        }

                    },

                    plugins: {

                        legend: {

                            display: false

                        },

                        tooltip: {

                            callbacks: {

                                label:
                                    function (
                                        context
                                    ) {

                                        return (
                                            "Predictions: " +
                                            context.raw
                                        );

                                    }

                            }

                        }

                    }

                }

            }
        );

    }
}

// ============================================================
// EMPTY ANALYTICS MESSAGE
// ============================================================

function showEmptyChartMessage(
    chartElement,
    hasData
) {

    if (!chartElement) {

        return;

    }


    if (hasData) {

        return;

    }


    const container =
        chartElement.parentElement;


    container.innerHTML = `
        <div class="analytics-empty-chart">
            <strong>
                No prediction data yet
            </strong>

            <span>
                Create a prediction to see analytics.
            </span>
        </div>
    `;

}

// ============================================================
// FEATURE IMPORTANCE
// ============================================================

const featureImportanceData =
    {{ feature_importance_data | tojson }};


// ============================================================
// FEATURE IMPORTANCE CHART ELEMENT
// ============================================================

const featureImportanceChartElement =
    document.getElementById(
        "featureImportanceChart"
    );


// ============================================================
// CREATE FEATURE IMPORTANCE CHART
// ============================================================

if (
    featureImportanceChartElement &&
    featureImportanceData.length > 0
) {

    new Chart(
        featureImportanceChartElement,
        {

            type: "bar",

            data: {

                labels:
                    featureImportanceData.map(
                        function (item) {

                            return item.feature;

                        }
                    ),

                datasets: [

                    {

                        labels:
                            featureImportanceData.map(
                                function (item) {

                                    const feature =
                                        item.feature;


                                    if (
                                        feature.length > 24
                                    ) {

                                        return (
                                            feature.substring(
                                                0,
                                                21
                                            ) + "..."
                                        );

                                    }


                                    return feature;

                                }
                            ),

                        borderWidth: 0,

                        borderRadius: 6

                    }

                ]

            },

            options: {

                indexAxis: "y",

                responsive: true,

                maintainAspectRatio: false,

                scales: {

                    x: {

                        beginAtZero: true,

                        title: {

                            display: true,

                            text:
                                "Importance (%)"

                        },

                        ticks: {

                            callback:
                                function (value) {

                                    return (
                                        value + "%"
                                    );

                                }

                        }

                    },

                    y: {

                        ticks: {

                            autoSkip: false,

                            font: {

                                size: 11

                            },

                            padding: 8

                        }

                    }

                },

                plugins: {

                    legend: {

                        display: false

                    },

                    tooltip: {

                        callbacks: {

                            title:
                                function (
                                    tooltipItems
                                ) {

                                    const index =
                                        tooltipItems[0]
                                            .dataIndex;


                                    return (
                                        featureImportanceData[
                                            index
                                        ].feature
                                    );

                                },


                            label:
                                function (
                                    context
                                ) {

                                    const index =
                                        context.dataIndex;


                                    const importance =
                                        featureImportanceData[
                                            index
                                        ].importance;


                                    return (
                                        "Importance: " +
                                        (
                                            importance *
                                            100
                                        ).toFixed(2) +
                                        "%"
                                    );

                                }

                        }

                    }

                }

            }

        }
    );

}