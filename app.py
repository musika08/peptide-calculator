import streamlit as st
from database import PEPTIDE_PRESETS
from calculator import calculate_dosage

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="PeptideCalc Pro v4.0", page_icon="🧪", layout="wide")

# --- 2. STYLING ---
st.markdown("""
<style>
    .syringe-container { border: 2px solid #333; border-radius: 4px; background-color: #f0f0f0; height: 30px; width: 100%; position: relative; margin: 10px 0; }
    .syringe-liquid { background-color: #ff4b4b; height: 100%; border-radius: 2px 0 0 2px; transition: width 0.5s ease-in-out; }
    .syringe-markings { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: repeating-linear-gradient(90deg, transparent, transparent 19%, #000 20%); opacity: 0.1; }
    .db-tag { background-color: #4b4bff; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.8em; font-weight: bold; display: inline-block; }
    .side-effect-box { background-color: #3e1818; border-left: 4px solid #ff4b4b; padding: 10px; border-radius: 4px; font-size: 0.9em; }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'vial_val' not in st.session_state: st.session_state.vial_val = 30.0
if 'dose_val' not in st.session_state: st.session_state.dose_val = 2.5

def load_preset():
    data = PEPTIDE_PRESETS[st.session_state.peptide_selector]
    st.session_state.vial_val = float(data["vial_mg"])
    st.session_state.dose_val = float(data["dose_mcg"])

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🧪 Peptide Pro")
    page = st.radio("Navigation", ["🧮 Calculator", "📚 Database"])

# --- 5. CALCULATOR PAGE ---
if page == "🧮 Calculator":
    st.subheader("🧪 Reconstitution Calculator")
    col1, col2 = st.columns([1, 1.2], gap="large")

    with col1:
        st.write("### 1️⃣ Input Settings")
        selected = st.selectbox("Select Peptide", sorted(PEPTIDE_PRESETS.keys()), key="peptide_selector", on_change=load_preset)
        info = PEPTIDE_PRESETS[selected]
        
        c_vial, c_unit = st.columns([2,1])
        v_qty = c_vial.number_input("Stock Amount", key="vial_val")
        v_unit = c_unit.selectbox("Unit", ["mg", "mcg", "g", "IU"])
        
        water = st.number_input("Bacteriostatic Water (mL)", value=2.0)
        
        c_dose, c_dunit = st.columns([2,1])
        d_qty = c_dose.number_input("Desired Dose", key="dose_val")
        d_unit = c_dunit.selectbox("Dose Unit", ["mg", "mcg", "IU"])
        
        syringe = st.radio("Syringe Type", ["U-100", "U-40"], horizontal=True)
        s_factor = 100 if "100" in syringe else 40

    with col2:
        st.write("### 2️⃣ Results")
        d_ml, units, per_vial, strength = calculate_dosage(v_qty, v_unit, water, d_qty, d_unit, s_factor, info)
        
        if units > 0:
            m1, m2, m3 = st.columns(3)
            m1.metric("Draw (mL)", f"{d_ml:.4f}")
            m2.metric("Units", f"{units:.1f}")
            m3.metric("Doses", int(per_vial))
            
            pct = min(units / s_factor * 100, 100)
            st.markdown(f'<div class="syringe-container"><div class="syringe-liquid" style="width: {pct}%;"></div><div class="syringe-markings"></div></div>', unsafe_allow_html=True)
            st.caption(f"Draw to **{units:.1f}** on a {syringe} syringe.")
            
            with st.expander(f"📖 {selected} Profile", expanded=True):
                st.markdown(info['benefits_summary'])
                st.markdown(f"<div class='side-effect-box'><strong>Side Effects:</strong><br>{info['side_effects_summary']}</div>", unsafe_allow_html=True)

# --- 6. DATABASE PAGE ---
else:
    st.subheader("📚 Clinical Database")
    # Simple search/filter
    search = st.text_input("🔍 Search Peptides").lower()
    for name, data in PEPTIDE_PRESETS.items():
        if search in name.lower():
            with st.container(border=True):
                st.markdown(f"### {name} <span class='db-tag'>{data['type']}</span>", unsafe_allow_html=True)
                st.write(data['benefits_detailed'])


