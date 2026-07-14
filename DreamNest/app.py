from flask import Flask, render_template, request, redirect, url_for, session
import os
import pandas as pd
import joblib

from ml.analyzer import analyze_dataset
from ml.cleaning import clean_dataset
from ml.encoding import encode_dataset
from ml.scaling import scale_dataset
from ml.splitter import split_dataset
from ml.pipeline_builder import build_pipeline

app = Flask(__name__)
app.secret_key = "dreamnest_secret_key"

# Pipeline Status
PIPELINE_STEPS = [
    "cleaning",
    "encoding",
    "scaling",
    "splitting",
    "pipeline"
]

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/run-encoding", methods=["POST"])
def run_encoding():

    cleaned_path = session.get("cleaned_dataset")

    if not cleaned_path or not os.path.exists(cleaned_path):
        return redirect(url_for("dashboard"))

    df = pd.read_csv(cleaned_path)

    encoded_df, encoded_features = encode_dataset(df)

    encoded_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "encoded_dataset.csv"
    )

    encoded_df.to_csv(
        encoded_path,
        index=False
    )

    session["encoding"] = True
    session["encoded_dataset"] = encoded_path
    session["encoded_features"] = encoded_features

    return redirect(url_for("dashboard"))

@app.route("/run-scaling", methods=["POST"])
def run_scaling():

    encoded_path = session.get("encoded_dataset")

    if not encoded_path or not os.path.exists(encoded_path):

        return redirect(url_for("dashboard"))

    df = pd.read_csv(encoded_path)

    scaled_df, scaled_features = scale_dataset(df)
    print("Scaled Features:", scaled_features)

    scaled_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "scaled_dataset.csv"
    )

    scaled_df.to_csv(
        scaled_path,
        index=False
    )

    session["scaling"] = True
    session["scaled_dataset"] = scaled_path
    session["scaled_features"] = scaled_features
    print("Session Scaled Features:", session["scaled_features"])

    return redirect(url_for("dashboard"))

@app.route("/run-splitting", methods=["POST"])
def run_splitting():

    scaled_path = session.get("scaled_dataset")

    if not scaled_path or not os.path.exists(scaled_path):
        return redirect(url_for("dashboard"))

    df = pd.read_csv(scaled_path)

    (
        X_train,
        X_test,
        y_train,
        y_test,
        train_rows,
        test_rows
    ) = split_dataset(df)

    upload_folder = app.config["UPLOAD_FOLDER"]

    X_train.to_csv(
        os.path.join(upload_folder, "X_train.csv"),
        index=False
    )

    X_test.to_csv(
        os.path.join(upload_folder, "X_test.csv"),
        index=False
    )

    y_train.to_frame().to_csv(
        os.path.join(upload_folder, "y_train.csv"),
        index=False
    )

    y_test.to_frame().to_csv(
        os.path.join(upload_folder, "y_test.csv"),
        index=False
    )

    session["splitting"] = True
    session["train_rows"] = train_rows
    session["test_rows"] = test_rows

    return redirect(url_for("dashboard"))

@app.route("/run-pipeline", methods=["POST"])
def run_pipeline():

    dataset_path = session.get("dataset_path")

    if not dataset_path or not os.path.exists(dataset_path):

        return redirect(url_for("dashboard"))

    df = pd.read_csv(dataset_path)

    pipeline, transformed = build_pipeline(df)

    pipeline_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "pipeline.pkl"
    )

    joblib.dump(
        pipeline,
        pipeline_path
    )

    session["pipeline"] = True
    session["pipeline_rows"] = transformed.shape[0]
    session["pipeline_columns"] = transformed.shape[1]

    return redirect(url_for("dashboard"))

