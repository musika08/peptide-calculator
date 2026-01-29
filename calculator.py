# calculator.py
import streamlit as st
from database import PEPTIDE_DB

def run_calculator():
    st.subheader("🧪 Peptide Dosage Calculator")
    
    # CSS for the visual syringe fill
    st.markdown("""
    <style>
        .syringe-container { border: 2px solid #333; border-radius: 4px; background-color: #f0f0f0; height: 30px; width: 100%; position: relative; margin-top: 10px; margin-bottom: 10px; }
        .syringe-liquid { background-color: #ff4b4b; height: 100%; border-radius: 2px 0 0 2px; transition: width 0.5s ease-in-out; }
        .syringe-markings { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: repeating-linear-gradient(90deg, transparent, transparent 19%, #000 20%); opacity: 0.1; }
    </style>
    """, unsafe_allow_html=True)

    def load_preset():
        selection = st.session_state.peptide_selector
        if selection in PEPTIDE_DB:
            data = PEPTIDE_DB[selection]
            # Map database keys to session state
            st.session_state.vial_val = float(data.get("vial_mg", 5.0))
            st.session_state.dose_val = float(data.get("dose_val", 250.0))
            st.session_state.stock_unit_selection = data.get("unit", "mg")
            st.session_state.dose_unit_selection = data.get("unit", "mcg")

    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.container(border=True):
            sorted_presets = sorted(list(PEPTIDE_DB.keys()))
            selected_peptide = st.selectbox("Select Peptide Preset", options=sorted_presets, key="peptide_selector", on_change=load_preset)
            
            p_data = PEPTIDE_DB[selected_peptide]

            # --- DYNAMIC SAFETY ALERTS ---
            if p_data.get("contra"):
                st.warning(f"⚠️ **Contraindications:** {p_data['contra']}")
            
            if "Without" in p_data.get("food", ""):
                st.info(f"🍽️ **Instruction:** Take on an empty stomach (2+ hours after eating).")

            st.divider()
            
            c1, c2 = st.columns(2)
            with c1:
                vial_size = st.number_input("Vial Amount", key="vial_val", min_value=0.1)
                vial_unit = st.selectbox("Vial Unit", ["mg", "mcg", "IU"], key="stock_unit_selection")
                bac_water = st.number_input("BAC Water Volume (ml)", value=2.0, min_value=0.1)
            
            with c2:
                dose_unit = st.selectbox("Dose Unit", ["mcg", "mg", "IU"], key="dose_unit_selection")
                desired_dose = st.number_input(f"Desired Dose", key="dose_val", min_value=0.1)

            # Calculation Logic
            # Standardizing to MCG for mass, or IU for HCG/Oxytocin
            if vial_unit == "mg": total_mass = vial_size * 1000
            elif vial_unit == "mcg": total_mass = vial_size
            else: total_mass = vial_size # IU

            if dose_unit == "mg": target_mass = desired_dose * 1000
            elif dose_unit == "mcg": target_mass = desired_dose
            else: target_mass = desired_dose # IU

            try:
                ml_per_dose = (target_mass * bac_water) / total_mass
                units = ml_per_dose * 100
                st.success(f"### Result: **{units:.1f} Units**")
                
                # Syringe Visual
                percentage = min(units, 100)
                st.markdown(f"""<div class="syringe-container"><div class="syringe-liquid" style="width: {percentage}%;"></div><div class="syringe-markings"></div></div>""", unsafe_allow_html=True)
            except:
                st.error("Check input values.")

    with col2:
        st.markdown("### 📍 Admin Guide")
        try:
            st.image("sites.jpeg", use_container_width=True)
        except:
            st.caption("Visual guide (sites.jpeg) missing.")
        
        with st.expander("📖 Protocol Details", expanded=True):
            st.markdown(f"**Frequency:** {p_data['freq']}")
            st.markdown(f"**Timing:** {p_data['timing']}")
            st.markdown(f"**Benefits:**\n{p_data['benefits']}")
