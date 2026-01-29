# app.py
import streamlit as st
from database import get_peptide_data
from calculator import render_calculator_page

# --- CONFIG ---
st.set_page_config(page_title="PeptideCalc Pro v4.0", page_icon="🧪", layout="wide")

# --- STYLES ---
st.markdown("""
<style>
    .syringe-container { border: 2px solid #333; border-radius: 4px; background-color: #f0f0f0; height: 30px; width: 100%; position: relative; margin-top: 10px; margin-bottom: 10px; }
    .syringe-liquid { background-color: #ff4b4b; height: 100%; border-radius: 2px 0 0 2px; transition: width 0.5s ease-in-out; }
    .syringe-markings { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: repeating-linear-gradient(90deg, transparent, transparent 19%, #000 20%); opacity: 0.1; }
    .db-tag { background-color: #4b4bff; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.8em; font-weight: bold; display: inline-block; margin-bottom: 10px; }
    .side-effect-box { background-color: #3e1818; border-left: 4px solid #ff4b4b; padding: 10px; margin-top: 10px; border-radius: 4px; font-size: 0.9em; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
PEPTIDE_PRESETS, FACTORS = get_peptide_data()

# --- STATE ---
if 'vial_val' not in st.session_state: st.session_state.vial_val = 30.0
if 'dose_val' not in st.session_state: st.session_state.dose_val = 2.5
if 'calc_count' not in st.session_state: st.session_state.calc_count = 0

# --- NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["🧮 Calculator", "📚 Peptide Database"])
st.sidebar.divider()
st.sidebar.caption("v4.0 | Modular Build")

if page == "🧮 Calculator":
    render_calculator_page(PEPTIDE_PRESETS)

elif page == "📚 Peptide Database":
    st.subheader("📚 Peptide Database")
    st.divider()
    
    col_search, col_filter = st.columns([3, 1])
    search_query = col_search.text_input("🔍 Search Peptides", placeholder="Search...").lower()
    all_cats = ["All", "Slimming & Fat Loss", "Skin, Hair & Beauty", "Muscle & Workout", "Nootropics & Brain", "Injury & Repair", "Wellness & Longevity", "Libido & Sexual Health"]
    category_filter = col_filter.selectbox("🏷️ Filter", all_cats)

    filtered_items = {n: d for n, d in PEPTIDE_PRESETS.items() 
                      if (category_filter == "All" or d.get('filter_cat') == category_filter)
                      and (search_query in n.lower() or search_query in d['benefits_detailed'].lower())}

    cols = st.columns(3)
    for idx, (name, info) in enumerate(filtered_items.items()):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"### {name}")
                st.markdown(f"<span class='db-tag'>{info['type']}</span>", unsafe_allow_html=True)
                st.markdown("**🌟 Clinical Benefits:**")
                st.markdown(info['benefits_detailed'])
                st.markdown(f"<div class='side-effect-box'><strong>⚠️ Side Effects:</strong><br>{info['side_effects_detailed'].replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
                with st.expander("📋 Detailed Protocol"):
                     st.markdown(info['protocol_detailed'])
                with st.expander("ℹ️ Mechanism & Storage"):
                    st.markdown(f"_{info['desc']}_")
                    st.markdown(f"**❄️ Storage:** {info['storage']}")
