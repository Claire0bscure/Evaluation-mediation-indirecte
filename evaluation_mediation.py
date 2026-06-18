import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

# Configuration de la page
st.set_page_config(
    page_title="Kit MCI - Évaluation Pédagogique", 
    layout="wide"
)

# ==========================================
# INITIALISATION DES VALEURS PAR DÉFAUT
# ==========================================
def initialiser_session():
    if "dispositif_config" not in st.session_state:
        st.session_state.dispositif_config = {
            "nom": "Mallette multisensorielle",
            "format": "Analogique",
            "support": "Jeu de manipulation",
            "zone_dispo": "Espace Famille (Salle 3)",
            "acces": "Accès libre",
            "freq": "Quotidienne (chaque matin)"
        }
    if "liste_criteres" not in st.session_state:
        st.session_state.liste_criteres = [
            "Susciter la manipulation physique par les enfants",
            "Prolonger le temps d'arrêt dans la salle de transition"
        ]
    if "liste_actions" not in st.session_state:
        st.session_state.liste_actions = [
            "Le visiteur discute avec ses proches du dispositif",
            "Le visiteur manipule les objets / le kit"
        ]
    if "obs_brutes" not in st.session_state:
        st.session_state.obs_brutes = []

initialiser_session()

# Constantes de l'application
AGES = [
    "Tous petits", "Enfants", "Adolescents", 
    "Jeunes adultes", "Adultes", "Séniors"
]
GENRES = ["Homme", "Femme", "Ne se prononce pas"]
OCCURRENCES = [
    "Non", "Brièvement", "Plusieurs fois", "De manière continue"
]
CRITERES_EVAL_P13 = [
    "Satisfaction face à l’utilisation observée",
    "Popularité du dispositif estimée",
    "Qualité matérielle (fragile ou robuste)",
    "Rapport prix / impact",
    "L’utilisation observée et l’utilisation attendue sont similaires",
    "Le dispositif réussit à ponctuer le parcours de visite"
]

LISTE_FORMATS = ["Analogique", "Numérique", "Mixte"]
LISTE_SUPPORTS = [
    "Jeu de manipulation", "Livret-jeu", 
    "Jeu de société", "Outil sensoriel"
]
LISTE_ACCES = ["Accès libre", "Sur demande / Au comptoir", "Autre"]
LISTE_MAINT = [
    "Quotidienne (chaque matin)", "Hebdomadaire", "À la demande"
]

# ==========================================
# FONCTION DE CHARGEMENT COULISSES (CALLBACK)
# ==========================================
def charger_sauvegarde_callback():
    fichier = st.session_state["json_uploader"]
    if fichier is not None:
        try:
            loaded_data = json.load(fichier)
            # Écriture forcée et directe dans le State profond
            st.session_state.dispositif_config = loaded_data.get(
                "dispositif_config", {}
            )
            st.session_state.liste_criteres = loaded_data.get(
                "liste_criteres", []
            )
            st.session_state.liste_actions = loaded_data.get(
                "liste_actions", []
            )
            st.session_state.obs_brutes = loaded_data.get(
                "obs_brutes", []
            )
            st.session_state["upload_success"] = True
        except Exception as e:
            st.session_state["upload_error"] = str(e)

