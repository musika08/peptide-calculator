import streamlit as st
from database import PEPTIDE_DB

def run_calculator():
    st.subheader("🧪 Peptide Dosage Calculator")
    
    # Check if a peptide was selected from the database or if we are in manual mode
    peptide_list = ["Manual / Other"] + list(PEPTIDE_DB.keys())
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.container(border=True):
            selected_peptide = st.selectbox("Select Peptide for Presets", options=peptide_list)
            
            # --- FEATURE 4: DEFAULT UNIT LOGIC ---
            # If HCG is selected, default to IU. Otherwise, default to mcg.
            if "HCG" in selected_peptide:
                default_unit_index = 2 # Index for IU
            else:
                default_unit_index = 0 # Index for mcg

            unit = st.radio(
                "Select Dosage Unit", 
                ["mcg", "mg", "IU"], 
                index=default_unit_index, 
                horizontal=True,
                help="HCG defaults to IU. Most other peptides use mcg."
            )
            
            st.divider()
            
            c1, c2 = st.columns(2)
            with c1:
                vial_size = st.number_input("Vial Amount (mg or IU)", min_value=0.1, value=5.0 if "HCG" not in selected_peptide else 5000.0, step=0.1)
                bac_water = st.number_input("BAC Water Volume (ml)", min_value=0.1, value=2.0, step=0.1)
            
            with c2:
                desired_dose = st.number_input(f"Desired Dose ({unit})", min_value=1.0, value=250.0, step=10.0)
                syringe_size = st.selectbox("Syringe Size", ["1ml (100 units)", "0.5ml (50 units)", "0.3ml (30 units)"])

            # --- CALCULATION LOGIC ---
            # Standardize everything to a "unit per ml" concentration
            # 1. Determine total mass in mcg (or keep as IU)
            if unit == "mcg":
                total_micrograms = vial_size * 1000
                dose_to_calc = desired_dose
            elif unit == "mg":
                total_micrograms = vial_size * 1000
                dose_to_calc = desired_dose * 1000
            else: # IU
                total_micrograms = vial_size
                dose_to_calc = desired_dose

            # 2. Math for the tick marks
            try:
                mcg_per_ml = total_micrograms / bac_water
                ml_per_dose = dose_to_calc / mcg_per_ml
                units_on_syringe = ml_per_dose * 100
                
                st.success(f"### Result: **{units_on_syringe:.1f} Units**")
                st.info(f"This dose will provide {desired_dose}{unit} using {ml_per_dose:.3f}ml of solution.")
                
            except ZeroDivisionError:
                st.error("Please enter valid numbers for vial size and water.")

    with col2:
        # --- FEATURE 5: VISUAL GUIDE ---
        st.markdown("### 📍 Administration Guide")
        try:
            st.image("sites.jpeg", caption="Subcutaneous Injection Sites", use_container_width=True)
        except:
            st.warning("Please ensure 'sites.jpeg' is in the same folder as this script.")
        
        # Display clinical data from database if a peptide is selected
        if selected_peptide != "Manual / Other":
            info = PEPTIDE_DB[selected_peptide]
            with st.expander("📖 Clinical Quick-Ref", expanded=True):
                st.markdown(f"**Goal:** {info['type']}")
                st.markdown(f"**Protocol:**\n{info['protocol']}")
                st.markdown(f"**Storage:** {info['storage']}")

if __name__ == "__main__":
    run_calculator()
