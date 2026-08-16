import json
import os
import secrets
import hmac
from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd

from flask import Flask, render_template, request, session



# ============================================================
# JSON / DATA HELPERS
# ============================================================

def make_json_safe(value):
    """Convert pandas/numpy values into JSON/template-safe Python values."""
    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:
            pass

    if isinstance(value, dict):
        return {
            str(key): make_json_safe(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            make_json_safe(item)
            for item in value
        ]

    return value


def safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

# ============================================================
# HIREWISE AI - APPLICATION INITIALIZATION
# ============================================================

import glob


BASE_DIR = Path(__file__).resolve().parent

# Flask application must exist before any @app.route decorators.
app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static")
)

# Keep paths independent of the terminal's current working directory.
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "model"
MODELS_DIR = BASE_DIR / "models"
DATASET_DIR = BASE_DIR / "dataset"

DATA_DIR.mkdir(parents=True, exist_ok=True)

HISTORY_DIR = str(DATA_DIR)
HISTORY_PATH = str(DATA_DIR / "prediction_history.json")

DATASET_PATH = str(
    DATASET_DIR / "hr.csv"
)

# Primary artifact names used by the project.
MODEL_PATH = str(MODEL_DIR / "model.pkl")
PREPROCESSOR_PATH = str(MODEL_DIR / "preprocessor.pkl")
FEATURE_IMPORTANCE_PATH = str(MODEL_DIR / "feature_importance.pkl")
MODEL_INFO_PATH = str(MODEL_DIR / "model_info.pkl")


def _find_artifact(primary_path, keywords, extensions=(".pkl", ".joblib")):
    """Find an artifact using the expected path first, then safe fallbacks."""
    primary = Path(primary_path)

    if primary.is_file():
        return str(primary)

    search_dirs = [
        MODEL_DIR,
        MODELS_DIR,
        BASE_DIR,
    ]

    candidates = []
    for directory in search_dirs:
        if directory.is_dir():
            for extension in extensions:
                candidates.extend(directory.glob(f"*{extension}"))

    keyword_matches = []
    for candidate in candidates:
        name = candidate.name.lower()
        if all(keyword.lower() in name for keyword in keywords):
            keyword_matches.append(candidate)

    if keyword_matches:
        keyword_matches.sort(key=lambda p: len(p.name))
        return str(keyword_matches[0])

    return str(primary)


# Fall back to common filenames if the exact training filename differs.
# Use exact artifact filenames first.
MODEL_PATH = str(MODEL_DIR / "model.pkl")
PREPROCESSOR_PATH = str(MODEL_DIR / "preprocessor.pkl")
FEATURE_IMPORTANCE_PATH = str(MODEL_DIR / "feature_importance.pkl")
MODEL_INFO_PATH = str(MODEL_DIR / "model_info.pkl")


# If model.pkl is not present, look for likely model filenames without
# accidentally selecting model_info.pkl.
def _find_model_path():
    primary = Path(MODEL_PATH)
    if primary.is_file():
        return str(primary)

    candidates = []
    for directory in [MODEL_DIR, MODELS_DIR, BASE_DIR]:
        if directory.is_dir():
            for candidate in directory.glob("*.pkl"):
                name = candidate.name.lower()
                if (
                    "model" in name
                    and "info" not in name
                    and "feature" not in name
                    and "preprocess" not in name
                ):
                    candidates.append(candidate)

    candidates.sort(key=lambda p: len(p.name))
    return str(candidates[0]) if candidates else str(primary)


MODEL_PATH = _find_model_path()



def _load_joblib(path, label):
    try:
        value = joblib.load(path)
        print(f"✓ {label} loaded successfully.")
        return value
    except Exception as exc:
        print(f"WARNING: Could not load {label.lower()}.")
        print(f"Path: {path}")
        print(exc)
        return None


# These globals are available before any route is called.
model = _load_joblib(
    MODEL_PATH,
    "Trained model"
)

preprocessor = _load_joblib(
    PREPROCESSOR_PATH,
    "Preprocessor"
)

model_info = _load_joblib(
    MODEL_INFO_PATH,
    "Model information"
)

# Feature importance is loaded by get_feature_importance_data() itself.
# This variable is provided for compatibility with older code/templates.
feature_importance = _load_joblib(
    FEATURE_IMPORTANCE_PATH,
    "Feature importance"
)

dataset = pd.DataFrame()

