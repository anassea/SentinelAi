import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Charger les fichiers de logs dans un DataFrame Pandas
log_data = pd.read_csv('./logs.csv')

# Concaténer les colonnes existantes pour créer une colonne 'texte'
log_data['texte'] = log_data['utilisateur'] + ' ' + log_data['activite'] + ' ' + log_data['base_de_donnees'] + ' ' + log_data['fichier']

# Remplacer les valeurs NaN dans la colonne 'texte' par une chaîne vide
log_data['texte'] = log_data['texte'].fillna('')

# Utiliser TF-IDF pour extraire des caractéristiques textuelles
tfidf_vectorizer = TfidfVectorizer()
X_tfidf = tfidf_vectorizer.fit_transform(log_data['texte'])

# Normaliser les données
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_tfidf.toarray())

# Entraîner le modèle Isolation Forest
model = IsolationForest(contamination=0.01)  # taux d'anomalie estimé
model.fit(X_scaled)

# Calculer les scores d'anomalie
anomaly_scores = model.decision_function(X_scaled)

# Ajouter les scores d'anomalie au DataFrame original
log_data['anomaly_score'] = anomaly_scores

# Afficher les données avec les scores d'anomalie
plt.figure(figsize=(10, 6))
plt.plot(log_data.index, log_data['anomaly_score'], label='Score d\'anomalie', color='blue')
plt.scatter(log_data[log_data['anomaly_score'] < 0].index, log_data[log_data['anomaly_score'] < 0]['anomaly_score'], label='Anomalies', color='red')
plt.title('Détection d\'anomalies')
plt.xlabel('Index')
plt.ylabel('Score d\'anomalie')
plt.legend()
plt.show()

# Définir les seuils pour les catégories de gravité
seuil_critical = -0.5
seuil_medium = -0.3

# Mapper les scores d'anomalie aux catégories de gravité
log_data['severity'] = 'Normal'
log_data.loc[log_data['anomaly_score'] < seuil_critical, 'severity'] = 'Critical'
log_data.loc[(log_data['anomaly_score'] >= seuil_critical) & (log_data['anomaly_score'] < seuil_medium), 'severity'] = 'Medium'

# Afficher les résultats par catégories de gravité dans un tableau
resultats = log_data.groupby('severity').size().reset_index(name='count')
print(resultats)
