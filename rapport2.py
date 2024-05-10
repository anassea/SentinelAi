import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, send_file, after_this_request
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os

app = Flask(__name__)

@app.route('/rapport', methods=['GET'])
def download_report():
    # Lecture des données à partir d'un fichier CSV
    incident_data = pd.read_csv('./logs.csv')

    # Générer et sauvegarder les graphiques
    if 'Type' in incident_data.columns:
        plt.figure(figsize=(8, 6))
        incident_data['Type'].value_counts().plot(kind='bar', color='skyblue')
        plt.title('Répartition des types d\'incidents')
        plt.xlabel('Type d\'incident')
        plt.ylabel('Nombre d\'incidents')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('incident_distribution.png')
        plt.close()

    if 'Timestamp' in incident_data.columns:
        incident_data['Timestamp'] = pd.to_datetime(incident_data['Timestamp'])
        incident_data['Date'] = incident_data['Timestamp'].dt.date
        incidents_by_date = incident_data.groupby('Date').size()
        plt.figure(figsize=(10, 6))
        incidents_by_date.plot(color='orange')
        plt.title('Évolution du nombre d\'incidents au fil du temps')
        plt.xlabel('Date')
        plt.ylabel('Nombre d\'incidents')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('incident_evolution.png')
        plt.close()

    # Générer le PDF du rapport
    pdf_filename = 'rapport_incident1.pdf'
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()

    # Créer le contenu du rapport
    elements = [
        Paragraph('Rapport d\'incidents', styles['Title']),
        Spacer(1, 12),
        Image('incident_distribution.png', width=400, height=300) if 'Type' in incident_data.columns else '',
        Spacer(1, 12),
        Image('incident_evolution.png', width=400, height=300) if 'Timestamp' in incident_data.columns else '',
        Spacer(1, 12),
        Paragraph('<b>Statistiques générales sur les incidents :</b>', styles['Heading3'])
    ]

    # Recommandations
    elements.append(Paragraph('<b>Recommandations :</b>', styles['Heading2']))

    # Analyse des tendances des incidents
    elements.append(Paragraph('<b>Analyse des tendances des incidents :</b>', styles['Heading3']))
    # Analyse des tendances en fonction des types d'incidents
    if 'Type' in incident_data.columns and 'Timestamp' in incident_data.columns:
        trend_analysis = incident_data.groupby(['Type', pd.Grouper(key='Timestamp', freq='M')]).size().unstack(
            fill_value=0)
        # Ajouter ici une analyse des tendances en fonction des types d'incidents, des périodes de temps, etc.
        elements.append(
            Paragraph(f"Analyse des tendances en fonction des types d'incidents : {trend_analysis}", styles['Normal']))
        # Ajouter une courbe pour chaque type d'incident
        plt.figure(figsize=(10, 6))
        for incident_type in trend_analysis.columns:
            plt.plot(trend_analysis.index, trend_analysis[incident_type], label=incident_type)
        plt.title('Évolution du nombre d\'incidents par type au fil du temps')
        plt.xlabel('Mois')
        plt.ylabel('Nombre d\'incidents')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        trend_plot_filename = 'incident_trend.png'
        plt.savefig(trend_plot_filename)
        plt.close()
        elements.append(Image(trend_plot_filename, width=400, height=300))
    else:
        elements.append(
            Paragraph('Données insuffisantes pour l\'analyse des tendances des incidents.', styles['Normal']))

    # Identification des vulnérabilités critiques
    elements.append(Paragraph('<b>Identification des vulnérabilités critiques :</b>', styles['Heading3']))
    # Analyse des incidents les plus fréquents ou graves
    if 'Type' in incident_data.columns:
        most_common_incidents = incident_data['Type'].value_counts().head(5)
        # Ajouter ici une analyse des incidents les plus fréquents ou graves, des points faibles du système, etc.
        elements.append(
            Paragraph(f"Incidents les plus fréquents ou graves : {most_common_incidents}", styles['Normal']))
    else:
        elements.append(
            Paragraph('Aucun incident identifié pour l\'analyse des vulnérabilités critiques.', styles['Normal']))

    # Statistiques générales sur les incidents
    elements.append(Paragraph('<b>Statistiques générales sur les incidents :</b>', styles['Heading3']))
    if 'Type' in incident_data.columns:
        total_incidents = len(incident_data)
        unique_types = len(incident_data['Type'].unique())
        # Ajouter ici des statistiques générales telles que le nombre total d'incidents, le nombre de types d'incidents uniques, etc.
        elements.append(Paragraph(f"Nombre total d'incidents : {total_incidents}", styles['Normal']))
        elements.append(Paragraph(f"Nombre de types d'incidents uniques : {unique_types}", styles['Normal']))
    else:
        elements.append(Paragraph('Aucune donnée d\'incident disponible pour les statistiques.', styles['Normal']))

    # Statistiques générales sur les incidents

    # Propositions pour améliorer la sécurité
    elements.append(Paragraph('<b>Propositions pour améliorer la sécurité :</b>', styles['Heading3']))
    # Ajouter des recommandations spécifiques basées sur les analyses et les connaissances en cybersécurité
    elements.append(Paragraph('Mise à jour régulière des logiciels et correctifs de sécurité.', styles['Normal']))
    elements.append(Paragraph('Renforcement de la formation et de la sensibilisation à la sécurité pour les utilisateurs.', styles['Normal']))
    elements.append(Paragraph('Mettre en place un système de détection d\'intrusion et renforcer la sécurité des mots de passe.', styles['Normal']))
    elements.append(Paragraph('Mise en place d\'une stratégie de surveillance et de détection des intrusions.', styles['Normal']))

    # Ajouter ici des recommandations spécifiques telles que la mise à jour des logiciels, la mise en place de politiques de sécurité, etc.

    # Créer un tableau pour les données d'incidents
    incident_table_data = [incident_data.columns.tolist()] + incident_data.values.tolist()
    incident_table = Table(incident_table_data)

    # Appliquer un style au tableau
    for i in range(len(incident_table_data)):
        if i == 0:
            bg_color = colors.grey
            text_color = colors.whitesmoke
            font_name = 'Helvetica-Bold'
        else:
            bg_color = colors.beige if i % 2 == 0 else colors.white
            text_color = colors.black
            font_name = 'Helvetica'
        incident_table.setStyle([
            ('BACKGROUND', (0, i), (-1, i), bg_color),
            ('TEXTCOLOR', (0, i), (-1, i), text_color),
            ('ALIGN', (0, i), (-1, i), 'CENTER'),
            ('FONTNAME', (0, i), (-1, i), font_name),
            ('BOTTOMPADDING', (0, i), (-1, i), 12),
            ('GRID', (0, i), (-1, i), 1, colors.black)
        ])

    elements.append(Paragraph('Liste des incidents avec des informations détaillées :', styles['Heading3']))
    elements.append(incident_table)

    # Écrire le PDF
    doc.build(elements)

    # Supprimer les fichiers temporaires après l'envoi du rapport
    @after_this_request
    def remove_files(response):
        try:
            os.remove(pdf_filename)
            os.remove('incident_distribution.png')
            os.remove('incident_evolution.png')
        except Exception as error:
            app.logger.error("Error removing or closing downloaded file handle", error)
        return response

    return send_file(pdf_filename, as_attachment=True, mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True, port=3000)