# ==========================================
# SIDEBAR : EXPORT / IMPORT SÉCURISÉ
# ==========================================
with st.sidebar:
    st.header("💾 Données de l'étude")
    
    nom_createur = st.text_input(
        "Nom du Responsable", 
        value=st.session_state.dispositif_config.get(
            "createur", "Équipe Médiation"
        )
    )
    st.session_state.dispositif_config["createur"] = nom_createur
    
    st.write("---")
    
    st.subheader("📂 Charger une sauvegarde")
    st.file_uploader(
        "Choisir un fichier .json", 
        type=["json"],
        key="json_uploader",
        on_change=charger_sauvegarde_callback
    )
    
    # Affichage des retours utilisateurs hors du flux d'exécution
    if st.session_state.pop("upload_success", False):
        st.success("✅ Sauvegarde verrouillée avec succès !")
    if "upload_error" in st.session_state:
        st.error(f"❌ Erreur de fichier : {st.session_state.pop('upload_error')}")
            
    st.write("---")
    
    st.subheader("📥 Exporter l'étude")
    data_to_save = {
        "dispositif_config": st.session_state.dispositif_config,
        "liste_criteres": st.session_state.liste_criteres,
        "liste_actions": st.session_state.liste_actions,
        "obs_brutes": st.session_state.obs_brutes
    }
    json_string = json.dumps(data_to_save, indent=2, ensure_ascii=False)
    st.download_button(
        label="📥 Télécharger le JSON",
        data=json_string,
        file_name="resultats_evaluation_kit.json",
        mime="application/json",
        use_container_width=True
    )

# --- STRUCTURE DES ONGLETS ---
st.title("🧰 Kit d'Évaluation de la Médiation Indirecte")

tab_prep, tab_obs, tab_anal = st.tabs([
    "📋 PARTIE 1 : Fiche Technique & Configuration", 
    "👁️ PARTIE 2 : Saisie Terrain & Formulaires", 
    "📊 PARTIE 3 : Analyses & Graphiques"
])

# ==========================================
# PARTIE 1 : FICHE TECHNIQUE & CONFIGURATION
# ==========================================
with tab_prep:
    st.header("1. Caractéristiques du kit de médiation")
    
    cfg = st.session_state.dispositif_config
    
    idx_fmt = LISTE_FORMATS.index(cfg.get("format")) if cfg.get("format") in LISTE_FORMATS else 0
    idx_sup = LISTE_SUPPORTS.index(cfg.get("support")) if cfg.get("support") in LISTE_SUPPORTS else 0
    idx_acc = LISTE_ACCES.index(cfg.get("acces")) if cfg.get("acces") in LISTE_ACCES else 0
    idx_mnt = LISTE_MAINT.index(cfg.get("freq")) if cfg.get("freq") in LISTE_MAINT else 0

    with st.form("form_prep_fix"):
        col1, col2 = st.columns(2)
        with col1:
            nom_disp = st.text_input(
                "Nom du kit pédagogique", 
                value=cfg.get("nom", "")
            )
            format_mci = st.selectbox(
                "Format principal du kit", 
                LISTE_FORMATS, 
                index=idx_fmt
            )
            type_support = st.selectbox(
                "Nature du support", 
                LISTE_SUPPORTS, 
                index=idx_sup
            )
        with col2:
            zone_dispo = st.text_input(
                "Zone de disponibilité du kit", 
                value=cfg.get("zone_dispo", "")
            )
            acces_disp = st.selectbox(
                "Modalité d'accès au dispositif", 
                LISTE_ACCES, 
                index=idx_acc
            )
            freq_maint = st.selectbox(
                "Fréquence de la maintenance", 
                LISTE_MAINT, 
                index=idx_mnt
            )
        
        if st.form_submit_button("Sauvegarder la configuration de base"):
            st.session_state.dispositif_config.update({
                "nom": nom_disp, "format": format_mci, "support": type_support,
                "zone_dispo": zone_dispo, "acces": acces_disp, "freq": freq_maint
            })
            st.success("✅ Configuration sauvegardée !")

    st.write("---")
    
    st.header("🎯 Objectifs & Critères Majeurs de Réussite")
    criteres_mis_a_jour = []
    for i, critere_suggere in enumerate(st.session_state.liste_criteres):
        col_c1, col_c2 = st.columns([6, 1])
        with col_c1:
            texte_critere = st.text_input(
                f"Critère majeur {i+1}", 
                value=critere_suggere, 
                key=f"crit_input_{i}"
            )
            criteres_mis_a_jour.append(texte_critere)
        with col_c2:
            st.write("#")
            if st.button("🗑️", key=f"del_crit_{i}"):
                st.session_state.liste_criteres.pop(i)
                st.rerun()
    st.session_state.liste_criteres = criteres_mis_a_jour

    if st.button("➕ Ajouter un critère personnalisé"):
        st.session_state.liste_criteres.append("")
        st.rerun()

    st.write("---")
    
    st.header("🏃 Actions spécifiques du public à observer")
    actions_mises_a_jour = []
    for j, action_suggeree in enumerate(st.session_state.liste_actions):
        col_a1, col_a2 = st.columns([6, 1])
        with col_a1:
            texte_action = st.text_input(
                f"Action {j+1}", 
                value=action_suggeree, 
                key=f"act_input_{j}"
            )
            actions_mises_a_jour.append(texte_action)
        with col_a2:
            st.write("#")
            if st.button("🗑️", key=f"del_act_{j}"):
                st.session_state.liste_actions.pop(j)
                st.rerun()
    st.session_state.liste_actions = actions_mises_a_jour

    if st.button("➕ Ajouter une action à observer"):
        st.session_state.liste_actions.append("")
        st.rerun()

    if st.button("💾 Valider et figer la configuration globale", type="primary"):
        st.session_state.dispositif_config["criteres"] = [
            c for c in st.session_state.liste_criteres if c.strip() != ""
        ]
        st.session_state.dispositif_config["actions_terrain"] = [
            a for a in st.session_state.liste_actions if a.strip() != ""
        ]
        st.success("🚀 Configuration du kit verrouillée !")

