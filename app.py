import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

st.set_page_config(page_title="Rot vs. Schwarz – Empirische & Erwartete Wahrscheinlichkeiten", layout="centered")
st.title("🎲 Rot oder Schwarz – Wahrscheinlichkeiten mit Kartenbildern")

def create_ace_card(color):
    img = Image.new("RGBA", (100,140), "white")  # weißer Hintergrund
    draw = ImageDraw.Draw(img)
    border_color = "red" if color == "rot" else "black"
    text_color = "red" if color == "rot" else "black"

    draw.rectangle([5,5,95,135], outline=border_color, width=4)
    try:
        font = ImageFont.truetype("arial.ttf", 70)
    except:
        font = ImageFont.load_default()
    w, h = draw.textsize("A", font=font)
    draw.text(((100 - w)/2, (140 - h)/2 - 10), "A", fill=text_color, font=font)
    return img

img_rot_path = "ass_rot.png"
img_schwarz_path = "ass_schwarz.png"

if not os.path.exists(img_rot_path):
    create_ace_card("rot").save(img_rot_path)
if not os.path.exists(img_schwarz_path):
    create_ace_card("schwarz").save(img_schwarz_path)

img_rot = Image.open(img_rot_path)
img_schwarz = Image.open(img_schwarz_path)

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

gesamt = st.session_state.rot + st.session_state.schwarz

if gesamt > 0:
    p_emp_rot = st.session_state.rot / gesamt
    p_emp_schwarz = st.session_state.schwarz / gesamt
else:
    p_emp_rot = p_emp_schwarz = 0.5

p_exp_rot = 0.5
p_exp_schwarz = 0.5

st.subheader("📊 Wahrscheinlichkeiten für die nächste Karte:")
st.write("**Empirisch geschätzt (basierend auf bisherigen Ziehungen):**")
st.write(f"🔴 Rot: {p_emp_rot:.2%}")
st.write(f"⚫ Schwarz: {p_emp_schwarz:.2%}")

st.write("**Erwartet (theoretisch):**")
st.write(f"🔴 Rot: {p_exp_rot:.2%}")
st.write(f"⚫ Schwarz: {p_exp_schwarz:.2%}")

st.write("---")
st.write("### Beispiel zur Interpretation:")
st.write("""
Wenn du z.B. bisher 4x Schwarz und 1x Rot gezogen hast, ist die empirische Wahrscheinlichkeit für Rot nur 20%,  
aber die erwartete Wahrscheinlichkeit bleibt bei 50%.  
Das bedeutet: Die bisherige Beobachtung zeigt eine Schieflage,  
aber die theoretische Chance für die nächste Karte ist unverändert 50% / 50%.
""")

if st.button("🔄 Zurücksetzen"):
    st.session_state.verlauf = []
    st.session_state.rot = 0
    st.session_state.schwarz = 0
