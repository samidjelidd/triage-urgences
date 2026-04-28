import streamlit as st
import random
import matplotlib.pyplot as plt

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Triage Urgences QC", page_icon="🏥", layout="wide")

# --- DICTIONNAIRES DE DONNÉES ---
symptomes_dict = {
    "1": "Signes d’AVC", "2": "Fièvre", "3": "Vomissement/Nausée",
    "4": "Diarrhée", "5": "Maux de tête", "6": "Toux",
    "7": "Douleur à la poitrine", "8": "Difficultés repiratoires",
    "9": "Signes d’infections (rouille)", "10": "Brûlure",
    "11": "Plaie ouverte/infectée", "12": "Douleur à la gorge",
    "13": "Constipation", "14": "Douleurs abdominales",
    "15": "Signes d’infections urinaire", "16": "Ongle incarné",
    "17": "Enflure d'une partie du corps", "18": "Symptômes semblables à un rhume"
}

ages_dict = {
    "1": "Entre 0 et 1 an", "2": "Entre 1 et 4 ans", 
    "3": "Entre 4 et 12 ans", "4": "Entre 12 et 60 ans", "5": "60 ans et plus"
}

# --- TITRE PRINCIPAL ---
st.title("🏥 Système de Triage des Urgences (Québec)")
st.markdown("---")

# --- CRÉATION DES ONGLETS ---
tab1, tab2 = st.tabs(["🩺 Évaluation Patient (Live)", "📊 Simulation d'Impact (Data)"])

