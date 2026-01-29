import streamlit as st
import math

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="PeptideCalc Pro - Calculator",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS FOR VISUAL SYRINGE & CARDS ---
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

# --- DATA (Hardcoded specifically for Calculator use) ---
PEPTIDE_PRESETS = {
    "AOD-9604": {
        "vial_mg": 5.0, "dose_mcg": 300.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Fat Loss", "benefits_summary": "- Targeted fat burning (lipolysis)\n- No blood sugar spikes\n- Cartilage repair support\n- Non-hormonal",
        "side_effects_summary": "- Injection site redness\n- Mild stomach upset\n- Headache",
        "protocol_summary": "300mcg daily, morning fasted."
    },
    "BPC-157": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Regenerative", "benefits_summary": "- Accelerates tendon/ligament repair\n- Heals gut lining\n- Reduces neuro-inflammation\n- Protects liver",
        "side_effects_summary": "- Mild nausea\n- Injection site irritation\n- Fatigue",
        "protocol_summary": "250-500mcg daily or 2x daily."
    },
    "BPC-157 + TB-500 Blend": {
        "vial_mg": 10.0, "dose_mcg": 500.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Regenerative Blend", "benefits_summary": "- Maximum recovery\n- Improves joint flexibility\n- Cardiovascular protection",
        "side_effects_summary": "- Head rush\n- Fatigue/Lethargy\n- Injection site stinging",
        "protocol_summary": "500mcg-1mg total fluid daily."
    },
    "CJC-1295 (No DAC)": {
        "vial_mg": 5.0, "dose_mcg": 100.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone", "benefits_summary": "- Increases lean muscle mass\n- Promotes deep sleep\n- Improves skin elasticity",
        "side_effects_summary": "- Flushing/Warmth\n- Head rush\n- Vivid dreams",
        "protocol_summary": "100mcg nightly, fasted."
    },
    "CJC-1295 + Ipamorelin Blend": {
        "vial_mg": 10.0, "dose_mcg": 200.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone Blend", "benefits_summary": "- Max natural GH secretion\n- Recomposition\n- Superior recovery",
        "side_effects_summary": "- Head rush/Flushing\n- Numb fingers\n- Water retention",
        "protocol_summary": "200-300mcg total nightly, fasted."
    },
    "Epithalon": {
        "vial_mg": 10.0, "dose_mcg": 5000.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Anti-Aging", "benefits_summary": "- Extends lifespan (Telomeres)\n- Resets circadian rhythm\n- Boosts melatonin",
        "side_effects_summary": "- Daytime drowsiness\n- Vivid dreams",
        "protocol_summary": "5mg-10mg daily for 10-20 days."
    },
    "GHK-Cu": {
        "vial_mg": 50.0, "dose_mcg": 2000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cosmetic/Repair", "benefits_summary": "- Boosts collagen & elastin\n- Tightens skin\n- Regrows hair",
        "side_effects_summary": "- Painful injection\n- Red welts\n- Zinc depletion",
        "protocol_summary": "1-2mg daily. Evening."
    },
    "Glow Blend (GHK-Cu/BPC/TB)": {
        "vial_mg": 70.0, "dose_mcg": 2500.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cosmetic/Recovery Blend", "benefits_summary": "- Painless GHK-Cu injection\n- Total body skin tightening\n- Rapid injury recovery",
        "side_effects_summary": "- Mild redness\n- Flushing\n- Fatigue",
        "protocol_summary": "2.5mg - 3mg total daily."
    },
    "HCG": {
        "vial_mg": 5000.0, "dose_mcg": 250.0, "default_dose_unit": "IU", "default_stock_unit": "IU", "iu_conversion": 1,
        "type": "Hormonal", "benefits_summary": "- Prevents testicular shrinkage\n- Maintains fertility\n- Boosts libido & mood",
        "side_effects_summary": "- Estrogen spikes\n- Acne/Water retention\n- Gynecomastia risk",
        "protocol_summary": "250-500 IU 2-3x per week."
    },
    "Ipamorelin": {
        "vial_mg": 5.0, "dose_mcg": 100.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone", "benefits_summary": "- Clean GH release\n- Fat loss & muscle sparing\n- Improved sleep quality",
        "side_effects_summary": "- Very mild\n- Slight water retention",
        "protocol_summary": "100-300mcg nightly, fasted."
    },
    "Kisspeptin": {
        "vial_mg": 10.0, "dose_mcg": 100.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Hormonal", "benefits_summary": "- Restarts HPTA axis safely\n- Boosts fertility\n- Increases libido",
        "side_effects_summary": "- Flushing/Warmth\n- Injection site redness",
        "protocol_summary": "100-200mcg daily."
    },
    "Klow Blend (GHK-Cu/BPC/TB/KPV)": {
        "vial_mg": 80.0, "dose_mcg": 3000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Ultimate Repair/Cosmetic Blend", "benefits_summary": "- Clears Acne, Psoriasis\n- Heals Gut\n- Systemic anti-inflammatory",
        "side_effects_summary": "- Red welts\n- Fatigue\n- Flushing",
        "protocol_summary": "3mg total daily."
    },
    "Melanotan II": {
        "vial_mg": 10.0, "dose_mcg": 500.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cosmetic", "benefits_summary": "- Deep, rapid tan\n- Extreme libido boost\n- Appetite suppression",
        "side_effects_summary": "- Severe Nausea\n- Facial Flushing\n- Spontaneous erections",
        "protocol_summary": "100-500mcg before UV exposure."
    },
    "MOTS-c": {
        "vial_mg": 10.0, "dose_mcg": 5000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Metabolic/Mitochondrial", "benefits_summary": "- Increases endurance\n- Prevents weight gain\n- Cellular energy boost",
        "side_effects_summary": "- Painful injection\n- Insomnia\n- Hyperactivity",
        "protocol_summary": "5mg once weekly."
    },
    "NAD+": {
        "vial_mg": 500.0, "dose_mcg": 25000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cellular Energy", "benefits_summary": "- Clears brain fog\n- Restores cellular energy\n- Repairs DNA damage",
        "side_effects_summary": "- Chest pressure (The Flush)\n- Anxiety/Panic feeling\n- Nausea/Cramps",
        "protocol_summary": "25-50mg 2-3x per week. SLOW INJECTION."
    },
    "Oxytocin Acetate": {
        "vial_mg": 2.0, "dose_mcg": 20.0, "default_dose_unit": "IU", "default_stock_unit": "mg", "iu_conversion": 600,
        "type": "Hormonal/Wellness", "benefits_summary": "- Reduces social anxiety\n- Lowers cortisol\n- Enhances bonding",
        "side_effects_summary": "- Nausea\n- Headache\n- Flushing",
        "protocol_summary": "20-50 IU as needed."
    },
    "PT-141": {
        "vial_mg": 10.0, "dose_mcg": 1000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Libido", "benefits_summary": "- Treats ED & Low Libido\n- Works when Viagra fails\n- Increases physical arousal",
        "side_effects_summary": "- Nausea\n- Flushing/Warmth\n- Headache",
        "protocol_summary": "1.5-2mg, 2 hours before activity."
    },
    "Retatrutide": {
        "vial_mg": 10.0, "dose_mcg": 2000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Metabolic (GLP-1/GIP/Glucagon)", "benefits_summary": "- Extreme weight loss (24%+)\n- Burns liver fat\n- Resets insulin sensitivity",
        "side_effects_summary": "- High Heart Rate\n- Skin sensitivity\n- Nausea/Constipation",
        "protocol_summary": "2mg weekly, titrate up."
    },
    "Semaglutide": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Metabolic (GLP-1)", "benefits_summary": "- Weight loss (15%)\n- Controls blood sugar\n- Cardioprotective",
        "side_effects_summary": "- Nausea/Vomiting\n- Severe Constipation\n- Fatigue",
        "protocol_summary": "0.25mg weekly, titrate up."
    },
    "TB-500": {
        "vial_mg": 5.0, "dose_mcg": 2500.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Regenerative", "benefits_summary": "- Heals muscle tears\n- Improves flexibility\n- Reduces scar tissue",
        "side_effects_summary": "- Head rush\n- Lethargy\n- Flu-like symptoms",
        "protocol_summary": "2.5mg twice weekly."
    },
    "Tesamorelin": {
        "vial_mg": 2.0, "dose_mcg": 1000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone", "benefits_summary": "- Burns belly fat\n- Increases muscle tone\n- Nootropic effects",
        "side_effects_summary": "- Injection redness\n- Joint stiffness\n- Carpal Tunnel",
        "protocol_summary": "1-2mg nightly, fasted."
    },
    "Tesamorelin + Ipamorelin Blend": {
        "vial_mg": 12.0, "dose_mcg": 350.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone/Fat Loss Blend", "benefits_summary": "- Max fat loss\n- Muscle definition\n- Deep sleep",
        "side_effects_summary": "- Flushing/Redness\n- Joint stiffness\n- Water retention",
        "protocol_summary": "350-500mcg total nightly, fasted."
    },
    "Tirzepatide": {
        "vial_mg": 30.0, "dose_mcg": 2.5, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Metabolic (GLP-1/GIP)", "benefits_summary": "- Massive weight loss (22%)\n- Eliminates 'Food Noise'\n- Less nausea",
        "side_effects_summary": "- Anhedonia\n- Constipation\n- Hair shedding",
        "protocol_summary": "2.5mg weekly, titrate up."
    },
}