try:
    dataset = pd.read_csv(DATASET_PATH)
    print(
        f"✓ Dataset loaded successfully: "
        f"{dataset.shape[0]} rows"
    )
except Exception as exc:
    print("\nWARNING: Could not load training dataset.")
    print(f"Path: {DATASET_PATH}")
    print(exc)

# ============================================================
# END APPLICATION INITIALIZATION
# ============================================================




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
# PREDICTION HISTORY
# ============================================================

HISTORY_DIR = "data"

HISTORY_PATH = (
    "data/prediction_history.json"
)

# ============================================================
# CREATE HISTORY DIRECTORY
# ============================================================

os.makedirs(
    HISTORY_DIR,
    exist_ok=True
)

# ============================================================
# INITIALIZE PREDICTION HISTORY
# ============================================================

def initialize_prediction_history():

    if not os.path.exists(
        HISTORY_PATH
    ):

        with open(
            HISTORY_PATH,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=4
            )
            
initialize_prediction_history()


# ============================================================
# PREDICTION HISTORY STATISTICS
# ============================================================

def get_prediction_history_stats():

    history = load_prediction_history()


    if not history:

        return {

            "total":
                0,

            "likely_to_leave":
                0,

            "likely_to_stay":
                0,

            "high_risk":
                0,

            "average_probability":
                0

        }


    total = len(
        history
    )

    likely_to_leave = 0
    likely_to_stay = 0
    high_risk = 0

    probabilities = []


    for item in history:

        prediction = str(
            item.get(
                "prediction",
                ""
            )
        ).strip().lower()


        risk_level = str(
            item.get(
                "risk_level",
                ""
            )
        ).strip().lower()


        # ----------------------------------------------------
        # PREDICTION COUNTS
        # ----------------------------------------------------

        if (
            "high attrition risk" in prediction
            or "likely to leave" in prediction
            or "attrition" in prediction
            and "low" not in prediction
        ):

            likely_to_leave += 1

        elif (
            "low attrition risk" in prediction
            or "likely to stay" in prediction
            or "stay" in prediction
        ):

            likely_to_stay += 1


        # ----------------------------------------------------
        # HIGH-RISK COUNT
        # ----------------------------------------------------

        if (
            risk_level == "high"
            or "high attrition risk" in prediction
        ):

            high_risk += 1


        # ----------------------------------------------------
        # PROBABILITY
        # ----------------------------------------------------

        try:

            probability = float(
                item.get(
                    "probability",
                    0
                )
            )

            # Support both:
            # 0.72 -> 72%
            # 72.0 -> 72%
            if 0 <= probability <= 1:
                probability *= 100

            probability = max(
                0,
                min(
                    probability,
                    100
                )
            )

        except (
            TypeError,
            ValueError
        ):

            continue


        probability = max(
            0,
            min(
                probability,
                100
            )
        )


        probabilities.append(
            probability
        )


    average_probability = (

        sum(probabilities)
        /
        len(probabilities)

        if probabilities

        else 0

    )


    return {

        "total":
            total,

        "likely_to_leave":
            likely_to_leave,

        "likely_to_stay":
            likely_to_stay,

        "high_risk":
            high_risk,

        "average_probability":
            round(
                average_probability,
                2
            )

    }


def get_model_comparison():

    comparison_data = None

    if isinstance(model_info, dict):

        comparison_data = (
            model_info.get(
                "model_comparison"
            )
        )


    if not comparison_data:

        return []


    records = []


    # --------------------------------------------------------
    # CASE 1: DICTIONARY
    # --------------------------------------------------------

    if isinstance(
        comparison_data,
        dict
    ):

        for model_name, metrics in (
            comparison_data.items()
        ):

            if not isinstance(
                metrics,
                dict
            ):

                continue


            records.append({

                "model":
                    str(model_name),

                "accuracy":
                    metrics.get(
                        "accuracy",
                        0
                    ),

                "precision":
                    metrics.get(
                        "precision",
                        0
                    ),

                "recall":
                    metrics.get(
                        "recall",
                        0
                    ),

                "f1_score":
                    (
                        metrics.get(
                            "f1_score"
                        )

                        or

                        metrics.get(
                            "f1",
                            0
                        )
                    )

            })


    # --------------------------------------------------------
    # CASE 2: LIST
    # --------------------------------------------------------

    elif isinstance(
        comparison_data,
        list
    ):

        for item in comparison_data:

            if not isinstance(
                item,
                dict
            ):

                continue


            model_name = (

                item.get(
                    "model"
                )

                or

                item.get(
                    "model_name"
                )

                or

                item.get(
                    "name"
                )

            )


            if not model_name:

                continue


            records.append({

                "model":
                    str(model_name),

                "accuracy":
                    item.get(
                        "accuracy",
                        0
                    ),

                "precision":
                    item.get(
                        "precision",
                        0
                    ),

                "recall":
                    item.get(
                        "recall",
                        0
                    ),

                "f1_score":
                    (
                        item.get(
                            "f1_score"
                        )

                        or

                        item.get(
                            "f1",
                            0
                        )
                    )

            })


    # --------------------------------------------------------
    # CONVERT VALUES TO PERCENTAGES
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


        if value <= 1:

            value *= 100


        return round(
            value,
            2
        )


    # --------------------------------------------------------
    # NORMALIZE ALL METRICS
    # --------------------------------------------------------

    for record in records:

        record["accuracy"] = (
            to_percentage(
                record["accuracy"]
            )
        )

        record["precision"] = (
            to_percentage(
                record["precision"]
            )
        )

        record["recall"] = (
            to_percentage(
                record["recall"]
            )
        )

        record["f1_score"] = (
            to_percentage(
                record["f1_score"]
            )
        )


    return records