# ==========================================
# ONGLET 1 : L'APPLICATION PATIENT
# ==========================================
with tab1:
    st.header("Formulaire d'évaluation d'urgence")
    st.info("Ce programme a pour but de désengorger les salles d'urgence au Québec. En cas de doute, remplissez ce formulaire. **En cas de danger imminent, composez le 911.**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 1. Choix de l'âge
        age_label = st.selectbox("Quel est votre tranche d'âge ?", list(ages_dict.values()))
        # Retrouver l'ID de l'âge
        age = list(ages_dict.keys())[list(ages_dict.values()).index(age_label)]
        
        # 2. Choix des symptômes
        symptomes_labels = st.multiselect("Sélectionnez vos symptômes :", list(symptomes_dict.values()))
        # Retrouver les IDs des symptômes
        choix_list = [list(symptomes_dict.keys())[list(symptomes_dict.values()).index(symp)] for symp in symptomes_labels]

    with col2:
        st.subheader("Questions de suivi")
        # Questions dynamiques basées sur les choix
        fièvre_haute = "non"
        douleur_dure = "non"
        
        if "2" in choix_list: # Fièvre
            fièvre_haute = st.radio("Avez-vous une fièvre de plus de 40°C ?", ["non", "oui"])
            
        if "7" in choix_list: # Douleur poitrine
            douleur_dure = st.radio("Votre douleur dure-t-elle plus de 5-10 minutes ?", ["non", "oui"])
            
        if len(choix_list) == 0:
            st.write("Veuillez sélectionner au moins un symptôme pour voir les questions.")

    st.markdown("---")
    
    # 3. Bouton d'évaluation
    if st.button("Lancer l'évaluation 🚀", use_container_width=True):
        stop = False
        
        # Logique de triage (Simplifiée pour l'exemple interactif, tirée de ton code)
        if "1" in choix_list or "8" in choix_list or fièvre_haute == "oui" or douleur_dure == "oui":
            st.error("🚨 **RÉSULTAT : Veuillez vous rendre à l'urgence immédiatement.**")
            stop = True
            
        elif ("2" in choix_list and age == "1") or ("2" in choix_list and "7" in choix_list):
            st.error("🚨 **RÉSULTAT : Veuillez vous rendre à l'urgence.**")
            stop = True
            
        elif "13" in choix_list and age == "5":
            st.warning("⚠️ **RÉSULTAT : Veuillez consulter un médecin en clinique.**")
            stop = True
            
        if not stop:
            st.success("✅ **RÉSULTAT : Une visite à l'urgence ne semble pas nécessaire.** Vous pouvez appeler le 811 (Info-Santé).")


# ==========================================
# ONGLET 2 : LA SIMULATION DE DONNÉES
# ==========================================
with tab2:
    st.header("Simulation de l'impact de l'application")
    st.write("Testez comment l'adoption de cette application par la population pourrait réduire l'engorgement des urgences.")
    
    colA, colB = st.columns(2)
    with colA:
        proportions_input = st.text_input("Proportions d'utilisation à tester (%) séparées par des virgules :", "10, 25, 50, 75")
    with colB:
        nb_simulations = st.slider("Nombre d'essais (simulations) :", min_value=100, max_value=2000, value=500, step=100)

    if st.button("Lancer la simulation 📊"):
        with st.spinner('Calcul des probabilités en cours...'):
            # Préparation des données
            liste_texte = proportions_input.split(',')
            proportions_a_tester = [float(t.strip()) for t in liste_texte]
            patients_par_sim = 1000
            symptomes_possibles = list(symptomes_dict.keys())
            ages_possibles = list(ages_dict.keys())

            moyennes_urgences, moyennes_cliniques, moyennes_pas_besoin = [], [], []

            # Fonction d'évaluation pour la simulation (Ton code exact)
            def evaluer_patient_sim(age, choix_list):
                if "1" in choix_list or "8" in choix_list: return "Urgence"
                if "2" in choix_list and age == "1": return "Urgence"
                if "13" in choix_list and age == "5": return "Clinique"
                if "14" in choix_list and age == "5": return "Clinique"
                # Ajout de hasard pour la simulation
                if random.random() < 0.2: return "Urgence"
                elif random.random() < 0.4: return "Clinique"
                return "Pas besoin"

            # Boucle de simulation
            for prop in proportions_a_tester:
                proportion_app = prop / 100.0
                total_urgence, total_clinique, total_pas_besoin = 0, 0, 0

                for sim in range(nb_simulations):
                    for patient in range(patients_par_sim):
                        age = random.choice(ages_possibles)
                        nb_symptomes = random.randint(1, 4)
                        choix_list = random.sample(symptomes_possibles, nb_symptomes)

                        hasard = random.random()
                        if hasard > proportion_app:
                            total_urgence += 1
                        else:
                            statut = evaluer_patient_sim(age, choix_list)
                            if statut == "Urgence": total_urgence += 1
                            elif statut == "Clinique": total_clinique += 1
                            else: total_pas_besoin += 1

                moyennes_urgences.append(total_urgence / nb_simulations)
                moyennes_cliniques.append(total_clinique / nb_simulations)
                moyennes_pas_besoin.append(total_pas_besoin / nb_simulations)

            # --- GRAPHIQUE MATPLOTLIB ---
            fig, ax = plt.subplots(figsize=(10, 5))
            largeur = 0.25
            
            urgences = [i - largeur for i in range(len(proportions_a_tester))]
            cliniques = range(len(proportions_a_tester))
            pas_besoin = [i + largeur for i in range(len(proportions_a_tester))]
            etiquettes = [f"{p}%" for p in proportions_a_tester]

            ax.bar(urgences, moyennes_urgences, width=largeur, label="Aller à l'urgence", color="#ff4b4b")
            ax.bar(cliniques, moyennes_cliniques, width=largeur, label="Clinique / Médecin", color="#ffa421")
            ax.bar(pas_besoin, moyennes_pas_besoin, width=largeur, label="Pas besoin / 811", color="#21c354")

            ax.set_title("Impact du taux d'utilisation de l'application sur 1000 patients", fontsize=14, fontweight='bold')
            ax.set_ylabel("Nombre de patients (Moyenne)")
            ax.set_xlabel("Taux d'utilisation de l'application")
            ax.set_xticks(cliniques)
            ax.set_xticklabels(etiquettes)
            ax.legend()
            ax.grid(axis='y', linestyle='--', alpha=0.7)

            # Affichage du graphique dans Streamlit
            st.pyplot(fig)
            st.success("Simulation terminée avec succès !")
