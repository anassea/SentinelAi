import json
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import numpy as np

def train_isolation_forest(data, contamination):
    isolation_forest = IsolationForest(contamination=contamination, random_state=42)
    isolation_forest.fit(data)
    return isolation_forest

def get_css_class(criticality):
    if criticality == 'normal':
        return 'normal'
    elif criticality == 'medium':
        return 'medium'
    elif criticality == 'critical':
        return 'critical'
    else:
        return 'normal'  # Valeur par défaut si la criticité n'est pas reconnue

def detect_anomalies():
    # Charger les données du fichier log
    with open('../log.json', 'r') as file:
        log_data = json.load(file)

    # Convertir les données en DataFrame pandas
    df = pd.DataFrame(log_data)

    # Sélectionner les colonnes pour l'analyse
    selected_features = ['http_status_code', 'hour', 'day_of_week', 'month', 'year']

    # Ajouter les colonnes resource_usage s'ils existent
    if any('resource_usage' in event for event in log_data):
        for event in log_data:
            if 'resource_usage' in event:
                for resource, value in event['resource_usage'].items():
                    if resource not in selected_features:
                        selected_features.append(resource)

    # Remplacer les valeurs manquantes par 0
    df.fillna(0, inplace=True)

    # Convertir les pourcentages en valeurs numériques
    for feature in ['cpu', 'ram', 'storage']:
        if feature in selected_features:
            df[feature] = df['resource_usage'].apply(
                lambda x: float(x[feature].rstrip('%')) / 100 if feature in x else 0)

    # Ajouter des caractéristiques temporelles
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['month'] = df['timestamp'].dt.month
    df['year'] = df['timestamp'].dt.year

    # Agrégation des données par heure
    hourly_aggregates = df.groupby('hour')[['cpu', 'ram', 'storage']].mean().add_suffix('_hourly')

    # Combinaison des caractéristiques agrégées avec le DataFrame original
    df = pd.merge(df, hourly_aggregates, left_on='hour', right_index=True)

    # Exclure les colonnes non numériques du sous-ensemble de données
    numeric_features = [col for col in selected_features if col != 'timestamp']
    X = df[numeric_features]

    # Normalisation des données
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Définir une plage de contamination
    contamination_range = np.linspace(0.01, 0.2, 20)

    best_model = None
    best_anomaly_score = float('-inf')

    # Recherche du meilleur modèle Isolation Forest
    for contamination in contamination_range:
        isolation_forest_model = train_isolation_forest(X_scaled, contamination)
        anomaly_scores = isolation_forest_model.decision_function(X_scaled)
        if anomaly_scores.mean() > best_anomaly_score:
            best_model = isolation_forest_model
            best_anomaly_score = anomaly_scores.mean()

    # Ajuster automatiquement le seuil de détection des anomalies
    threshold = np.percentile(best_model.decision_function(X_scaled), 100 * (1 - best_anomaly_score))

    # Prédire les anomalies dans les données en utilisant le meilleur modèle Isolation Forest
    anomalies_mask = best_model.decision_function(X_scaled) < threshold

    if np.any(anomalies_mask):
        anomalies = df[anomalies_mask].copy()  # Copie explicite du DataFrame

        # Recalculer les scores d'anomalie pour les données sélectionnées
        anomaly_scores_selected = best_model.decision_function(X_scaled[anomalies_mask])
        anomalies.loc[:, 'anomaly_score'] = anomaly_scores_selected

        # Déterminer le niveau de criticité de chaque anomalie
        anomalies['criticality'] = pd.cut(anomalies['anomaly_score'], bins=[float('-inf'), -0.05, 0.05, float('inf')],
                                          labels=['critical', 'medium', 'normal'])

        # Écrire les résultats dans le fichier JavaScript Incidents.js
        with open("C:\\Users\\anasse\\PycharmProjects\\pythonProject\\src\\components\\Incidents.js", "w") as js_file:
            js_file.write("import React from 'react';\n\n")
            js_file.write("function Incidents() {\n")
            js_file.write("  return (\n")
            js_file.write("    <div>\n")
            js_file.write("      <h2>Liste des incidents</h2>\n")
            js_file.write("      <table border='1'>\n")
            js_file.write("        <tr><th>Timestamp</th><th>Message</th><th>Anomaly Score</th><th>Criticality</th></tr>\n")
            for index, incident in anomalies.iterrows():
                # Déterminer la classe CSS en fonction de la criticité
                css_class = get_css_class(incident['criticality'])
                js_file.write(f"        <tr key='{index}'>\n")
                js_file.write(f"          <td className='{css_class}'>{incident['timestamp']}</td><td className='{css_class}'>{incident['message']}</td><td className='{css_class}'>{incident['anomaly_score']}</td><td className='{css_class}'>{incident['criticality']}</td>\n")
                js_file.write("        </tr>\n")
            js_file.write("      </table>\n")
            js_file.write("    </div>\n")
            js_file.write("  );\n}\n\n")
            js_file.write("export default Incidents;\n")

    else:
        return "Aucune anomalie détectée."

if __name__ == '__main__':
    detect_anomalies()
