import streamlit as st

st.set_page_config(page_title="Schwarz oder Rot", page_icon="🃏")

# Initialisierung des Session-State
if 'history' not in st.session_state:
    st.session_state.history = []

# Ziehung hinzufügen
def add_draw(color):
    st.session_state.history.append(color)
    if len(st.session_state.history) > 5:
        st.session_state.history.pop(0)

# Letzte Ziehung entfernen
def undo_draw():
    if st.session_state.history:
        st.session_state.history.pop()

# Anzeige
st.title("🃏 Schwarz oder Rot - Wahrscheinlichkeitsrechner")

# Verlauf anzeigen
st.subheader("Letzte 5 Ziehungen:")
emoji_map = {'red': '🟥', 'black': '⬛'}
st.markdown("".join(emoji_map[c] for c in st.session_state.history))

# Buttons
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("🟥 Rot"):
        add_draw('red')
with col2:
    if st.button("⬛ Schwarz"):
        add_draw('black')
with col3:
    if st.button("⤺ Zurück"):
        undo_draw()

# Wahrscheinlichkeiten berechnen
red_count = st.session_state.history.count('red')
black_count = st.session_state.history.count('black')
total = red_count + black_count

st.subheader("Wahrscheinlichkeiten:")
if total > 0:
    st.write(f"🟥 Rot: {red_count / total:.1%}")
    st.write(f"⬛ Schwarz: {black_count / total:.1%}")
else:
    st.write("Noch keine Ziehungen")

st.caption("Erwartete Wahrscheinlichkeit: 50% Rot / 50% Schwarz")
