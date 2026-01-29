# calculator.py
import streamlit as st

def render_calculator_page(PEPTIDE_PRESETS):
    def load_preset():
        selection = st.session_state.peptide_selector
        data = PEPTIDE_PRESETS[selection]
        st.session_state.vial_val = float(data["vial_mg"])
        st.session_state.stock_unit_selection = data.get("default_stock_unit", "mg")
        st.session_state.dose_unit_selection = data.get("default_dose_unit", "mcg")
        st.session_state.dose_val = float(data["dose_mcg"])
        st.session_state.calc_count += 1

    st.subheader("🧪 Reconstitution Calculator")
    st.divider()

    left_col, right_col = st.columns([1, 1.2], gap="large")

    with left_col:
        st.info("1️⃣ **Configuration**")
        sorted_presets = sorted(list(PEPTIDE_PRESETS.keys()))
        default_idx = sorted_presets.index("Tirzepatide") if "Tirzepatide" in sorted_presets else 0

        selected_peptide = st.selectbox("Select Peptide Profile", sorted_presets, index=default_idx, key="peptide_selector", on_change=load_preset)
        peptide_info = PEPTIDE_PRESETS[selected_peptide]

        st.write("📦 **Stock & Water**")
        c1, c2, c3 = st.columns([1.5, 1, 1.5])
        with c1:
            vial_qty = st.number_input("Stock Amount", key="vial_val", min_value=0.0, step=1.0, format="%.1f")
        with c2:
            vial_unit = st.selectbox("Unit", ["mg", "mcg", "g", "IU"], key="stock_unit_selection")
        with c3:
            water_ml = st.number_input("Water Added (mL)", value=2.0, step=0.5, min_value=0.1, format="%.1f")

        st.write("🎯 **Dosing**")
        c4, c5 = st.columns([2, 1])
        with c5:
            dose_unit = st.selectbox("Dose Unit", ["mcg", "mg", "g", "IU"], key="dose_unit_selection")
        with c4:
            if dose_unit == 'mg': step = 0.5
            elif dose_unit == 'IU': step = 5.0
            elif dose_unit == 'mcg': step = 50.0
            else: step = 0.001
            desired_dose = st.number_input("Desired Dose", key="dose_val", min_value=0.0, step=step, format="%.4f" if dose_unit=='g' else "%.2f")
        
        syringe_type = st.radio("Syringe Type", ["U-100 (Standard)", "U-40 (Vet)"], horizontal=True)
        syringe_factor = 100 if "U-100" in syringe_type else 40

    with right_col:
        st.success("2️⃣ **Profile & Results**")
        if vial_qty > 0 and water_ml > 0 and desired_dose > 0:
            if vial_unit == 'mg': total_stock_units = vial_qty * 1000
            elif vial_unit == 'g': total_stock_units = vial_qty * 1000000
            elif vial_unit == 'mcg': total_stock_units = vial_qty
            else: total_stock_units = vial_qty 
            
            if dose_unit == 'mg': target_dose_units = desired_dose * 1000
            elif dose_unit == 'g': target_dose_units = desired_dose * 1000000
            elif dose_unit == 'mcg': target_dose_units = desired_dose
            else: target_dose_units = desired_dose

            concentration_per_ml = total_stock_units / water_ml
            draw_ml = target_dose_units / concentration_per_ml
            units = draw_ml * syringe_factor
            doses_per_vial = total_stock_units / target_dose_units if target_dose_units > 0 else 0

            c_res1, c_res2, c_res3 = st.columns(3)
            c_res1.metric("Draw Volume", f"{draw_ml:.4f} mL")
            c_res2.metric("Syringe Units", f"{units:.1f} Units")
            c_res3.metric("Doses / Vial", f"{int(doses_per_vial)}")
            
            percentage = min(units / syringe_factor * 100, 100)
            st.markdown(f"""<div class="syringe-container"><div class="syringe-liquid" style="width: {percentage}%;"></div><div class="syringe-markings"></div></div>""", unsafe_allow_html=True)
            st.caption(f"Draw to **{units:.1f}** on your {syringe_type} syringe.")

            with st.expander(f"📖 **Profile: {selected_peptide}**", expanded=True):
                st.markdown(f"**Type:** {peptide_info['type']}")
                st.markdown("**🌟 Key Benefits:**")
                st.markdown(peptide_info['benefits_summary'])
                st.markdown(f"<div class='side-effect-box'><strong>⚠️ Side Effects:</strong><br>{peptide_info['side_effects_summary'].replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
        else:
            st.info("Enter inputs to see results.")

    st.divider()
    with st.expander("🛠️ How to Reconstitute (Mix)", expanded=True):
         st.markdown(f"1. **Clean:** Wipe tops with alcohol.\n2. **Withdraw:** Draw **{water_ml} mL** of BAC Water.\n3. **Inject:** Slowly into the peptide vial.\n4. **Mix:** Swirl gently, do not shake.\n5. **Store:** Refrigerate.")

    
