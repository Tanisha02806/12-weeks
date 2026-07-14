import pandas as pd
from sklearn.preprocessing import OneHotEncoder


def encode_dataset(df):

    """
    Encode categorical features using OneHotEncoder.
    """

    encoded_df = df.copy()

    # Separate target column
    if "SalePrice" in encoded_df.columns:
        y = encoded_df["SalePrice"]
        X = encoded_df.drop(columns=["SalePrice"])
    else:
        y = None
        X = encoded_df

    categorical_columns = X.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    numerical_columns = X.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    encoder = OneHotEncoder(
        sparse_output=False,
        handle_unknown="ignore"
    )

    if categorical_columns:

        encoded_array = encoder.fit_transform(
            X[categorical_columns]
        )

        encoded_columns = encoder.get_feature_names_out(
            categorical_columns
        )

        encoded_features = pd.DataFrame(
            encoded_array,
            columns=encoded_columns,
            index=X.index
        )

        X = X.drop(columns=categorical_columns)

        X = pd.concat(
            [X, encoded_features],
            axis=1
        )

    if y is not None:
        X["SalePrice"] = y

    return X, len(categorical_columns)