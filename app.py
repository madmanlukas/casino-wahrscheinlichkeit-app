import streamlit as st
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Emoji-Zuordnung
emoji_map = {'red': '🟥', 'black': '⬛'}
label_map = {0: 'red', 1: 'black'}
reverse_map = {'red': 0, 'black': 1}

st.set_page_config(page_title="Lernendes Orakel", page_icon="🔮")
st.title("🔮 Lernendes Orakel – Schwarz oder Rot")

# Initialisierung
if 'history_all' not in st.session_state:
    st.session_state.history_all = []

if 'model' not in st.session_state:
    st.session_state.model = None

def train_model_from_history():
    # Trainingsdaten generieren aus history_all (5er Sequenzen)
    data = st.session_state.history_all
    X, y = [], []
    for i in range(len(data) - 5):
        seq = data[i:i+6]
        X.append([reverse_map[c] for c in seq[:5]])
        y.append(reverse_map[seq[5]])
    if X and y:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(np.array(X), np.array(y))
        st.session_state.model = model

# Eingabe-Handling
def add_draw(color):
    st.session_state.history_all.append(color)
    if len(st.session_state.history_all) >= 6:
        train_model_from_history()

def undo_draw():
    if st.session_state.history_all:
        st.session_state.history_all.pop()
        if len(st.session_state.history_all) >= 6:
            train_model_from_history()
        else:
            st.session_state.model = None

# Anzeige letzter 5
st.subheader("Letzte 5 Ziehungen:")
st.markdown("".join([emoji_map[c] for c in st.session_state.history_all[-5:]]))

# Buttons
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("🟥 Rot"):
        add_draw("red")
with col2:
    if st.button("⬛ Schwarz"):
        add_draw("black")
with col3:
    if st.button("⤺ Zurück"):
        undo_draw()

# Vorhersage
if len(st.session_state.history_all) < 6:
    remaining = 6 - len(st.session_state.history_all)
    st.info(f"🔄 Noch {remaining} Eingabe{'n' if remaining != 1 else ''}, bis Vorhersagen verfügbar sind.")
elif st.session_state.model:
    input_seq = [reverse_map[c] for c in st.session_state.history_all[-5:]]
    prediction = st.session_state.model.predict([input_seq])[0]
    probabilities = st.session_state.model.predict_proba([input_seq])[0]

    st.subheader("🔮 Orakel sagt:")
    st.markdown(f"**Nächste Karte:** {emoji_map[label_map[prediction]]}")
    st.markdown(f"**🟥 Rot:** {probabilities[0]*100:.1f}%")
    st.markdown(f"**⬛ Schwarz:** {probabilities[1]*100:.1f}%")
    st.caption("Hinweis: Das Orakel berücksichtigt alle bisherigen Eingaben – es erkennt scheinbare Muster, aber keine echten Wahrscheinlichkeiten.")

# Statistik – aufklappbar
with st.expander("📊 Statistik anzeigen"):
    total = len(st.session_state.history_all)
    red_count = st.session_state.history_all.count("red")
    black_count = st.session_state.history_all.count("black")

    if total > 0:
        red_pct = (red_count / total) * 100
        black_pct = (black_count / total) * 100
    else:
        red_pct = black_pct = 0

    st.write(f"**Gesamtanzahl Züge:** {total}")
    st.write(f"🟥 **Rot:** {red_count} ({red_pct:.1f} %)")
    st.write(f"⬛ **Schwarz:** {black_count} ({black_pct:.1f} %)")

