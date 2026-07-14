import pandas as pd
from sklearn.model_selection import train_test_split


def split_dataset(df):

    """
    Split dataset into training and testing sets.
    """

    if "SalePrice" not in df.columns:
        raise ValueError("Target column 'SalePrice' not found.")

    X = df.drop(columns=["SalePrice"])
    y = df["SalePrice"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    return (
        X_train,
        X_test,
        y_train,
        y_test,
        len(X_train),
        len(X_test)
    )