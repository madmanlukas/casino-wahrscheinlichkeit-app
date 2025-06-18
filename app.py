import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="Rot vs. Schwarz mit Verlauf (Bilder)", layout="centered")
st.title("🎲 Rot-oder-Schwarz Wahrscheinlichkeits-Rechner mit Kartenbildern")

# Kartenbilder laden
def load_images():
    img_rot = Image.open("ass_rot.png")
    img_schwarz = Image.open("ass_schwarz.png")
    return img_rot, img_schwarz

# Prüfe, ob Bilder vorhanden sind, sonst Hinweis
if not (os.path.exists("ass_rot.png") and os.path.exists("ass_schwarz.png")):
    st.error("Bitte stelle sicher, dass die Dateien 'ass_rot.png' und 'ass_schwarz.png' im gleichen Ordner liegen wie dieses Skript.")
    st.stop()

img_rot, img_schwarz = load_images()

# Session State initialisieren
if "verlauf" not in st.session_state:
    st.session_state.verlauf = []
if "rot" not in st.session_state:
    st.session_state.rot = 0
if "schwarz" not in st.session_state:
    st.session_state.schwarz = 0

def ziehe_farbe(farbe):
    st.session_state.verlauf.append(farbe)
    if len(st.session_state.verlauf) > 5:
        st.session_state.verlauf.pop(0)
    if farbe == "rot":
        st.session_state.rot += 1
    else:
        st.session_state.schwarz += 1

def rueckgaengig():
    if st.session_state.verlauf:
        letzte = st.session_state.verlauf.pop()
        if letzte == "rot":
            st.session_state.rot -= 1
        else:
            st.session_state.schwarz -= 1

# Buttons
col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("🔴 Rot gezogen"):
        ziehe_farbe("rot")
with col2:
    if st.button("⚫ Schwarz gezogen"):
        ziehe_farbe("schwarz")
with col3:
    if st.button("↩️ Zurück"):
        rueckgaengig()

# Verlauf mit Bildern anzeigen
st.subheader("🃏 Verlauf der letzten 5 Ziehungen:")
if st.session_state.verlauf:
    cols = st.columns(len(st.session_state.verlauf))
    for idx, farbe in enumerate(st.session_state.verlauf):
        if farbe == "rot":
            cols[idx].image(img_rot, width=80)
        else:
            cols[idx].image(img_schwarz, width=80)
else:
    st.write("Noch keine Ziehungen.")

# Wahrscheinlichkeiten anzeigen
gesamt = st.session_state.rot + st.session_state.schwarz

st.subheader("📊 Bisherige Ziehungen:")
st.write(f"🔴 Rot: {st.session_state.rot}")
st.write(f"⚫ Schwarz: {st.session_state.schwarz}")
st.write(f"📦 Gesamt: {gesamt}")

st.subheader("🔮 Wahrscheinlichkeit für die nächste Karte:")
if gesamt == 0:
    st.info("Noch keine Ziehungen – theoretisch 50 % / 50 %")
    p_rot, p_schwarz = 0.5, 0.5
else:
    p_rot = st.session_state.rot / gesamt
    p_schwarz = st.session_state.schwarz / gesamt
    st.success(f"🔴 Rot: {p_rot:.2%}")
    st.success(f"⚫ Schwarz: {p_schwarz:.2%}")

# Reset Button
if st.button("🔄 Zurücksetzen"):
    st.session_state.verlauf = []
    st.session_state.rot = 0
    st.session_state.schwarz = 0
