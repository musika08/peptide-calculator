import streamlit as st

# --- 1. CONFIGURATION: WIDE MODE ---
st.set_page_config(
    page_title="PeptideCalc Pro",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- EXPANDED KNOWLEDGE BASE (ALPHABETICAL + STORAGE) ---
PEPTIDE_PRESETS = {
    "Custom (Enter manually)": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "freq": "As directed", 
        "type": "N/A",
        "desc": "Manual calculation for custom compounds.", 
        "benefits": "N/A",
        "note": "Verify molecular weight and concentration if applicable.",
        "side_effects": "Unknown.",
        "storage": "Dependant on compound."
    },
    "BPC-157": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "freq": "Daily (or 2x Daily)", 
        "type": "Regenerative",
        "desc": "Body Protection Compound-157. Accelerates healing of soft tissue (tendons, ligaments) and protects gut health.", 
        "benefits": "Tendon/Ligament repair, Gut inflammation reduction, Faster injury recovery.",
        "note": "🕒 **ANYTIME.** Can be taken with or without food.",
        "side_effects": "Very rare. Occasional nausea or injection site irritation.",
        "storage": "Refrigerate after mixing. Stable for ~30 days."
    },
    "CJC-1295 (No DAC)": {
        "vial_mg": 5.0, "dose_mcg": 100.0, "freq": "Daily (PM)", 
        "type": "Growth Hormone",
        "desc": "Modified GRF 1-29. Stimulates pulsatile Growth Hormone release.", 
        "benefits": "Lean muscle growth, Fat loss, Deep sleep quality.",
        "note": "⚠️ **FASTED ONLY.** Inject immediately **before bed** on empty stomach.",
        "side_effects": "Head rush, flushing (warm face), vivid dreams.",
        "storage": "Refrigerate. Sensitive to light/heat."
    },
    "Epithalon": {
        "vial_mg": 10.0, "dose_mcg": 5000.0, "freq": "Daily (Course)", 
        "type": "Anti-Aging",
        "desc": "Synthetic tetrapeptide that increases telomerase activity, potentially lengthening telomeres.", 
        "benefits": "Longevity, Sleep cycle regulation (Melatonin), Telomere lengthening.",
        "note": "🕒 **ANYTIME.** Usually taken in a 10-20 day course, then cycled off.",
        "side_effects": "None reported/Very mild.",
        "storage": "Refrigerate after mixing."
    },
    "GHK-Cu": {
        "vial_mg": 50.0, "dose_mcg": 2000.0, "freq": "Daily", 
        "type": "Cosmetic/Repair",
        "desc": "Copper Tripeptide-1. Increases collagen production. Used for skin, scarring, and hair.", 
        "benefits": "Skin elasticity/tightening, Wrinkle reduction, Hair regrowth, Wound healing.",
        "note": "🌙 **EVENING PREFERRED.** High concentrations can sting—rotate sites.",
        "side_effects": "Injection site pain (stinging), redness, copper toxicity (if overdosed).",
        "storage": "Refrigerate. Can degrade if exposed to strong light."
    },
    "HCG": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "freq": "2-3x / Week", 
        "type": "Hormonal",
        "desc": "Human Chorionic Gonadotropin. Mimics LH to maintain testicular function.", 
        "benefits": "Testicular size maintenance, Fertility, Endogenous testosterone signal.",
        "note": "🌅 **MORNING.** Usually taken upon waking.",
        "side_effects": "Estrogen elevation, acne, water retention.",
        "storage": "MUST Refrigerate immediately. Fragile peptide."
    },
    "Ipamorelin": {
        "vial_mg": 5.0, "dose_mcg": 100.0, "freq": "Daily (PM)", 
        "type": "Growth Hormone",
        "desc": "Selective GH Secretagogue. Stimulates GH release without major cortisol spikes.", 
        "benefits": "Recovery, Collagen synthesis, Body composition, Sleep.",
        "note": "⚠️ **FASTED ONLY.** Inject immediately **before bed** on empty stomach.",
        "side_effects": "Head rush, mild water retention.",
        "storage": "Refrigerate. Do not shake vigorously."
    },
    "Kisspeptin": {
        "vial_mg": 10.0, "dose_mcg": 100.0, "freq": "As needed", 
        "type": "Hormonal",
        "desc": "Stimulates GnRH release, increasing LH and FSH. Used to restart HPTA axis.", 
        "benefits": "Testosterone support, Fertility improvement, HPTA axis restart.",
        "note": "🕒 **ANYTIME.** Often used as a safer alternative to HCG.",
        "side_effects": "Flushing, injection site reactions.",
        "storage": "Refrigerate after mixing."
    },
    "Melanotan II": {
        "vial_mg": 10.0, "dose_mcg": 500.0, "freq": "Daily (Loading)", 
        "type": "Cosmetic",
        "desc": "Stimulates tanning and acts as a potent aphrodisiac.", 
        "benefits": "Deep tanning (melanin), Strong libido boost, Appetite suppression.",
        "note": "☀️ **BEFORE UV EXPOSURE.** Take 30 mins before tanning bed or sun.",
        "side_effects": "Nausea (common), facial flushing, increased libido, appetite suppression.",
        "storage": "Refrigerate. Stable for ~30-60 days."
    },
    "NAD+": {
        "vial_mg": 500.0, "dose_mcg": 50000.0, "freq": "2-3x / Week", 
        "type": "Cellular Energy",
        "desc": "Nicotinamide Adenine Dinucleotide. Critical for cellular energy (ATP) and anti-aging.", 
        "benefits": "Mental clarity, Energy boost, DNA repair, Anti-aging.",
        "note": "⚠️ **SLOW INJECTION.** If injected too fast, causes chest pressure and anxiety.",
        "side_effects": "Chest pressure, palpitations, nausea, lightheadedness (short duration).",
        "storage": "Refrigerate. Very sensitive to heat degradation."
    },
    "PT-141": {
        "vial_mg": 10.0, "dose_mcg": 1000.0, "freq": "As needed", 
        "type": "Libido",
        "desc": "Bremelanotide. Treats hypoactive sexual desire via the CNS.", 
        "benefits": "Rapid libido enhancement (Men & Women), Erectile function.",
        "note": "⏰ **BEFORE ACTIVITY.** Inject **45-60 minutes before** sexual activity.",
        "side_effects": "Nausea, flushing, headache, increased blood pressure.",
        "storage": "Refrigerate after mixing."
    },
    "Retatrutide": {
        "vial_mg": 10.0, "dose_mcg": 2000.0, "freq": "Once Weekly", 
        "type": "Metabolic (GLP-1/GIP/Glucagon)",
        "desc": "Triple agonist (GLP-1, GIP, Glucagon). The newest generation weight loss peptide with high potency.", 
        "benefits": "Maximum weight loss potential, Fat burning, Metabolic reset.",
        "note": "🕒 **ANYTIME (Weekly).** Start low. Potent metabolic effects.",
        "side_effects": "Increased heart rate, nausea, arrhythmia risk, appetite suppression.",
        "storage": "Refrigerate strictly. Do not freeze once mixed."
    },
    "Semaglutide": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "freq": "Once Weekly", 
        "type": "Metabolic (GLP-1)",
        "desc": "GLP-1 Agonist. Increases insulin secretion and reduces appetite. FDA approved for weight management.", 
        "benefits": "Significant weight loss, Appetite suppression, Blood sugar control.",
        "note": "🕒 **ANYTIME (Weekly).** Taken on the same day each week. Meals do not affect absorption.",
        "side_effects": "Nausea, vomiting, diarrhea, constipation, fatigue.",
        "storage": "Refrigerate. Protect from light."
    },
    "TB-500": {
        "vial_mg": 5.0, "dose_mcg": 2500.0, "freq": "2x / Week", 
        "type": "Regenerative",
        "desc": "Synthetic Thymosin Beta-4. Promotes flexibility, reduces inflammation, and aids recovery.", 
        "benefits": "Muscle recovery, Reduced inflammation, Improved flexibility, hair growth.",
        "note": "🕒 **ANYTIME.** Timing relative to meals does not matter.",
        "side_effects": "Fatigue, temporary head rush.",
        "storage": "Refrigerate after mixing."
    },
    "Tesamorelin": {
        "vial_mg": 2.0, "dose_mcg": 1000.0, "freq": "Daily (PM)", 
        "type": "Growth Hormone",
        "desc": "Potent GHRH analog. Specific for reducing visceral belly fat.", 
        "benefits": "Visceral (belly) fat reduction, Triglyceride reduction, Muscle tone.",
        "note": "⚠️ **FASTED ONLY.** Inject immediately **before bed** on empty stomach.",
        "side_effects": "Injection site reactions, joint pain, water retention.",
        "storage": "Refrigerate. Use within 20-30 days."
    },
    "Tirzepatide": {
        "vial_mg": 10.0, "dose_mcg": 2500.0, "freq": "Once Weekly", 
        "type": "Metabolic (GLP-1/GIP)",
        "desc": "Dual GIP/GLP-1 Agonist. Potent weight loss and metabolic regulation.", 
        "benefits": "Potent weight loss, Improved insulin sensitivity, Reduced food noise.",
        "note": "🕒 **ANYTIME (Weekly).** Taken on the same day each week.",
        "side_effects": "Nausea, diarrhea, decreased appetite, constipation.",
        "storage": "Refrigerate. Do not freeze."
    },
}

