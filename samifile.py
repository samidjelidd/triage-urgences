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

st.title("🏥 Système de Triage des Urgences (Québec)")
st.markdown("---")

tab1, tab2 = st.tabs(["🩺 Évaluation Patient (Live)", "📊 Simulation d'Impact (Data)"])

# ==========================================
# ONGLET 1 : L'APPLICATION PATIENT (100% TON CODE)
# ==========================================
with tab1:
    st.info("Ce programme a pour but de désengorger les salles d'urgence au Québec. En cas de doute sur la nécessité de vous rendre à l'urgence, veuillez remplir le questionnaire suivant. Si vous êtes dans une situation de danger imminent, contactez dès maintenant le 911.")
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.subheader("1. Informations Générales")
        age_label = st.selectbox("Quel est votre tranche d'âge ?", list(ages_dict.values()))
        age = list(ages_dict.keys())[list(ages_dict.values()).index(age_label)]
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("2. Vos Symptômes")
        symptomes_labels = st.multiselect("Sélectionnez un ou plusieurs symptômes :", list(symptomes_dict.values()))
        choix_list = [list(symptomes_dict.keys())[list(symptomes_dict.values()).index(symp)] for symp in symptomes_labels]

    with col2:
        st.subheader("3. Précisions Médicales")
        if len(choix_list) == 0:
            st.write("👈 *Sélectionnez vos symptômes à gauche pour voir les questions de suivi.*")
            
        # Initialisation de toutes les variables à "non" pour éviter les erreurs
        q_fievre_40, q_vomi_sang, q_vomi_6h, q_vomi_toux, q_abdo_insup, q_selle_sang = "non", "non", "non", "non", "non", "non"
        q_deshydratation_4, q_immun_4, q_tete_soudain, q_tete_extreme, q_tete_trauma = "non", "non", "non", "non", "non"
        q_tete_eruption, q_tete_aggrave, q_tete_chronique, q_respi_corps, q_respi_diff = "non", "non", "non", "non", "non"
        q_respi_2sem, q_respi_sang, q_respi_immun, q_respi_diag, q_respi_aggrave = "non", "non", "non", "non", "non"
        q_poitrine_5min, q_poitrine_essouffle, q_rouille_spasme, q_rouille_profonde = "non", "non", "non", "non"
        q_brulure_blanche, q_brulure_paume, q_brulure_visage, q_brulure_cloque, q_brulure_elec, q_brulure_vetement = "non", "non", "non", "non", "non", "non"
        q_plaie_15min, q_plaie_ouverte, q_plaie_morsure, q_plaie_engourdi, q_plaie_pus, q_plaie_infection = "non", "non", "non", "non", "non", "non"
        q_gorge_eruption, q_gorge_ganglion, q_gorge_paleur, q_gorge_deshydrat, q_gorge_abces = "non", "non", "non", "non", "non"
        q_gorge_3jours, q_gorge_7jours, q_gorge_salive, q_gorge_irradie, q_const_26h, q_const_gaz = "non", "non", "non", "non", "non", "non"
        q_abdo_chirurgie, q_abdo_enceinte, q_abdo_poignard, q_abdo_26h, q_abdo_dur, q_abdo_choc = "non", "non", "non", "non", "non", "non"
        q_urin_enceinte, q_urin_dos, q_urin_incap, q_urin_diabete = "non", "non", "non", "non"
        q_ongle_rouge, q_ongle_coeur, q_ongle_pus, q_ongle_massif, q_ongle_diabete = "non", "non", "non", "non", "non"
        q_enflure_rouge, q_enflure_choc, q_enflure_urine, q_enflure_jambes, q_enflure_avaler = "non", "non", "non", "non", "non"
        q_rhume_cotes, q_rhume_bleu, q_rhume_parler, q_rhume_sommeil, q_rhume_deshydrat = "non", "non", "non", "non", "non"
        temps_fievre = "1"

        with st.container():
            # EXACTEMENT LES QUESTIONS DE TON IPYNB
            if "2" in choix_list:
                st.markdown("#### 🤒 Fièvre")
                q_fievre_40 = st.radio("Avez-vous une fièvre de plus de 40°C?", ["Non", "Oui"], horizontal=True).lower()
                temps_fievre_label = st.selectbox("Depuis combien de temps avez-vous de la fièvre?", ["Moins de 24 heures", "Entre 24 et 48 heures", "Plus de 48 heures"])
                temps_fievre_dict = {"Moins de 24 heures": "1", "Entre 24 et 48 heures": "2", "Plus de 48 heures": "3"}
                temps_fievre = temps_fievre_dict[temps_fievre_label]

            if "3" in choix_list:
                st.markdown("#### 🤢 Vomissement/Nausée")
                q_vomi_sang = st.radio("Votre vomi contient-t-il du sang et/ou est-il de couleur noir ou anormale (ex: vert fluo) ?", ["Non", "Oui"], horizontal=True).lower()
                q_vomi_6h = st.radio("Vomissez-vous, sans amélioration, depuis plus de 6 heures?", ["Non", "Oui"], horizontal=True).lower()
                if "6" in choix_list:
                    q_vomi_toux = st.radio("Vomissez-vous systématiquement à chaque fois que vous toussez?", ["Non", "Oui"], horizontal=True).lower()

            if "4" in choix_list:
                st.markdown("#### 🚽 Diarrhée")
                if "14" in choix_list:
                    q_abdo_insup = st.radio("Considérez-vous vos douleurs abdominales comme insuportable?", ["Non", "Oui"], horizontal=True).lower()
                q_selle_sang = st.radio("Vos selles contiennent-t-elles du sang et/ou sont-elles de couleur noir ?", ["Non", "Oui"], horizontal=True).lower()
                q_deshydratation_4 = st.radio("Avez-vous des signes de déshydratation (bouche sèche, urine peu fréquente, somnolence/étourdissement)?", ["Non", "Oui"], horizontal=True).lower()
                if age in ["1", "2", "3"]:
                    q_immun_4 = st.radio("Souffrez-vous d'une maladie chronique ou d'un système immunitaire affaibli ou déficient?", ["Non", "Oui"], horizontal=True).lower()

            if "5" in choix_list:
                st.markdown("#### 🤕 Maux de tête")
                q_tete_soudain = st.radio("Votre mal de tête est-il arrivé subitement?", ["Non", "Oui"], horizontal=True).lower()
                if q_tete_soudain == "oui":
                    q_tete_extreme = st.radio("Votre mal de tête est-il extrêmement douloureux?", ["Non", "Oui"], horizontal=True).lower()
                q_tete_trauma = st.radio("Avez-vous vécu un traumatisme récemment? (ex: chute, accident)", ["Non", "Oui"], horizontal=True).lower()
                if "2" in choix_list:
                    q_tete_eruption = st.radio("Avez-vous des éruptions cutannées?", ["Non", "Oui"], horizontal=True).lower()
                q_tete_aggrave = st.radio("Votre mal de tête s'aggrave-t-il rapidement?", ["Non", "Oui"], horizontal=True).lower()
                q_tete_chronique = st.radio("Souffrez-vous de maladies chroniques comme l’hypertension ou un trouble de coagulation?", ["Non", "Oui"], horizontal=True).lower()

            if "6" in choix_list:
                st.markdown("#### 🗣️ Toux")
                q_respi_corps = st.radio("Pensez-vous avoir un corps étranger dans vos voies respiratoires?", ["Non", "Oui"], horizontal=True).lower()
                q_respi_diff = st.radio("Avez-vous de la difficulté à respirer ou une respiration sifflante?", ["Non", "Oui"], horizontal=True).lower()
                q_respi_2sem = st.radio("Toussez-vous fréquemment depuis plus de deux semaines?", ["Non", "Oui"], horizontal=True).lower()
                q_respi_sang = st.radio("Toussez-vous du sang?", ["Non", "Oui"], horizontal=True).lower()
                q_respi_immun = st.radio("Votre système immunitaire est-il affaibli (cancer, maladie chronique, etc) ?", ["Non", "Oui"], horizontal=True).lower()
                q_respi_diag = st.radio("Avez-vous été récemment diagnostiqué d'une infection (bronchite, pneumonie, asthme) ?", ["Non", "Oui"], horizontal=True).lower()
                if q_respi_diag == "oui":
                    q_respi_aggrave = st.radio("Votre état s'est-il aggraver depuis votre diagnostic?", ["Non", "Oui"], horizontal=True).lower()

            if "7" in choix_list:
                st.markdown("#### 💔 Douleur à la poitrine")
                q_poitrine_5min = st.radio("Votre douleur dure-t-elle plus de 5-10 minutes?", ["Non", "Oui"], horizontal=True).lower()
                q_poitrine_essouffle = st.radio("Votre douleur s'accompagne-t-elle d'essoufflement, d'étourdissements ou de perte de conscience?", ["Non", "Oui"], horizontal=True).lower()

            if "9" in choix_list:
                st.markdown("#### 🧲 Infections (rouille)")
                q_rouille_spasme = st.radio("Avez-vous des spasmes musculaires ou raideurs, particulièrement au niveau de la mâchoire, du cou, de l'abdomen ou du dos?", ["Non", "Oui"], horizontal=True).lower()
                q_rouille_profonde = st.radio("La plaie est-elle profonde, souillée par de la terre, difficile à nettoyer, ou présente-t-elle des signes d'infection locale grave?", ["Non", "Oui"], horizontal=True).lower()

            if "10" in choix_list:
                st.markdown("#### 🔥 Brûlure")
                q_brulure_blanche = st.radio("Votre peau est-elle blanchâtre, brunâtre ou carbonisée (noire) ?", ["Non", "Oui"], horizontal=True).lower()
                q_brulure_paume = st.radio("La brûlure est-elle plus grande que la paume de la main de la victime ou touche-t-elle plus de 10 % de la surface corporelle?", ["Non", "Oui"], horizontal=True).lower()
                q_brulure_visage = st.radio("La brûlure touche-t-elle le visage, le cou, les mains, les pieds, les articulations ou les organes génitaux?", ["Non", "Oui"], horizontal=True).lower()
                q_brulure_cloque = st.radio("Retrouvez-vous plusieurs cloques dont la surface totale dépasse la moitié de la paume de la main?", ["Non", "Oui"], horizontal=True).lower()
                q_brulure_elec = st.radio("La brûlures est-elle provoquée par l'électricité, des produits chimiques ou l'inhalation de fumée?", ["Non", "Oui"], horizontal=True).lower()
                q_brulure_vetement = st.radio("Y-a-t-il des vêtements fondus ou restés collés à la peau brûlée?", ["Non", "Oui"], horizontal=True).lower()

            if "11" in choix_list:
                st.markdown("#### 🩸 Plaie ouverte/infectée")
                q_plaie_15min = st.radio("Le sang sort-il depuis plus de 15 minutes malgré un pression directe?", ["Non", "Oui"], horizontal=True).lower()
                q_plaie_ouverte = st.radio("La plaie est-elle grande ouverte, profonde, ou laisse voir des tissus internes (muscles, os)?", ["Non", "Oui"], horizontal=True).lower()
                q_plaie_morsure = st.radio("La plaie provient-elle d'une morsure (humaine ou animal) ou contient-elle un objet coincé à l'intérieur?", ["Non", "Oui"], horizontal=True).lower()
                q_plaie_engourdi = st.radio("La partie du corps blessée présente-t-elle un engourdissement?", ["Non", "Oui"], horizontal=True).lower()
                q_plaie_pus = st.radio("La plaie présente-elle du pus ou une odeur nauséabonde?", ["Non", "Oui"], horizontal=True).lower()
                q_plaie_infection = st.radio("La plaie présente-elle des signes d'infections (rougeur qui s'étend rapidement, chaleur intense, gonflement important ou douleur croissante)?", ["Non", "Oui"], horizontal=True).lower()

            if "12" in choix_list:
                st.markdown("#### 🗣️ Douleur à la gorge")
                if "2" not in choix_list:
                    q_gorge_eruption = st.radio("Le mal de gorge est-il accompagné d'une éruption cutanée ?", ["Non", "Oui"], horizontal=True).lower()
                q_gorge_ganglion = st.radio("Le mal de gorge est-il accompagné de ganglions enflés ?", ["Non", "Oui"], horizontal=True).lower()
                q_gorge_paleur = st.radio("Présentez-vous une pâleur inhabituelle ou des lèvres et des doigts bleutés?", ["Non", "Oui"], horizontal=True).lower()
                if "4" not in choix_list:
                    q_gorge_deshydrat = st.radio("Observez-vous des signes de déshydratation (bouche sèche, absence de larmes, diminution des urines)?", ["Non", "Oui"], horizontal=True).lower()
                q_gorge_abces = st.radio("Constatez-vous un abcès (gonflement près d'une amygdale ou déviation de la luette)?", ["Non", "Oui"], horizontal=True).lower()
                if age in ["4", "5"] and "2" in choix_list:
                    q_gorge_3jours = st.radio("Votre fièvre persiste-t-elle depuis plus de 3 jours?", ["Non", "Oui"], horizontal=True).lower()
                q_gorge_7jours = st.radio("Votre douleur à la gorge persiste-t-elle depuis plus de 7 jours sans amélioration?", ["Non", "Oui"], horizontal=True).lower()
                q_gorge_salive = st.radio("Remarquez-vous la présence de sang dans votre salive?", ["Non", "Oui"], horizontal=True).lower()
                q_gorge_irradie = st.radio("Ressentez-vous une douleur intense irradiant vers le cou ou l’oreille?", ["Non", "Oui"], horizontal=True).lower()

            if "13" in choix_list:
                st.markdown("#### 🚽 Constipation")
                if "14" in choix_list:
                    q_const_26h = st.radio("Votre douleur abdominale est-elle intense et sans amélioration depuis plus de 26 heures? (Constipation)", ["Non", "Oui"], horizontal=True).lower()
                q_const_gaz = st.radio("Êtes-vous dans l'incapacité de passer des gaz, en plus des selles?", ["Non", "Oui"], horizontal=True).lower()

            if "14" in choix_list:
                st.markdown("#### 🤕 Douleurs abdominales")
                q_abdo_chirurgie = st.radio("Avez-vous eu une chirurgie abdominale récemment?", ["Non", "Oui"], horizontal=True).lower()
                if age in ["4", "5"]:
                    q_abdo_enceinte = st.radio("Il y a-t-il des chances que vous soyez enceinte? (Abdomen)", ["Non", "Oui"], horizontal=True).lower()
                q_abdo_poignard = st.radio("Votre douleur est-elle survenue en *coup de poignard*?", ["Non", "Oui"], horizontal=True).lower()
                q_abdo_26h = st.radio("Votre douleur abdominale est-elle intense et sans amélioration depuis plus de 26 heures?", ["Non", "Oui"], horizontal=True).lower()
                q_abdo_dur = st.radio("Votre ventre est-il dur au toucher ou tendu comme du bois?", ["Non", "Oui"], horizontal=True).lower()
                q_abdo_choc = st.radio("Éprouvez-vous des signes de choc (évanouissement, étourdissements, confusion, peau moite ou rythme cardiaque très rapide)?", ["Non", "Oui"], horizontal=True).lower()

            if "15" in choix_list:
                st.markdown("#### 🚽 Signes d'infections urinaire")
                if "14" not in choix_list and age in ["4", "5"]:
                    q_urin_enceinte = st.radio("Il y a-t-il des chances que vous soyez enceinte? (Urinaire)", ["Non", "Oui"], horizontal=True).lower()
                q_urin_dos = st.radio("Avez-vous une douleur vive dans le bas du dos (souvent d'un seul côté) ou une augmentation marquée de la douleur au ventre ?", ["Non", "Oui"], horizontal=True).lower()
                q_urin_incap = st.radio("Êtes-vous en totale incapacité d'uriner?", ["Non", "Oui"], horizontal=True).lower()
                q_urin_diabete = st.radio("Êtes-vous une personnes diabétiques ou immunodéprimées?", ["Non", "Oui"], horizontal=True).lower()

            if "16" in choix_list:
                st.markdown("#### 🦶 Ongle incarné")
                q_ongle_rouge = st.radio("Remarquez-vous des signes de propagation (ligne rouge qui remonte le long du pied ou de la jambe) ?", ["Non", "Oui"], horizontal=True).lower()
                q_ongle_coeur = st.radio("Ressentez-vous une douleur qui *bat* au rythme de votre cœur?", ["Non", "Oui"], horizontal=True).lower()
                q_ongle_pus = st.radio("Remarquez-vous des écoulements suspects (pus, sang ou odeur nauséabonde)?", ["Non", "Oui"], horizontal=True).lower()
                q_ongle_massif = st.radio("Remarquez-vous un gonflement massif, une nécrose (peau qui noircit) ou une décoloration importante de l'orteil?", ["Non", "Oui"], horizontal=True).lower()
                if "15" not in choix_list:
                    q_ongle_diabete = st.radio("Êtes-vous une personne atteinte de diabète, troubles circulatoires ou un système immunitaire affaibli?", ["Non", "Oui"], horizontal=True).lower()

            if "17" in choix_list:
                st.markdown("#### 🎈 Enflure d'une partie du corps")
                q_enflure_rouge = st.radio("La zone enfelé est-elle rouge, chaude au toucher et douloureuse ou sensible?", ["Non", "Oui"], horizontal=True).lower()
                q_enflure_choc = st.radio("Avez-vous récemment subit un choc avec déformation visible du membre ou incapacité de bouger l'articulation?", ["Non", "Oui"], horizontal=True).lower()
                q_enflure_urine = st.radio("Remarquez-vous une diminution de l'urine ou un gonflement de votre abdomen?", ["Non", "Oui"], horizontal=True).lower()
                q_enflure_jambes = st.radio("Remarquez-vous l'enflure de vos deux jambes accompagnée d'un essoufflement marqué, même au repos?", ["Non", "Oui"], horizontal=True).lower()
                q_enflure_avaler = st.radio("Avez-vous une difficultés à avaler, des étourdissements, de l'urticaire ou une accélération du rythme cardiaque?", ["Non", "Oui"], horizontal=True).lower()

            if "18" in choix_list:
                st.markdown("#### 🤧 Symptômes semblables à un rhume")
                q_rhume_cotes = st.radio("Votre peau se creuse-t-elle entre vos côtes ou au-dessus de votre clavicule à chaque inspiration?", ["Non", "Oui"], horizontal=True).lower()
                if "12" not in choix_list:
                    q_rhume_bleu = st.radio("Vos lèvres ou vos doigts deviennent-ils bleutés?", ["Non", "Oui"], horizontal=True).lower()
                q_rhume_parler = st.radio("Avez-vous une incapacité à parler ou à boire normalement en raison de l'essoufflement?", ["Non", "Oui"], horizontal=True).lower()
                q_rhume_sommeil = st.radio("Avez-vous une somnolence extrême, difficulté à vous réveiller, confusion ou léthargie?", ["Non", "Oui"], horizontal=True).lower()
                if "4" not in choix_list and "12" not in choix_list:
                    q_rhume_deshydrat = st.radio("Avez-vous des signes de déshydratation sévère (absence d'urine depuis plus de 8 heures, bouche très sèche ou absence de larmes lors des pleurs) ?", ["Non", "Oui"], horizontal=True).lower()

    st.markdown("---")
    
    # 4. Le bouton d'Analyse (EXACTEMENT LA MÊME LOGIQUE QUE LE NOTEBOOK)
    if st.button("Lancer le Triage Médical 🚨", use_container_width=True):
        stop = False

        if "1" in choix_list or "8" in choix_list:
            st.error("🚨 **Veuillez vous rendre à l'urgence.**")
            stop = True
        if not stop and "2" in choix_list and age == "1":
            st.error("🚨 **Veuillez vous rendre à l'urgence.**")
            stop = True
        if not stop and "2" in choix_list and "7" in choix_list:
            st.error("🚨 **Veuillez vous rendre à l'urgence.**")
            stop = True
        if not stop and "3" in choix_list and "7" in choix_list:
            st.error("🚨 **Veuillez vous rendre à l'urgence.**")
            stop = True
        if not stop and "4" in choix_list and age == "1":
            st.error("🚨 **Veuillez vous rendre à l'urgence.**")
            stop = True
        if not stop and "9" in choix_list and "2" in choix_list:
            st.error("🚨 **Veuillez vous rendre à l'urgence.**")
            stop = True
        if not stop and "10" in choix_list:
            if age == "1" or age == "2" or age == "5":
                st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                stop = True
        if not stop and "11" in choix_list and "2" in choix_list:
            st.error("🚨 **Veuillez vous rendre à l'urgence.**")
            stop = True
        if not stop and "13" in choix_list and "3" in choix_list:
            st.error("🚨 **Veuillez vous rendre à l'urgence.**")
            stop = True
        if not stop and "13" in choix_list and "2" in choix_list:
            st.error("🚨 **Veuillez vous rendre à l'urgence.**")
            stop = True
        if not stop and "13" in choix_list and age == "5":
            st.warning("⚠️ **Veuillez consulter un médecin.**")
            stop = True
        if not stop and "14" in choix_list and age == "5":
            st.warning("⚠️ **Veuillez consulter un médecin.**")
            stop = True
        if not stop and "15" in choix_list and "2" in choix_list:
            st.error("🚨 **Veuillez vous rendre à l'urgence.**")
            stop = True
        if not stop and "15" in choix_list and "3" in choix_list:
            st.error("🚨 **Veuillez vous rendre à l'urgence.**")
            stop = True
        if not stop and "16" in choix_list and "2" in choix_list:
            st.error("🚨 **Veuillez vous rendre à l'urgence.**")
            stop = True
        if not stop and "17" in choix_list and "2" in choix_list:
            st.error("🚨 **Veuillez vous rendre à l'urgence.**")
            stop = True

        # QUESTIONS SUIVANTES
        if not stop and "2" in choix_list:
            if age == "1":
                st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                stop = True
            if not stop:
                if q_fievre_40 == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True

        if not stop and "3" in choix_list:
            if not stop:
                if q_vomi_sang == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_vomi_6h == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop and "6" in choix_list:
                if q_vomi_toux == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True

        if not stop and "4" in choix_list:
            if not stop and "14" in choix_list:
                if q_abdo_insup == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_selle_sang == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_deshydratation_4 == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if age in ["1", "2", "3"]:
                    if q_immun_4 == "oui":
                        st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                        stop = True

        if not stop and "5" in choix_list:
            if q_tete_soudain == "oui":
                if q_tete_extreme == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_tete_trauma == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop and "2" in choix_list:
                if q_tete_eruption == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_tete_aggrave == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_tete_chronique == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True

        if not stop and "6" in choix_list:
            if q_respi_corps == "oui":
                st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                stop = True
            if not stop:
                if q_respi_diff == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_respi_2sem == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_respi_sang == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_respi_immun == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_respi_diag == "oui":
                    if q_respi_aggrave == "oui":
                        st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                        stop = True

        if not stop and "7" in choix_list:
            if q_poitrine_5min == "oui":
                st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                stop = True
            if not stop:
                if q_poitrine_essouffle == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True

        if not stop and "9" in choix_list:
            if not stop:
                if q_rouille_spasme == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_rouille_profonde == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True

        if not stop and "10" in choix_list:
            if not stop:
                if q_brulure_blanche == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_brulure_paume == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_brulure_visage == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_brulure_cloque == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_brulure_elec == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_brulure_vetement == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True

        if not stop and "11" in choix_list:
            if not stop:
                if q_plaie_15min == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_plaie_ouverte == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_plaie_morsure == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_plaie_engourdi == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_plaie_pus == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_plaie_infection == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True

        if not stop and "12" in choix_list:
            if age in ["1", "2", "3"]:
                if "2" in choix_list:
                    if temps_fievre == "3":
                        st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                        stop = True
            if not stop and "2" not in choix_list:
                if q_gorge_eruption == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_gorge_ganglion == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_gorge_paleur == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop and "4" not in choix_list:
                if q_gorge_deshydrat == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_gorge_abces == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop and age in ["4", "5"]:
                if "2" in choix_list:
                    if q_gorge_3jours == "oui":
                        st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                        stop = True
            if not stop:
                if q_gorge_7jours == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_gorge_salive == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_gorge_irradie == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True

        if not stop and "13" in choix_list:
            if not stop and "14" in choix_list:
                if q_const_26h == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_const_gaz == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True

        if not stop and "14" in choix_list:
            if not stop:
                if q_abdo_chirurgie == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop and age in ["4", "5"]:
                if q_abdo_enceinte == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_abdo_poignard == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_abdo_26h == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_abdo_dur == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_abdo_choc == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True

        if not stop and "15" in choix_list:
            if not stop and "14" not in choix_list:
                if age in ["4", "5"]:
                    if q_urin_enceinte == "oui":
                        st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                        stop = True
            if not stop:
                if q_urin_dos == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_urin_incap == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_urin_diabete == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True

        if not stop and "16" in choix_list:
            if not stop:
                if q_ongle_rouge == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_ongle_coeur == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_ongle_pus == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_ongle_massif == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop and "15" not in choix_list:
                if q_ongle_diabete == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True

        if not stop and "17" in choix_list:
            if not stop:
                if q_enflure_rouge == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_enflure_choc == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_enflure_urine == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_enflure_jambes == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_enflure_avaler == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True

        if not stop and "18" in choix_list:
            if q_rhume_cotes == "oui":
                st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                stop = True
            if not stop and "12" not in choix_list:
                if q_rhume_bleu == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_rhume_parler == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop:
                if q_rhume_sommeil == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True
            if not stop and "4" not in choix_list and "12" not in choix_list:
                if q_rhume_deshydrat == "oui":
                    st.error("🚨 **Veuillez vous rendre à l'urgence.**")
                    stop = True

        if not stop:
            st.success("""✅ **Suite à l'analyse de vos symptômes, une visite à l'urgence ne semble pas nécessaire. En cas de doute ou si votre état semble s'aggraver, vous pouvez recommencer le quiz ou appeler directement le 811 (Info-Santé).**""")

