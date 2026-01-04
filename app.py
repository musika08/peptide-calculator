import streamlit as st

# --- 1. CONFIGURATION: WIDE MODE ---
st.set_page_config(
    page_title="PeptideCalc Pro",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- EXPANDED KNOWLEDGE BASE (UPDATED WITH TIMING) ---
PEPTIDE_PRESETS = {
    "Custom (Enter manually)": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "freq": "As directed", 
        "type": "N/A",
        "desc": "Manual calculation for custom compounds.", 
        "note": "Verify molecular weight and concentration if applicable."
    },
    "BPC-157": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "freq": "Daily (or 2x Daily)", 
        "type": "Regenerative",
        "desc": "Body Protection Compound-157. Accelerates healing of soft tissue (tendons, ligaments) and protects gut health.", 
        "note": "🕒 **ANYTIME.** Can be taken with or without food. For gut health specifically, taking it orally or injecting 30 mins after a meal is sometimes preferred."
    },
    "TB-500": {
        "vial_mg": 5.0, "dose_mcg": 2500.0, "freq": "2x / Week", 
        "type": "Regenerative",
        "desc": "Synthetic Thymosin Beta-4. Promotes flexibility, reduces inflammation, and aids recovery.", 
        "note": "🕒 **ANYTIME.** Timing relative to meals does not matter."
    },
    "Semaglutide": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "freq": "Once Weekly", 
        "type": "Metabolic (GLP-1)",
        "desc": "GLP-1 Agonist. Increases insulin secretion and reduces appetite. FDA approved for weight management.", 
        "note": "🕒 **ANYTIME (Weekly).** Taken on the same day each week. Meals do not affect absorption, but eating light prevents nausea."
    },
    "Tirzepatide": {
        "vial_mg": 10.0, "dose_mcg": 2500.0, "freq": "Once Weekly", 
        "type": "Metabolic (GLP-1/GIP)",
        "desc": "Dual GIP/GLP-1 Agonist. Potent weight loss and metabolic regulation.", 
        "note": "🕒 **ANYTIME (Weekly).** Taken on the same day each week. Meals do not affect absorption."
    },
    "GHK-Cu": {
        "vial_mg": 50.0, "dose_mcg": 2000.0, "freq": "Daily", 
        "type": "Cosmetic/Repair",
        "desc": "Copper Tripeptide-1. Increases collagen production. Used for skin, scarring, and hair.", 
        "note": "🌙 **EVENING PREFERRED.** High concentrations can sting—rotate sites. Zinc supplements are often recommended to balance copper."
    },
    "CJC-1295 (No DAC)": {
        "vial_mg": 5.0, "dose_mcg": 100.0, "freq": "Daily (PM)", 
        "type": "Growth Hormone",
        "desc": "Modified GRF 1-29. Stimulates pulsatile Growth Hormone release.", 
        "note": "⚠️ **FASTED ONLY.** Inject immediately **before bed**. You must have an **EMPTY STOMACH** (2-3 hours after last meal) or the insulin spike will blunt the effect."
    },
    "Ipamorelin": {
        "vial_mg": 5.0, "dose_mcg": 100.0, "freq": "Daily (PM)", 
        "type": "Growth Hormone",
        "desc": "Selective GH Secretagogue. Stimulates GH release without major cortisol spikes.", 
        "note": "⚠️ **FASTED ONLY.** Inject immediately **before bed**. You must have an **EMPTY STOMACH** (2-3 hours after last meal) or the effect is wasted."
    },
    "Melanotan 2": {
        "vial_mg": 10.0, "dose_mcg": 500.0, "freq": "Daily (Loading)", 
        "type": "Cosmetic",
        "desc": "Stimulates tanning and acts as a potent aphrodisiac.", 
        "note": "☀️ **BEFORE UV EXPOSURE.** Take 30 mins before tanning bed or sun. If using for libido only, take 4 hours before effect is needed."
    },
    "PT-141": {
        "vial_mg": 10.0, "dose_mcg": 1000.0, "freq": "As needed", 
        "type": "Libido",
        "desc": "Bremelanotide. Treats hypoactive sexual desire via the CNS.", 
        "note": "⏰ **BEFORE ACTIVITY.** Inject **45-60 minutes before** sexual activity. Do not exceed 1 dose every 72 hours."
    },
    "Tesamorelin": {
        "vial_mg": 2.0, "dose_mcg": 1000.0, "freq": "Daily (PM)", 
        "type": "Growth Hormone",
        "desc": "Potent GHRH analog. Specific for reducing visceral belly fat.", 
        "note": "⚠️ **FASTED ONLY.** Inject immediately **before bed**. Must be on an **EMPTY STOMACH** (at least 2 hours after food)."
    },
    "HCG": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "freq": "2-3x / Week", 
        "type": "Hormonal",
        "desc": "Human Chorionic Gonadotropin. Mimics LH to maintain testicular function.", 
        "note": "🌅 **MORNING.** Usually taken upon waking. Consistency in timing is key."
    },
}

FACTORS = {'mcg': 1, 'mg': 1000, 'g': 1000000}

# Initialize State
if 'vial_val' not in st.session_state: st.session_state.vial_val = 5.0
if 'dose_val' not in st.session_state: st.session_state.dose_val = 250.0
if 'stock_unit_index' not in st.session_state: st.session_state.stock_unit_index = 0
if 'dose_unit_index' not in st.session_state: st.session_state.dose_unit_index = 0