# ============================================================
# MODEL METRIC INTERPRETATION
# ============================================================

def get_metric_interpretation(
    metrics
):

    if not isinstance(metrics, dict) or not metrics:

        return {

            "accuracy": (
                "Accuracy information is not available."
            ),

            "precision": (
                "Precision information is not available."
            ),

            "recall": (
                "Recall information is not available."
            ),

            "f1_score": (
                "F1 Score information is not available."
            )

        }


    accuracy = metrics.get(
        "accuracy",
        0
    )

    precision = metrics.get(
        "precision",
        0
    )

    recall = metrics.get(
        "recall",
        0
    )

    f1_score = metrics.get(
        "f1_score",
        0
    )


    # --------------------------------------------------------
    # ACCURACY
    # --------------------------------------------------------

    accuracy_text = (
        f"The model correctly classified "
        f"{accuracy:.2f}% of the observations "
        f"in the test dataset."
    )


    # --------------------------------------------------------
    # PRECISION
    # --------------------------------------------------------

    precision_text = (
        f"Among observations predicted as "
        f"attrition, {precision:.2f}% were "
        f"actually attrition cases in the "
        f"test dataset."
    )


    # --------------------------------------------------------
    # RECALL
    # --------------------------------------------------------

    recall_text = (
        f"The model identified "
        f"{recall:.2f}% of the actual attrition "
        f"cases in the test dataset."
    )


    # --------------------------------------------------------
    # F1 SCORE
    # --------------------------------------------------------

    f1_text = (
        f"The F1 Score is {f1_score:.2f}%, "
        f"combining precision and recall into "
        f"a single balanced metric."
    )


    return {

        "accuracy":
            accuracy_text,

        "precision":
            precision_text,

        "recall":
            recall_text,

        "f1_score":
            f1_text

    }
    
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
# LOAD PREDICTION HISTORY
# ============================================================