FACTORS = {'mcg': 1, 'mg': 1000, 'g': 1000000}

# Initialize State
if 'vial_val' not in st.session_state: st.session_state.vial_val = 5.0
if 'dose_val' not in st.session_state: st.session_state.dose_val = 250.0
if 'stock_unit_index' not in st.session_state: st.session_state.stock_unit_index = 0
if 'dose_unit_index' not in st.session_state: st.session_state.dose_unit_index = 0
if 'dose_unit_selection' not in st.session_state: st.session_state.dose_unit_selection = "mcg"
if 'calc_count' not in st.session_state: st.session_state.calc_count = 0

# --- LOGIC ---
def load_preset():
    selection = st.session_state.peptide_selector
    data = PEPTIDE_PRESETS[selection]
    
    # 1. Update Stock
    st.session_state.vial_val = float(data["vial_mg"])
    st.session_state.stock_unit_index = 0 

    # 2. Smart Dose Unit Switching
    target_mcg = float(data["dose_mcg"])
    if target_mcg < 1000:
        st.session_state.dose_unit_selection = "mcg"
        st.session_state.dose_val = target_mcg
    else:
        st.session_state.dose_unit_selection = "mg"
        st.session_state.dose_val = target_mcg / 1000

    st.session_state.calc_count += 1

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

