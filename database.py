import streamlit as st

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="PeptideCalc Pro - Database",
    page_icon="📚",
    layout="wide"
)

# --- CSS FOR DATABASE CARDS ---
st.markdown("""
<style>
    .db-tag {
        background-color: #4b4bff;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.8em;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    .side-effect-box {
        background-color: #3e1818;
        border-left: 4px solid #ff4b4b;
        padding: 10px;
        margin-top: 10px;
        border-radius: 4px;
        font-size: 0.9em;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# --- FULL CLINICAL DATA (Isolated) ---
PEPTIDE_PRESETS = {
    "AOD-9604": {
        "type": "Fat Loss", "filter_cat": "Slimming & Fat Loss",
        "desc": "Anti-Obesity Drug 9604. A modified fragment of the HGH C-terminus.",
        "benefits_detailed": "- **Targeted Lipolysis:** Stimulates fat breakdown.\n- **Metabolic Safety:** No insulin resistance.\n- **Joint Support:** Aids cartilage repair.",
        "side_effects_detailed": "• Well tolerated\n• Minor injection site redness\n• Mild headache",
        "protocol_detailed": "**Dosage:** 300mcg\n\n**Frequency:** Daily\n\n**Timing:** Morning Fasted\n\n**Cycle:** 3-6 Months",
        "storage": "Refrigerate."
    },
    "BPC-157": {
        "type": "Regenerative", "filter_cat": "Injury & Repair",
        "desc": "Body Protection Compound-157. Derived from gastric juice.",
        "benefits_detailed": "- **Connective Tissue:** Speeds up soft tissue healing.\n- **Angiogenesis:** Forms new blood vessels.\n- **Gastroprotection:** Heals ulcers.",
        "side_effects_detailed": "• Rare fatigue\n• Mild nausea",
        "protocol_detailed": "**Dosage:** 250mcg - 500mcg\n\n**Frequency:** Daily or Twice Daily\n\n**Timing:** SubQ near injury\n\n**Cycle:** 4-6 Weeks",
        "storage": "Refrigerate."
    },
    "BPC-157 + TB-500 Blend": {
        "type": "Regenerative Blend", "filter_cat": "Injury & Repair",
        "desc": "The 'Wolverine Stack'. Synergistic combination.",
        "benefits_detailed": "- **Total Repair:** Targets tendon and muscle simultaneously.\n- **Mobility:** Improves joint range.\n- **Cardioprotection:** Reduces scar tissue.",
        "side_effects_detailed": "• Temporary head rush\n• Lethargy\n• Stinging site",
        "protocol_detailed": "**Dosage:** 500mcg - 1000mcg\n\n**Frequency:** Daily\n\n**Cycle:** 4-8 Weeks",
        "storage": "Refrigerate."
    },
    "CJC-1295 (No DAC)": {
        "type": "Growth Hormone", "filter_cat": "Muscle & Workout",
        "desc": "Modified GRF 1-29. Stimulates pulsatile GH release.",
        "benefits_detailed": "- **Hyperplasia:** Stimulates muscle cell division.\n- **Sleep:** Improves Stage 4 deep sleep.\n- **Anti-Aging:** Increases collagen.",
        "side_effects_detailed": "• Immediate head rush\n• Warm/flushed face\n• Vivid dreams",
        "protocol_detailed": "**Dosage:** 100mcg\n\n**Frequency:** 5 days on / 2 off\n\n**Timing:** Nightly Fasted",
        "storage": "Refrigerate."
    },
    "CJC-1295 + Ipamorelin Blend": {
        "type": "Growth Hormone Blend", "filter_cat": "Muscle & Workout",
        "desc": "The Gold Standard GH Stack.",
        "benefits_detailed": "- **Synergy:** Maximizes natural GH.\n- **Visceral Fat:** Mobilizes deep abdominal stores.\n- **Safety:** No cortisol spikes.",
        "side_effects_detailed": "• Head rush\n• Numb fingers\n• Water weight",
        "protocol_detailed": "**Dosage:** 200-300mcg\n\n**Frequency:** 5 on / 2 off\n\n**Timing:** Before Bed Fasted",
        "storage": "Refrigerate."
    },
    "Epithalon": {
        "type": "Anti-Aging", "filter_cat": "Wellness & Longevity",
        "desc": "Synthetic tetrapeptide for telomerase activity.",
        "benefits_detailed": "- **Telomeres:** DNA protection.\n- **Endocrine Reset:** Hypothalamus sensitivity.\n- **Sleep:** Normalizes melatonin.",
        "side_effects_detailed": "• Extremely safe\n• Daytime drowsiness",
        "protocol_detailed": "**Dosage:** 5mg - 10mg\n\n**Frequency:** Daily\n\n**Cycle:** 10-20 Day Course",
        "storage": "Refrigerate."
    },
    "GHK-Cu": {
        "type": "Cosmetic/Repair", "filter_cat": "Skin, Hair & Beauty",
        "desc": "Copper Tripeptide-1. Genomic modulator.",
        "benefits_detailed": "- **Skin:** Increases collagen synthesis by 70%.\n- **Hair:** Enlarges follicles.\n- **DNA:** Resets repair genes.",
        "side_effects_detailed": "• Injection pain (Burning)\n• Red welts\n• Zinc depletion",
        "protocol_detailed": "**Dosage:** 1mg - 2mg\n\n**Frequency:** Daily\n\n**Cycle:** 30 Days on/off",
        "storage": "Refrigerate."
    },
    "Glow Blend (GHK-Cu/BPC/TB)": {
        "type": "Cosmetic/Recovery Blend", "filter_cat": "Skin, Hair & Beauty",
        "desc": "Buffered GHK-Cu to reduce 'sting'.",
        "benefits_detailed": "- **Painless:** BPC-157 neutralizes acidity.\n- **Rejuvenation:** Skin, hair, and gut.\n- **Synergy:** Increases GH receptors.",
        "side_effects_detailed": "• Mild redness\n• Flushing\n• Fatigue",
        "protocol_detailed": "**Dosage:** 2.5mg - 3mg\n\n**Timing:** Evening\n\n**Cycle:** 4-6 Weeks",
        "storage": "Refrigerate."
    },
    "HCG": {
        "type": "Hormonal", "filter_cat": "Libido & Sexual Health",
        "desc": "Human Chorionic Gonadotropin. Mimics LH.",
        "benefits_detailed": "- **Testicular Health:** Prevents atrophy during TRT.\n- **Fertility:** Maintains spermatogenesis.\n- **Libido:** Distinct mood/drive boost.",
        "side_effects_detailed": "• Estrogen spikes\n• Acne\n• Water retention",
        "protocol_detailed": "**Dosage:** 250-500 IU\n\n**Frequency:** 2-3x per week",
        "storage": "Refrigerate."
    },
    "Ipamorelin": {
        "type": "Growth Hormone", "filter_cat": "Muscle & Workout",
        "desc": "Selective GH Secretagogue. Mildest GHRP.",
        "benefits_detailed": "- **Pure Signal:** No hunger spikes.\n- **Protection:** Preserves lean muscle.\n- **Sleep:** Increases REM stages.",
        "side_effects_detailed": "• Well tolerated\n• Slight water retention",
        "protocol_detailed": "**Dosage:** 100-300mcg\n\n**Timing:** Nightly Fasted\n\n**Cycle:** 8-12 Weeks",
        "storage": "Refrigerate."
    },
    "Kisspeptin": {
        "type": "Hormonal", "filter_cat": "Libido & Sexual Health",
        "desc": "Stimulates hypothalamus to release GnRH.",
        "benefits_detailed": "- **HPTA Restart:** Safest restart method.\n- **Fertility:** Stimulates FSH.\n- **Safety:** No desensitization.",
        "side_effects_detailed": "• Mild flushing\n• Site redness",
        "protocol_detailed": "**Dosage:** 100-200mcg\n\n**Frequency:** Daily\n\n**Cycle:** 4 Weeks",
        "storage": "Refrigerate."
    },
    "Klow Blend (GHK-Cu/BPC/TB/KPV)": {
        "type": "Ultimate Repair/Cosmetic Blend", "filter_cat": "Skin, Hair & Beauty",
        "desc": "The 80mg Master Stack with KPV.",
        "benefits_detailed": "- **Dermatology:** Treats acne and psoriasis.\n- **Gut Health:** Strongest stack for IBD.\n- **Mast Cells:** KPV stabilizes histamine.",
        "side_effects_detailed": "• Red welts common\n• Fatigue\n• Flushing",
        "protocol_detailed": "**Dosage:** 3mg\n\n**Timing:** Evening\n\n**Cycle:** 4-8 Weeks",
        "storage": "Refrigerate."
    },
    "Melanotan II": {
        "type": "Cosmetic", "filter_cat": "Skin, Hair & Beauty",
        "desc": "Alpha-MSH analog for melanin.",
        "benefits_detailed": "- **Photoprotection:** Deep natural tan.\n- **Libido:** Potent aphrodisiac.\n- **Metabolic:** Suppresses appetite.",
        "side_effects_detailed": "• Nausea\n• Spontaneous erections\n• Darkening moles",
        "protocol_detailed": "**Dosage:** 100-500mcg\n\n**Timing:** Before UV exposure",
        "storage": "Refrigerate."
    },
    "MOTS-c": {
        "type": "Metabolic/Mitochondrial", "filter_cat": "Muscle & Workout",
        "desc": "Exercise mimetic peptide.",
        "benefits_detailed": "- **Endurance:** Increases oxygen utility.\n- **Metabolic:** Prevents insulin resistance.\n- **Biogenesis:** New mitochondria.",
        "side_effects_detailed": "• Injection pain\n• Insomnia if late\n• Restlessness",
        "protocol_detailed": "**Dosage:** 5-10mg\n\n**Frequency:** Once Weekly\n\n**Timing:** Morning",
        "storage": "Refrigerate."
    },
    "NAD+": {
        "type": "Cellular Energy", "filter_cat": "Wellness & Longevity",
        "desc": "Nicotinamide Adenine Dinucleotide fuel.",
        "benefits_detailed": "- **Cognition:** Clears brain fog.\n- **Mitochondria:** Efficient ATP production.\n- **Addiction:** Neurotransmitter balance.",
        "side_effects_detailed": "• Intense chest pressure\n• Anxiety sensation\n• Palpitations",
        "protocol_detailed": "**Dosage:** 25-50mg\n\n**Frequency:** 2-3x per week\n\n**Note:** INJECT SLOWLY.",
        "storage": "Refrigerate."
    },
    "Oxytocin Acetate": {
        "type": "Hormonal/Wellness", "filter_cat": "Nootropics & Brain",
        "desc": "The 'Love Hormone' neurotransmitter.",
        "benefits_detailed": "- **Social:** Reduces social anxiety.\n- **Pain:** Analgesic properties.\n- **Intimacy:** Enhances emotional trust.",
        "side_effects_detailed": "• Nausea\n• Headache\n• Flushing",
        "protocol_detailed": "**Dosage:** 10-25 IU\n\n**Timing:** Before social events",
        "storage": "Refrigerate."
    },
    "PT-141": {
        "type": "Libido", "filter_cat": "Libido & Sexual Health",
        "desc": "Bremelanotide. Hypothalamic target.",
        "benefits_detailed": "- **Mechanism:** Works on nervous system, not vascular.\n- **Efficacy:** FDA approved for low libido.\n- **Response:** Increases physical arousal.",
        "side_effects_detailed": "• Nausea (40% of users)\n• Elevated BP",
        "protocol_detailed": "**Dosage:** 1.5mg - 2mg\n\n**Timing:** 2-4 hours BEFORE activity",
        "storage": "Refrigerate."
    },
    "Retatrutide": {
        "type": "Metabolic (GLP-1/GIP/Glucagon)", "filter_cat": "Slimming & Fat Loss",
        "desc": "The 'Triple G' Agonist.",
        "benefits_detailed": "- **Efficacy:** 24.2% average weight loss.\n- **Liver:** Resolves NAFLD fatty liver.\n- **Energy:** Increases calorie burn.",
        "side_effects_detailed": "• Tachycardia\n• Sensitive skin\n• Nausea",
        "protocol_detailed": "**Dosage:** 2mg -> Max 12mg\n\n**Frequency:** Once Weekly",
        "storage": "Refrigerate."
    },
    "Semaglutide": {
        "type": "Metabolic (GLP-1)", "filter_cat": "Slimming & Fat Loss",
        "desc": "Standard for medical weight loss.",
        "benefits_detailed": "- **Satiety:** Slows gastric emptying.\n- **Heart:** 20% reduction in cardiac events.\n- **Addiction:** Reduces sugar cravings.",
        "side_effects_detailed": "• Nausea/Vomiting\n• Fatigue",
        "protocol_detailed": "**Dosage:** 0.25mg -> Max 2.4mg\n\n**Frequency:** Once Weekly",
        "storage": "Refrigerate."
    },
    "TB-500": {
        "type": "Regenerative", "filter_cat": "Injury & Repair",
        "desc": "Muscle repair peptide.",
        "benefits_detailed": "- **Repair:** Primary for tears/strains.\n- **Flexibility:** Reduces inflammation.\n- **Cardiac:** Repairs heart scarring.",
        "side_effects_detailed": "• Head rush\n• Lethargy",
        "protocol_detailed": "**Dosage:** 2.5mg\n\n**Frequency:** 2x Per Week",
        "storage": "Refrigerate."
    },
    "Tesamorelin": {
        "type": "Growth Hormone", "filter_cat": "Slimming & Fat Loss",
        "desc": "FDA GHRH for visceral fat.",
        "benefits_detailed": "- **Visceral Fat:** Targets fat around organs.\n- **Cognition:** Improves memory.\n- **Cardio:** Lowers triglycerides.",
        "side_effects_detailed": "• Joint stiffness\n• Carpal tunnel",
        "protocol_detailed": "**Dosage:** 1mg - 2mg\n\n**Timing:** Nightly Fasted",
        "storage": "Refrigerate."
    },
    "Tesamorelin + Ipamorelin Blend": {
        "type": "Growth Hormone/Fat Loss Blend", "filter_cat": "Slimming & Fat Loss",
        "desc": "The 'Shred Stack'.",
        "benefits_detailed": "- **Recomposition:** Burns fat/builds muscle.\n- **Metabolic:** Amplifies fasting burn.\n- **Synergy:** Better sleep benefits.",
        "side_effects_detailed": "• Joint pain\n• Numbness\n• Flushing",
        "protocol_detailed": "**Dosage:** 350-500mcg\n\n**Frequency:** 5 on / 2 off",
        "storage": "Refrigerate."
    },
    "Tirzepatide": {
        "type": "Metabolic (GLP-1/GIP)", "filter_cat": "Slimming & Fat Loss",
        "desc": "Dual Agonist (Mounjaro).",
        "benefits_detailed": "- **Weight Loss:** 20%+ average loss.\n- **Food Noise:** Eliminates obsessions.\n- **Tolerability:** Less nausea than GLP-1 alone.",
        "side_effects_detailed": "• Anhedonia (Flat mood)\n• Cold extremities\n• Hair shedding",
        "protocol_detailed": "**Dosage:** 2.5mg -> Max 15mg\n\n**Frequency:** Once Weekly",
        "storage": "Refrigerate."
    },
}

# --- SEARCH & FILTER UI ---
st.subheader("📚 Peptide Clinical Database")
st.divider()

cats = ["All", "Slimming & Fat Loss", "Skin, Hair & Beauty", "Muscle & Workout", "Nootropics & Brain", "Injury & Repair", "Wellness & Longevity", "Libido & Sexual Health"]
col1, col2 = st.columns([3, 1])
with col1: query = st.text_input("🔍 Search Peptides", placeholder="Search...").lower()
with col2: cat_filter = st.selectbox("🏷️ Filter", cats)

# --- FILTERING ---
filtered = {n: d for n, d in PEPTIDE_PRESETS.items() 
            if (cat_filter == "All" or d['filter_cat'] == cat_filter) 
            and (query in n.lower() or query in d['benefits_detailed'].lower())}

# --- GRID RENDER ---
num_cols = 3
cols = st.columns(num_cols)
for i, (name, info) in enumerate(filtered.items()):
    with cols[i % num_cols]:
        with st.container(border=True):
            st.markdown(f"### {name}")
            st.markdown(f"<span class='db-tag'>{info['type']}</span>", unsafe_allow_html=True)
            st.markdown("**🌟 Clinical Benefits:**")
            st.markdown(info['benefits_detailed'])
            st.markdown(f"<div class='side-effect-box'><strong>⚠️ Side Effects:</strong><br>{info['side_effects_detailed'].replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
            with st.expander("📋 Detailed Protocol", expanded=True): st.markdown(info['protocol_detailed'])
            with st.expander("ℹ️ Description & Mechanism"):
                st.markdown(f"_{info['desc']}_")
                st.markdown(f"**❄️ Storage:** {info['storage']}")
