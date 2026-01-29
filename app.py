# app.py - Clinical UI v4.0
import streamlit as st
from database import PEPTIDE_PRESETS
from calculator import calculate_dosage

# --- 1. PAGE CONFIG ---
st.set_page_config(
    page_title="PeptideCalc Pro v4.0",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS STYLING (Syringe & Clinical Boxes) ---
st.markdown("""
<style>
    .syringe-container {
        border: 2px solid #333;
        border-radius: 4px;
        background-color: #f0f0f0;
        height: 35px;
        width: 100%;
        position: relative;
        margin: 15px 0;
    }
    .syringe-liquid {
        background-color: #ff4b4b;
        height: 100%;
        border-radius: 2px 0 0 2px;
        transition: width 0.8s ease-in-out;
    }
    .syringe-markings {
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: repeating-linear-gradient(90deg, transparent, transparent 19%, #000 20%);
        opacity: 0.2;
    }
    .benefit-box {
        background-color: #1e2a1e;
        border-left: 5px solid #4bff4b;
        padding: 15px;
        border-radius: 5px;
        color: #d1ffd1;
        margin-bottom: 15px;
    }
    .side-effect-box {
        background-color: #3e1818;
        border-left: 5px solid #ff4b4b;
        padding: 15px;
        border-radius: 5px;
        color: #ffd1d1;
        margin-bottom: 15px;
    }
    .db-tag {
        background-color: #4b4bff;
        color: white;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.85em;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. PERSISTENT STATE & PRESET LOADER ---
if 'vial_val' not in st.session_state: st.session_state.vial_val = 30.0
if 'dose_val' not in st.session_state: st.session_state.dose_val = 2.5

def update_presets():
    selected = st.session_state.peptide_selector
    data = PEPTIDE_PRESETS[selected]
    st.session_state.vial_val = float(data["vial_mg"])
    st.session_state.dose_val = float(data["dose_mcg"])

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🧪 Peptide Pro v4.0")
    page = st.radio("Navigation", ["🧮 Calculator", "📚 Peptide Database"])
    st.divider()
    st.caption("Professional Reconstitution Tool")

# --- 5. CALCULATOR PAGE ---
if page == "🧮 Calculator":
    st.header("🧪 Reconstitution Calculator")
    
    left, right = st.columns([1, 1.3], gap="large")
    
    with left:
        st.subheader("1️⃣ Inputs")
        # Peptide Selection
        selected_p = st.selectbox(
            "Select Peptide Profile", 
            sorted(PEPTIDE_PRESETS.keys()), 
            key="peptide_selector", 
            on_change=update_presets
        )
        info = PEPTIDE_PRESETS[selected_p]
        
        # Reconstitution Math Inputs
        c1, c2 = st.columns([2, 1])
        v_qty = c1.number_input("Vial Quantity (Mass/Units)", key="vial_val", format="%.2f")
        v_unit = c2.selectbox("Unit", ["mg", "mcg", "IU"], index=0)
        
        water = st.number_input("Bacteriostatic Water (mL)", value=2.0, step=0.5, min_value=0.1)
        
        c3, c4 = st.columns([2, 1])
        d_qty = c3.number_input("Desired Dose", key="dose_val", format="%.2f")
        d_unit = c4.selectbox("Dose Unit", ["mcg", "mg", "IU"], index=0)
        
        syringe_type = st.radio("Syringe Type", ["U-100 (Standard)", "U-40 (Vet)"], horizontal=True)
        s_factor = 100 if "U-100" in syringe_type else 40

    with right:
        st.subheader("2️⃣ Results & Clinical Data")
        
        # Calculate Logic
        d_ml, units, per_vial, strength = calculate_dosage(v_qty, v_unit, water, d_qty, d_unit, s_factor, info)
        
        if units > 0:
            # Metrics
            m1, m2, m3 = st.columns(3)
            m1.metric("Draw Volume", f"{d_ml:.4f} mL")
            m2.metric("Syringe Units", f"{units:.1f} Units")
            m3.metric("Doses per Vial", int(per_vial))
            
            # Visual Syringe
            pct = min((units / s_factor) * 100, 100)
            st.markdown(f"**Visual Fill ({units:.1f} Units):**")
            st.markdown(f'''
                <div class="syringe-container">
                    <div class="syringe-liquid" style="width: {pct}%;"></div>
                    <div class="syringe-markings"></div>
                </div>
            ''', unsafe_allow_html=True)
            
            # Clinical Highlights
            st.markdown(f"### 📖 {selected_p} Profile")
            
            with st.container():
                st.markdown("**🌟 Clinical Benefits:**")
                st.markdown(f'<div class="benefit-box">{info["benefits_detailed"]}</div>', unsafe_allow_html=True)
                
                st.markdown("**⚠️ Side Effects & Contraindications:**")
                st.markdown(f'<div class="side-effect-box">{info["side_effects_detailed"]}</div>', unsafe_allow_html=True)
                
                st.markdown("**📋 Protocol & Timing:**")
                st.info(info['protocol_detailed'])
                
                st.caption(f"**❄️ Storage:** {info['storage']}")
        else:
            st.warning("Please enter a valid dosage to see calculations.")

    st.divider()
    st.subheader("💉 Injection Guide")
    st.write("Subcutaneous injections should be rotated frequently to prevent lipohypertrophy.")
    

# --- 6. DATABASE PAGE ---
else:
    st.header("📚 Complete Clinical Database")
    
    search = st.text_input("🔍 Search Peptides (e.g. 'Fat Loss' or 'BPC')", "").lower()
    
    # Grid Layout for Database
    db_cols = st.columns(2)
    filtered_peptides = {n: d for n, d in PEPTIDE_PRESETS.items() if search in n.lower() or search in d['type'].lower()}
    
    for idx, (name, data) in enumerate(filtered_peptides.items()):
        with db_cols[idx % 2]:
            with st.container(border=True):
                st.markdown(f"### {name}")
                st.markdown(f'<span class="db-tag">{data["type"]}</span>', unsafe_allow_html=True)
                st.write(f"*{data['desc']}*")
                
                with st.expander("Show Full Clinical Data"):
                    st.markdown("**Benefits:**")
                    st.write(data['benefits_detailed'])
                    st.markdown("**Side Effects:**")
                    st.write(data['side_effects_detailed'])
                    st.markdown("**Standard Protocol:**")
                    st.write(data['protocol_detailed'])
