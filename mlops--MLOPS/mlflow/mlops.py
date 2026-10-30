import pandas as pd

# MLflow
import mlflow
import mlflow.sklearn

# Scikit-learn datasets
from sklearn.datasets import load_iris

# Train-test split
from sklearn.model_selection import train_test_split

# ML algorithms
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# Evaluation metrics
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

iris=load_iris()
x=iris.data
y=iris.target

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.25,random_state=0)

mlflow.set_experiment('Iris Classification_experiment')

# logistic regression model

with mlflow.start_run():

    # 1. Create model
    lr_model = LogisticRegression(
        solver="lbfgs",
        max_iter=200
    )

    # 2. Train model
    lr_model.fit(x_train, y_train)

    print("Model training completed!")

    # 3. Make predictions
    lr_prediction = lr_model.predict(x_test)

    # 4. Calculate accuracy
    lr_accuracy = accuracy_score(y_test, lr_prediction)

    # 5. Confusion matrix
    lr_conf_matrix = confusion_matrix(y_test, lr_prediction)

    # 6. Log parameters and metrics
    mlflow.log_param("model", "LogisticRegression")
    mlflow.log_param("solver", "lbfgs")
    mlflow.log_param("max_iter", 200)

    mlflow.log_metric("accuracy", lr_accuracy)

    # 7. Plot confusion matrix
    plt.figure(figsize=(6, 6))

    sns.heatmap(
        lr_conf_matrix,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=iris.target_names,
        yticklabels=iris.target_names
    )

    plt.title("Confusion Matrix - Logistic Regression")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    plt.savefig("lr_confusion_matrix.png")
    mlflow.log_artifact("lr_confusion_matrix.png")
    plt.close()

    # 8. Log model to MLflow
    mlflow.sklearn.log_model(
        lr_model,
        name="Logistic_regression_model"
    )

    # 9. Register model
    log_model_uri = (
        f"runs:/{mlflow.active_run().info.run_id}/Logistic_regression_model"
    )

    registered_model = mlflow.register_model(
        log_model_uri,
        "Logistic_Regression_model"
    )

# 10. Display results
print(f"Logistic Regression Model Accuracy: {lr_accuracy}")
print("Confusion Matrix:")
print(lr_conf_matrix)


# random forest model


with mlflow.start_run():

    # 1. Create Random Forest model
    rf_model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    # 2. Train model
    rf_model.fit(x_train, y_train)

    print("Random Forest training completed!")

    # 3. Make predictions
    rf_prediction = rf_model.predict(x_test)

    # 4. Calculate accuracy
    rf_accuracy = accuracy_score(y_test, rf_prediction)

    # 5. Confusion matrix
    rf_conf_matrix = confusion_matrix(y_test, rf_prediction)

    # 6. Log parameters
    mlflow.log_param("model", "RandomForestClassifier")
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("random_state", 42)

    # 7. Log accuracy
    mlflow.log_metric("accuracy", rf_accuracy)

    # 8. Create confusion matrix
    plt.figure(figsize=(6, 6))

    sns.heatmap(
        rf_conf_matrix,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=iris.target_names,
        yticklabels=iris.target_names
    )

    plt.title("Confusion Matrix - Random Forest")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    plt.savefig("rf_confusion_matrix.png")
    mlflow.log_artifact("rf_confusion_matrix.png")
    plt.close()

    # 9. Log Random Forest model
    mlflow.sklearn.log_model(
        rf_model,
        name="random_forest_model",
        skops_trusted_types=["sklearn.tree._tree.Tree"]
    )

    # 10. Register model
    rf_model_uri = (
        f"runs:/{mlflow.active_run().info.run_id}/random_forest_model"
    )

    rf_registered_model = mlflow.register_model(
        rf_model_uri,
        "Random_Forest_model"
    )

# 11. Display results
print(f"Random Forest Accuracy: {rf_accuracy}")
print("Random Forest Confusion Matrix:")
print(rf_conf_matrix)






     






    


