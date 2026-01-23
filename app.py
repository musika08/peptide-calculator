import streamlit as st
import math

# --- 1. CONFIGURATION: WIDE MODE ---
st.set_page_config(
    page_title="PeptideCalc Pro",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS FOR VISUAL SYRINGE ONLY ---
st.markdown("""
<style>
    .syringe-container {
        border: 2px solid #333;
        border-radius: 4px;
        background-color: #f0f0f0;
        height: 30px;
        width: 100%;
        position: relative;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .syringe-liquid {
        background-color: #ff4b4b;
        height: 100%;
        border-radius: 2px 0 0 2px;
        transition: width 0.5s ease-in-out;
    }
    .syringe-markings {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: repeating-linear-gradient(90deg, transparent, transparent 19%, #000 20%);
        opacity: 0.1;
    }
</style>
""", unsafe_allow_html=True)

# --- EXPANDED KNOWLEDGE BASE WITH BLENDS ---
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
        "benefits": "Heals tendons, ligaments, and bones; Protects gut health and heals ulcers (leaky gut); Angiogenesis (creates new blood vessels); Neuroprotective; Reduces systemic inflammation.",
        "note": "🕒 **ANYTIME.** Can be taken with or without food.",
        "side_effects": "Very rare. Occasional nausea or injection site irritation.",
        "storage": "Refrigerate after mixing. Stable for ~30 days."
    },
    "BPC-157 + TB-500 Blend": {
        "vial_mg": 10.0, "dose_mcg": 500.0, "freq": "Daily (or 2x Daily)", 
        "type": "Regenerative Blend",
        "desc": "The ultimate tissue-repair combination (often called the 'Wolverine Stack'). Combines the rapid tendon/gut healing of BPC with the muscle repair and flexibility of TB-500.", 
        "benefits": "Maximum-speed tissue healing (muscles, tendons, ligaments); Extreme anti-inflammatory effects; Promotes new blood vessel growth; Gut health protection; Increased flexibility.",
        "note": "🕒 **ANYTIME.** Dosage is for TOTAL peptide volume. A 500mcg dose yields 250mcg of each peptide.",
        "side_effects": "Fatigue, temporary head rush, mild injection site irritation.",
        "storage": "Refrigerate after mixing. Stable for ~30 days."
    },
    "CJC-1295 (No DAC)": {
        "vial_mg": 5.0, "dose_mcg": 100.0, "freq": "Daily (PM)", 
        "type": "Growth Hormone",
        "desc": "Modified GRF 1-29. Stimulates pulsatile Growth Hormone release.", 
        "benefits": "Lean muscle growth; Accelerates fat loss; Improves sleep quality/deep sleep; Enhances skin elasticity and joint health; Quicker recovery times.",
        "note": "⚠️ **FASTED ONLY.** Inject immediately **before bed** on empty stomach.",
        "side_effects": "Head rush, flushing (warm face), vivid dreams.",
        "storage": "Refrigerate. Sensitive to light/heat."
    },
    "CJC-1295 + Ipamorelin Blend": {
        "vial_mg": 10.0, "dose_mcg": 200.0, "freq": "Daily (PM)", 
        "type": "Growth Hormone Blend",
        "desc": "A synergistic blend of a GHRH (CJC-1295) and a GHRP (Ipamorelin). By combining the two, it creates a much stronger natural Growth Hormone pulse than either peptide alone.", 
        "benefits": "Maximum natural GH release; Builds lean muscle mass; Rapidly burns fat; Superior deep/REM sleep; Extreme anti-aging effects for skin and nails; Quicker recovery.",
        "note": "⚠️ **FASTED ONLY.** Inject immediately **before bed** on an empty stomach (no food for 2 hours prior). A 200mcg dose yields 100mcg of each.",
        "side_effects": "Head rush (common), flushing (warm face), vivid dreams, mild water retention.",
        "storage": "Refrigerate. Sensitive to light. Do not shake vigorously."
    },
    "Epithalon": {
        "vial_mg": 10.0, "dose_mcg": 5000.0, "freq": "Daily (Course)", 
        "type": "Anti-Aging",
        "desc": "Synthetic tetrapeptide that increases telomerase activity, potentially lengthening telomeres.", 
        "benefits": "Increases lifespan/longevity (telomere elongation); Restores natural melatonin production; Normalizes circadian rhythm; Immune system enhancement; High antioxidant activity.",
        "note": "🕒 **ANYTIME.** Usually taken in a 10-20 day course, then cycled off.",
        "side_effects": "None reported/Very mild.",
        "storage": "Refrigerate after mixing."
    },
    "GHK-Cu": {
        "vial_mg": 50.0, "dose_mcg": 2000.0, "freq": "Daily", 
        "type": "Cosmetic/Repair",
        "desc": "Copper Tripeptide-1. Increases collagen production. Used for skin, scarring, and hair.", 
        "benefits": "Boosts collagen and elastin production; Skin tightening and wrinkle reduction; Stimulates hair follicles (hair regrowth); Accelerated wound healing; Powerful anti-inflammatory.",
        "note": "🌙 **EVENING PREFERRED.** High concentrations can sting—rotate sites.",
        "side_effects": "Injection site pain (stinging), redness, copper toxicity (if overdosed).",
        "storage": "Refrigerate. Can degrade if exposed to strong light."
    },
    "Glow Blend (GHK-Cu/BPC/TB)": {
        "vial_mg": 70.0, "dose_mcg": 2500.0, "freq": "Daily", 
        "type": "Cosmetic/Recovery Blend",
        "desc": "A 70mg tri-blend of GHK-Cu, BPC-157, and TB-500. Combines full-body tissue recovery with extreme skin and hair rejuvenation. BPC/TB buffer the notorious GHK-Cu sting.", 
        "benefits": "Massive collagen and elastin boost; Accelerates wound and tissue healing; Enhances skin tightness; Hair follicle regeneration; Increased flexibility; Gut health support.",
        "note": "🌙 **EVENING PREFERRED.** Rotate injection sites daily. Dosage is for TOTAL peptide volume.",
        "side_effects": "Mild injection site pain/redness, temporary flushing.",
        "storage": "Refrigerate strictly. Keep away from strong light."
    },
    "HCG": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "freq": "2-3x / Week", 
        "type": "Hormonal",
        "desc": "Human Chorionic Gonadotropin. Mimics LH to maintain testicular function.", 
        "benefits": "Prevents testicular atrophy; Enhances fertility and sperm count; Restores endogenous testosterone production; Supports libido; Helps maintain hormone balance during TRT.",
        "note": "🌅 **MORNING.** Usually taken upon waking.",
        "side_effects": "Estrogen elevation, acne, water retention.",
        "storage": "MUST Refrigerate immediately. Fragile peptide."
    },
    "Ipamorelin": {
        "vial_mg": 5.0, "dose_mcg": 100.0, "freq": "Daily (PM)", 
        "type": "Growth Hormone",
        "desc": "Selective GH Secretagogue. Stimulates GH release without major cortisol spikes.", 
        "benefits": "Burns body fat; Increases lean muscle mass; Deepens sleep; Strengthens bones; Strong anti-aging effects on skin/nails; No cortisol or prolactin spikes.",
        "note": "⚠️ **FASTED ONLY.** Inject immediately **before bed** on empty stomach.",
        "side_effects": "Head rush, mild water retention.",
        "storage": "Refrigerate. Do not shake vigorously."
    },
    "Kisspeptin": {
        "vial_mg": 10.0, "dose_mcg": 100.0, "freq": "As needed", 
        "type": "Hormonal",
        "desc": "Stimulates GnRH release, increasing LH and FSH. Used to restart HPTA axis.", 
        "benefits": "Triggers natural LH/FSH release; Restores testosterone production naturally; Enhances fertility; Improves mood and libido; Safer alternative to HCG for HPTA axis restart.",
        "note": "🕒 **ANYTIME.** Often used as a safer alternative to HCG.",
        "side_effects": "Flushing, injection site reactions.",
        "storage": "Refrigerate after mixing."
    },
    "Klow Blend (GHK-Cu/BPC/TB/KPV)": {
        "vial_mg": 80.0, "dose_mcg": 3000.0, "freq": "Daily", 
        "type": "Ultimate Repair/Cosmetic Blend",
        "desc": "The 80mg 'Klow' master stack. Combines GHK-Cu, BPC-157, TB-500, and KPV. The addition of KPV makes this a powerhouse for systemic inflammation, gut health (IBD), and clearing skin conditions.", 
        "benefits": "Superior anti-inflammatory action (via KPV); Gut/intestinal healing; Clears acne and psoriasis; Extreme skin rejuvenation and collagen synthesis; Rapid soft tissue repair.",
        "note": "🌙 **EVENING PREFERRED.** High volume blend. Dose is for TOTAL peptide volume.",
        "side_effects": "Injection site pain/redness, temporary flushing.",
        "storage": "Refrigerate strictly. Keep away from strong light."
    },
    "Melanotan II": {
        "vial_mg": 10.0, "dose_mcg": 500.0, "freq": "Daily (Loading)", 
        "type": "Cosmetic",
        "desc": "Stimulates tanning and acts as a potent aphrodisiac.", 
        "benefits": "Deep, long-lasting tan with less UV exposure; Skin cancer protection (via melanin); Extreme libido boost and spontaneous erections; Appetite suppression for weight loss.",
        "note": "☀️ **BEFORE UV EXPOSURE.** Take 30 mins before tanning bed or sun.",
        "side_effects": "Nausea (common), facial flushing, increased libido, appetite suppression.",
        "storage": "Refrigerate. Stable for ~30-60 days."
    },
    "NAD+": {
        "vial_mg": 500.0, "dose_mcg": 25000.0, "freq": "2-3x / Week", 
        "type": "Cellular Energy",
        "desc": "Nicotinamide Adenine Dinucleotide. Critical for cellular energy (ATP) and anti-aging.", 
        "benefits": "Massive cellular energy (ATP) boost; DNA repair and telomere stability; Activates Sirtuins (longevity genes); Clears brain fog/mental clarity; Neuroprotective; Aids in addiction recovery.",
        "note": "⚠️ **SLOW INJECTION.** If injected too fast, causes chest pressure and anxiety.",
        "side_effects": "Chest pressure, palpitations, nausea, lightheadedness (short duration).",
        "storage": "Refrigerate. Very sensitive to heat degradation."
    },
    "PT-141": {
        "vial_mg": 10.0, "dose_mcg": 1000.0, "freq": "As needed", 
        "type": "Libido",
        "desc": "Bremelanotide. Treats hypoactive sexual desire via the CNS.", 
        "benefits": "Treats erectile dysfunction directly in the brain; Skyrockets libido in both men and women; Harder/longer-lasting erections; Improves orgasm quality; FDA approved for HSDD.",
        "note": "⏰ **BEFORE ACTIVITY.** Inject **45-60 minutes before** sexual activity.",
        "side_effects": "Nausea, flushing, headache, increased blood pressure.",
        "storage": "Refrigerate after mixing."
    },
    "Retatrutide": {
        "vial_mg": 10.0, "dose_mcg": 2000.0, "freq": "Once Weekly", 
        "type": "Metabolic (GLP-1/GIP/Glucagon)",
        "desc": "Triple agonist (GLP-1, GIP, Glucagon). The newest generation weight loss peptide with high potency.", 
        "benefits": "Unmatched weight loss (up to 24%+); Increases basal metabolic rate; Actively burns fat (via glucagon); Resolves non-alcoholic fatty liver disease (NAFLD); Superior lipid and blood sugar control.",
        "note": "🕒 **ANYTIME (Weekly).** Start low. Potent metabolic effects.",
        "side_effects": "Increased heart rate, nausea, arrhythmia risk, appetite suppression.",
        "storage": "Refrigerate strictly. Do not freeze once mixed."
    },
    "Semaglutide": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "freq": "Once Weekly", 
        "type": "Metabolic (GLP-1)",
        "desc": "GLP-1 Agonist. Increases insulin secretion and reduces appetite. FDA approved for weight management.", 
        "benefits": "Significant weight loss (15%+); Curbs cravings and appetite; Reverses insulin resistance; Cardioprotective (reduces risk of stroke/heart attack); Lowers inflammation.",
        "note": "🕒 **ANYTIME (Weekly).** Taken on the same day each week. Meals do not affect absorption.",
        "side_effects": "Nausea, vomiting, diarrhea, constipation, fatigue.",
        "storage": "Refrigerate. Protect from light."
    },
    "TB-500": {
        "vial_mg": 5.0, "dose_mcg": 2500.0, "freq": "2x / Week", 
        "type": "Regenerative",
        "desc": "Synthetic Thymosin Beta-4. Promotes flexibility, reduces inflammation, and aids recovery.", 
        "benefits": "Accelerates tissue healing (muscle, tendon, and ligament); Upregulates cell migration; Promotes extreme flexibility; Reduces chronic inflammation; Cardioprotective properties; Supports hair growth.",
        "note": "🕒 **ANYTIME.** Timing relative to meals does not matter.",
        "side_effects": "Fatigue, temporary head rush.",
        "storage": "Refrigerate after mixing."
    },
    "Tesamorelin": {
        "vial_mg": 2.0, "dose_mcg": 1000.0, "freq": "Daily (PM)", 
        "type": "Growth Hormone",
        "desc": "Potent GHRH analog. Specific for reducing visceral belly fat.", 
        "benefits": "Significantly targets and reduces stubborn visceral belly fat; Lowers cholesterol and triglycerides; Increases IGF-1 levels; Preserves and builds lean muscle; FDA approved (Egrifta).",
        "note": "⚠️ **FASTED ONLY.** Inject immediately **before bed** on empty stomach.",
        "side_effects": "Injection site reactions, joint pain, water retention.",
        "storage": "Refrigerate. Use within 20-30 days."
    },
    "Tesamorelin + Ipamorelin Blend": {
        "vial_mg": 12.0, "dose_mcg": 350.0, "freq": "Daily (PM)", 
        "type": "Growth Hormone/Fat Loss Blend",
        "desc": "Potent combination for visceral fat loss and anti-aging. Tesa targets belly fat while Ipamorelin boosts overall GH pulses.", 
        "benefits": "Rapidly reduces visceral (belly) fat; Preserves and builds lean muscle; Deep sleep quality; Enhanced recovery; Anti-aging for skin.",
        "note": "⚠️ **FASTED ONLY.** Inject immediately **before bed** on an empty stomach (fasted for 2 hours).",
        "side_effects": "Injection site reactions, joint pain, mild water retention, flushing.",
        "storage": "Refrigerate strictly. Use within 20-30 days."
    },
    "Tirzepatide": {
        "vial_mg": 30.0, "dose_mcg": 2500.0, "freq": "Once Weekly", 
        "type": "Metabolic (GLP-1/GIP)",
        "desc": "Dual GIP/GLP-1 Agonist. Potent weight loss and metabolic regulation.", 
        "benefits": "Superior weight loss compared to Semaglutide (20%+); Silences \"food noise\" and obsessive cravings; Massive improvement in insulin sensitivity; Reduces systemic inflammation and A1C.",
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

# === LEFT COLUMN: INPUTS & GUIDES ===
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
        # Step logic: 1.0 for mg, 50.0 for mcg, 0.001 for g
        if dose_unit == 'mg':
            step = 1.0
            fmt = "%.1f"
        elif dose_unit == 'mcg':
            step = 50.0
            fmt = "%.1f"
        else: # 'g'
            step = 0.001
            fmt = "%.4f"
        
        desired_dose = st.number_input("Desired Dose", key="dose_val", min_value=0.0, step=step, format=fmt)
    
    syringe_type = st.radio("Syringe Type", ["U-100 (Standard)", "U-40 (Vet)"], horizontal=True)
    syringe_factor = 100 if "U-100" in syringe_type else 40

    st.divider()

    # --- DYNAMIC MIXING GUIDE ---
    with st.expander("🛠️ How to Reconstitute (Mix)"):
        st.markdown(f"""
        1. **Clean:** Wipe the top of the **{vial_qty} {vial_unit}** peptide vial and the water vial with an alcohol swab.
        2. **Withdraw:** Draw exactly **{water_ml} mL** of Bacteriostatic Water.
        3. **Inject:** Slowly inject the **{water_ml} mL** of water into the peptide vial. Aim for the glass wall, not the powder directly.
        4. **Mix:** **Do not shake.** Gently swirl the vial until dissolved.
        5. **Store:** Refrigerate immediately.
        """)

    # --- INJECTION VISUAL GUIDE (Local File) ---
    with st.expander("💉 Visual Guide: Injection Sites", expanded=True):
        try:
            st.image("injection_sites.png", caption="Recommended Subcutaneous Zones", use_container_width=True)
        except:
            st.warning("⚠️ Image not found. Please upload 'injection_sites.png' to your GitHub repository.")


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
        
        # --- NEW: CYCLE CALCULATOR ---
        # Calculate doses per vial
        doses_per_vial = total_peptide_mcg / desired_dose_mcg
        
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

        st.divider()

        # --- B. CALCULATION RESULTS ---
        
        # 1. Standard Metrics + Cycle Info
        c1, c2, c3 = st.columns(3)
        c1.metric("Draw Volume", f"{draw_ml:.4f} mL")
        c2.metric("Syringe Units", f"{units:.1f} Units")
        c3.metric("Doses / Vial", f"{int(doses_per_vial)}")
        
        # 2. Split Dosing Logic & Visual Syringe
        percentage = min(units / syringe_factor * 100, 100)
        
        if units > syringe_factor:
            # DOSE TOO HIGH - SPLIT IT
            num_injections = math.ceil(units / syringe_factor)
            dose_per = units / num_injections
            st.error(f"⚠️ **Volume too large for one syringe!**")
            st.warning(f"💡 **Recommendation:** Split into **{num_injections}** injections of **{dose_per:.1f} Units** each.")
            
            # Show full bar
            st.markdown(f"""
            <div style="margin-bottom:5px; font-weight:bold;">Visual Fill (1 Full Syringe + Overflow):</div>
            <div class="syringe-container">
                <div class="syringe-liquid" style="width: 100%; background-color: #ff0000;"></div>
                <div class="syringe-markings"></div>
            </div>
            """, unsafe_allow_html=True)

        else:
            # DOSE OK
            st.markdown(f"""
            <div style="margin-bottom:5px; font-weight:bold;">Visual Syringe Fill ({units:.1f} Units):</div>
            <div class="syringe-container">
                <div class="syringe-liquid" style="width: {percentage}%;"></div>
                <div class="syringe-markings"></div>
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"Draw to the **{units:.1f}** mark on your {syringe_type} syringe.")

        # DOWNLOAD
        protocol_text = f"Peptide: {selected_peptide}\nFreq: {peptide_info['freq']}\nStock: {vial_qty}{vial_unit} + {water_ml}mL Water\nConc: {concentration_mg_ml:.2f} mg/mL\nDose: {desired_dose}{dose_unit} = {units:.1f} Units ({syringe_type})\nSupply: 1 vial lasts approx {int(doses_per_vial)} doses.\n\nDetails:\n{peptide_info['desc']}\nBenefits: {peptide_info['benefits']}\nStorage: {peptide_info['storage']}\nInstructions: {peptide_info['note']}"
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

# --- DISCLAIMER ---
st.markdown("---")
st.caption("⚠️ **Medical Disclaimer:** This tool is for educational and informational purposes only and does not constitute medical advice. Always verify calculations with a professional. The developers assume no liability for errors or misuse.")
