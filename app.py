import streamlit as st

st.set_page_config(page_title="Rot vs. Schwarz", layout="centered")
st.title("🎲 Rot-oder-Schwarz-Wahrscheinlichkeits-Rechner")

if "rot" not in st.session_state:
    st.session_state.rot = 0
if "schwarz" not in st.session_state:
    st.session_state.schwarz = 0

col1, col2 = st.columns(2)
with col1:
    if st.button("🔴 Rot gezogen"):
        st.session_state.rot += 1
with col2:
    if st.button("⚫ Schwarz gezogen"):
        st.session_state.schwarz += 1

gesamt = st.session_state.rot + st.session_state.schwarz

st.subheader("📊 Bisherige Ziehungen:")
st.write(f"🔴 Rot: {st.session_state.rot}")
st.write(f"⚫ Schwarz: {st.session_state.schwarz}")
st.write(f"📦 Gesamt: {gesamt}")

st.subheader("🔮 Nächste Karte – Wahrscheinlichkeit:")
if gesamt == 0:
    st.info("Noch keine Ziehungen – theoretisch 50 % / 50 %")
    p_rot, p_schwarz = 0.5, 0.5
else:
    p_rot = st.session_state.rot / gesamt
    p_schwarz = st.session_state.schwarz / gesamt

st.success(f"🔴 Rot: {p_rot:.2%}")
st.success(f"⚫ Schwarz: {p_schwarz:.2%}")

if st.button("🔄 Zurücksetzen"):
    st.session_state.rot = 0
    st.session_state.schwarz = 0