def load_prediction_history():

    try:

        with open(
            HISTORY_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            history = json.load(
                file
            )

    except FileNotFoundError:

        # History file does not exist yet.
        initialize_prediction_history()

        return []

    except json.JSONDecodeError:

        # History file exists but contains invalid JSON.
        return []

    except OSError:

        # File cannot be accessed.
        return []


    # --------------------------------------------------------
    # VALIDATE TOP-LEVEL STRUCTURE
    # --------------------------------------------------------

    if not isinstance(
        history,
        list
    ):

        return []


    # --------------------------------------------------------
    # KEEP ONLY VALID RECORDS
    # --------------------------------------------------------

    valid_history = []


    for item in history:

        if not isinstance(
            item,
            dict
        ):

            continue


        # A usable history record should have
        # at least a prediction and timestamp.

        if not item.get(
            "prediction"
        ):

            continue


        if not item.get(
            "timestamp"
        ):

            continue


        valid_history.append(
            item
        )


    # --------------------------------------------------------
    # NEWEST FIRST
    # --------------------------------------------------------

    valid_history.sort(
        key=lambda item: item.get(
            "timestamp",
            ""
        ),
        reverse=True
    )


    return valid_history

# ============================================================
# SAVE PREDICTION HISTORY
# ============================================================

def save_prediction_history(
    history
):

    """
    Save the complete prediction-history list to JSON.
    """

    os.makedirs(
        os.path.dirname(HISTORY_PATH),
        exist_ok=True
    )

    if not isinstance(history, list):
        history = []

    with open(
        HISTORY_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=4,
            ensure_ascii=False
        )


# ============================================================
# PREPARE FEATURE IMPORTANCE FOR ANALYTICS
# ============================================================

def get_feature_importance_data():

    try:

        loaded_feature_importance = joblib.load(
            FEATURE_IMPORTANCE_PATH
        )

    except Exception as e:

        print(
            "WARNING: Could not load feature importance."
        )

        print(e)

        return []


    records = []


    # ========================================================
    # CASE 1: PANDAS DATAFRAME
    # ========================================================

    if isinstance(
        loaded_feature_importance,
        pd.DataFrame
    ):

        dataframe = loaded_feature_importance.copy()


        # Find feature-name column

        feature_column = None

        for column in [
            "Display Feature",
            "feature",
            "Feature",
            "name"
        ]:

            if column in dataframe.columns:

                feature_column = column

                break


        # Find importance column

        importance_column = None

        for column in [
            "Importance",
            "importance",
            "Importance Score",
            "importance_score"
        ]:

            if column in dataframe.columns:

                importance_column = column

                break


        if (
            feature_column is not None
            and
            importance_column is not None
        ):

            for _, row in dataframe.iterrows():

                try:

                    importance_value = float(
                        row[importance_column]
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    continue


                records.append({

                    "feature":
                        str(
                            row[feature_column]
                        ),

                    "importance":
                        importance_value

                })


    # ========================================================
    # CASE 2: DICTIONARY
    # ========================================================

    elif isinstance(
        loaded_feature_importance,
        dict
    ):

        for feature, importance in (
            loaded_feature_importance.items()
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


    # ========================================================
    # CASE 3: LIST
    # ========================================================

    elif isinstance(
        loaded_feature_importance,
        list
    ):

        for item in loaded_feature_importance:

            if not isinstance(
                item,
                dict
            ):

                continue


            feature_name = (

                item.get(
                    "feature"
                )

                or

                item.get(
                    "Display Feature"
                )

                or

                item.get(
                    "name"
                )

            )


            importance_value = (

                item.get(
                    "importance"
                )

                if item.get(
                    "importance"
                ) is not None

                else

                item.get(
                    "Importance"
                )

            )


            if (
                feature_name is None
                or
                importance_value is None
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


    # ========================================================
    # SORT
    # ========================================================

    records.sort(

        key=lambda item:
            item["importance"],

        reverse=True

    )


    # ========================================================
    # TOP 10
    # ========================================================

    records = records[:10]


    # ========================================================
    # CREATE DISPLAY NAMES
    # ========================================================

    cleaned_records = []


    for item in records:

        raw_name = str(
            item.get(
                "feature",
                "Unknown Feature"
            )
        )


        display_name = raw_name.replace(
            "num__",
            ""
        )


        display_name = display_name.replace(
            "cat__",
            ""
        )


        display_name = display_name.replace(
            "_",
            " "
        )


        display_name = display_name.strip().title()


        cleaned_records.append({

            "feature":
                raw_name,

            "importance":
                item["importance"],

            "Display Feature":
                display_name,

            "Importance":
                item["importance"]

        })


    return cleaned_records

# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )



# ============================================================
# PREDICTION INPUT VALIDATION
# ============================================================

def validate_prediction_inputs(
    age,
    monthly_income,
    num_companies_worked
):
    """Centralized validation used by the prediction endpoint."""
    errors = []

    if age < 18 or age > 70:
        errors.append("Age must be between 18 and 70.")

    if monthly_income < 100:
        errors.append("Monthly income must be at least 100.")

    if num_companies_worked < 0 or num_companies_worked > 20:
        errors.append(
            "Number of companies worked must be between 0 and 20."
        )

    return errors


def get_risk_level(probability):
    """Return a consistent risk label from an attrition probability."""
    probability = safe_float(probability)

    if probability >= 70:
        return "High"

    if probability >= 40:
        return "Medium"

    return "Low"


def get_risk_message(probability):
    """Return the user-facing interpretation for a prediction."""
    probability = safe_float(probability)

    if probability >= 70:
        return (
            "The model estimates a high probability of employee "
            "attrition based on the submitted characteristics."
        )

    if probability >= 40:
        return (
            "The model estimates a moderate probability of employee "
            "attrition. The result should be reviewed alongside other "
            "employee information."
        )

    return (
        "The model estimates a relatively low probability of employee "
        "attrition based on the submitted characteristics."
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

            "prediction":
                result,

            "probability":
                round(
                    attrition_probability,
                    2
                ),

            "risk_level":
                (
                    "High"
                    if result == "High Attrition Risk"
                    else "Low"
                ),

            "job_role":
                job_role,

            "features":
                {
                    key: (
                        value.item()
                        if hasattr(
                            value,
                            "item"
                        )
                        else value
                    )
                    for key, value in (
                        employee_data
                        .iloc[0]
                        .to_dict()
                        .items()
                    )
                },

            "model":
                (
                    model_info.get(
                        "model_name",
                        "Classification Model"
                    )
                    if isinstance(
                        model_info,
                        dict
                    )
                    else "Classification Model"
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
            ),

            form_data=(
                request.form.to_dict()
                if request.method == "POST"
                else {}
            )

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

    if not history:
        return {
            "labels": [
                "0–20%",
                "21–40%",
                "41–60%",
                "61–80%",
                "81–100%"
            ],
            "values": [0, 0, 0, 0, 0]
        }

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
    
    model_comparison = (
        get_model_comparison()
    )
    
    history_stats = (
        get_prediction_history_stats()
    )
    
    metric_interpretation = (
        get_metric_interpretation(
            model_metrics
        )
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
        
        model_metrics=model_metrics,
        
        model_comparison=model_comparison,
        
        metric_interpretation=metric_interpretation,
        
        history_stats=history_stats

    )
    
# ============================================================
# ATTRITION INSIGHTS
# ============================================================

def get_attrition_insights():

    empty_result = {

        "overtime": [],
        "job_satisfaction": [],
        "business_travel": [],
        "work_life_balance": [],

        "overtime_highest": {
            "label": "N/A",
            "rate": 0
        },

        "job_satisfaction_highest": {
            "label": "N/A",
            "rate": 0
        },

        "business_travel_highest": {
            "label": "N/A",
            "rate": 0
        },

        "work_life_balance_highest": {
            "label": "N/A",
            "rate": 0
        }

    }


    if dataset.empty:

        return empty_result


    # --------------------------------------------------------
    # HELPER: BUILD GROUP ATTRITION RATES
    # --------------------------------------------------------

    def build_insights(
        column
    ):

        if (
            column not in dataset.columns
            or "attrition" not in dataset.columns
        ):

            return []


        grouped = (
            dataset
            .groupby(column)["attrition"]
            .apply(
                lambda values:
                (
                    values.astype(str).str.strip().eq("Yes")
                ).mean() * 100
            )
            .reset_index()
        )


        results = []

        for _, row in grouped.iterrows():

            results.append({

                "label":
                    str(
                        row[column]
                    ),

                "rate":
                    round(
                        float(
                            row["attrition"]
                        ),
                        2
                    )

            })


        return results


    # --------------------------------------------------------
    # BUILD ALL INSIGHTS
    # --------------------------------------------------------

    overtime_insights = build_insights(
        "over_time"
    )

    satisfaction_insights = build_insights(
        "job_satisfaction"
    )

    travel_insights = build_insights(
        "business_travel"
    )

    work_life_insights = build_insights(
        "work_life_balance"
    )


    # --------------------------------------------------------
    # HELPER: HIGHEST RATE
    # --------------------------------------------------------

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
                item.get(
                    "rate",
                    0
                )
        )


        return {

            "label":
                highest.get(
                    "label",
                    "N/A"
                ),

            "rate":
                highest.get(
                    "rate",
                    0
                )

        }


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
# PREDICTION HISTORY PAGE
# ============================================================

@app.route("/history")
def prediction_history():

    history = load_prediction_history()

    history_stats = (
        get_prediction_history_stats()
    )

    return render_template(

        "history.html",

        history=history,

        history_stats=history_stats

    )
    


# ============================================================
# APPLICATION STATUS / HEALTH CHECK
# ============================================================

@app.route("/status")
def application_status():

    return {
        "status": "ok",
        "model_loaded": model is not None,
        "preprocessor_loaded": preprocessor is not None,
        "model_info_loaded": isinstance(model_info, dict),
        "feature_importance_loaded": bool(
            get_feature_importance_data()
        ),
        "dataset_loaded": not dataset.empty,
        "history_records": len(
            load_prediction_history()
        )
    }


# ============================================================
# PREDICTION HISTORY API
# ============================================================

@app.route("/api/prediction-history")
def prediction_history_api():

    history = load_prediction_history()

    return {
        "count": len(history),
        "history": make_json_safe(history)
    }


# ============================================================
# MODEL INFORMATION API
# ============================================================

@app.route("/api/model-info")
def model_info_api():

    return {
        "model_info": make_json_safe(
            model_info
            if isinstance(model_info, dict)
            else {}
        ),
        "feature_importance": make_json_safe(
            get_feature_importance_data()
        ),
        "model_comparison": make_json_safe(
            get_model_comparison()
        )
    }



# ============================================================
# APPLICATION ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def handle_404(error):

    return render_template(
        "404.html",
        error="The requested page could not be found."
    ), 404


@app.errorhandler(500)
def handle_500(error):

    # Log the exception server-side, but never expose its details to users.
    print("APPLICATION ERROR:")
    print(type(error).__name__)
    print(str(error))

    return render_template(
        "error.html",
        error=(
            "Something went wrong while processing your request. "
            "Please try again."
        )
    ), 500




# ============================================================
# SECURITY CONFIGURATION — 5.12
# ============================================================

# Secret key must be supplied through the environment in production.
# A development fallback keeps local coursework execution working.
SECRET_KEY = os.environ.get(
    "HIREWISE_SECRET_KEY",
    "hirewise-development-secret-change-before-production"
)

app.config["SECRET_KEY"] = SECRET_KEY

# Limit request body size to reduce accidental/abusive oversized requests.
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024

# Safer browser cookie defaults.
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = (
    os.environ.get(
        "HIREWISE_COOKIE_SECURE",
        "0"
    ).lower()
    in ("1", "true", "yes")
)


def _get_csrf_token():
    """Create/retrieve a per-session CSRF token."""
    token = session.get("_csrf_token")

    if not token:
        token = secrets.token_urlsafe(32)
        session["_csrf_token"] = token

    return token


@app.context_processor
def inject_security_helpers():
    return {
        "csrf_token": _get_csrf_token
    }


@app.before_request
def protect_prediction_post():
    """Protect the prediction form against cross-site POST requests."""
    if (
        request.method == "POST"
        and request.path == "/predict"
    ):

        expected = session.get(
            "_csrf_token"
        )

        supplied = request.form.get(
            "_csrf_token",
            ""
        )

        if (
            not expected
            or not supplied
            or not hmac.compare_digest(
                str(expected),
                str(supplied)
            )
        ):

            return render_template(
                "predict.html",
                error=(
                    "Your form session has expired or "
                    "the security token is invalid. "
                    "Please refresh the page and try again."
                ),
                form_data=request.form.to_dict()
            ), 400


@app.after_request
def add_security_headers(response):
    """Add baseline browser security headers."""
    response.headers.setdefault(
        "X-Content-Type-Options",
        "nosniff"
    )

    response.headers.setdefault(
        "X-Frame-Options",
        "SAMEORIGIN"
    )

    response.headers.setdefault(
        "Referrer-Policy",
        "strict-origin-when-cross-origin"
    )

    response.headers.setdefault(
        "Permissions-Policy",
        "camera=(), microphone=(), geolocation=()"
    )

    response.headers.setdefault(
        "Content-Security-Policy",
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' "
        "https://cdn.jsdelivr.net https://fonts.googleapis.com; "
        "style-src 'self' 'unsafe-inline' "
        "https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data:; "
        "connect-src 'self'; "
        "frame-ancestors 'self'; "
        "base-uri 'self'; "
        "form-action 'self'"
    )

    return response


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

APP_ENV = os.environ.get(
    "HIREWISE_ENV",
    "development"
)

# Debug is explicitly controlled by environment rather than
# being hard-coded for future deployment.
DEBUG_MODE = (
    os.environ.get(
        "HIREWISE_DEBUG",
        "0"
    ).lower()
    in ("1", "true", "yes")
)

# ============================================================
# STARTUP SUMMARY
# ============================================================

print("\n--- HIREWISE AI STARTUP CHECK ---")
print(f"Model path: {MODEL_PATH}")
print(f"Preprocessor path: {PREPROCESSOR_PATH}")
print(f"Feature importance path: {FEATURE_IMPORTANCE_PATH}")
print(f"Model info path: {MODEL_INFO_PATH}")
print(f"Dataset path: {DATASET_PATH}")
print(f"History path: {HISTORY_PATH}")
print("---------------------------------\n")

# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(debug=DEBUG_MODE)