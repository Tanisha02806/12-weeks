import pandas as pd


def clean_dataset(df):
    """
    Cleans missing values in the dataset.

    Numerical columns -> Median
    Categorical columns -> Mode
    """

    cleaned_df = df.copy()

    missing_before = cleaned_df.isnull().sum().sum()

    # Numerical columns
    numerical_columns = cleaned_df.select_dtypes(
        include=["int64", "float64"]
    ).columns

    for column in numerical_columns:

        if cleaned_df[column].isnull().sum() > 0:

            median = cleaned_df[column].median()

            cleaned_df[column] = cleaned_df[column].fillna(median)

    # Categorical columns
    categorical_columns = cleaned_df.select_dtypes(
        include=["object", "category"]
    ).columns

    for column in categorical_columns:

        if cleaned_df[column].isnull().sum() > 0:

            mode = cleaned_df[column].mode()[0]

            cleaned_df[column] = cleaned_df[column].fillna(mode)

    missing_after = cleaned_df.isnull().sum().sum()

    return cleaned_df, missing_before, missing_after