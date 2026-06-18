# 🧰 Kit d'Évaluation de la Médiation Indirecte
Cette application web interactive est un outil d'aide à la saisie et à l'analyse de données de terrain pour l'évaluation de dispositifs de médiation culturelle (ex: écrans tactiles, livrets-jeux, outils sensoriels...).

Elle permet aux professionnels de la médiation de cartographier l'engagement des publics (individuels ou collectifs) et de générer automatiquement des indicateurs démographiques croisés.

## 🚀 Fonctionnalités principales
- Configuration sur mesure : Définition des caractéristiques du dispositif, des critères de réussite personnalisés et des actions spécifiques à observer.
- Saisie Terrain Fluide : Formulaires adaptés pour l'enregistrement rapide des comportements, que le public soit seul ou en groupe (famille, fratrie).
- Tableau de Bord Dynamique : Visualisation immédiate des données via des graphiques interactifs (répartition par genre, pyramide des âges, matrice d'analyse croisée).
- Gestion des Sauvegardes : Export et import des sessions d'études au format JSON pour conserver un historique sans base de données lourde.

## 🛠️ Installation locale (Optionnelle)
Si vous souhaitez exécuter cette application sur votre machine plutôt que via le serveur Web :

Clonez ce dépôt ou téléchargez les fichiers.
Installez les dépendances requises :
```bash
pip install -r requirements.txt
```

Lancez l'application Streamlit :
```bash
streamlit run evaluation_mediation.py
```

## 📦 Fichiers du dépôt
`mediation.py` : Code source principal de l'application Streamlit.
`requirements.txt` : Liste des bibliothèques Python nécessaires au déploiement (Streamlit, Pandas, Plotly).

_Développé dans le cadre de l'optimisation des outils d'évaluation de la médiation culturelle._