# ==========================================
# ONGLET 2 : LA SIMULATION DE DONNÉES 
# ==========================================
with tab2:
    st.header("Simulation de l'impact de l'application")
    
    colA, colB = st.columns(2)
    with colA:
        proportions_input = st.text_input("Entrez les proportions d'utilisation à tester, séparées par des virgules (ex: 10, 25, 50) :", "10, 25, 50")
    with colB:
        nb_simulations_texte = st.text_input("Nombre d'essais par proportion (ex: 1000) :", "1000")

    if st.button("Lancer la simulation 📊"):
        with st.spinner('Calcul de la simulation en cours...'):
            
            # Fonction exacte de ton Notebook
            def demander_oui_non():
                return random.choices(["oui", "non"], weights=[0.1, 0.9])[0]

            def evaluer_patient_sim(age, choix_list):
                temps_fievre = None

                if "1" in choix_list or "8" in choix_list: return "Urgence"
                if "2" in choix_list and age == "1": return "Urgence"
                if "2" in choix_list and "7" in choix_list: return "Urgence"
                if "3" in choix_list and "7" in choix_list: return "Urgence"
                if "4" in choix_list and age == "1": return "Urgence"
                if "9" in choix_list and "2" in choix_list: return "Urgence"
                if "10" in choix_list:
                    if age == "1" or age == "2" or age == "5": return "Urgence"
                if "11" in choix_list and "2" in choix_list: return "Urgence"
                if "13" in choix_list and "3" in choix_list: return "Urgence"
                if "13" in choix_list and "2" in choix_list: return "Urgence"
                if "13" in choix_list and age == "5": return "Clinique"
                if "14" in choix_list and age == "5": return "Clinique"
                if "15" in choix_list and "2" in choix_list: return "Urgence"
                if "15" in choix_list and "3" in choix_list: return "Urgence"
                if "16" in choix_list and "2" in choix_list: return "Urgence"
                if "17" in choix_list and "2" in choix_list: return "Urgence"

                if "2" in choix_list:
                    if demander_oui_non() == "oui": return "Urgence"
                    temps_fievre = random.choice(["1", "2", "3", "4", "5"])
                if "3" in choix_list:
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if "6" in choix_list:
                        if demander_oui_non() == "oui": return "Urgence"
                if "4" in choix_list:
                    if "14" in choix_list:
                        if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if age == "1" or age == "2" or age == "3":
                        if demander_oui_non() == "oui": return "Urgence"
                if "5" in choix_list:
                    if demander_oui_non() == "oui":
                        if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if "2" in choix_list:
                        if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                if "6" in choix_list:
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui":
                        if demander_oui_non() == "oui": return "Urgence"
                if "7" in choix_list:
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                if "9" in choix_list:
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                if "10" in choix_list:
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                if "11" in choix_list:
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                if "12" in choix_list:
                    if age == "1" or age == "2" or age == "3":
                        if "2" in choix_list:
                            if temps_fievre == "3": return "Urgence"
                    if "2" not in choix_list:
                        if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if "4" not in choix_list:
                        if demander_oui_non() == "oui": return "Urgence"
                    if age == "4" or age == "5":
                        if "2" in choix_list:
                            if demander_oui_non() == "oui": return "Urgence"
                        if demander_oui_non() == "oui": return "Urgence"
                        if demander_oui_non() == "oui": return "Urgence"
                        if demander_oui_non() == "oui": return "Urgence"
                if "13" in choix_list:
                    if "14" in choix_list:
                        if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                if "14" in choix_list:
                    if demander_oui_non() == "oui": return "Urgence"
                    if age == "4" or age == "5":
                        if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                if "15" in choix_list:
                    if "14" not in choix_list:
                        if age == "4" or age == "5":
                            if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                if "16" in choix_list:
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if "15" not in choix_list:
                        if demander_oui_non() == "oui": return "Urgence"
                if "17" in choix_list:
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                if "18" in choix_list:
                    if demander_oui_non() == "oui": return "Urgence"
                    if "12" not in choix_list:
                        if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if demander_oui_non() == "oui": return "Urgence"
                    if "4" not in choix_list and "12" not in choix_list:
                        if demander_oui_non() == "oui": return "Urgence"

                return "Pas besoin"

            liste_texte = proportions_input.split(',')
            proportions_a_tester = [float(texte.strip()) for texte in liste_texte]
            nb_simulations = int(nb_simulations_texte)
            patients_par_sim = 1000
            symptomes_possibles = list(symptomes_dict.keys())
            ages_possibles = list(ages_dict.keys())

            moyennes_urgences = []
            moyennes_cliniques = []
            moyennes_pas_besoin = []

            for prop in proportions_a_tester:
                proportion_app = prop / 100.0
                total_urgence = 0
                total_clinique = 0
                total_pas_besoin = 0

                for sim in range(nb_simulations):
                    for patient in range(patients_par_sim):
                        age = random.choice(ages_possibles)
                        nb_symptomes = random.randint(1, 4)
                        choix_list = random.sample(symptomes_possibles, nb_symptomes)

                        hasard = random.random()
                        if hasard > proportion_app:
                            total_urgence = total_urgence + 1
                        else:
                            statut = evaluer_patient_sim(age, choix_list)
                            if statut == "Urgence":
                                total_urgence = total_urgence + 1
                            elif statut == "Clinique":
                                total_clinique = total_clinique + 1
                            else:
                                total_pas_besoin = total_pas_besoin + 1

                moyenne_urg = total_urgence / nb_simulations
                moyenne_cli = total_clinique / nb_simulations
                moyenne_pas = total_pas_besoin / nb_simulations

                moyennes_urgences.append(moyenne_urg)
                moyennes_cliniques.append(moyenne_cli)
                moyennes_pas_besoin.append(moyenne_pas)

            # --- GRAPHIQUE MATPLOTLIB EXACT ---
            fig, ax = plt.subplots()
            largeur = 0.25
            urgences = []
            cliniques = []
            pas_besoin = []
            etiquettes_axe_x = []

            index = 0
            for prop in proportions_a_tester:
                urgences.append(index - largeur)
                cliniques.append(index)
                pas_besoin.append(index + largeur)
                etiquettes_axe_x.append(str(prop) + "%")
                index = index + 1

            ax.bar(urgences, moyennes_urgences, width=largeur, label="Aller à l'urgence", color="red")
            ax.bar(cliniques, moyennes_cliniques, width=largeur, label="Clinique / Médecin", color="orange")
            ax.bar(pas_besoin, moyennes_pas_besoin, width=largeur, label="Pas besoin / 811", color="green")

            ax.set_title("Impact de l'utilisation de l'application sur l'orientation des patients")
            ax.set_ylabel("Nombre de patients (Moyenne)")
            ax.set_xlabel("Taux d'utilisation de l'application (%)")
            ax.set_xticks(cliniques)
            ax.set_xticklabels(etiquettes_axe_x)
            ax.legend()
            
            st.pyplot(fig)
            st.success("✅ Simulation terminée avec succès !")
