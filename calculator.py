import streamlit as st
import math

# --- CONFIGURATION ---
st.set_page_config(
    page_title="PeptideCalc Pro - Calculator",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS FOR SYRINGE ---
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

# --- KNOWLEDGE BASE (Calculator Edition) ---
PEPTIDE_PRESETS = {
    "AOD-9604": {"vial_mg": 5.0, "dose_mcg": 300.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None, "type": "Fat Loss", "benefits_summary": "- Targeted fat burning\n- No blood sugar spikes\n- Cartilage repair", "side_effects_summary": "- Injection site redness\n- Mild stomach upset", "protocol_summary": "300mcg daily, morning fasted."},
    "BPC-157": {"vial_mg": 5.0, "dose_mcg": 250.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None, "type": "Regenerative", "benefits_summary": "- Accelerates tendon repair\n- Heals gut lining\n- Protects organs", "side_effects_summary": "- Mild nausea\n- Site irritation", "protocol_summary": "250-500mcg daily."},
    "BPC-157 + TB-500 Blend": {"vial_mg": 10.0, "dose_mcg": 500.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None, "type": "Regenerative Blend", "benefits_summary": "- Maximum injury recovery\n- Joint flexibility", "side_effects_summary": "- Head rush\n- Lethargy", "protocol_summary": "500mcg-1mg total fluid daily."},
    "CJC-1295 (No DAC)": {"vial_mg": 5.0, "dose_mcg": 100.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None, "type": "Growth Hormone", "benefits_summary": "- Increases lean muscle\n- Deep sleep\n- Skin elasticity", "side_effects_summary": "- Flushing\n- Vivid dreams", "protocol_summary": "100mcg nightly, fasted."},
    "CJC-1295 + Ipamorelin Blend": {"vial_mg": 10.0, "dose_mcg": 200.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None, "type": "Growth Hormone Blend", "benefits_summary": "- Max natural GH release\n- Recovery & Sleep", "side_effects_summary": "- Numb fingers\n- Water retention", "protocol_summary": "200-300mcg nightly, fasted."},
    "Epithalon": {"vial_mg": 10.0, "dose_mcg": 5000.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None, "type": "Anti-Aging", "benefits_summary": "- Extends telomeres\n- Resets circadian rhythm", "side_effects_summary": "- Daytime drowsiness", "protocol_summary": "5mg-10mg daily for 10-20 days."},
    "GHK-Cu": {"vial_mg": 50.0, "dose_mcg": 2000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None, "type": "Cosmetic/Repair", "benefits_summary": "- Boosts collagen\n- Tightens skin\n- Hair regrowth", "side_effects_summary": "- Painful injection\n- Zinc depletion", "protocol_summary": "1-2mg daily. Evening."},
    "Glow Blend (GHK-Cu/BPC/TB)": {"vial_mg": 70.0, "dose_mcg": 2500.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None, "type": "Cosmetic/Recovery Blend", "benefits_summary": "- Painless GHK injection\n- Rapid injury recovery", "side_effects_summary": "- Mild redness\n- Fatigue", "protocol_summary": "2.5mg - 3mg total daily."},
    "HCG": {"vial_mg": 5000.0, "dose_mcg": 250.0, "default_dose_unit": "IU", "default_stock_unit": "IU", "iu_conversion": 1, "type": "Hormonal", "benefits_summary": "- Prevents testicular shrinkage\n- Maintains fertility", "side_effects_summary": "- Estrogen spikes\n- Acne", "protocol_summary": "250-500 IU 2-3x per week."},
    "Ipamorelin": {"vial_mg": 5.0, "dose_mcg": 100.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None, "type": "Growth Hormone", "benefits_summary": "- Clean GH release\n- Muscle sparing\n- Improved sleep", "side_effects_summary": "- Slight water retention", "protocol_summary": "100-300mcg nightly, fasted."},
    "Kisspeptin": {"vial_mg": 10.0, "dose_mcg": 100.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None, "type": "Hormonal", "benefits_summary": "- Restarts HPTA axis\n- Boosts fertility", "side_effects_summary": "- Flushing\n- Headache", "protocol_summary": "100-200mcg daily."},
    "Klow Blend (GHK-Cu/BPC/TB/KPV)": {"vial_mg": 80.0, "dose_mcg": 3000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None, "type": "Ultimate Repair/Cosmetic Blend", "benefits_summary": "- Clears Acne/Psoriasis\n- Heals Gut", "side_effects_summary": "- Red welts\n- Fatigue", "protocol_summary": "3mg total daily."},
    "Melanotan II": {"vial_mg": 10.0, "dose_mcg": 500.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None, "type": "Cosmetic", "benefits_summary": "- Rapid tan\n- Libido boost\n- Appetite suppression", "side_effects_summary": "- Severe Nausea\n- Flushing", "protocol_summary": "100-500mcg before UV."},
    "MOTS-c": {"vial_mg": 10.0, "dose_mcg": 5000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None, "type": "Metabolic", "benefits_summary": "- Endurance boost\n- Mitochondrial biogenesis", "side_effects_summary": "- Painful injection\n- Insomnia", "protocol_summary": "5mg once weekly."},
    "NAD+": {"vial_mg": 500.0, "dose_mcg": 25000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None, "type": "Cellular Energy", "benefits_summary": "- Clears brain fog\n- Repairs DNA damage", "side_effects_summary": "- Chest pressure\n- Anxiety feeling", "protocol_summary": "25-50mg 2-3x per week. SLOW."},
    "Oxytocin Acetate": {"vial_mg": 2.0, "dose_mcg": 20.0, "default_dose_unit": "IU", "default_stock_unit": "mg", "iu_conversion": 600, "type": "Hormonal/Wellness", "benefits_summary": "- Reduces anxiety\n- Enhances bonding", "side_effects_summary": "- Nausea\n- Headache", "protocol_summary": "20-50 IU as needed."},
    "PT-141": {"vial_mg": 10.0, "dose_mcg": 1000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None, "type": "Libido", "benefits_summary": "- Treats ED & Low Libido\n- Physical arousal", "side_effects_summary": "- Nausea\n- Flushing", "protocol_summary": "1.5-2mg, 2-4h before activity."},
    "Retatrutide": {"vial_mg": 10.0, "dose_mcg": 2.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None, "type": "Metabolic (Triple G)", "benefits_summary": "- Extreme weight loss\n- Burns liver fat", "side_effects_summary": "- High heart rate\n- Nausea", "protocol_summary": "2mg weekly, titrate up."},
    "Semaglutide": {"vial_mg": 5.0, "dose_mcg": 0.25, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None, "type": "Metabolic (GLP-1)", "benefits_summary": "- Weight loss\n- Blood sugar control", "side_effects_summary": "- Nausea\n- Constipation", "protocol_summary": "0.25mg weekly, titrate up."},
    "TB-500": {"vial_mg": 5.0, "dose_mcg": 2500.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None, "type": "Regenerative", "benefits_summary": "- Heals muscle tears\n- Improves flexibility", "side_effects_summary": "- Head rush\n- Lethargy", "protocol_summary": "2.5mg twice weekly."},
    "Tesamorelin": {"vial_mg": 2.0, "dose_mcg": 1.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None, "type": "Growth Hormone", "benefits_summary": "- Burns visceral belly fat\n- Nootropic effects", "side_effects_summary": "- Joint stiffness\n- Carpal Tunnel", "protocol_summary": "1-2mg nightly, fasted."},
    "Tesamorelin + Ipamorelin Blend": {"vial_mg": 12.0, "dose_mcg": 350.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None, "type": "Growth Hormone/Fat Loss Blend", "benefits_summary": "- Max visceral fat loss\n- Deep sleep", "side_effects_summary": "- Flushing\n- Joint pain", "protocol_summary": "350-500mcg nightly, fasted."},
    "Tirzepatide": {"vial_mg": 30.0, "dose_mcg": 2.5, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None, "type": "Metabolic (GLP-1/GIP)", "benefits_summary": "- Massive weight loss\n- Eliminates food noise", "side_effects_summary": "- Anhedonia\n- Constipation", "protocol_summary": "2.5mg weekly, titrate up."},
}

# --- STATE HANDLING ---
if 'vial_val' not in st.session_state: st.session_state.vial_val = 30.0
if 'dose_val' not in st.session_state: st.session_state.dose_val = 2.5
if 'stock_unit_index' not in st.session_state: st.session_state.stock_unit_index = 0
if 'dose_unit_selection' not in st.session_state: st.session_state.dose_unit_selection = "mg"

def load_preset():
    sel = st.session_state.peptide_selector
    data = PEPTIDE_PRESETS[sel]
    st.session_state.vial_val = float(data["vial_mg"])
    st.session_state.stock_unit_index = 3 if data.get("default_stock_unit") == "IU" else 0
    st.session_state.dose_unit_selection = data.get("default_dose_unit", "mcg")
    st.session_state.dose_val = float(data["dose_mcg"])

# --- UI ---
st.title("🧮 Peptide Reconstitution Calculator")
st.divider()

l_col, r_col = st.columns([1, 1.2], gap="large")

with l_col:
    st.subheader("1️⃣ Configuration")
    sorted_p = sorted(list(PEPTIDE_PRESETS.keys()))
    d_idx = sorted_p.index("Tirzepatide") if "Tirzepatide" in sorted_p else 0
    sel_pep = st.selectbox("Select Peptide Profile", sorted_p, index=d_idx, key="peptide_selector", on_change=load_preset)
    p_info = PEPTIDE_PRESETS[sel_pep]

    st.write("**📦 Stock & Water**")
    c1, c2, c3 = st.columns([1.5, 1, 1.5])
    with c1: v_qty = st.number_input("Stock Amount", key="vial_val", min_value=0.0, step=1.0)
    with c2: v_unit = st.selectbox("Unit", ["mg", "mcg", "g", "IU"], index=st.session_state.stock_unit_index)
    with c3: h2o = st.number_input("Water (mL)", value=2.0, step=0.5, min_value=0.1)

    st.write("**🎯 Dosing**")
    c4, c5 = st.columns([2, 1])
    with c5: d_unit = st.selectbox("Dose Unit", ["mcg", "mg", "g", "IU"], key="dose_unit_selection")
    with c4:
        st_size = 0.5 if d_unit == 'mg' else 50.0 if d_unit == 'mcg' else 5.0 if d_unit == 'IU' else 0.001
        d_dose = st.number_input("Desired Dose", key="dose_val", min_value=0.0, step=st_size)
    
    s_type = st.radio("Syringe Type", ["U-100", "U-40"], horizontal=True)
    s_factor = 100 if "U-100" in s_type else 40

with r_col:
    st.subheader("2️⃣ Results")
    if v_qty > 0 and h2o > 0 and d_dose > 0:
        conv = p_info.get("iu_conversion")
        
        # Calculation Engine
        if conv and conv > 1:
            mg = v_qty if v_unit == 'mg' else v_qty/1000 if v_unit == 'mcg' else v_qty*1000 if v_unit == 'g' else v_qty/conv
            t_stock = mg * conv if v_unit != 'IU' else v_qty
            t_target = d_dose if d_unit == 'IU' else d_dose * conv if d_unit == 'mg' else (d_dose/1000) * conv
        elif conv == 1:
            t_stock, t_target = v_qty, d_dose
        else:
            t_stock = v_qty * 1000 if v_unit == 'mg' else v_qty if v_unit == 'mcg' else v_qty * 1000000
            t_target = d_dose * 1000 if d_unit == 'mg' else d_dose if d_unit == 'mcg' else d_dose * 1000000

        if t_stock > 0:
            draw = t_target / (t_stock / h2o)
            units = draw * s_factor
            d_per_v = t_stock / t_target
        else: draw, units, d_per_v = 0, 0, 0

        c1, c2, c3 = st.columns(3)
        c1.metric("Draw (mL)", f"{draw:.4f}")
        c2.metric("Units", f"{units:.1f}")
        c3.metric("Doses/Vial", f"{int(d_per_v)}")
        
        perc = min(units / s_factor * 100, 100)
        st.markdown(f"""<div class="syringe-container"><div class="syringe-liquid" style="width: {perc}%;"></div><div class="syringe-markings"></div></div>""", unsafe_allow_html=True)
        st.caption(f"Draw to **{units:.1f}** on a {s_type} syringe.")

        with st.expander(f"📖 Profile: {sel_pep}", expanded=True):
            st.markdown(f"**Type:** {p_info['type']}\n\n**🌟 Benefits:**\n{p_info['benefits_summary']}")
            st.warning(f"**⚠️ Side Effects:**\n{p_info['side_effects_summary']}")
            st.info(f"**📋 Protocol:** {p_info['protocol_summary']}")
    else: st.info("Enter values to calculate.")

st.divider()
st.caption("v4.0 | Calculator-Only Build")
