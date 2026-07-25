import pandas as pd

def predict_price(model, feature_names, user_input):

    # Create one-row dataframe with all features initialized to 0
    input_df = pd.DataFrame(
        [[0] * len(feature_names)],
        columns=feature_names
    )

    # -----------------------------
    # Numerical Features
    # -----------------------------
    numeric_features = [
        "area",
        "bedrooms",
        "bathrooms",
        "stories",
        "parking"
    ]

    for feature in numeric_features:
        if feature in input_df.columns:
            input_df.at[0, feature] = user_input[feature]

    # -----------------------------
    # Binary Features
    # -----------------------------
    binary_features = [
        "mainroad",
        "guestroom",
        "basement",
        "hotwaterheating",
        "airconditioning",
        "prefarea"
    ]

    for feature in binary_features:

        encoded_column = f"{feature}_yes"

        if (
            encoded_column in input_df.columns and
            user_input[feature].lower() == "yes"
        ):
            input_df.at[0, encoded_column] = 1

    # -----------------------------
    # Furnishing Status
    # -----------------------------
    furnishing = user_input["furnishingstatus"].lower()

    furnishing_column = f"furnishingstatus_{furnishing}"

    if furnishing_column in input_df.columns:
        input_df.at[0, furnishing_column] = 1

    # -----------------------------
    # Prediction
    # -----------------------------
    prediction = model.predict(input_df)[0]

    return round(prediction, 2)