# --- LOGIC ---
def load_preset():
    selection = st.session_state.peptide_selector
    data = PEPTIDE_PRESETS[selection]
    st.session_state.vial_val = float(data["vial_mg"])
    st.session_state.stock_unit_index = 0 
    target_mcg = float(data["dose_mcg"])
    current_dose_unit = st.session_state.get("dose_unit_selection", "mcg")
    st.session_state.dose_val = target_mcg / FACTORS[current_dose_unit]

def convert_dose_unit():
    new_unit = st.session_state.dose_unit_selection
    old_unit = st.session_state.get("_prev_dose_unit", "mcg")
    current_val = st.session_state.dose_val
    val_in_mcg = current_val * FACTORS[old_unit]
    new_val = val_in_mcg / FACTORS[new_unit]
    st.session_state.dose_val = new_val
    st.session_state._prev_dose_unit = new_unit

def get_mcg(value, unit):
    return value * FACTORS[unit]

# --- UI HEADER (ALIGNED) ---
col_title, col_space, col_btn = st.columns([2, 2, 1])

with col_title:
    st.subheader("🧪 PeptideCalc Pro")
    st.caption("v1.0 | by Musika | *Educational Use Only*")

with col_btn:
    st.write("") 
    st.link_button("☕ Support (Ko-fi)", "https://ko-fi.com/musika", use_container_width=True)

st.divider()

# --- MAIN DASHBOARD ---
left_col, right_col = st.columns([1, 1.2], gap="large")

# === LEFT COLUMN: INPUTS ===
with left_col:
    st.info("1️⃣ **Configuration**")
    
    selected_peptide = st.selectbox("Select Peptide Profile", list(PEPTIDE_PRESETS.keys()), key="peptide_selector", on_change=load_preset)
    
    st.write("📦 **Stock & Water**")
    c1, c2, c3 = st.columns([1.5, 1, 1.5])
    with c1:
        vial_qty = st.number_input("Stock Amount", key="vial_val", min_value=0.0, step=1.0, format="%.1f")
    with c2:
        vial_unit = st.selectbox("Unit", ["mg", "mcg", "g"], index=st.session_state.stock_unit_index, key="stock_unit_selection")
    with c3:
        water_ml = st.number_input("Water Added (mL)", value=2.0, step=0.1, min_value=0.1, format="%.1f")

    st.warning("⚠️ **Safety Check:** Ensure inputs match your physical supplies.")

    st.write("🎯 **Dosing**")
    c4, c5 = st.columns([2, 1])
    with c4:
        fmt = "%.4f" if st.session_state.get("dose_unit_selection") in ['mg', 'g'] else "%.1f"
        step = 0.01 if st.session_state.get("dose_unit_selection") in ['mg', 'g'] else 10.0
        desired_dose = st.number_input("Desired Dose", key="dose_val", min_value=0.0, step=step, format=fmt)
    with c5:
        dose_unit = st.selectbox("Dose Unit", ["mcg", "mg", "g"], index=0, key="dose_unit_selection", on_change=convert_dose_unit)
        if "_prev_dose_unit" not in st.session_state: st.session_state._prev_dose_unit = dose_unit
    
    syringe_type = st.radio("Syringe Type", ["U-100 (Standard)", "U-40 (Vet)"], horizontal=True)
    syringe_factor = 100 if "U-100" in syringe_type else 40


# === RIGHT COLUMN: DETAILS & RESULTS ===
with right_col:
    st.success("2️⃣ **Profile & Results**")

    if vial_qty > 0 and water_ml > 0 and desired_dose > 0:
        total_peptide_mcg = get_mcg(vial_qty, vial_unit)
        desired_dose_mcg = get_mcg(desired_dose, dose_unit)
        concentration_mcg_ml = total_peptide_mcg / water_ml
        concentration_mg_ml = concentration_mcg_ml / 1000
        draw_ml = desired_dose_mcg / concentration_mcg_ml
        units = draw_ml * syringe_factor
        peptide_info = PEPTIDE_PRESETS[selected_peptide]

        # --- A. PEPTIDE DETAILS (TOP) ---
        with st.expander(f"📖 **Profile: {selected_peptide}**", expanded=True):
            if selected_peptide == "Custom (Enter manually)":
                 st.write("Manual mode selected.")
            else:
                st.markdown(f"**Type:** {peptide_info['type']}")
                st.markdown(f"**Description:** {peptide_info['desc']}")
                st.markdown(f"**Frequency:** {peptide_info['freq']}")
                st.info(f"**📋 Instructions:** {peptide_info['note']}")
                st.caption("Common injection sites: Subcutaneous fat (Abdomen, Thigh, or Back of Arm).")

        st.divider()

        # --- B. CALCULATION RESULTS (BOTTOM) ---
        m1, m2 = st.columns(2)
        m1.metric("Draw Volume", f"{draw_ml:.4f} mL")
        m2.metric("Syringe Units", f"{units:.1f} Units")
        
        # BAR
        bar_val = min(units / syringe_factor, 1.0)
        if units > syringe_factor:
            st.progress(1.0)
            st.error(f"⚠️ Dose ({units:.1f} U) > 1 Full Syringe!")
        else:
            st.progress(bar_val)
            st.caption(f"Draw to **{units:.1f}** mark.")

        # DOWNLOAD
        protocol_text = f"Peptide: {selected_peptide}\nFreq: {peptide_info['freq']}\nStock: {vial_qty}{vial_unit} + {water_ml}mL Water\nConc: {concentration_mg_ml:.2f} mg/mL\nDose: {desired_dose}{dose_unit} = {units:.1f} Units ({syringe_type})\n\nDetails:\n{peptide_info['desc']}\nInstructions: {peptide_info['note']}"
        st.download_button("💾 Save Protocol", protocol_text, "protocol.txt", use_container_width=True)

    else:
        st.info("Enter inputs to see results.")