# ==========================================
# PARTIE 2 : SAISIE TERRAIN ADAPTÉE
# ==========================================
with tab_obs:
    st.header("2. Saisie des observations terrain")
    type_visite = st.radio(
        "Type d'utilisation constatée :", 
        ["Individuelle (Un seul visiteur)", "Groupée (Famille / Groupe)"], 
        horizontal=True
    )
    
    st.write("---")
    
    if type_visite == "Individuelle (Un seul visiteur)":
        st.markdown("### 👤 Saisie unique pour Visiteur Individuel")
        with st.form("form_individuel", clear_on_submit=True):
            col_i1, col_i2 = st.columns(2)
            with col_i1:
                g_ind = st.radio("Genre du visiteur", GENRES, horizontal=True)
                a_ind = st.selectbox("Tranche d'âge du visiteur", AGES)
            with col_i2:
                c_ind = st.radio(
                    "Comportement / Considération", 
                    ["Pas remarqué", "Remarqué mais ignoré", "Remarqué et utilisé"]
                )
            
            st.markdown("##### Actions spécifiques constatées :")
            dict_actions_ind = {}
            for act in st.session_state.liste_actions:
                if act.strip():
                    dict_actions_ind[act] = st.select_slider(
                        f"Occurrence : {act}", 
                        options=OCCURRENCES, 
                        key=f"ind_{act}"
                    )
            
            if st.form_submit_button("Enregistrer le visiteur individuel"):
                st.session_state.obs_brutes.append({
                    "type": "Individuelle",
                    "taille_groupe": 1,
                    "profils": [{"genre": g_ind, "age": a_ind, "quantite": 1}],
                    "considerations": {
                        "Pas remarqué": 1 if c_ind == "Pas remarqué" else 0, 
                        "Remarqué mais ignoré": 1 if c_ind == "Remarqué mais ignoré" else 0, 
                        "Remarqué et utilisé": 1 if c_ind == "Remarqué et utilisé" else 0
                    },
                    "actions": dict_actions_ind
                })
                st.toast("✅ Données individuelles enregistrées !", icon="👤")
                st.rerun()
                
    else:
        st.markdown("### 👥 Décompte Global pour Utilisation en Groupe")
        with st.form("form_groupe", clear_on_submit=True):
            taille_groupe = st.number_input(
                "Nombre de personnes au total dans le groupe", 
                min_value=1, 
                value=2
            )
            
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                st.markdown("**Membres observés par Genre :**")
                g_inputs = {
                    g: st.number_input(
                        f"Total - {g}", min_value=0, step=1, key=f"grp_g_{g}"
                    ) for g in GENRES
                }
            with col_g2:
                st.markdown("**Membres observés par Âge :**")
                a_inputs = {
                    a: st.number_input(
                        f"Total - {a}", min_value=0, step=1, key=f"grp_a_{a}"
                    ) for a in AGES
                }
                
            st.markdown("---")
            st.markdown("##### Niveau d'engagement global dans le groupe :")
            col_c1, col_c2, col_c3 = st.columns(3)
            c_pas = col_c1.number_input("Nombre : N'ont pas remarqué", min_value=0, step=1)
            c_ign = col_c2.number_input("Nombre : Ont ignoré", min_value=0, step=1)
            c_uti = col_c3.number_input("Nombre : Ont manipulé / utilisé", min_value=0, step=1)
            
            st.markdown("##### Actions constatées au sein du collectif :")
            dict_actions_grp = {}
            for act in st.session_state.liste_actions:
                if act.strip():
                    dict_actions_grp[act] = st.select_slider(
                        f"Intensité globale : {act}", 
                        options=["Aucun membre", "Minorité", "Majorité", "Tout le groupe"], 
                        key=f"grp_{act}"
                    )
            
            if st.form_submit_button("Enregistrer le groupe"):
                sum_g = sum(g_inputs.values())
                sum_a = sum(a_inputs.values())
                sum_c = c_pas + c_ign + c_uti
                
                if sum_g > taille_groupe or sum_a > taille_groupe or sum_c > taille_groupe:
                    st.error("❌ Erreur de cohérence : Les sous-totaux dépassent la taille du groupe.")
                else:
                    liste_profils_groupe = []
                    for g, q_g in g_inputs.items():
                        for a, q_a in a_inputs.items():
                            if q_g > 0 and q_a > 0:
                                min_repart = min(q_g, q_a)
                                liste_profils_groupe.append({
                                    "genre": g, "age": a, "quantite": min_repart
                                })
                    
                    st.session_state.obs_brutes.append({
                        "type": "Collective",
                        "taille_groupe": taille_groupe,
                        "profils": liste_profils_groupe if liste_profils_groupe else [
                            {"genre": "Ne se prononce pas", "age": "Adultes", "quantite": taille_groupe}
                        ],
                        "considerations": {"Pas remarqué": c_pas, "Remarqué mais ignoré": c_ign, "Remarqué et utilisé": c_uti},
                        "actions": dict_actions_grp
                    })
                    st.toast("✅ Données de groupe enregistrées !", icon="👥")
                    st.rerun()

