import joblib

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler


def build_pipeline(df):

    """
    Build a preprocessing pipeline.
    """

    X = df.drop(columns=["SalePrice"])

    numerical_columns = X.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    categorical_columns = X.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    preprocessor = ColumnTransformer(

        transformers=[

            (
                "num",
                StandardScaler(),
                numerical_columns
            ),

            (
                "cat",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_columns
            )

        ]

    )

    pipeline = Pipeline(

        steps=[

            ("preprocessor", preprocessor)

        ]

    )

    pipeline.fit(X)

    transformed = pipeline.transform(X)

    return pipeline, transformed