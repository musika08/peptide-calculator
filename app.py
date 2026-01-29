# app.py
import streamlit as st
import math
from database import PEPTIDE_PRESETS

# --- CONFIGURATION ---
st.set_page_config(
    page_title="PeptideCalc Pro v4.0",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS ---
st.markdown("""
<style>
    .syringe-container { border: 2px solid #333; border-radius: 4px; background-color: #f0f0f0; height: 30px; width: 100%; position: relative; margin: 10px 0; }
    .syringe-liquid { background-color: #ff4b4b; height: 100%; border-radius: 2px 0 0 2px; transition: width 0.5s ease-in-out; }
    .syringe-markings { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: repeating-linear-gradient(90deg, transparent, transparent 19%, #000 20%); opacity: 0.1; }
    .db-tag { background-color: #4b4bff; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.8em; font-weight: bold; display: inline-block; margin-bottom: 10px; }
    .side-effect-box { background-color: #3e1818; border-left: 4px solid #ff4b4b; padding: 10px; margin-top: 10px; border-radius: 4px; font-size: 0.9em; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# Initialize State
if 'vial_val' not in st.session_state: st.session_state.vial_val = 30.0
if 'dose_val' not in st.session_state: st.session_state.dose_val = 2.5
if 'stock_unit_index' not in st.session_state: st.session_state.stock_unit_index = 0
if 'calc_count' not in st.session_state: st.session_state.calc_count = 0

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/biotech.png", width=60)
    st.title("Navigation")
    page = st.radio("Go to:", ["🧮 Calculator", "📚 Peptide Database"])
    st.markdown("---")
    st.caption("v4.0 | separated architecture")

# ==============================================================================
# PAGE 1: CALCULATOR
# ==============================================================================
if page == "🧮 Calculator":
    def load_preset():
        data = PEPTIDE_PRESETS[st.session_state.peptide_selector]
        st.session_state.vial_val = float(data["vial_mg"])
        st.session_state.stock_unit_index = 3 if data.get("default_stock_unit") == "IU" else 0
        st.session_state.dose_val = float(data["dose_mcg"])
        st.session_state.calc_count += 1

    st.subheader("🧪 Reconstitution Calculator")
    st.divider()
    left_col, right_col = st.columns([1, 1.2], gap="large")

    with left_col:
        st.info("1️⃣ **Configuration**")
        sorted_presets = sorted(list(PEPTIDE_PRESETS.keys()))
        selected_peptide = st.selectbox("Select Peptide Profile", sorted_presets, index=sorted_presets.index("Tirzepatide") if "Tirzepatide" in sorted_presets else 0, key="peptide_selector", on_change=load_preset)
        peptide_info = PEPTIDE_PRESETS[selected_peptide]

        st.write("📦 **Stock & Water**")
        c1, c2, c3 = st.columns([1.5, 1, 1.5])
        with c1: vial_qty = st.number_input("Stock Amount", key="vial_val", min_value=0.0, step=1.0, format="%.1f")
        with c2: vial_unit = st.selectbox("Unit", ["mg", "mcg", "g", "IU"], index=st.session_state.stock_unit_index, key="stock_unit_selection")
        with c3: water_ml = st.number_input("Water Added (mL)", value=2.0, step=0.5, min_value=0.1)

        st.write("🎯 **Dosing**")
        c4, c5 = st.columns([2, 1])
        with c5: dose_unit = st.selectbox("Dose Unit", ["mcg", "mg", "g", "IU"], key="dose_unit_selection")
        with c4:
            step_val = 0.5 if st.session_state.dose_unit_selection == 'mg' else 50.0
            desired_dose = st.number_input("Desired Dose", key="dose_val", min_value=0.0, step=step_val)
        
        syringe_type = st.radio("Syringe Type", ["U-100 (Standard)", "U-40 (Vet)"], horizontal=True)
        syringe_factor = 100 if "U-100" in syringe_type else 40

    with right_col:
        st.success("2️⃣ **Profile & Results**")
        if vial_qty > 0 and water_ml > 0 and desired_dose > 0:
            # Calculation logic
            conv = peptide_info.get("iu_conversion")
            stock_mg = vial_qty if vial_unit=='mg' else (vial_qty/1000 if vial_unit=='mcg' else (vial_qty*1000 if vial_unit=='g' else 0))
            
            if conv and conv > 1:
                total_stock_units = stock_mg * conv if vial_unit != 'IU' else vial_qty
                target_dose_units = desired_dose if dose_unit == 'IU' else (desired_dose * conv if dose_unit == 'mg' else (desired_dose/1000)*conv)
                display_strength = f"{stock_mg:.1f}mg ≈ {int(total_stock_units)} IU"
            elif conv == 1:
                total_stock_units, target_dose_units = vial_qty, desired_dose
                display_strength = f"{int(vial_qty)} IU"
            else:
                total_stock_units = (vial_qty * 1000) if vial_unit=='mg' else (vial_qty if vial_unit=='mcg' else vial_qty*1000000)
                target_dose_units = (desired_dose * 1000) if dose_unit=='mg' else (desired_dose if dose_unit=='mcg' else desired_dose*1000000)
                display_strength = f"{total_stock_units/1000:.1f} mg"

            conc = total_stock_units / water_ml
            draw_ml = target_dose_units / conc if conc > 0 else 0
            units = draw_ml * syringe_factor
            doses = total_stock_units / target_dose_units if target_dose_units > 0 else 0

            # UI Rendering
            res_c1, res_c2, res_c3 = st.columns(3)
            res_c1.metric("Draw Volume", f"{draw_ml:.4f} mL")
            res_c2.metric("Syringe Units", f"{units:.1f} Units")
            res_c3.metric("Doses / Vial", f"{int(doses)}")
            
            # Visual Bar
            fill = min(units / syringe_factor * 100, 100)
            st.markdown(f"""<div style="font-weight:bold;">Visual Fill:</div><div class="syringe-container"><div class="syringe-liquid" style="width: {fill}%;"></div><div class="syringe-markings"></div></div>""", unsafe_allow_html=True)
            
            with st.expander(f"📖 **Profile: {selected_peptide}**", expanded=True):
                st.markdown(f"**🌟 Key Benefits:**\n{peptide_info['benefits_summary']}")
                st.markdown(f"<div class='side-effect-box'><strong>⚠️ Side Effects:</strong><br>{peptide_info['side_effects_summary'].replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
                st.info(f"**📋 Protocol:** {peptide_info['protocol_summary']}")
        else:
            st.info("Enter inputs to see results.")

# ==============================================================================
# PAGE 2: DATABASE
# ==============================================================================
elif page == "📚 Peptide Database":
    st.subheader("📚 Peptide Database")
    all_cats = ["All", "Slimming & Fat Loss", "Skin, Hair & Beauty", "Muscle & Workout", "Nootropics & Brain", "Injury & Repair", "Wellness & Longevity", "Libido & Sexual Health"]
    col_s, col_f = st.columns([3, 1])
    search = col_s.text_input("🔍 Search", placeholder="Search...").lower()
    cat_filt = col_f.selectbox("🏷️ Filter", all_cats)
    
    items = {n: d for n, d in PEPTIDE_PRESETS.items() if (cat_filt == "All" or d['filter_cat'] == cat_filt) and (search in n.lower() or search in d['benefits_detailed'].lower())}
    
    db_cols = st.columns(3)
    for i, (name, info) in enumerate(items.items()):
        with db_cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"### {name}\n<span class='db-tag'>{info['type']}</span>", unsafe_allow_html=True)
                st.markdown(f"**Benefits:**\n{info['benefits_detailed']}")
                st.markdown(f"<div class='side-effect-box'><strong>Side Effects:</strong><br>{info['side_effects_detailed']}</div>", unsafe_allow_html=True)
                with st.expander("📋 Protocol"): st.markdown(info['protocol_detailed'])
