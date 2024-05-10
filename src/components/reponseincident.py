from flask import Flask, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes and methods


def load_and_prepare_data():
    # Reading the CSV file and preparing data
    df = pd.read_csv("../../logs.csv")
    df = pd.get_dummies(df, columns=['Utilisateur', 'Base_donnee'])
    X = df.drop(['Timestamp', 'Type', 'Fichier', 'Description'], axis=1)
    y = df['Type']
    return train_test_split(X, y, test_size=0.2, random_state=42)


def train_model(X_train, y_train):
    # Define the hyperparameters grid
    param_grid = {
        'n_estimators': [50, 100, 150],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    rf = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(rf, param_grid, cv=5, n_jobs=-1, verbose=2)
    grid_search.fit(X_train, y_train)
    return grid_search


@app.route('/classification-report', methods=['GET'])
def get_classification_report():
    X_train, X_test, y_train, y_test = load_and_prepare_data()
    grid_search = train_model(X_train, y_train)
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)

    # Generate classification report
    report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)

    # Generate recommendations based on prediction
    recommendations = {
        "intrusion": "Implement an intrusion detection system and strengthen password security.",
        "Sabotage": "Monitor suspicious user activities and restrict access to sensitive resources. Ensure regular data backup.",
        "connexion": "Set up two-factor authentication to enhance connection security. Use VPNs for remote connections.",
        "lecture": "Review file access permissions and restrict access to sensitive data. Monitor access to sensitive files.",
        "écriture": "Strengthen access controls and limit write privileges to prevent unauthorized changes. Conduct regular audits of data modifications.",
        "tentative": "Block access for suspicious users and revoke their access privileges. Review activity logs to identify unauthorized access attempts."
    }

    recommendations_list = [
        {"Alert": idx + 1, "ID": df.loc[idx, 'Timestamp'], "Type": pred,
         "Recommendation": recommendations.get(pred, "Normal state.")}
        for idx, pred in enumerate(best_model.predict(X_test))
    ]

    response_data = {
        "best_params": grid_search.best_params_,
        "classification_report": report,
        "recommendations": recommendations_list
    }

    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True, port=5003)