# --- UI HEADER ---
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
        water_ml = st.number_input("Water Added (mL)", value=2.0, step=0.5, min_value=0.1, format="%.1f")

    st.warning("⚠️ **Safety Check:** Ensure inputs match your physical supplies.")

    st.write("🎯 **Dosing**")
    c4, c5 = st.columns([2, 1])
    with c5:
        dose_unit = st.selectbox(
            "Dose Unit", 
            ["mcg", "mg", "g"], 
            key="dose_unit_selection", 
            on_change=convert_dose_unit
        )
        if "_prev_dose_unit" not in st.session_state: st.session_state._prev_dose_unit = dose_unit
    with c4:
        fmt = "%.4f" if dose_unit in ['mg', 'g'] else "%.1f"
        step = 0.01 if dose_unit in ['mg', 'g'] else 10.0
        desired_dose = st.number_input("Desired Dose", key="dose_val", min_value=0.0, step=step, format=fmt)
    
    syringe_type = st.radio("Syringe Type", ["U-100 (Standard)", "U-40 (Vet)"], horizontal=True)
    syringe_factor = 100 if "U-100" in syringe_type else 40

    # --- NEW: MIXING GUIDE (Fixed Strings) ---
    with st.expander("🛠️ How to Reconstitute (Mix)"):
        st.markdown("""
        1. **Clean:** Wipe the tops of both the peptide vial and water vial with an alcohol swab.
        2. **Withdraw:** Draw your desired amount of Bacteriostatic Water (e.g., 2.0mL).
        3. **Inject:** Slowly inject the water into the peptide vial. Aim for the glass wall, not the powder directly.
        4. **Mix:** **Do not shake.** Gently swirl the vial until dissolved.
        5. **Store:** Refrigerate immediately.
        """)


# === RIGHT COLUMN: RESULTS ===
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

        # --- A. PEPTIDE DETAILS ---
        with st.expander(f"📖 **Profile: {selected_peptide}**", expanded=True):
            if selected_peptide == "Custom (Enter manually)":
                 st.write("Manual mode selected.")
            else:
                st.markdown(f"**Type:** {peptide_info['type']}")
                st.markdown(f"**Description:** {peptide_info['desc']}")
                st.markdown(f"**🌟 Benefits:** {peptide_info['benefits']}")
                st.markdown(f"**Frequency:** {peptide_info['freq']}")
                st.warning(f"**⚠️ Side Effects:** {peptide_info['side_effects']}")
                st.info(f"**📋 Instructions:** {peptide_info['note']}")
                st.markdown(f"**❄️ Storage:** {peptide_info['storage']}")
                st.caption("Common injection sites: Subcutaneous fat (Abdomen, Thigh, or Back of Arm).")

        st.divider()

        # --- B. CALCULATION RESULTS ---
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
        protocol_text = f"Peptide: {selected_peptide}\nFreq: {peptide_info['freq']}\nStock: {vial_qty}{vial_unit} + {water_ml}mL Water\nConc: {concentration_mg_ml:.2f} mg/mL\nDose: {desired_dose}{dose_unit} = {units:.1f} Units ({syringe_type})\n\nDetails:\n{peptide_info['desc']}\nBenefits: {peptide_info['benefits']}\nStorage: {peptide_info['storage']}\nInstructions: {peptide_info['note']}"
        st.download_button("💾 Save Protocol", protocol_text, "protocol.txt", use_container_width=True)

    else:
        st.info("Enter inputs to see results.")

# --- FOOTER ---
st.divider()
c_foot1, c_foot2 = st.columns([1,1])
with c_foot1:
    st.caption(f"🔢 Calculations performed this session: **{st.session_state.calc_count}**")
with c_foot2:
    st.markdown("[![Hits](https://hits.sh/peptide-calculator.streamlit.app.svg?style=flat-square&label=Total%20Visits&extraCount=2023&color=79c83d)](https://hits.sh/peptide-calculator.streamlit.app/)")
