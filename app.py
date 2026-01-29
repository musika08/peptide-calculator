# app.py
import streamlit as st
from database import PEPTIDE_PRESETS, FACTORS
from calculator import perform_calc

st.set_page_config(page_title="PeptideCalc Pro v4.1", page_icon="🧪", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .syringe-container { border: 2px solid #333; border-radius: 4px; background-color: #f0f0f0; height: 30px; width: 100%; position: relative; margin: 10px 0; }
    .syringe-liquid { background-color: #ff4b4b; height: 100%; border-radius: 2px 0 0 2px; transition: width 0.5s; }
    .syringe-markings { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: repeating-linear-gradient(90deg, transparent, transparent 19%, #000 20%); opacity: 0.1; }
    .side-effect-box { background-color: #3e1818; border-left: 4px solid #ff4b4b; padding: 12px; border-radius: 4px; font-size: 0.9em; line-height: 1.6; color: #ffd1d1; margin-top: 10px; }
    .db-tag { background-color: #4b4bff; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.8em; font-weight: bold; display: inline-block; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

if 'vial_val' not in st.session_state: st.session_state.vial_val = 30.0
if 'dose_val' not in st.session_state: st.session_state.dose_val = 2.5
if 'stock_unit_index' not in st.session_state: st.session_state.stock_unit_index = 0
if 'dose_unit_selection' not in st.session_state: st.session_state.dose_unit_selection = "mg"
if 'water_val' not in st.session_state: st.session_state.water_val = 2.0

def update_presets():
    sel = st.session_state.peptide_selector
    data = PEPTIDE_PRESETS[sel]
    st.session_state.stock_unit_index = 3 if data.get("default_stock_unit") == "IU" else 0
    st.session_state.dose_unit_selection = data.get("default_dose_unit", "mcg")
    st.session_state.vial_val = float(data["vial_mg"])
    st.session_state.dose_val = float(data["dose_mcg"])
    st.session_state.water_val = 3.0 if sel == "Oxytocin Acetate" else 2.0

with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/biotech.png", width=60)
    page = st.radio("Navigation", ["🧮 Calculator", "📚 Peptide Database"])

if page == "🧮 Calculator":
    st.subheader("🧪 Reconstitution Calculator")
    l, r = st.columns([1, 1.2], gap="large")

    with l:
        st.info("1️⃣ **Inputs**")
        sorted_keys = sorted(list(PEPTIDE_PRESETS.keys()))
        sel_p = st.selectbox("Select Peptide", sorted_keys, index=sorted_keys.index("Tirzepatide"), key="peptide_selector", on_change=update_presets)
        info = PEPTIDE_PRESETS[sel_p]
        
        c1, c2, c3 = st.columns([1.5, 1, 1.5])
        v_qty = c1.number_input("Stock Amount", key="vial_val", format="%.1f")
        v_unit = c2.selectbox("Unit", ["mg", "mcg", "g", "IU"], index=st.session_state.stock_unit_index, key="stock_unit_selection")
        water = c3.number_input("Water Added (mL)", key="water_val", min_value=0.1, format="%.1f")

        c4, c5 = st.columns([2, 1])
        d_unit = c5.selectbox("Dose Unit", ["mcg", "mg", "g", "IU"], key="dose_unit_selection")
        d_qty = c4.number_input("Desired Dose", key="dose_val", format="%.1f")
        
        syringe = st.radio("Syringe Type", ["U-100", "U-40"], horizontal=True)
        s_factor = 100 if "100" in syringe else 40

        st.divider()
        st.write("### 🛠️ How to Reconstitute")
        st.markdown(f"1. **Clean:** Wipe vial tops.\n2. **Draw:** Withdraw **{water} mL** Water.\n3. **Mix:** Slowly inject into **{v_qty}{v_unit}** vial.\n4. **Store:** Refrigerate immediately.")

    with r:
        st.success("2️⃣ **Profile & Results**")
        d_ml, units, per_vial = perform_calc(v_qty, v_unit, water, d_qty, d_unit, s_factor, info)
        
        if units > 0:
            res_cols = st.columns(3)
            res_cols[0].metric("Draw Volume", f"{d_ml:.4f} mL")
            res_cols[1].metric("Syringe Units", f"{units:.1f} Units")
            res_cols[2].metric("Doses/Vial", int(per_vial))
            
            pct = min(units / s_factor * 100, 100)
            st.markdown(f'<div class="syringe-container"><div class="syringe-liquid" style="width: {pct}%;"></div><div class="syringe-markings"></div></div>', unsafe_allow_html=True)
            
            with st.container():
                st.markdown(f"### 📖 {sel_p} Profile")
                st.markdown(f"**🌟 Comprehensive Benefits:**\n{info['benefits_detailed']}")
                st.info(f"**📋 Dosage Protocol:**\n{info['protocol_detailed']}")
                
                # Rendering Side Effects + Contraindications vertically
                se_clean = info["side_effects_detailed"].strip().replace('\\n', '<br>')
                ci_clean = info.get("contraindications", "None recorded.").strip().replace('\\n', '<br>')
                
                st.markdown(f'''
                <div class="side-effect-box">
                    <strong>⚠️ Side Effects:</strong><br>{se_clean}
                    <hr style="border: 0.5px solid #ff4b4b; margin: 10px 0;">
                    <strong>⛔ Contraindications:</strong><br>{ci_clean}
                </div>
                ''', unsafe_allow_html=True)

    st.divider()
    with st.expander("💉 Visual Guide: Injection Sites", expanded=False):
        st.write("Common subcutaneous injection zones: Abdomen, Upper Thigh, and Back of Arm.")
        
elif page == "📚 Peptide Database":
    st.subheader("📚 Peptide Database")
    # ... (Database view loop)
    for name, i in PEPTIDE_PRESETS.items():
        with st.container(border=True):
            st.markdown(f"### {name}")
            st.markdown(f"**Clinical Benefits:**\n{i['benefits_detailed']}")
            
            se_db = i["side_effects_detailed"].strip().replace('\\n', '<br>')
            ci_db = i.get("contraindications", "None recorded.").strip().replace('\\n', '<br>')
            
            st.markdown(f'''
            <div class="side-effect-box">
                <strong>Side Effects:</strong><br>{se_db}
                <hr style="border: 0.5px solid #ff4b4b; margin: 10px 0;">
                <strong>Contraindications:</strong><br>{ci_db}
            </div>
            ''', unsafe_allow_html=True)
