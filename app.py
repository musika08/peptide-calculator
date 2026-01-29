# app.py
import streamlit as st
import sys
import os

# FORCE PATH RECOGNITION
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    from database import get_peptide_data
    from calculator import render_calculator_page
except ImportError as e:
    st.error(f"Critical Error: {e}. Ensure database.py and calculator.py are in the same folder as app.py.")
    st.stop()

# --- APP CONFIG ---
st.set_page_config(page_title="PeptideCalc Pro", page_icon="🧪", layout="wide")

# --- CSS STYLES ---
st.markdown("""
<style>
    .syringe-container { border: 2px solid #333; border-radius: 4px; background: #f0f0f0; height: 30px; width: 100%; position: relative; margin: 10px 0; }
    .syringe-liquid { background: #ff4b4b; height: 100%; transition: width 0.5s; }
    .syringe-markings { position: absolute; inset: 0; background: repeating-linear-gradient(90deg, transparent, transparent 19%, #000 20%); opacity: 0.1; }
    .db-tag { background: #4b4bff; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.8em; font-weight: bold; display: inline-block; }
</style>
""", unsafe_allow_html=True)

# --- LOAD ---
PEPTIDE_PRESETS, FACTORS = get_peptide_data()

# --- INITIALIZE STATE ---
if 'vial_val' not in st.session_state: st.session_state.vial_val = 30.0
if 'dose_val' not in st.session_state: st.session_state.dose_val = 2.5
if 'calc_count' not in st.session_state: st.session_state.calc_count = 0

# --- SIDEBAR ---
page = st.sidebar.radio("Navigation", ["🧮 Calculator", "📚 Peptide Database"])
st.sidebar.divider()
st.sidebar.caption("v4.0 | Modular")

if page == "🧮 Calculator":
    render_calculator_page(PEPTIDE_PRESETS)
else:
    st.subheader("📚 Peptide Database")
    query = st.text_input("🔍 Search", placeholder="Search peptides...").lower()
    
    items = {n: d for n, d in PEPTIDE_PRESETS.items() if query in n.lower() or query in d['desc'].lower()}
    
    cols = st.columns(3)
    for idx, (name, info) in enumerate(items.items()):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"### {name}")
                st.markdown(f"<span class='db-tag'>{info['type']}</span>", unsafe_allow_html=True)
                st.write(info['desc'])
                with st.expander("Show Details"):
                    st.markdown(info['benefits_detailed'])
