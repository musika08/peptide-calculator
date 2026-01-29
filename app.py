# app.py - Clinical UI v4.0 (Full Data Restoration)
import streamlit as st
from database import PEPTIDE_PRESETS
from calculator import calculate_dosage

# --- 1. PAGE CONFIG ---
st.set_page_config(
    page_title="PeptideCalc Pro v4.0",
    page_icon="🧪",
    layout="wide"
)

# --- 2. CSS STYLING (Restoring Visual Depth) ---
st.markdown("""
<style>
    .syringe-container {
        border: 2px solid #333; border-radius: 4px; background-color: #f0f0f0;
        height: 35px; width: 100%; position: relative; margin: 15px 0;
    }
    .syringe-liquid {
        background-color: #ff4b4b; height: 100%; border-radius: 2px 0 0 2px;
        transition: width 0.8s ease-in-out;
    }
    .syringe-markings {
        position: absolute; top: 0; left: 0; right: 0; bottom: 0;
        background: repeating-linear-gradient(90deg, transparent, transparent 19%, #000 20%);
        opacity: 0.2;
    }
    .clinical-card {
        padding: 20px; border-radius: 10px; margin-bottom: 20px; line-height: 1.6;
    }
    .benefit-section { background-color: #1e2a1e; border-left: 5px solid #4bff4b; color: #d1ffd1; }
    .warning-section { background-color: #3e1818; border-left: 5px solid #ff4b4b; color: #ffd1d1; }
    .protocol-section { background-color: #1a1c23; border-left: 5px solid #4b4bff; color: #d1d1ff; }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'vial_val' not in st.session_state: st.session_state.vial_val = 30.0
if 'dose_val' not in st.session_state: st.session_state.dose_val = 2.5

def update_presets():
    data = PEPTIDE_PRESETS[st.session_state.peptide_selector]
    st.session_state.vial_val = float(data["vial_mg"])
    st.session_state.dose_val = float(data["dose_mcg"])

# --- 4. CALCULATOR INTERFACE ---
st.title("🧪 PeptideCalc Pro v4.0")
st.divider()

col_input, col_result = st.columns([1, 1.4], gap="large")

with col_input:
    st.subheader("1️⃣ Setup & Math")
    selected_p = st.selectbox("Select Peptide Profile", sorted(PEPTIDE_PRESETS.keys()), key="peptide_selector", on_change=update_presets)
    info = PEPTIDE_PRESETS[selected_p]
    
    c1, c2 = st.columns(2)
    v_qty = c1.number_input("Vial Amount", key="vial_val", format="%.2f")
    v_unit = c2.selectbox("Vial Unit", ["mg", "mcg", "IU"], index=0)
    
    water = st.number_input("Bacteriostatic Water (mL)", value=2.0, step=0.5)
    
    c3, c4 = st.columns(2)
    d_qty = c3.number_input("Desired Dose", key="dose_val", format="%.2f")
    d_unit = c4.selectbox("Dose Unit", ["mcg", "mg", "IU"], index=0)
    
    syringe_type = st.radio("Syringe Type", ["U-100 (Standard)", "U-40 (Vet)"], horizontal=True)
    s_factor = 100 if "U-100" in syringe_type else 40

    # --- RECONSTITUTION GUIDE (RESTORED) ---
    with st.expander("🛠️ How to Reconstitute (Step-by-Step)", expanded=False):
        st.markdown(f"""
        1. **Sanitize:** Wipe the top of the **{v_qty}{v_unit}** vial and the water vial with alcohol.
        2. **Draw Water:** Use a syringe to pull **{water}mL** of Bacteriostatic Water.
        3. **Inject:** Insert the needle into the peptide vial at an angle. Aim for the **glass wall**, not the powder.
        4. **Dissolve:** Do **NOT** shake. Gently swirl until the liquid is clear.
        5. **Store:** Refrigerate immediately. Potency degrades at room temperature.
        """)

with col_result:
    st.subheader("2️⃣ Dosage Results")
    d_ml, units, per_vial, strength = calculate_dosage(v_qty, v_unit, water, d_qty, d_unit, s_factor, info)
    
    res_c1, res_c2, res_c3 = st.columns(3)
    res_c1.metric("Draw Volume", f"{d_ml:.4f} mL")
    res_c2.metric("Syringe Units", f"{units:.1f} Units")
    res_c3.metric("Doses / Vial", int(per_vial))

    # --- VISUAL SYRINGE ---
    pct = min((units / s_factor) * 100, 100)
    st.markdown(f"**Syringe Fill Level ({units:.1f} Units):**")
    st.markdown(f'<div class="syringe-container"><div class="syringe-liquid" style="width: {pct}%;"></div><div class="syringe-markings"></div></div>', unsafe_allow_html=True)
    
    # --- CLINICAL DATA (BULLET FORMAT RESTORED) ---
    st.divider()
    st.subheader(f"📖 Clinical Profile: {selected_p}")
    
    # Benefits Section
    st.markdown('<div class="clinical-card benefit-section"><strong>🌟 Key Benefits:</strong>' + info["benefits_detailed"] + '</div>', unsafe_allow_html=True)
    
    # Side Effects & Contraindications
    st.markdown('<div class="clinical-card warning-section"><strong>⚠️ Side Effects & Contraindications:</strong>' + info["side_effects_detailed"] + '</div>', unsafe_allow_html=True)
    
    # Protocol Section
    st.markdown('<div class="clinical-card protocol-section"><strong>📋 Dosage & Frequency Protocol:</strong>' + info["protocol_detailed"] + '</div>', unsafe_allow_html=True)
    
    st.caption(f"**❄️ Storage Requirements:** {info['storage']}")

st.divider()
st.subheader("💉 Visual Guide: Injection Zones")

st.caption("Rotate injection sites between the abdomen, thighs, and upper arms to maintain skin health.")
