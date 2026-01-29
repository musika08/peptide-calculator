# calculator.py
import streamlit as st

# --- COMPLETE PEPTIDE DATABASE ---
PEPTIDE_DB = {
    "AOD-9604": {
        "vial_mg": 5.0, "dose_val": 300.0, "unit": "mcg", "freq": "Daily", "timing": "Morning", "food": "Without (Empty stomach)",
        "type": "Fat Loss", "filter_cat": "Slimming & Fat Loss",
        "desc": "Anti-Obesity Drug 9604. A modified fragment of the HGH molecule.",
        "benefits": "- Targeted lipolysis (fat breakdown)\n- No impact on blood sugar\n- Bone and cartilage repair properties",
        "side": "• Injection site redness\n• Rare headache\n• Mild stomach upset",
        "contra": "No known major contraindications; general safety profile is high.",
        "storage": "Refrigerate."
    },
    "BPC-157": {
        "vial_mg": 5.0, "dose_val": 250.0, "unit": "mcg", "freq": "1-2x Daily", "timing": "Morning/Night", "food": "With or without",
        "type": "Repair Peptide", "filter_cat": "Injury & Repair",
        "desc": "Body Protection Compound. Derived from human gastric juice.",
        "benefits": "- Heals tendons/ligaments/bone\n- Seals 'Leaky Gut' and IBD\n- Angiogenesis (blood vessel growth)",
        "side": "• Rare nausea\n• Dizziness\n• Site irritation",
        "contra": "Active malignancies (due to angiogenesis).",
        "storage": "Refrigerate. Sensitive to shaking."
    },
    "CJC-1295 + Ipamorelin": {
        "vial_mg": 10.0, "dose_val": 250.0, "unit": "mcg", "freq": "Daily (5 on/2 off)", "timing": "Nightly", "food": "Without (Empty stomach)",
        "type": "GH Secretagogue", "filter_cat": "Muscle & Workout",
        "desc": "The 'Gold Standard' for natural Growth Hormone elevation.",
        "benefits": "- Lean muscle growth\n- Massive improvement in sleep quality\n- Fat loss and skin tightening",
        "side": "• Facial flushing\n• Vivid dreams\n• Tingling in hands",
        "contra": "Pituitary adenomas.",
        "storage": "Refrigerate. Do not shake."
    },
    "GHK-Cu": {
        "vial_mg": 50.0, "dose_val": 2.0, "unit": "mg", "freq": "Daily", "timing": "Evening", "food": "With or without",
        "type": "Cosmetic/Repair", "filter_cat": "Skin, Hair & Beauty",
        "desc": "Copper Tripeptide-1 for skin and hair rejuvenation.",
        "benefits": "- Increases collagen synthesis by 70%\n- Thickens dermis/tightens skin\n- Hair follicle enlargement",
        "side": "• Significant injection stinging\n• Red welts\n• Zinc depletion",
        "contra": "Known copper toxicity (Wilson's Disease).",
        "storage": "Refrigerate. Protect from light."
    },
    "HCG": {
        "vial_mg": 5000.0, "dose_val": 250.0, "unit": "IU", "freq": "2-3x Weekly", "timing": "Morning", "food": "With or without",
        "type": "Hormonal", "filter_cat": "Libido & Sexual Health",
        "desc": "Mimics LH to keep testes active during TRT.",
        "benefits": "- Prevents testicular shrinkage\n- Maintains fertility\n- Boosts libido and mood",
        "side": "• High Estrogen (E2)\n• Acne\n• Water retention",
        "contra": "Androgen-sensitive tumors.",
        "storage": "Refrigerate after mixing."
    },
    "NAD+": {
        "vial_mg": 500.0, "dose_val": 50.0, "unit": "mg", "freq": "2-3x Weekly", "timing": "Morning", "food": "With or without",
        "type": "Cellular Energy", "filter_cat": "Wellness & Longevity",
        "desc": "Coenzyme for mitochondrial health and DNA repair.",
        "benefits": "- Clears brain fog\n- Massive energy boost\n- Reduces cravings (addiction support)",
        "side": "• Intense chest pressure (The Flush)\n• Nausea/Cramping\n• Anxiety sensation",
        "contra": "History of specific malignancies.",
        "storage": "Refrigerate immediately."
    },
    "PT-141": {
        "vial_mg": 10.0, "dose_val": 1.75, "unit": "mg", "freq": "As needed", "timing": "2-4 hrs pre-activity", "food": "With or without",
        "type": "Libido", "filter_cat": "Libido & Sexual Health",
        "desc": "Works via the CNS to increase sexual desire.",
        "benefits": "- Treats ED and HSDD\n- Increases arousal for Men & Women\n- Works where Viagra fails",
        "side": "• Intense nausea\n• Flushing\n• High blood pressure",
        "contra": "Uncontrolled hypertension.",
        "storage": "Refrigerate."
    },
    "Retatrutide": {
        "vial_mg": 10.0, "dose_val": 2.0, "unit": "mg", "freq": "Once Weekly", "timing": "Any time", "food": "With or without",
        "type": "Triple G Agonist", "filter_cat": "Slimming & Fat Loss",
        "desc": "Triple agonist targeting GLP-1, GIP, and Glucagon.",
        "benefits": "- Highest weight loss efficacy recorded (24%+)\n- Drastic reduction in liver fat\n- Increased resting energy expenditure",
        "side": "• Tachycardia (High Heart Rate)\n• Skin sensitivity\n• Intense GI upset",
        "contra": "Pre-existing heart conditions or tachycardia.",
        "storage": "Refrigerate."
    },
    "Semaglutide": {
        "vial_mg": 5.0, "dose_val": 0.25, "unit": "mg", "freq": "Once Weekly", "timing": "Any time", "food": "With or without",
        "type": "GLP-1 Agonist", "filter_cat": "Slimming & Fat Loss",
        "desc": "Standard GLP-1 agonist for weight management.",
        "benefits": "- 15% average weight loss\n- Improved cardiovascular markers\n- Blood glucose stabilization",
        "side": "• Nausea\n• Fatigue\n• Gastrointestinal reflux",
        "contra": "History of pancreatitis or thyroid tumors.",
        "storage": "Refrigerate."
    },
    "Tirzepatide": {
        "vial_mg": 30.0, "dose_val": 2.5, "unit": "mg", "freq": "Once Weekly", "timing": "Any time", "food": "With or without",
        "type": "GLP-1/GIP Agonist", "filter_cat": "Slimming & Fat Loss",
        "desc": "Dual agonist (Mounjaro) for superior weight loss and insulin control.",
        "benefits": "- 22%+ average weight loss\n- Eliminates 'food noise'\n- Resets insulin sensitivity",
        "side": "• Nausea/Vomiting\n• Constipation\n• Fatigue",
        "contra": "History of Medullary Thyroid Carcinoma.",
        "storage": "Refrigerate."
    },
    "TB-500": {
        "vial_mg": 5.0, "dose_val": 2.5, "unit": "mg", "freq": "2x Weekly", "timing": "Any time", "food": "With or without",
        "type": "Regenerative", "filter_cat": "Injury & Repair",
        "desc": "Thymosin Beta-4. Promotes cell migration and tissue repair.",
        "benefits": "- Systemic tissue healing\n- Reduced inflammation/scar tissue\n- Improves range of motion",
        "side": "• Temporary lethargy\n• Flu-like symptoms (rare)\n• Injection site redness",
        "contra": "Active cancer (growth factor mechanism).",
        "storage": "Refrigerate."
    }
}

