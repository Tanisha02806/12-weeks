import pandas as pd


def analyze_dataset(df):
    """
    Analyze the uploaded dataset.
    Returns useful information for preprocessing.
    """

    numerical_columns = df.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    target_column = None

    if "SalePrice" in df.columns:
        target_column = "SalePrice"

    return {
        "numerical_columns": numerical_columns,
        "categorical_columns": categorical_columns,
        "target_column": target_column
    }