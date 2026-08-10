import json
import os
from datetime import datetime

import joblib
import pandas as pd

from flask import Flask, render_template, request

# ============================================================
# DATASET STATISTICS
# ============================================================

def get_dataset_statistics():

    if dataset.empty:

        return {

            "total_records": 0,

            "attrition_count": 0,

            "attrition_rate": 0,

            "average_age": 0,

            "average_income": 0

        }


    total_records = len(
        dataset
    )


    attrition_count = (
        dataset["attrition"]
        .eq("Yes")
        .sum()
    )


    attrition_rate = (
        attrition_count /
        total_records
    ) * 100


    average_age = (
        dataset["age"]
        .mean()
    )


    average_income = (
        dataset["monthly_income"]
        .mean()
    )


    return {

        "total_records":
            total_records,

        "attrition_count":
            int(attrition_count),

        "attrition_rate":
            round(
                attrition_rate,
                2
            ),

        "average_age":
            round(
                average_age,
                1
            ),

        "average_income":
            round(
                average_income,
                2
            )

    }
    
# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)


# ============================================================
# FILE PATHS
# ============================================================

MODEL_PATH = "model/hirewise_model.pkl"

PREPROCESSOR_PATH = "model/preprocessor.pkl"

FEATURE_IMPORTANCE_PATH = "model/feature_importance.pkl"

MODEL_INFO_PATH = "model/model_info.pkl"

HISTORY_PATH = "data/prediction_history.json"

DATASET_PATH = "dataset/WA_Fn-UseC_-HR-Employee-Attrition.csv"

# ============================================================
# LOAD TRAINED MODEL
# ============================================================

try:

    model = joblib.load(
        MODEL_PATH
    )

    print("✓ Trained model loaded successfully.")

except Exception as e:

    print(
        "\nERROR: Could not load trained model."
    )

    print(e)

    model = None


# ============================================================
# LOAD PREPROCESSOR
# ============================================================

try:

    preprocessor = joblib.load(
        PREPROCESSOR_PATH
    )

    print("✓ Preprocessor loaded successfully.")

except Exception as e:

    print(
        "\nERROR: Could not load preprocessor."
    )

    print(e)

    preprocessor = None


# ============================================================
# LOAD FEATURE IMPORTANCE
# ============================================================

try:

    feature_importance = joblib.load(
        FEATURE_IMPORTANCE_PATH
    )

    print(
        "✓ Feature importance loaded successfully."
    )

    print(
        "Feature importance type:",
        type(feature_importance)
    )

    print(
        "Feature importance value:"
    )

    print(
        feature_importance
    )

except Exception as e:

    print(
        "WARNING: Could not load feature importance."
    )

    print(e)

    feature_importance = None
    
# ============================================================
# PREPARE FEATURE IMPORTANCE FOR ANALYTICS
# ============================================================

