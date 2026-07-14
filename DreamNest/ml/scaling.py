import pandas as pd
from sklearn.preprocessing import StandardScaler


def scale_dataset(df):

    """
    Scale all numerical features using StandardScaler.
    """

    scaled_df = df.copy()

    # Separate target column
    if "SalePrice" in scaled_df.columns:

        y = scaled_df["SalePrice"]

        X = scaled_df.drop(columns=["SalePrice"])

    else:

        y = None

        X = scaled_df

    numerical_columns = X.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    scaler = StandardScaler()

    if numerical_columns:

        X[numerical_columns] = scaler.fit_transform(
            X[numerical_columns]
        )

    if y is not None:

        X["SalePrice"] = y

    return X, len(numerical_columns)