# --- STATE MANAGEMENT ---
if 'vial_val' not in st.session_state: st.session_state.vial_val = 30.0
if 'dose_val' not in st.session_state: st.session_state.dose_val = 2.5
if 'stock_unit_index' not in st.session_state: st.session_state.stock_unit_index = 0
if 'dose_unit_selection' not in st.session_state: st.session_state.dose_unit_selection = "mg"

def load_preset():
    selection = st.session_state.peptide_selector
    data = PEPTIDE_PRESETS[selection]
    st.session_state.vial_val = float(data["vial_mg"])
    st.session_state.stock_unit_index = 3 if data.get("default_stock_unit") == "IU" else 0
    st.session_state.dose_unit_selection = data.get("default_dose_unit", "mcg")
    st.session_state.dose_val = float(data["dose_mcg"])

# --- UI ---
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
    with c1: vial_qty = st.number_input("Stock Amount", key="vial_val", min_value=0.0, step=1.0)
    with c2: vial_unit = st.selectbox("Unit", ["mg", "mcg", "g", "IU"], index=st.session_state.stock_unit_index)
    with c3: water_ml = st.number_input("Water Added (mL)", value=2.0, step=0.5, min_value=0.1)

    st.write("🎯 **Dosing**")
    c4, c5 = st.columns([2, 1])
    with c5: dose_unit = st.selectbox("Dose Unit", ["mcg", "mg", "g", "IU"], key="dose_unit_selection")
    with c4:
        step = 0.5 if dose_unit == 'mg' else 50.0 if dose_unit == 'mcg' else 5.0 if dose_unit == 'IU' else 0.001
        desired_dose = st.number_input("Desired Dose", key="dose_val", min_value=0.0, step=step)
    
    syringe_type = st.radio("Syringe Type", ["U-100 (Standard)", "U-40 (Vet)"], horizontal=True)
    syringe_factor = 100 if "U-100" in syringe_type else 40