# ==========================================
# PARTIE 3 : ANALYSES & GRAPHES AVANCÉS
# ==========================================
with tab_anal:
    st.header("📊 Tableau de Bord Démographique Filtrable")
    
    if not st.session_state.obs_brutes:
        st.info("Aucune observation disponible. Saisissez ou importez des données.")
    else:
        rows_profils = []
        rows_considerations = []
        
        for idx, obs in enumerate(st.session_state.obs_brutes):
            for prof in obs["profils"]:
                rows_profils.append({
                    "Session_ID": idx, "Type": obs["type"],
                    "Genre": prof["genre"], "Age": prof["age"], "Quantite": prof["quantite"]
                })
            for cond_name, cond_val in obs["considerations"].items():
                if cond_val > 0:
                    rows_considerations.append({
                        "Session_ID": idx, "Comportement": cond_name, "Nombre": cond_val
                    })
                    
        df_p = pd.DataFrame(rows_profils)
        df_c = pd.DataFrame(rows_considerations)
        
        st.markdown("### 🔍 Sélection des catégories cibles")
        col_filtre1, col_filtre2 = st.columns(2)
        with col_filtre1:
            genres_choisis = st.multiselect("Filtrer par Genre :", options=GENRES, default=GENRES)
        with col_filtre2:
            ages_choisis = st.multiselect("Filtrer par Tranche d'Âge :", options=AGES, default=AGES)
            
        df_p_filtré = df_p[(df_p["Genre"].isin(genres_choisis)) & (df_p["Age"].isin(ages_choisis))]
        
        st.write("---")
        
        if df_p_filtré.empty:
            st.warning("⚠️ Aucun profil ne correspond à cette combinaison de filtres.")
        else:
            g_layout1, g_layout2 = st.columns(2)
            
            with g_layout1:
                st.subheader("🥧 Répartition globale par Genre")
                df_genre = df_p_filtré.groupby("Genre", as_index=False)["Quantite"].sum()
                fig_pie = px.pie(
                    df_genre, values="Quantite", names="Genre", 
                    color="Genre", hole=0.4,
                    color_discrete_map={"Homme": "#1f77b4", "Femme": "#e377c2", "Ne se prononce pas": "#7f7f7f"}
                )
                fig_pie.update_traces(textinfo='percent+value', textfont_size=14)
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with g_layout2:
                st.subheader("⏳ Pyramide des Âges du public")
                df_pyramide = df_p_filtré.groupby(["Age", "Genre"])["Quantite"].sum().unstack(fill_value=0)
                for age_cat in AGES:
                    if age_cat not in df_pyramide.index:
                        df_pyramide.loc[age_cat] = 0
                df_pyramide = df_pyramide.reindex(AGES)
                
                val_hommes = df_pyramide.get("Homme", pd.Series(0, index=AGES)).values
                val_femmes = df_pyramide.get("Femme", pd.Series(0, index=AGES)).values
                
                fig_pyr = go.Figure()
                fig_pyr.add_trace(go.Bar(
                    y=AGES, x=-val_hommes, name='Hommes', 
                    orientation='h', marker_color='#1f77b4',
                    hovertemplate="Hommes: %{customdata}<extra></extra>",
                    customdata=val_hommes
                ))
                fig_pyr.add_trace(go.Bar(
                    y=AGES, x=val_femmes, name='Femmes', 
                    orientation='h', marker_color='#e377c2',
                    hovertemplate="Femmes: %{x}<extra></extra>"
                ))
                fig_pyr.update_layout(
                    barmode='relative',
                    xaxis=dict(
                        title='Effectifs', 
                        tickvals=[-max(val_hommes+[1]), 0, max(val_femmes+[1])], 
                        ticktext=[str(max(val_hommes+[1])), '0', str(max(val_femmes+[1]))]
                    ),
                    yaxis=dict(title="Tranches d'âge")
                )
                st.plotly_chart(fig_pyr, use_container_width=True)
                
            st.write("---")
            
            st.subheader("🗺️ Matrice d'analyse croisée (Genre & Âge)")
            df_matrix = df_p_filtré.groupby(["Genre", "Age"])["Quantite"].sum().unstack(fill_value=0)
            df_matrix = df_matrix.reindex(index=GENRES, columns=AGES, fill_value=0)
            
            fig_heat = px.imshow(
                df_matrix, text_auto=True,
                labels=dict(x="Tranche d'âge", y="Genre", color="Nombre"),
                x=AGES, y=GENRES, color_continuous_scale="Blugrn"
            )
            st.plotly_chart(fig_heat, use_container_width=True)
            
        st.write("---")
        
        st.subheader("🎯 Auto-évaluation de la pertinence (Grille officielle)")
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            for crit in CRITERES_EVAL_P13[:3]:
                st.slider(f"Note : {crit}", 1, 5, 3, key=f"p13_{crit}")
        with col_e2:
            for crit in CRITERES_EVAL_P13[3:]:
                st.slider(f"Note : {crit}", 1, 5, 3, key=f"p13_{crit}")
                
        criteres_personnalises = st.session_state.dispositif_config.get("criteres", [])
        if criteres_personnalises:
            st.markdown("##### Atteinte de vos objectifs initiaux personnalisés :")
            for cp in criteres_personnalises:
                st.slider(f"Objectif : {cp}", 0, 100, 50, format="%d%%", key=f"custom_{cp}")