def get_feature_importance_data():

    if feature_importance is None:

        return []


    records = []


    # --------------------------------------------------------
    # CASE 1: DICTIONARY
    # --------------------------------------------------------

    if isinstance(
        feature_importance,
        dict
    ):

        for feature, importance in (
            feature_importance.items()
        ):

            try:

                importance_value = float(
                    importance
                )

            except (
                TypeError,
                ValueError
            ):

                continue


            records.append({

                "feature":
                    str(feature),

                "importance":
                    importance_value

            })


    # --------------------------------------------------------
    # CASE 2: LIST
    # --------------------------------------------------------

    elif isinstance(
        feature_importance,
        list
    ):

        for item in feature_importance:

            # --------------------------------------------
            # LIST OF DICTIONARIES
            # --------------------------------------------

            if isinstance(
                item,
                dict
            ):

                feature_name = (
                    item.get("feature")
                    or item.get("name")
                )

                importance_value = (
                    item.get("importance")
                )


                if (
                    feature_name is None
                    or importance_value is None
                ):

                    continue


                try:

                    importance_value = float(
                        importance_value
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    continue


                records.append({

                    "feature":
                        str(feature_name),

                    "importance":
                        importance_value

                })


            # --------------------------------------------
            # LIST OF TUPLES / LISTS
            # --------------------------------------------

            elif isinstance(
                item,
                (
                    tuple,
                    list
                )
            ):

                if len(item) < 2:

                    continue


                feature_name = item[0]

                importance_value = item[1]


                try:

                    importance_value = float(
                        importance_value
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    continue


                records.append({

                    "feature":
                        str(feature_name),

                    "importance":
                        importance_value

                })


    # --------------------------------------------------------
    # SORT HIGHEST → LOWEST
    # --------------------------------------------------------

    records.sort(

        key=lambda item:
            item["importance"],

        reverse=True

    )


    # --------------------------------------------------------
    # KEEP TOP FEATURES
    # --------------------------------------------------------

    records = records[:10]


    return records

# ============================================================
# CONVERT FEATURE IMPORTANCE TO RECORDS
# ============================================================

feature_importance_records = (
    feature_importance.to_dict(
        orient="records"
    )
)


# ============================================================
# CLEAN FEATURE NAMES
# ============================================================

for item in feature_importance_records:

    feature_name = item.get(
        "Display Feature",
        "Unknown Feature"
    )

    feature_name = str(
        feature_name
    )

    # Remove preprocessing prefixes

    feature_name = feature_name.replace(
        "num__",
        ""
    )

    feature_name = feature_name.replace(
        "cat__",
        ""
    )

    # Replace underscores

    feature_name = feature_name.replace(
        "_",
        " "
    )

    # Make readable

    item["Display Feature"] = (
        feature_name.title()
    )


print(
    "\n--- FEATURE IMPORTANCE LOADED ---"
)

print(
    feature_importance_records
)


# ============================================================
# LOAD MODEL INFORMATION
# ============================================================

try:

    model_info = joblib.load(
        MODEL_INFO_PATH
    )

    print(
        "✓ Model information loaded successfully."
    )

    print(
        "Model information type:",
        type(model_info)
    )
    
    print(
        "Model information:"
    )
    
    print(
        model_info
    )

except Exception as e:

    print(
        "WARNING: Could not load model information."
    )

    print(e)

    model_info = {}
    
# ============================================================
# PREPARE MODEL EVALUATION METRICS
# ============================================================

def get_model_metrics():

    if not model_info:

        return {

            "model_name":
                "Unavailable",

            "accuracy":
                0,

            "precision":
                0,

            "recall":
                0,

            "f1_score":
                0

        }


    # --------------------------------------------------------
    # MODEL NAME
    # --------------------------------------------------------

    model_name = (

        model_info.get(
            "model_name"
        )

        or

        model_info.get(
            "selected_model"
        )

        or

        model_info.get(
            "best_model"
        )

        or

        "Random Forest"

    )


    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    metrics = (
        model_info.get(
            "metrics",
            {}
        )
    )


    # --------------------------------------------------------
    # GET INDIVIDUAL VALUES
    # --------------------------------------------------------

    accuracy = (

        metrics.get(
            "accuracy"
        )

        if metrics

        else model_info.get(
            "accuracy",
            0
        )

    )


    precision = (

        metrics.get(
            "precision"
        )

        if metrics

        else model_info.get(
            "precision",
            0
        )

    )


    recall = (

        metrics.get(
            "recall"
        )

        if metrics

        else model_info.get(
            "recall",
            0
        )

    )


    f1_score = (

        metrics.get(
            "f1_score"
        )

        or

        metrics.get(
            "f1"
        )

        if metrics

        else (

            model_info.get(
                "f1_score"
            )

            or

            model_info.get(
                "f1",
                0
            )

        )

    )


    # --------------------------------------------------------
    # CONVERT TO PERCENTAGES
    # --------------------------------------------------------

    def to_percentage(
        value
    ):

        try:

            value = float(
                value
            )

        except (
            TypeError,
            ValueError
        ):

            return 0


        # Metrics such as 0.84
        # become 84%.

        if value <= 1:

            value *= 100


        return round(
            value,
            2
        )


    return {

        "model_name":
            str(
                model_name
            ),

        "accuracy":
            to_percentage(
                accuracy
            ),

        "precision":
            to_percentage(
                precision
            ),

        "recall":
            to_percentage(
                recall
            ),

        "f1_score":
            to_percentage(
                f1_score
            )

    }
    
# ============================================================
# PREDICTION HISTORY
# ============================================================

def load_prediction_history():

    """
    Load prediction history from JSON.

    Returns an empty list if the file does not
    exist or cannot be read.
    """

    if not os.path.exists(
        HISTORY_PATH
    ):

        return []


    try:

        with open(
            HISTORY_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            history = json.load(
                file
            )


        # Make sure the JSON contains a list

        if not isinstance(
            history,
            list
        ):

            return []


        return history


    except (
        json.JSONDecodeError,
        OSError
    ):

        return []


# ============================================================
# SAVE PREDICTION HISTORY
# ============================================================

def save_prediction_history(
    history
):

    """
    Save prediction history to JSON.
    """

    # Make sure data directory exists

    os.makedirs(
        os.path.dirname(
            HISTORY_PATH
        ),
        exist_ok=True
    )


    with open(
        HISTORY_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=4
        )


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# PREDICTION PAGE
# ============================================================

@app.route(
    "/predict",
    methods=[
        "GET",
        "POST"
    ]
)
def predict():


    # ========================================================
    # GET REQUEST
    # ========================================================

    if request.method == "GET":

        return render_template(
            "predict.html"
        )


    # ========================================================
    # POST REQUEST
    # ========================================================

    try:

        # ====================================================
        # CHECK ML COMPONENTS
        # ====================================================

        if model is None:

            raise RuntimeError(
                "Trained model could not be loaded."
            )


        if preprocessor is None:

            raise RuntimeError(
                "Preprocessor could not be loaded."
            )


        # ====================================================
        # 1. GET FORM VALUES
        # ====================================================

        age = int(
            request.form[
                "age"
            ]
        )


        business_travel = request.form[
            "business_travel"
        ]


        job_role = request.form[
            "job_role"
        ]


        job_satisfaction = request.form[
            "job_satisfaction"
        ]


        monthly_income = float(
            request.form[
                "monthly_income"
            ]
        )


        num_companies_worked = int(
            request.form[
                "num_companies_worked"
            ]
        )


        over_time = request.form[
            "over_time"
        ]


        environment_satisfaction = request.form[
            "environment_satisfaction"
        ]


        work_life_balance = request.form[
            "work_life_balance"
        ]


        # ====================================================
        # 2. BASIC SERVER-SIDE VALIDATION
        # ====================================================

        if age < 18 or age > 70:

            raise ValueError(
                "Age must be between 18 and 70."
            )


        if monthly_income < 100:

            raise ValueError(
                "Monthly income must be at least 100."
            )


        if (
            num_companies_worked < 0
            or num_companies_worked > 20
        ):

            raise ValueError(
                "Number of companies worked must be between 0 and 20."
            )


        # ====================================================
        # 3. CREATE DATAFRAME
        # ====================================================

        employee_data = pd.DataFrame({

            "age": [
                age
            ],

            "business_travel": [
                business_travel
            ],

            "job_role": [
                job_role
            ],

            "job_satisfaction": [
                job_satisfaction
            ],

            "monthly_income": [
                monthly_income
            ],

            "num_companies_worked": [
                num_companies_worked
            ],

            "over_time": [
                over_time
            ],

            "environment_satisfaction": [
                environment_satisfaction
            ],

            "work_life_balance": [
                work_life_balance
            ]

        })


        # ====================================================
        # 4. PREPROCESS INPUT
        # ====================================================

        processed_data = (
            preprocessor.transform(
                employee_data
            )
        )


        # ====================================================
        # 5. MAKE PREDICTION
        # ====================================================

        prediction = model.predict(
            processed_data
        )


        # ====================================================
        # 6. GET PROBABILITY
        # ====================================================

        probabilities = (
            model.predict_proba(
                processed_data
            )
        )


        # Probability of class 1 = Attrition

        attrition_probability = (
            probabilities[0][1] * 100
        )


        # ====================================================
        # 7. DETERMINE RISK LEVEL
        # ====================================================

        if prediction[0] == 1:

            result = (
                "High Attrition Risk"
            )

            result_class = (
                "high-risk"
            )

        else:

            result = (
                "Low Attrition Risk"
            )

            result_class = (
                "low-risk"
            )


        # ====================================================
        # 8. RISK INTERPRETATION
        # ====================================================

        if attrition_probability >= 70:

            risk_message = (
                "The model estimates a high probability "
                "of employee attrition based on the "
                "submitted characteristics."
            )


        elif attrition_probability >= 40:

            risk_message = (
                "The model estimates a moderate probability "
                "of employee attrition. The result should "
                "be reviewed alongside other employee "
                "information."
            )


        else:

            risk_message = (
                "The model estimates a relatively low "
                "probability of employee attrition based "
                "on the submitted characteristics."
            )


        # ====================================================
        # 9. SAVE PREDICTION TO HISTORY
        # ====================================================

        history = (
            load_prediction_history()
        )


        history_record = {

            "timestamp":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "job_role":
                job_role,

            "prediction":
                result,

            "probability":
                round(
                    attrition_probability,
                    2
                ),

            "model":
                model_info.get(
                    "model_name",
                    "Classification Model"
                )

        }


        # Add newest prediction first

        history.insert(
            0,
            history_record
        )


        # Keep latest 20 predictions

        history = history[:20]


        save_prediction_history(
            history
        )


        # ====================================================
        # 10. RENDER RESULT
        # ====================================================

        return render_template(

            "result.html",

            result=result,

            result_class=result_class,

            probability=round(
                attrition_probability,
                2
            ),

            risk_message=risk_message,

            employee=(
                employee_data
                .iloc[0]
                .to_dict()
            ),

            feature_importance=(
                feature_importance_records
            ),

            model_info=model_info

        )


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as e:

        print(
            "\n======================================"
        )

        print(
            "PREDICTION ERROR"
        )

        print(
            "======================================"
        )

        print(
            type(e).__name__
        )

        print(
            str(e)
        )


        return render_template(

            "predict.html",

            error=(
                "Unable to process the prediction. "
                "Please check the entered information "
                "and try again."
            )

        )


# ============================================================
# PREDICTION HISTORY PAGE
# ============================================================

@app.route(
    "/prediction-history"
)
def prediction_history():

    history = (
        load_prediction_history()
    )


    return render_template(

        "history.html",

        history=history

    )
    
# ============================================================
# PREDICTION STATISTICS
# ============================================================

def get_prediction_statistics():

    history = (
        load_prediction_history()
    )


    total_predictions = len(
        history
    )


    if total_predictions == 0:

        return {

            "total_predictions":
                0,

            "high_risk_count":
                0,

            "low_risk_count":
                0,

            "high_risk_percentage":
                0,

            "average_probability":
                0

        }


    high_risk_count = sum(

        1
        for item in history

        if item.get(
            "prediction"
        ) == "High Attrition Risk"

    )


    low_risk_count = (

        total_predictions
        -
        high_risk_count

    )


    probabilities = [

        float(
            item.get(
                "probability",
                0
            )
        )

        for item in history

    ]


    average_probability = (

        sum(probabilities)
        /
        len(probabilities)

    )


    high_risk_percentage = (

        high_risk_count
        /
        total_predictions

    ) * 100


    return {

        "total_predictions":
            total_predictions,

        "high_risk_count":
            high_risk_count,

        "low_risk_count":
            low_risk_count,

        "high_risk_percentage":
            round(
                high_risk_percentage,
                2
            ),

        "average_probability":
            round(
                average_probability,
                2
            )

    }

# ============================================================
# PREDICTION CHART DATA
# ============================================================

def get_prediction_chart_data():

    history = (
        load_prediction_history()
    )


    high_risk_count = sum(

        1

        for item in history

        if item.get(
            "prediction"
        ) == "High Attrition Risk"

    )


    low_risk_count = sum(

        1

        for item in history

        if item.get(
            "prediction"
        ) == "Low Attrition Risk"

    )


    return {

        "labels": [
            "Low Attrition Risk",
            "High Attrition Risk"
        ],

        "values": [
            low_risk_count,
            high_risk_count
        ]

    }
    
# ============================================================
# PROBABILITY DISTRIBUTION DATA
# ============================================================

def get_probability_distribution_data():

    history = load_prediction_history()

    buckets = {
        "0–20%": 0,
        "21–40%": 0,
        "41–60%": 0,
        "61–80%": 0,
        "81–100%": 0
    }

    for item in history:

        try:

            probability = float(
                item.get(
                    "probability",
                    0
                )
            )

        except (
            TypeError,
            ValueError
        ):

            continue


        if probability <= 20:

            buckets["0–20%"] += 1

        elif probability <= 40:

            buckets["21–40%"] += 1

        elif probability <= 60:

            buckets["41–60%"] += 1

        elif probability <= 80:

            buckets["61–80%"] += 1

        else:

            buckets["81–100%"] += 1


    return {

        "labels": list(
            buckets.keys()
        ),

        "values": list(
            buckets.values()
        )

    }
    
# ============================================================
# ANALYTICS PAGE
# ============================================================

@app.route("/analytics")
def analytics():

    dataset_stats = (
        get_dataset_statistics()
    )


    prediction_stats = (
        get_prediction_statistics()
    )


    prediction_chart_data = (
        get_prediction_chart_data()
    )
    
    probability_distribution_data = (
        get_probability_distribution_data()
    )
    
    attrition_insights = (
        get_attrition_insights()
    )
    
    attrition_summary = (
        get_attrition_insight_summary(
            attrition_insights
        )
    )
    
    feature_importance_data = (
        get_feature_importance_data()
    )

    model_metrics = (
        get_model_metrics()
    )
    
    return render_template(

        "analytics.html",

        dataset_stats=dataset_stats,

        prediction_stats=prediction_stats,

        prediction_chart_data=prediction_chart_data,

        probability_distribution_data=(probability_distribution_data),
        
        attrition_insights=attrition_insights,
        
        attrition_summary=attrition_summary,

        feature_importance_data=feature_importance_data,
        
        model_metrics=model_metrics

    )
    
# ============================================================
# ATTRITION INSIGHTS
# ============================================================

def get_attrition_insights():

    if dataset.empty:

        # ========================================================
        # FIND HIGHEST OBSERVED RATE
        # ========================================================

        def get_highest_rate(
            items
        ):

            if not items:

                return {
                    "label": "N/A",
                    "rate": 0
                }


            highest = max(
                items,
                key=lambda item:
                    item["rate"]
            )


            return {

                "label":
                    highest["label"],

                "rate":
                    highest["rate"]

            }


        # ========================================================
        # RETURN INSIGHTS
        # ========================================================

        return {

            "overtime":
                overtime_insights,

            "job_satisfaction":
                satisfaction_insights,

            "business_travel":
                travel_insights,

            "work_life_balance":
                work_life_insights,

            "overtime_highest":
                get_highest_rate(
                    overtime_insights
                ),

            "job_satisfaction_highest":
                get_highest_rate(
                    satisfaction_insights
                ),

            "business_travel_highest":
                get_highest_rate(
                    travel_insights
                ),

            "work_life_balance_highest":
                get_highest_rate(
                    work_life_insights
                )

        }


    # --------------------------------------------------------
    # OVERTIME
    # --------------------------------------------------------

    overtime_data = (
        dataset
        .groupby("over_time")["attrition"]
        .apply(
            lambda values:
            (
                values == "Yes"
            ).mean() * 100
        )
        .reset_index()
    )


    overtime_insights = []

    for _, row in overtime_data.iterrows():

        overtime_insights.append({

            "label":
                str(
                    row["over_time"]
                ),

            "rate":
                round(
                    float(
                        row["attrition"]
                    ),
                    2
                )

        })


    # --------------------------------------------------------
    # JOB SATISFACTION
    # --------------------------------------------------------

    satisfaction_data = (
        dataset
        .groupby(
            "job_satisfaction"
        )["attrition"]
        .apply(
            lambda values:
            (
                values == "Yes"
            ).mean() * 100
        )
        .reset_index()
    )


    satisfaction_insights = []

    for _, row in satisfaction_data.iterrows():

        satisfaction_insights.append({

            "label":
                str(
                    row["job_satisfaction"]
                ),

            "rate":
                round(
                    float(
                        row["attrition"]
                    ),
                    2
                )

        })


    # --------------------------------------------------------
    # BUSINESS TRAVEL
    # --------------------------------------------------------

    travel_data = (
        dataset
        .groupby(
            "business_travel"
        )["attrition"]
        .apply(
            lambda values:
            (
                values == "Yes"
            ).mean() * 100
        )
        .reset_index()
    )


    travel_insights = []

    for _, row in travel_data.iterrows():

        travel_insights.append({

            "label":
                str(
                    row["business_travel"]
                ),

            "rate":
                round(
                    float(
                        row["attrition"]
                    ),
                    2
                )

        })


    # --------------------------------------------------------
    # WORK-LIFE BALANCE
    # --------------------------------------------------------

    work_life_data = (
        dataset
        .groupby(
            "work_life_balance"
        )["attrition"]
        .apply(
            lambda values:
            (
                values == "Yes"
            ).mean() * 100
        )
        .reset_index()
    )


    work_life_insights = []

    for _, row in work_life_data.iterrows():

        work_life_insights.append({

            "label":
                str(
                    row["work_life_balance"]
                ),

            "rate":
                round(
                    float(
                        row["attrition"]
                    ),
                    2
                )

        })


    return {

        "overtime":
            overtime_insights,

        "job_satisfaction":
            satisfaction_insights,

        "business_travel":
            travel_insights,

        "work_life_balance":
            work_life_insights

    }
    
# ============================================================
# ATTRITION INSIGHT SUMMARY
# ============================================================

def get_attrition_insight_summary(
    insights
):

    overtime = (
        insights["overtime_highest"]
    )

    satisfaction = (
        insights["job_satisfaction_highest"]
    )

    travel = (
        insights["business_travel_highest"]
    )

    work_life = (
        insights["work_life_balance_highest"]
    )


    summary = {

        "overtime": (
            f"The highest observed attrition rate "
            f"among overtime groups was "
            f"{overtime['rate']}% for employees "
            f"with overtime set to "
            f"'{overtime['label']}'."
        ),

        "job_satisfaction": (
            f"The highest observed attrition rate "
            f"among job satisfaction levels was "
            f"{satisfaction['rate']}% at "
            f"satisfaction level "
            f"{satisfaction['label']}."
        ),

        "business_travel": (
            f"The highest observed attrition rate "
            f"among business travel groups was "
            f"{travel['rate']}% for "
            f"'{travel['label']}'."
        ),

        "work_life_balance": (
            f"The highest observed attrition rate "
            f"among work-life balance groups was "
            f"{work_life['rate']}% for "
            f"'{work_life['label']}'."
        )

    }


    return summary

# ============================================================
# LOAD TRAINING DATASET
# ============================================================

try:

    dataset = pd.read_csv(
        DATASET_PATH
    )

    print(
        f"✓ Dataset loaded successfully: "
        f"{dataset.shape[0]} rows"
    )

except Exception as e:

    print(
        "\nWARNING: Could not load training dataset."
    )

    print(e)

    dataset = pd.DataFrame()

# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )