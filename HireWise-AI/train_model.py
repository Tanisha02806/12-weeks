import pandas as pd
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    roc_auc_score
)


# ============================================================
# 1. LOAD DATASET
# ============================================================

df = pd.read_csv("dataset/hr.csv")

print("Dataset loaded successfully!")
print("Shape:", df.shape)


# ============================================================
# 2. DISPLAY DATASET COLUMNS
# ============================================================

print("\n--- ACTUAL DATASET COLUMNS ---")

for column in df.columns:
    print(column)


# ============================================================
# 3. SELECT FEATURES
# ============================================================

features = [
    "age",
    "business_travel",
    "job_role",
    "job_satisfaction",
    "monthly_income",
    "num_companies_worked",
    "over_time",
    "environment_satisfaction",
    "work_life_balance"
]

target = "attrition"


# Create feature matrix and target variable

X = df[features]
y = df[target]


# ============================================================
# 4. CHECK SELECTED FEATURES
# ============================================================

print("\n--- SELECTED FEATURES ---")

print(X.head())


print("\n--- SELECTED FEATURE DATA TYPES ---")

print(X.dtypes)


print("\n--- TARGET BEFORE ENCODING ---")

print(y.head())


# ============================================================
# 5. ENCODE TARGET
# ============================================================

# No  -> 0
# Yes -> 1

y = y.map({
    "No": 0,
    "Yes": 1
})


print("\n--- TARGET AFTER ENCODING ---")

print(y.head())


print("\n--- TARGET DISTRIBUTION ---")

print(y.value_counts())


# ============================================================
# 6. DEFINE NUMERICAL FEATURES
# ============================================================

numeric_features = [
    "age",
    "monthly_income",
    "num_companies_worked"
]


# ============================================================
# 7. DEFINE CATEGORICAL FEATURES
# ============================================================

categorical_features = [
    "business_travel",
    "job_role",
    "job_satisfaction",
    "over_time",
    "environment_satisfaction",
    "work_life_balance"
]


# ============================================================
# 8. DISPLAY FEATURE TYPES
# ============================================================

print("\n--- NUMERICAL FEATURES ---")

for feature in numeric_features:
    print(feature)


print("\n--- CATEGORICAL FEATURES ---")

for feature in categorical_features:
    print(feature)


# ============================================================
# 9. CREATE PREPROCESSING PIPELINE
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            StandardScaler(),
            numeric_features
        ),
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ]
)


# ============================================================
# 10. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ============================================================
# 11. DISPLAY SPLIT INFORMATION
# ============================================================

print("\n--- DATA SPLIT ---")

print("Training samples:", X_train.shape[0])
print("Testing samples:", X_test.shape[0])


print("\n--- TRAINING TARGET DISTRIBUTION ---")

print(
    y_train.value_counts(normalize=True)
)


print("\n--- TESTING TARGET DISTRIBUTION ---")

print(
    y_test.value_counts(normalize=True)
)


# ============================================================
# 12. PREPROCESS THE DATA
# ============================================================

print("\n--- STARTING PREPROCESSING ---")

X_train_processed = preprocessor.fit_transform(X_train)

X_test_processed = preprocessor.transform(X_test)


print("\n--- PREPROCESSING COMPLETE ---")

print(
    "Original training features:",
    X_train.shape[1]
)

print(
    "Processed training features:",
    X_train_processed.shape[1]
)

print(
    "Original testing features:",
    X_test.shape[1]
)

print(
    "Processed testing features:",
    X_test_processed.shape[1]
)


# ============================================================
# 13. LOGISTIC REGRESSION
# ============================================================

print("\n--- TRAINING LOGISTIC REGRESSION ---")

logistic_model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

logistic_model.fit(
    X_train_processed,
    y_train
)

print("Logistic Regression training complete!")


# ============================================================
# 14. LOGISTIC REGRESSION PREDICTIONS
# ============================================================

y_pred = logistic_model.predict(
    X_test_processed
)

# IMPORTANT:
# predict_proba() gives:
# column 0 = probability of No Attrition
# column 1 = probability of Attrition

y_probability = logistic_model.predict_proba(
    X_test_processed
)


# ============================================================
# 15. LOGISTIC REGRESSION EVALUATION
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)


print("\n======================================")
print("LOGISTIC REGRESSION RESULTS")
print("======================================")

print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1 Score:  {f1:.4f}")


print("\n--- LOGISTIC REGRESSION CLASSIFICATION REPORT ---")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "No Attrition",
            "Attrition"
        ],
        zero_division=0
    )
)


# ============================================================
# 16. DECISION TREE
# ============================================================

print("\n--- TRAINING DECISION TREE ---")

decision_tree = DecisionTreeClassifier(
    random_state=42
)

decision_tree.fit(
    X_train_processed,
    y_train
)

print("Decision Tree training complete!")


# ============================================================
# 17. DECISION TREE PREDICTIONS
# ============================================================

tree_pred = decision_tree.predict(
    X_test_processed
)

tree_probability = decision_tree.predict_proba(
    X_test_processed
)


# ============================================================
# 18. DECISION TREE EVALUATION
# ============================================================

tree_accuracy = accuracy_score(
    y_test,
    tree_pred
)

tree_precision = precision_score(
    y_test,
    tree_pred,
    zero_division=0
)

tree_recall = recall_score(
    y_test,
    tree_pred,
    zero_division=0
)

tree_f1 = f1_score(
    y_test,
    tree_pred,
    zero_division=0
)


print("\n======================================")
print("DECISION TREE RESULTS")
print("======================================")

print(f"Accuracy:  {tree_accuracy:.4f}")
print(f"Precision: {tree_precision:.4f}")
print(f"Recall:    {tree_recall:.4f}")
print(f"F1 Score:  {tree_f1:.4f}")


print("\n--- DECISION TREE CLASSIFICATION REPORT ---")

print(
    classification_report(
        y_test,
        tree_pred,
        target_names=[
            "No Attrition",
            "Attrition"
        ],
        zero_division=0
    )
)


# ============================================================
# 19. RANDOM FOREST
# ============================================================

print("\n--- TRAINING RANDOM FOREST ---")

random_forest = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

random_forest.fit(
    X_train_processed,
    y_train
)

print("Random Forest training complete!")


# ============================================================
# 20. RANDOM FOREST PREDICTIONS
# ============================================================

forest_pred = random_forest.predict(
    X_test_processed
)

forest_probability = random_forest.predict_proba(
    X_test_processed
)


# ============================================================
# 21. RANDOM FOREST EVALUATION
# ============================================================

forest_accuracy = accuracy_score(
    y_test,
    forest_pred
)

forest_precision = precision_score(
    y_test,
    forest_pred,
    zero_division=0
)

forest_recall = recall_score(
    y_test,
    forest_pred,
    zero_division=0
)

forest_f1 = f1_score(
    y_test,
    forest_pred,
    zero_division=0
)


print("\n======================================")
print("RANDOM FOREST RESULTS")
print("======================================")

print(f"Accuracy:  {forest_accuracy:.4f}")
print(f"Precision: {forest_precision:.4f}")
print(f"Recall:    {forest_recall:.4f}")
print(f"F1 Score:  {forest_f1:.4f}")


print("\n--- RANDOM FOREST CLASSIFICATION REPORT ---")

print(
    classification_report(
        y_test,
        forest_pred,
        target_names=[
            "No Attrition",
            "Attrition"
        ],
        zero_division=0
    )
)


# ============================================================
# 22. CONFUSION MATRICES
# ============================================================

logistic_cm = confusion_matrix(
    y_test,
    y_pred
)

tree_cm = confusion_matrix(
    y_test,
    tree_pred
)

forest_cm = confusion_matrix(
    y_test,
    forest_pred
)


print("\n======================================")
print("CONFUSION MATRICES")
print("======================================")


print("\nLogistic Regression:")
print(logistic_cm)


print("\nDecision Tree:")
print(tree_cm)


print("\nRandom Forest:")
print(forest_cm)


# ============================================================
# 23. ROC-AUC
# ============================================================

# We use [:, 1] because column 1 represents
# the probability of Attrition (class 1).

logistic_auc = roc_auc_score(
    y_test,
    y_probability[:, 1]
)

tree_auc = roc_auc_score(
    y_test,
    tree_probability[:, 1]
)

forest_auc = roc_auc_score(
    y_test,
    forest_probability[:, 1]
)


print("\n======================================")
print("ROC-AUC SCORES")
print("======================================")


print(
    f"Logistic Regression: {logistic_auc:.4f}"
)

print(
    f"Decision Tree:       {tree_auc:.4f}"
)

print(
    f"Random Forest:       {forest_auc:.4f}"
)


# ============================================================
# 24. FINAL MODEL COMPARISON
# ============================================================

comparison = pd.DataFrame({

    "Model": [
        "Logistic Regression",
        "Decision Tree",
        "Random Forest"
    ],

    "Accuracy": [
        accuracy,
        tree_accuracy,
        forest_accuracy
    ],

    "Precision": [
        precision,
        tree_precision,
        forest_precision
    ],

    "Recall": [
        recall,
        tree_recall,
        forest_recall
    ],

    "F1 Score": [
        f1,
        tree_f1,
        forest_f1
    ],

    "ROC-AUC": [
        logistic_auc,
        tree_auc,
        forest_auc
    ]
})


print("\n======================================")
print("FINAL MODEL COMPARISON")
print("======================================")

print(
    comparison.to_string(
        index=False
    )
)


# ============================================================
# 25. BEST MODEL BY F1 SCORE
# ============================================================

best_model_row = comparison.loc[
    comparison["F1 Score"].idxmax()
]

print("\n======================================")
print("BEST MODEL BY F1 SCORE")
print("======================================")

print(
    "Model:",
    best_model_row["Model"]
)

print(
    f"F1 Score: {best_model_row['F1 Score']:.4f}"
)

print(
    f"ROC-AUC: {best_model_row['ROC-AUC']:.4f}"
)

# ============================================================
# 26. PROCESSED FEATURE NAMES
# ============================================================

feature_names = preprocessor.get_feature_names_out()


# ============================================================
# 27. RANDOM FOREST FEATURE IMPORTANCE
# ============================================================

feature_importance = random_forest.feature_importances_


importance_df = pd.DataFrame({

    "Feature": feature_names,

    "Importance": feature_importance

})


# Sort by importance

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)


# Clean feature names

importance_df["Display Feature"] = (
    importance_df["Feature"]
    .str.replace("num__", "", regex=False)
    .str.replace("cat__", "", regex=False)
)


# ============================================================
# 28. DISPLAY TOP FEATURES
# ============================================================

top_features = importance_df.head(10)


print("\n======================================")
print("TOP 10 IMPORTANT FEATURES")
print("======================================")


print(
    top_features[
        ["Display Feature", "Importance"]
    ].to_string(index=False)
)

# ============================================================
# 29. BALANCED LOGISTIC REGRESSION
# ============================================================

balanced_logistic = LogisticRegression(
    max_iter=1000,
    random_state=42,
    class_weight="balanced"
)

balanced_logistic.fit(
    X_train_processed,
    y_train
)

balanced_logistic_pred = balanced_logistic.predict(
    X_test_processed
)

balanced_logistic_probability = balanced_logistic.predict_proba(
    X_test_processed
)

balanced_logistic_accuracy = accuracy_score(
    y_test,
    balanced_logistic_pred
)

balanced_logistic_precision = precision_score(
    y_test,
    balanced_logistic_pred,
    zero_division=0
)

balanced_logistic_recall = recall_score(
    y_test,
    balanced_logistic_pred,
    zero_division=0
)

balanced_logistic_f1 = f1_score(
    y_test,
    balanced_logistic_pred,
    zero_division=0
)

balanced_logistic_auc = roc_auc_score(
    y_test,
    balanced_logistic_probability[:, 1]
)

print("\n======================================")
print("BALANCED LOGISTIC REGRESSION")
print("======================================")

print(
    f"Accuracy:  {balanced_logistic_accuracy:.4f}"
)

print(
    f"Precision: {balanced_logistic_precision:.4f}"
)

print(
    f"Recall:    {balanced_logistic_recall:.4f}"
)

print(
    f"F1 Score:  {balanced_logistic_f1:.4f}"
)

print(
    f"ROC-AUC:   {balanced_logistic_auc:.4f}"
)

# ============================================================
# 30. BALANCED DECISION TREE
# ============================================================

balanced_tree = DecisionTreeClassifier(
    random_state=42,
    class_weight="balanced",
    max_depth=5
)

balanced_tree.fit(
    X_train_processed,
    y_train
)

balanced_tree_pred = balanced_tree.predict(
    X_test_processed
)

balanced_tree_probability = balanced_tree.predict_proba(
    X_test_processed
)

balanced_tree_accuracy = accuracy_score(
    y_test,
    balanced_tree_pred
)

balanced_tree_precision = precision_score(
    y_test,
    balanced_tree_pred,
    zero_division=0
)

balanced_tree_recall = recall_score(
    y_test,
    balanced_tree_pred,
    zero_division=0
)

balanced_tree_f1 = f1_score(
    y_test,
    balanced_tree_pred,
    zero_division=0
)

balanced_tree_auc = roc_auc_score(
    y_test,
    balanced_tree_probability[:, 1]
)

print("\n======================================")
print("BALANCED DECISION TREE")
print("======================================")

print(
    f"Accuracy:  {balanced_tree_accuracy:.4f}"
)

print(
    f"Precision: {balanced_tree_precision:.4f}"
)

print(
    f"Recall:    {balanced_tree_recall:.4f}"
)

print(
    f"F1 Score:  {balanced_tree_f1:.4f}"
)

print(
    f"ROC-AUC:   {balanced_tree_auc:.4f}"
)

# ============================================================
# 31. BALANCED RANDOM FOREST
# ============================================================

balanced_forest = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced",
    max_depth=8
)

balanced_forest.fit(
    X_train_processed,
    y_train
)

balanced_forest_pred = balanced_forest.predict(
    X_test_processed
)

balanced_forest_probability = balanced_forest.predict_proba(
    X_test_processed
)

balanced_forest_accuracy = accuracy_score(
    y_test,
    balanced_forest_pred
)

balanced_forest_precision = precision_score(
    y_test,
    balanced_forest_pred,
    zero_division=0
)

balanced_forest_recall = recall_score(
    y_test,
    balanced_forest_pred,
    zero_division=0
)

balanced_forest_f1 = f1_score(
    y_test,
    balanced_forest_pred,
    zero_division=0
)

balanced_forest_auc = roc_auc_score(
    y_test,
    balanced_forest_probability[:, 1]
)

print("\n======================================")
print("BALANCED RANDOM FOREST")
print("======================================")

print(
    f"Accuracy:  {balanced_forest_accuracy:.4f}"
)

print(
    f"Precision: {balanced_forest_precision:.4f}"
)

print(
    f"Recall:    {balanced_forest_recall:.4f}"
)

print(
    f"F1 Score:  {balanced_forest_f1:.4f}"
)

print(
    f"ROC-AUC:   {balanced_forest_auc:.4f}"
)

# ============================================================
# 32. BALANCED MODEL COMPARISON
# ============================================================

