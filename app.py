import streamlit as st
import pandas as pd
import time

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="StaySmart Hospitality - SMIT Maroc",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLING CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    .main { background-color: #020617; color: #f8fafc; }
    .stApp { background-color: #020617; }
    h1, h2, h3 { color: #f8fafc !important; }
    .metric-card { background-color: #0f172a; border: 1px solid #1e293b; padding: 15px; border-radius: 12px; }
    </style>
""", unsafe_allow_html=True)

# --- INITIALISATION DE LA SESSION STATE ---
if "is_unlocked" not in st.session_state:
    st.session_state.is_unlocked = False
if "checked_in" not in st.session_state:
    st.session_state.checked_in = True
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Bonjour M. Benani ! Je suis Yasmine, votre concierge virtuelle. Comment puis-je vous aider aujourd'hui ?"}
    ]
if "extras_total" not in st.session_state:
    st.session_state.extras_total = 1050

# --- NAVIGATION DANS LA SIDEBAR ---
st.sidebar.markdown("### 🏨 StaySmart Hospitality")
st.sidebar.caption("Programme SMIT • Digitalisation Hôtelière")
st.sidebar.markdown("---")

view_mode = st.sidebar.radio(
    "Choisir la Vue Démo :",
    ["📱 Application Mobile Client", "📊 Back-Office Admin Hôtel", "⚙️ Vue Split (Côte à côte)"]
)

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Réinitialiser la Démo", use_container_width=True):
    st.session_state.clear()
    st.rerun()


# =========================================================================
# FONCTION : APPLICATION MOBILE CLIENT
# =========================================================================
def render_client_app():
    st.markdown("### 📱 Simulation Smartphone Client")
    st.markdown("<p style='font-size: 12px; color: #94a3b8;'>Hôtel Palais Royal Atlas • Chambre 304</p>", unsafe_allow_html=True)
    
    # Navigation interne dans l'App mobile
    client_tab = st.tabs(["🔑 Clé Mobile", "📋 Check-In", "🤖 Concierge IA", "🧾 Services & Extras"])

    # --- ONGLET 1 : CLÉ MOBILE (BLE/NFC) ---
    with client_tab[0]:
        st.markdown("#### 🔒 Clé Numérique de la Chambre 304")
        st.info("Approchez votre smartphone de la serrure connectée pour déverrouiller.")

        # Boîte visuelle de la clé
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            lock_status = st.session_state.is_unlocked
            bg_color = "rgba(16, 185, 129, 0.2)" if lock_status else "rgba(15, 23, 42, 0.8)"
            border_color = "#10b981" if lock_status else "#334155"
            icon = "🔓" if lock_status else "🔒"
            text_state = "DÉVERROUILLÉ (Porte 304 Ouverte)" if lock_status else "VERROUILLÉ"
            text_color = "#10b981" if lock_status else "#94a3b8"

            st.markdown(f"""
                <div style="background: {bg_color}; border: 3px solid {border_color}; padding: 30px; border-radius: 50%; width: 160px; height: 160px; display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 0 auto; text-align: center; box-shadow: 0 0 25px rgba(234, 179, 8, 0.2);">
                    <span style="font-size: 40px;">{icon}</span>
                </div>
                <p style="text-align: center; font-weight: bold; color: {text_color}; margin-top: 15px;">{text_state}</p>
            """, unsafe_allow_html=True)

            if st.button("📲 Simuler le Tap / Déverrouillage BLE", use_container_width=True):
                st.session_state.is_unlocked = not st.session_state.is_unlocked
                st.rerun()

        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Code Wi-Fi", "PalaisRoyal2026")
        with col_b:
            st.metric("Climatisation", "21°C (Auto)")

    # --- ONGLET 2 : CHECK-IN 100% DIGITAL ---
    with client_tab[1]:
        st.markdown("#### 📋 Check-in Express & Scan OCR")
        if st.session_state.checked_in:
            st.success("✅ Check-in validé avec succès ! Votre identité (Passeport N° AB98231) a été vérifiée par OCR.")
        else:
            with st.form("checkin_form"):
                uploaded_file = st.file_uploader("Scanner Passeport ou CNI", type=["png", "jpg", "pdf"])
                arrival_time = st.selectbox("Heure d'arrivée estimée", ["14:00 - Standard", "12:00 - Early Check-in", "18:00 - Tardive"])
                signature = st.text_input("Signature Électronique (Nom complet)", "Karim Benani")
                
                submitted = st.form_submit_button("Valider et Générer la Clé")
                if submitted:
                    st.session_state.checked_in = True
                    st.success("Dossier validé ! Clé numérique transmise sur votre mobile.")
                    st.rerun()

    # --- ONGLET 3 : CONCIERGE IA (YASMINE) ---
    with client_tab[2]:
        st.markdown("#### 🤖 Yasmine - Concierge Virtuelle IA")
        
        # Affichage de l'historique des messages
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # Puces de requêtes rapides
        st.caption("Suggestions rapides :")
        col_r1, col_r2, col_r3 = st.columns(3)
        if col_r1.button("🧺 Serviettes"):
            st.session_state.messages.append({"role": "user", "content": "Demander des serviettes supplémentaires"})
            st.session_state.messages.append({"role": "assistant", "content": "C'est noté ! J'envoie deux serviettes de bain supplémentaires à la chambre 304 d'ici 5 minutes."})
            st.rerun()
        if col_r2.button("🍽️ Room Service"):
            st.session_state.messages.append({"role": "user", "content": "Commander un room service"})
            st.session_state.messages.append({"role": "assistant", "content": "Le menu digital est ouvert. Votre commande sera livrée en 20 minutes."})
            st.rerun()
        if col_r3.button("🍲 Gastronomie"):
            st.session_state.messages.append({"role": "user", "content": "Recommander un restaurant traditionnel"})
            st.session_state.messages.append({"role": "assistant", "content": "Je vous recommande 'Al Fassia' ou 'Dar Moha'. Souhaitez-vous que je réserve une table ?"})
            st.rerun()

        # Input Chat normal
        if user_prompt := st.chat_input("Posez votre question à Yasmine..."):
            st.session_state.messages.append({"role": "user", "content": user_prompt})
            with st.chat_message("user"):
                st.write(user_prompt)
            
            # Réponse IA simulée
            ai_reply = "J'ai transmis votre requête à notre équipe hôtelière. Elle sera traitée immédiatement !"
            if "serviette" in user_prompt.lower():
                ai_reply = "Des serviettes supplémentaires sont en route pour la Chambre 304."
            elif "restaurant" in user_prompt.lower():
                ai_reply = "Excellente idée ! Je vous ai envoyé les meilleures tables gastronomiques sur votre app."

            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            with st.chat_message("assistant"):
                st.write(ai_reply)

    # --- ONGLET 4 : SERVICES & CHECK-OUT ---
    with client_tab[3]:
        st.markdown("#### 🧾 Facturation & Check-out Express")
        st.write("Prestations en cours sur votre séjour :")
        
        extras_df = pd.DataFrame([
            {"Prestation": "Petit-Déjeuner Beldi", "Date": "Aujourd'hui", "Montant (MAD)": 0},
            {"Prestation": "Hammam & Spa Royal", "Date": "Hier", "Montant (MAD)": 600},
            {"Prestation": "Dîner Gastronomique (Room Service)", "Date": "Hier", "Montant (MAD)": 450},
        ])
        st.dataframe(extras_df, use_container_width=True)

        st.markdown(f"**Total Extras en cours :** `{st.session_state.extras_total} MAD`")
        
        if st.button("🚀 Effectuer le Check-out Express & Payer", type="primary", use_container_width=True):
            st.success("Check-out effectué avec succès ! Votre facture détaillée a été envoyée par email. Merci d'avoir séjourné chez nous.")


# =========================================================================
# FONCTION : BACK-OFFICE ADMIN HOTEL
# =========================================================================
def render_admin_dashboard():
    st.markdown("### 📊 Back-Office & Supervision Hôtelière")
    st.markdown("<p style='font-size: 12px; color: #94a3b8;'>Centre de contrôle en temps réel pour l'équipe de direction et la réception</p>", unsafe_allow_html=True)
    
    # KPI Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Taux Check-in Digital", "84.2%", "+12% ce mois")
    c2.metric("Clés BLE Actives", "142 / 180", "78.8% taux d'usage")
    c3.metric("Satisfaction IA (CSAT)", "4.9 / 5", "98% résolu")
    c4.metric("Revenu Extras (Upsell)", "48,500 MAD", "+18% vs N-1")

    st.markdown("---")
    st.markdown("#### 🏨 Tableau de Suivi des Résidents & Clés Numériques")

    # Tableau de supervision des chambres
    rooms_data = pd.DataFrame([
        {"Chambre": "Chambre 304", "Client": "M. Karim Benani", "Check-in": "Validé (OCR OK)", "Clé Numérique": "Active (BLE)", "Requêtes IA": 4},
        {"Chambre": "Chambre 212", "Client": "Mme. Sarah Lahlou", "Check-in": "En attente ID", "Clé Numérique": "Non émise", "Requêtes IA": 0},
        {"Chambre": "Chambre 105", "Client": "M. Thomas Dupont", "Check-in": "Validé (OCR OK)", "Clé Numérique": "Active (NFC)", "Requêtes IA": 2},
        {"Chambre": "Chambre 402", "Client": "M. Mehdi Tazi", "Check-in": "Validé (OCR OK)", "Clé Numérique": "Active (BLE)", "Requêtes IA": 1},
    ])
    
    st.dataframe(rooms_data, use_container_width=True)

    # Actions Admin rapides
    col_act1, col_act2 = st.columns(2)
    with col_act1:
        selected_room = st.selectbox("Sélectionner une chambre pour action", ["Chambre 304", "Chambre 212", "Chambre 105"])
        if st.button("🔓 Forcer le déverrouillage à distance"):
            st.success(f"Ordre de déverrouillage envoyé par IoT à la {selected_room}.")
    with col_act2:
        if st.button("🚫 Révoquer la clé numérique"):
            st.warning(f"La clé numérique de la {selected_room} a été révoquée.")

    st.markdown("---")
    st.markdown("#### 📈 Analyses & Ventes Additionnelles (Générées par l'IA)")
    
    # Graphique Streamlit natif
    chart_data = pd.DataFrame(
        [18500, 14200, 9800, 6000],
        index=["Spa & Hammam", "Room Service", "Excursions", "Late Check-out"]
    )
    st.bar_chart(chart_data, color="#eab308")


# =========================================================================
# ROUTAGE DES VUES PRINCIPALES
# =========================================================================
if view_mode == "📱 Application Mobile Client":
    render_client_app()
elif view_mode == "📊 Back-Office Admin Hôtel":
    render_admin_dashboard()
else:  # Vue Split
    col_left, col_right = st.columns(2)
    with col_left:
        render_client_app()
    with col_right:
        render_admin_dashboard()