with right_col:
    st.success("2️⃣ **Profile & Results**")
    if vial_qty > 0 and water_ml > 0 and desired_dose > 0:
        conversion = peptide_info.get("iu_conversion")
        total_stock_units = 0
        
        # Calculation Logic
        if conversion and conversion > 1:
            if vial_unit in ['mg', 'mcg', 'g']:
                mg = vial_qty if vial_unit == 'mg' else vial_qty/1000 if vial_unit == 'mcg' else vial_qty*1000
                total_stock_units = mg * conversion
            else: total_stock_units = vial_qty
            
            if dose_unit == 'IU': target_dose_units = desired_dose
            elif dose_unit == 'mg': target_dose_units = desired_dose * conversion
            else: target_dose_units = (desired_dose/1000) * conversion
        elif conversion == 1:
            total_stock_units = vial_qty
            target_dose_units = desired_dose
        else:
            total_stock_units = vial_qty * 1000 if vial_unit == 'mg' else vial_qty if vial_unit == 'mcg' else vial_qty * 1000000
            target_dose_units = desired_dose * 1000 if dose_unit == 'mg' else desired_dose if dose_unit == 'mcg' else desired_dose * 1000000

        if total_stock_units > 0:
            draw_ml = target_dose_units / (total_stock_units / water_ml)
            units = draw_ml * syringe_factor
            doses_per_vial = total_stock_units / target_dose_units
        else: draw_ml, units, doses_per_vial = 0, 0, 0

        c1, c2, c3 = st.columns(3)
        c1.metric("Draw Volume", f"{draw_ml:.4f} mL")
        c2.metric("Syringe Units", f"{units:.1f} Units")
        c3.metric("Doses / Vial", f"{int(doses_per_vial)}")
        
        percentage = min(units / syringe_factor * 100, 100)
        st.markdown(f"""<div style="font-weight:bold;">Visual Fill:</div><div class="syringe-container"><div class="syringe-liquid" style="width: {percentage}%;"></div><div class="syringe-markings"></div></div>""", unsafe_allow_html=True)
        st.caption(f"Draw to **{units:.1f}** on your syringe.")

        with st.expander(f"📖 Profile: {selected_peptide}", expanded=True):
            st.markdown(f"**Type:** {peptide_info['type']}\n\n**🌟 Key Benefits:**\n{peptide_info['benefits_summary']}")
            st.markdown(f"<div style='background-color:#3e1818; padding:10px; border-radius:4px;'><strong>⚠️ Side Effects:</strong><br>{peptide_info['side_effects_summary'].replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
            st.info(f"**📋 Quick Protocol:** {peptide_info['protocol_summary']}")
    else:
        st.info("Enter inputs to see results.")

st.divider()
with st.expander("🛠️ How to Reconstitute (Mix)", expanded=True):
    if vial_qty > 0 and water_ml > 0:
        st.markdown(f"1. **Clean:** Wipe vial tops.\n2. **Withdraw:** Draw **{water_ml} mL** Bacteriostatic Water.\n3. **Inject:** Slowly into peptide vial wall.\n4. **Mix:** Swirl gently, do not shake.\n5. **Store:** Refrigerate.")