improved_comparison = pd.DataFrame({

    "Model": [

        "Logistic Regression",
        "Balanced Logistic Regression",

        "Decision Tree",
        "Balanced Decision Tree",

        "Random Forest",
        "Balanced Random Forest"
    ],

    "Accuracy": [

        accuracy,
        balanced_logistic_accuracy,

        tree_accuracy,
        balanced_tree_accuracy,

        forest_accuracy,
        balanced_forest_accuracy
    ],

    "Precision": [

        precision,
        balanced_logistic_precision,

        tree_precision,
        balanced_tree_precision,

        forest_precision,
        balanced_forest_precision
    ],

    "Recall": [

        recall,
        balanced_logistic_recall,

        tree_recall,
        balanced_tree_recall,

        forest_recall,
        balanced_forest_recall
    ],

    "F1 Score": [

        f1,
        balanced_logistic_f1,

        tree_f1,
        balanced_tree_f1,

        forest_f1,
        balanced_forest_f1
    ],

    "ROC-AUC": [

        logistic_auc,
        balanced_logistic_auc,

        tree_auc,
        balanced_tree_auc,

        forest_auc,
        balanced_forest_auc
    ]
})


print("\n======================================")
print("ORIGINAL VS BALANCED MODELS")
print("======================================")

print(
    improved_comparison.to_string(
        index=False
    )
)

# ============================================================
# 33. SELECT BEST MODEL
# ============================================================

best_model_row = improved_comparison.loc[
    improved_comparison["F1 Score"].idxmax()
]

best_model_name = best_model_row["Model"]


print("\n======================================")
print("FINAL MODEL SELECTION")
print("======================================")

print("Selected model:", best_model_name)

print(
    f"Accuracy:  {best_model_row['Accuracy']:.4f}"
)

print(
    f"Precision: {best_model_row['Precision']:.4f}"
)

print(
    f"Recall:    {best_model_row['Recall']:.4f}"
)

print(
    f"F1 Score:  {best_model_row['F1 Score']:.4f}"
)

print(
    f"ROC-AUC:   {best_model_row['ROC-AUC']:.4f}"
)

# ============================================================
# 34. GET FINAL MODEL OBJECT
# ============================================================

model_mapping = {

    "Logistic Regression":
        logistic_model,

    "Balanced Logistic Regression":
        balanced_logistic,

    "Decision Tree":
        decision_tree,

    "Balanced Decision Tree":
        balanced_tree,

    "Random Forest":
        random_forest,

    "Balanced Random Forest":
        balanced_forest
}


final_model = model_mapping[best_model_name]

# ============================================================
# 35. SAVE FINAL MODEL
# ============================================================

joblib.dump(
    final_model,
    "model/hirewise_model.pkl"
)

print("\nFinal model saved successfully!")

# ============================================================
# 36. SAVE PREPROCESSOR
# ============================================================

joblib.dump(
    preprocessor,
    "model/preprocessor.pkl"
)

print("Preprocessor saved successfully!")

top_features = importance_df.head(10)

print("\n======================================")
print("TOP 10 IMPORTANT FEATURES")
print("======================================")

print(
    top_features[
        ["Display Feature", "Importance"]
    ].to_string(index=False)
)

# ============================================================
# 37. SAVE FEATURE IMPORTANCE
# ============================================================

feature_importance_data = top_features[
    ["Display Feature", "Importance"]
].copy()


joblib.dump(
    feature_importance_data,
    "model/feature_importance.pkl"
)


print("\nFeature importance saved successfully!")

# ============================================================
# 38. SAVE MODEL INFORMATION
# ============================================================

# ============================================================
# SAVE MODEL INFORMATION
# ============================================================

model_info = {
    "model_name": best_model_name,
    "task": "Binary Classification",
    "target": "Employee Attrition"
}

joblib.dump(
    model_info,
    "model/model_info.pkl"
)

print("Model information saved successfully!")

# ============================================================
# END
# ============================================================

print("\n======================================")
print("ALL CLASSIFICATION MODELS COMPLETED")
print("======================================")