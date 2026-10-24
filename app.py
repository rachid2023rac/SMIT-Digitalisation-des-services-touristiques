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
    </style>
""", unsafe_allow_html=True)

# --- INITIALISATION DE LA SESSION STATE ---
if "is_unlocked" not in st.session_state:
    st.session_state.is_unlocked = False
if "ocr_validated" not in st.session_state:
    st.session_state.ocr_validated = True
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
    ["📱 Application Client (Guest App)", "📊 Back-Office & KPIs Admin", "⚙️ Vue Split (Côte à côte)"]
)

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Réinitialiser la Démo", use_container_width=True):
    st.session_state.clear()
    st.rerun()


# =========================================================================
# 1. APPLICATION MOBILE CLIENT (GUEST APP)
# =========================================================================
def render_client_app():
    st.markdown("### 📱 Application Client (Guest App)")
    st.markdown("<p style='font-size: 12px; color: #94a3b8;'>Hôtel Palais Royal Atlas • Chambre 304</p>", unsafe_allow_html=True)
    
    client_tab = st.tabs(["🔑 Clé Numérique", "📋 Check-in OCR", "🤖 Yasmine (IA)", "🧾 Extras & Départ"])

    # --- ONGLET 1 : CLÉ NUMÉRIQUE BLUETOOTH / NFC (CHAMBRE 304) ---
    with client_tab[0]:
        st.markdown("#### 🔒 Clé Numérique (Chambre 304)")
        st.info("Approchez votre smartphone de la serrure connectée (BLE / NFC).")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            lock_status = st.session_state.is_unlocked
            bg_color = "rgba(16, 185, 129, 0.2)" if lock_status else "rgba(15, 23, 42, 0.8)"
            border_color = "#10b981" if lock_status else "#334155"
            icon = "🔓" if lock_status else "🔒"
            text_state = "DÉVERROUILLÉ (Porte 304 Ouverte)" if lock_status else "VERROUILLÉ"
            text_color = "#10b981" if lock_status else "#94a3b8"

            st.markdown(f"""
                <div style="background: {bg_color}; border: 3px solid {border_color}; padding: 30px; border-radius: 50%; width: 150px; height: 150px; display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 0 auto; text-align: center; box-shadow: 0 0 25px rgba(234, 179, 8, 0.2);">
                    <span style="font-size: 35px;">{icon}</span>
                </div>
                <p style="text-align: center; font-weight: bold; color: {text_color}; margin-top: 15px;">{text_state}</p>
            """, unsafe_allow_html=True)

            if st.button("📲 Simuler le Tap Bluetooth / NFC", use_container_width=True):
                st.session_state.is_unlocked = not st.session_state.is_unlocked
                st.rerun()

        st.markdown("---")
        c_a, c_b = st.columns(2)
        c_a.metric("Wi-Fi Haut Débit", "PalaisRoyal2026")
        c_b.metric("Climatisation", "21°C (Auto)")

    # --- ONGLET 2 : CHECK-IN 100% DIGITAL & OCR ---
    with client_tab[1]:
        st.markdown("#### 📋 Check-in 100% Digital & Scan OCR")
        if st.session_state.ocr_validated:
            st.success("✅ Pièce d'identité validée par OCR (Passeport / CNI n° AB98231).")
            if st.button("🔄 Refaire le scan ID"):
                st.session_state.ocr_validated = False
                st.rerun()
        else:
            uploaded_id = st.file_uploader("Téléverser Passeport ou CNI pour Scan OCR", type=["png", "jpg", "pdf"])
            arrival_slot = st.selectbox("Heure d'arrivée estimée", ["14:00 - Standard", "12:00 - Early Check-in", "17:00 - Arrivée Tardive"])
            signature_text = st.text_input("Signature Tactile / Électronique", "Karim Benani")
            
            if st.button("Valider le Check-in OCR"):
                st.session_state.ocr_validated = True
                st.success("Check-in validé avec succès ! Votre clé numérique est active.")
                st.rerun()

    # --- ONGLET 3 : CONCIERGE IA "YASMINE" ---
    with client_tab[2]:
        st.markdown("#### 🤖 Yasmine - Concierge IA")
        
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        st.caption("Requêtes instantanées suggérées :")
        col_r1, col_r2, col_r3 = st.columns(3)
        if col_r1.button("🧺 Serviettes"):
            st.session_state.messages.append({"role": "user", "content": "Demander des serviettes supplémentaires"})
            st.session_state.messages.append({"role": "assistant", "content": "C'est noté ! J'envoie deux serviettes de bain supplémentaires à la Chambre 304 d'ici 5 minutes."})
            st.rerun()
        if col_r2.button("☕ Petit-déj Beldi"):
            st.session_state.messages.append({"role": "user", "content": "Commander le Petit-déjeuner Beldi en chambre"})
            st.session_state.messages.append({"role": "assistant", "content": "Votre Petit-déjeuner Beldi (Msemmen, Amlou, Huile d'Argan) a bien été enregistré pour demain à 8h30."})
            st.rerun()
        if col_r3.button("🧖 Hammam & Spa"):
            st.session_state.messages.append({"role": "user", "content": "Réserver une session Hammam & Spa"})
            st.session_state.messages.append({"role": "assistant", "content": "Votre session au Hammam & Spa Royal est confirmée pour aujourd'hui à 17:00 (600 MAD inclus sur votre note)."})
            st.rerun()

        if user_prompt := st.chat_input("Posez votre question à Yasmine..."):
            st.session_state.messages.append({"role": "user", "content": user_prompt})
            with st.chat_message("user"):
                st.write(user_prompt)
            
            ai_response = "J'ai bien pris en compte votre demande. Notre équipe s'en charge immédiatement !"
            if "serviette" in user_prompt.lower():
                ai_response = "Des serviettes supplémentaires sont en route pour la Chambre 304."
            elif "hammam" in user_prompt.lower() or "spa" in user_prompt.lower():
                ai_response = "Votre réservation au Hammam & Spa a été ajoutée à votre agenda digital."

            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            with st.chat_message("assistant"):
                st.write(ai_response)

    # --- ONGLET 4 : CHECK-OUT EXPRESS & EXTRAS (HAMMAM / PETIT-DÉJEUNER) ---
    with client_tab[3]:
        st.markdown("#### 🧾 Extras & Check-out Express")
        st.write("Détail de vos prestations et consommations :")
        
        extras_df = pd.DataFrame([
            {"Prestation": "Petit-Déjeuner Beldi Traditionnel", "Type": "Restauration", "Montant (MAD)": 0},
            {"Prestation": "Hammam & Soin Spa Royal", "Type": "Bien-être", "Montant (MAD)": 600},
            {"Prestation": "Dîner Gastronomique (Room Service)", "Type": "Restauration", "Montant (MAD)": 450},
        ])
        st.dataframe(extras_df, use_container_width=True)

        st.markdown(f"**Total Extras en cours :** `{st.session_state.extras_total} MAD`")
        
        if st.button("🚀 Effectuer le Check-out Express en 1 clic", type="primary", use_container_width=True):
            st.success("Check-out effectué avec succès ! Facture acquittée et transmise par e-mail. Merci de votre séjour.")


# =========================================================================
# 2. BACK-OFFICE ADMIN HÔTEL (KPIs, VALIDATION OCR, UPSELLING)
# =========================================================================
def render_admin_dashboard():
    st.markdown("### 📊 Back-Office & Pilotage Hôtelier")
    st.markdown("<p style='font-size: 12px; color: #94a3b8;'>Supervision globale, validation OCR, clés actives et analyse d'upsell</p>", unsafe_allow_html=True)
    
    # 1. Tableau de bord KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Taux de Digitalisation", "84.2%", "+12% vs mois dernier")
    c2.metric("Clés Actives (BLE/NFC)", "142 / 180", "Actives en temps réel")
    c3.metric("Satisfaction IA (CSAT)", "4.9 / 5", "98% de requêtes résolues")
    c4.metric("Revenus Upselling Extras", "48,500 MAD", "+18% via Yasmine")

    st.markdown("---")

    # 2. Validation OCR & Suivi des Résidents
    st.markdown("#### 📋 Validation OCR & Suivi des Check-ins en Temps Réel")
    
    guests_df = pd.DataFrame([
        {"Chambre": "Chambre 304", "Client": "M. Karim Benani", "Statut OCR": "Validé (Automatique)", "Clé Numérique": "Active (BLE)", "Requêtes IA": 4},
        {"Chambre": "Chambre 212", "Client": "Mme. Sarah Lahlou", "Statut OCR": "En attente pièce ID", "Clé Numérique": "Non émise", "Requêtes IA": 0},
        {"Chambre": "Chambre 105", "Client": "M. Thomas Dupont", "Statut OCR": "Validé (Automatique)", "Clé Numérique": "Active (NFC)", "Requêtes IA": 2},
        {"Chambre": "Chambre 402", "Client": "M. Mehdi Tazi", "Statut OCR": "Validé (Automatique)", "Clé Numérique": "Active (BLE)", "Requêtes IA": 1},
    ])
    st.dataframe(guests_df, use_container_width=True)

    col_adm1, col_adm2 = st.columns(2)
    with col_adm1:
        target_room = st.selectbox("Sélectionner une chambre", ["Chambre 304", "Chambre 212", "Chambre 105", "Chambre 402"])
        if st.button("🔓 Forcer l'ouverture à distance"):
            st.success(f"Ordre IoT envoyé : Porte de la {target_room} déverrouillée.")
    with col_adm2:
        if st.button("🚫 Révoquer la clé numérique d'accès"):
            st.warning(f"La clé numérique de la {target_room} a été révoquée immédiatement.")

    st.markdown("---")

    # 3. Statistiques d'Upselling (Hammam, Petit-déjeuner Beldi, Extras)
    st.markdown("#### 📈 Statistiques d'Upsell & Ventes Additionnelles (Générées par l'IA)")
    
    upsell_data = pd.DataFrame(
        [18500, 14200, 9800, 6000],
        index=["Hammam & Spa Royal", "Petit-Déjeuner Beldi", "Room Service", "Late Check-out"]
    )
    st.bar_chart(upsell_data, color="#eab308")


# =========================================================================
# ROUTAGE DES VUES
# =========================================================================
if view_mode == "📱 Application Client (Guest App)":
    render_client_app()
elif view_mode == "📊 Back-Office & KPIs Admin":
    render_admin_dashboard()
else:
    col_l, col_r = st.columns(2)
    with col_l:
        render_client_app()
    with col_r:
        render_admin_dashboard()