def run_calculator():
    # CSS for the visual syringe bar
    st.markdown("""
    <style>
        .syringe-container { border: 2px solid #333; border-radius: 4px; background-color: #f0f0f0; height: 30px; width: 100%; position: relative; margin-top: 10px; }
        .syringe-liquid { background-color: #ff4b4b; height: 100%; border-radius: 2px 0 0 2px; transition: width 0.5s ease-in-out; }
        .syringe-markings { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: repeating-linear-gradient(90deg, transparent, transparent 19%, #000 20%); opacity: 0.1; }
    </style>
    """, unsafe_allow_html=True)

    def load_preset():
        selection = st.session_state.peptide_selector
        data = PEPTIDE_DB[selection]
        st.session_state.vial_val = float(data["vial_mg"])
        st.session_state.dose_val = float(data["dose_val"])
        st.session_state.stock_unit_selection = data["unit"] if data["unit"] != "IU" else "IU"
        st.session_state.dose_unit_selection = data["unit"]

    st.subheader("🧪 Reconstitution Calculator")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        with st.container(border=True):
            sorted_presets = sorted(list(PEPTIDE_DB.keys()))
            selected_peptide = st.selectbox("Select Peptide Preset", options=sorted_presets, key="peptide_selector", on_change=load_preset)
            p_data = PEPTIDE_DB[selected_peptide]

            if p_data.get("contra"):
                st.warning(f"⚠️ **Contraindications:** {p_data['contra']}")
            
            st.divider()
            
            c1, c2 = st.columns(2)
            with c1:
                vial_size = st.number_input("Vial Amount", key="vial_val", min_value=0.1)
                vial_unit = st.selectbox("Vial Unit", ["mg", "mcg", "IU"], key="stock_unit_selection")
                bac_water = st.number_input("BAC Water (ml)", value=2.0, min_value=0.1)
            
            with c2:
                dose_unit = st.selectbox("Dose Unit", ["mcg", "mg", "IU"], key="dose_unit_selection")
                desired_dose = st.number_input("Desired Dose", key="dose_val", min_value=0.1)

            # Calculation
            total_mass = vial_size * 1000 if vial_unit == "mg" else vial_size
            target_mass = desired_dose * 1000 if dose_unit == "mg" else desired_dose
            
            try:
                ml_per_dose = (target_mass * bac_water) / total_mass
                units = ml_per_dose * 100
                st.success(f"### Result: **{units:.1f} Units**")
                
                percentage = min(units, 100)
                st.markdown(f"""<div class="syringe-container"><div class="syringe-liquid" style="width: {percentage}%;"></div><div class="syringe-markings"></div></div>""", unsafe_allow_html=True)
            except:
                st.error("Check input values.")

    with col2:
        st.markdown("### 📍 Injection Sites")
        try:
            st.image("sites.jpeg", use_container_width=True)
        except:
            st.warning("sites.jpeg not found.")
        
        with st.expander("📖 Clinical Protocol", expanded=True):
            st.markdown(f"**Timing:** {p_data['timing']}\n\n**Food:** {p_data['food']}")
            st.info(f"**Frequency:** {p_data['freq']}")