@app.route("/run-cleaning", methods=["POST"])
def run_cleaning():

    dataset_path = session.get("dataset_path")

    if not dataset_path or not os.path.exists(dataset_path):

        return redirect(url_for("dashboard"))

    df = pd.read_csv(dataset_path)

    cleaned_df, missing_before, missing_after = clean_dataset(df)

    cleaned_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "cleaned_dataset.csv"
    )

    cleaned_df.to_csv(
        cleaned_path,
        index=False
    )

    session["cleaning"] = True
    session["missing_before"] = int(missing_before)
    session["missing_after"] = int(missing_after)
    session["cleaned_dataset"] = cleaned_path

    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():

    dataset_name = session.get("dataset_name")
    dataset_path = session.get("dataset_path")

    # -------------------------------
    # Dataset Information
    # -------------------------------

    dataset_loaded = False
    rows = "--"
    columns = "--"
    missing_values = "--"

    # -------------------------------
    # Cleaning Information
    # -------------------------------

    missing_before = session.get("missing_before", "--")
    missing_after = session.get("missing_after", "--")

    # -------------------------------
    # Encoding Information
    # -------------------------------

    encoded_features = session.get(
        "encoded_features",
        "--"
    )
    
    # -------------------------------
    # Scaling Information
    # -------------------------------

    scaled_features = session.get(
        "scaled_features",
        "--"
    )

    train_rows = session.get(
        "train_rows",
        "--"
    )

    test_rows = session.get(
        "test_rows",
        "--"
    )
    
    pipeline_rows = session.get(
        "pipeline_rows",
        "--"
    )

    pipeline_columns = session.get(
        "pipeline_columns",
        "--"
    )
    
    # -------------------------------
    # Pipeline Status
    # -------------------------------

    cleaning = session.get("cleaning", False)
    encoding = session.get("encoding", False)
    scaling = session.get("scaling", False)
    splitting = session.get("splitting", False)
    pipeline = session.get("pipeline", False)

    # -------------------------------
    # Progress
    # -------------------------------

    progress = 0

    if dataset_path and os.path.exists(dataset_path):

        try:

            df = pd.read_csv(dataset_path)

            dataset_loaded = True

            rows = df.shape[0]
            columns = df.shape[1]
            missing_values = df.isnull().sum().sum()

            completed_steps = sum([
                cleaning,
                encoding,
                scaling,
                splitting,
                pipeline
            ])

            progress = 20 + (completed_steps * 16)

        except Exception as e:

            print("Dashboard Error:", e)

            dataset_loaded = False
            progress = 0

    return render_template(
        "dashboard.html",
        dataset_loaded=dataset_loaded,
        dataset_name=dataset_name,
        rows=rows,
        columns=columns,
        missing_values=missing_values,
        progress=progress,
        cleaning=cleaning,
        encoding=encoding,
        scaling=scaling,
        splitting=splitting,
        pipeline=pipeline,
        missing_before=missing_before,
        missing_after=missing_after,
        encoded_features=encoded_features,
        scaled_features=scaled_features,
        train_rows=train_rows,
        test_rows=test_rows,
        pipeline_rows=pipeline_rows,
        pipeline_columns=pipeline_columns
    )
        
@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        if "csvFile" not in request.files:
            return "No file selected."

        file = request.files["csvFile"]

        if file.filename == "":
            return "Please choose a CSV file."

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(filepath)
        
        session["dataset_path"] = filepath
        session["dataset_name"] = file.filename
        
        # Reset pipeline progress
        for step in PIPELINE_STEPS:
            session[step] = False

        # Read CSV using Pandas
        try:

            df = pd.read_csv(filepath)

            rows = df.shape[0]
            columns = df.shape[1]
            missing_values = df.isnull().sum().sum()

            # Get first 5 rows
            preview_data = df.head().values.tolist()

            # Get column names
            headers = df.columns.tolist()
            
            analysis = analyze_dataset(df)

            numerical_columns = analysis["numerical_columns"]

            categorical_columns = analysis["categorical_columns"]

            target_column = analysis["target_column"]

        except Exception:

            return render_template(
                "upload.html",
                message="❌ Invalid CSV file.",
                rows="--",
                columns="--",
                missing_values="--",
                headers=[],
                preview_data=[],
                numerical_columns=[],
                categorical_columns=[],
                target_column=None
            )

        return render_template(
            "upload.html",
            message="✅ Dataset uploaded successfully!",
            rows=rows,
            columns=columns,
            missing_values=missing_values,
            headers=headers,
            preview_data=preview_data,
            numerical_columns=numerical_columns,
            categorical_columns=categorical_columns,
            target_column=target_column
        )

    return render_template(
        "upload.html",
        rows="--",
        columns="--",
        missing_values="--",
        headers=[],
        preview_data=[],
        numerical_columns=[],
        categorical_columns=[],
        target_column=None
    )

if __name__ == "__main__":
    app.run(debug=True)