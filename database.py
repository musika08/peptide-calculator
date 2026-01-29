import streamlit as st

# --- CONFIGURATION ---
st.set_page_config(
    page_title="PeptideCalc Pro - Database",
    page_icon="📚",
    layout="wide"
)

# --- CSS FOR CARDS ---
st.markdown("""
<style>
    .db-tag { background-color: #4b4bff; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.8em; font-weight: bold; display: inline-block; margin-bottom: 10px; }
    .side-effect-box { background-color: #3e1818; border-left: 4px solid #ff4b4b; padding: 10px; margin-top: 10px; border-radius: 4px; font-size: 0.9em; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# --- KNOWLEDGE BASE (Clinical Edition) ---
PEPTIDE_PRESETS = {
    "AOD-9604": {"type": "Fat Loss", "filter_cat": "Slimming & Fat Loss", "desc": "Anti-Obesity Drug 9604. Fragment of HGH.", "benefits_detailed": "- **Targeted Lipolysis:** Breaks fat cells.\n- **Metabolic Safety:** No insulin spike.", "side_effects_detailed": "• Injection redness\n• Rare headache", "protocol_detailed": "**Dosage:** 300mcg daily fasted.", "storage": "Refrigerate."},
    "BPC-157": {"type": "Regenerative", "filter_cat": "Injury & Repair", "desc": "Body Protection Compound. Derived from gastric juice.", "benefits_detailed": "- **Healing:** Speeds up tendon/ligament repair.\n- **Gut:** Heals ulcers/IBS.", "side_effects_detailed": "• Rare nausea\n• Fatigue", "protocol_detailed": "**Dosage:** 250-500mcg daily.", "storage": "Refrigerate."},
    "BPC-157 + TB-500 Blend": {"type": "Regenerative Blend", "filter_cat": "Injury & Repair", "desc": "The 'Wolverine Stack'. Synergistic repair.", "benefits_detailed": "- **Total Repair:** Targets bone and muscle.\n- **Mobility:** Improves joint range.", "side_effects_detailed": "• Head rush\n• Lethargy", "protocol_detailed": "**Dosage:** 500mcg-1mg total.", "storage": "Refrigerate."},
    "CJC-1295 (No DAC)": {"type": "Growth Hormone", "filter_cat": "Muscle & Workout", "desc": "GHRH analog for pulsatile GH.", "benefits_detailed": "- **Sleep:** Improves deep Stage 4 sleep.\n- **Aging:** Increases collagen synthesis.", "side_effects_detailed": "• Warm flushing\n• Vivid dreams", "protocol_detailed": "**Dosage:** 100mcg nightly fasted.", "storage": "Refrigerate."},
    "CJC-1295 + Ipamorelin Blend": {"type": "Growth Hormone Blend", "filter_cat": "Muscle & Workout", "desc": "Gold Standard GH stack.", "benefits_detailed": "- **Fat:** Mobilizes visceral belly fat.\n- **Recovery:** Natural GH secretion.", "side_effects_detailed": "• Numb fingers\n• Water weight", "protocol_detailed": "**Dosage:** 200-300mcg nightly.", "storage": "Refrigerate."},
    "Epithalon": {"type": "Anti-Aging", "filter_cat": "Wellness & Longevity", "desc": "Tetrapeptide for telomerase.", "benefits_detailed": "- **DNA:** Protects telomere length.\n- **Sleep:** Resets pineal gland/melatonin.", "side_effects_detailed": "• Extremely safe\n• Drowsiness", "protocol_detailed": "**Dosage:** 5-10mg daily (10-20 days).", "storage": "Refrigerate."},
    "GHK-Cu": {"type": "Cosmetic/Repair", "filter_cat": "Skin, Hair & Beauty", "desc": "Copper Tripeptide-1. Genomic modulator.", "benefits_detailed": "- **Skin:** 70% increase in collagen.\n- **Hair:** Increases follicle size.", "side_effects_detailed": "• Painful sting\n• Zinc depletion", "protocol_detailed": "**Dosage:** 1-2mg daily.", "storage": "Refrigerate."},
    "Glow Blend (GHK-Cu/BPC/TB)": {"type": "Cosmetic/Recovery Blend", "filter_cat": "Skin, Hair & Beauty", "desc": "70mg Tri-Blend for skin.", "benefits_detailed": "- **Painless:** BPC buffers copper sting.\n- **Total Rejuvenation:** Skin & Muscle.", "side_effects_detailed": "• Redness\n• Fatigue", "protocol_detailed": "**Dosage:** 2.5-3mg total.", "storage": "Refrigerate."},
    "HCG": {"type": "Hormonal", "filter_cat": "Libido & Sexual Health", "desc": "Mimics LH for testicular health.", "benefits_detailed": "- **Testes:** Prevents atrophy on TRT.\n- **Fertility:** Maintains sperm count.", "side_effects_detailed": "• Estrogen spikes\n• Acne", "protocol_detailed": "**Dosage:** 250-500 IU 2-3x weekly.", "storage": "Refrigerate."},
    "Ipamorelin": {"type": "Growth Hormone", "filter_cat": "Muscle & Workout", "desc": "Selective GH Secretagogue.", "benefits_detailed": "- **Pure Pulse:** GH release without hunger.\n- **REM:** Increases sleep quality.", "side_effects_detailed": "• Well tolerated\n• Slight water", "protocol_detailed": "**Dosage:** 100-300mcg nightly.", "storage": "Refrigerate."},
    "Kisspeptin": {"type": "Hormonal", "filter_cat": "Libido & Sexual Health", "desc": "Stimulates GnRH in hypothalamus.", "benefits_detailed": "- **Restart:** Safely restores natural T.\n- **Fertility:** Stimulates FSH.", "side_effects_detailed": "• Mild flushing\n• Headache", "protocol_detailed": "**Dosage:** 100-200mcg daily.", "storage": "Refrigerate."},
    "Klow Blend (GHK-Cu/BPC/TB/KPV)": {"type": "Ultimate Repair/Cosmetic Blend", "filter_cat": "Skin, Hair & Beauty", "desc": "Master Stack with KPV.", "benefits_detailed": "- **Skin:** Clears acne/eczema.\n- **Gut:** Strongest stack for IBD.", "side_effects_detailed": "• Red welts\n• Fatigue", "protocol_detailed": "**Dosage:** 3mg daily.", "storage": "Refrigerate."},
    "Melanotan II": {"type": "Cosmetic", "filter_cat": "Skin, Hair & Beauty", "desc": "Alpha-MSH analog for tan.", "benefits_detailed": "- **Tan:** Rapid melanin production.\n- **Libido:** Intense arousal effect.", "side_effects_detailed": "• Severe nausea\n• Darkening moles", "protocol_detailed": "**Dosage:** 100-500mcg before UV.", "storage": "Refrigerate."},
    "MOTS-c": {"type": "Metabolic", "filter_cat": "Muscle & Workout", "desc": "Exercise mimetic peptide.", "benefits_detailed": "- **Endurance:** Increases VO2 Max.\n- **Weight:** Prevents diet-induced gain.", "side_effects_detailed": "• Stinging site\n• Insomnia", "protocol_detailed": "**Dosage:** 5-10mg once weekly.", "storage": "Refrigerate."},
    "NAD+": {"type": "Cellular Energy", "filter_cat": "Wellness & Longevity", "desc": "Fuel for cellular engines.", "benefits_detailed": "- **Brain:** Clears fog immediately.\n- **Aging:** Repairs DNA damage.", "side_effects_detailed": "• Chest pressure\n• Anxiety", "protocol_detailed": "**Dosage:** 25-50mg 2-3x weekly (Slow).", "storage": "Refrigerate."},
    "Oxytocin Acetate": {"type": "Hormonal/Wellness", "filter_cat": "Nootropics & Brain", "desc": "The 'Love Hormone' modulator.", "benefits_detailed": "- **Social:** Reduces social anxiety.\n- **Bonding:** Enhances emotional trust.", "side_effects_detailed": "• Nausea\n• Headache", "protocol_detailed": "**Dosage:** 10-25 IU as needed.", "storage": "Refrigerate."},
    "PT-141": {"type": "Libido", "filter_cat": "Libido & Sexual Health", "desc": "Bremelanotide for desire.", "benefits_detailed": "- **Desire:** Targets brain desire centers.\n- **Efficacy:** Works when PDE5i fails.", "side_effects_detailed": "• Nausea (Common)\n• High BP", "protocol_detailed": "**Dosage:** 1.5-2mg, 2-4h before activity.", "storage": "Refrigerate."},
    "Retatrutide": {"type": "Metabolic", "filter_cat": "Slimming & Fat Loss", "desc": "Triple G Agonist.", "benefits_detailed": "- **Weight:** ~24% total weight loss.\n- **Liver:** Resolves fatty liver.", "side_effects_detailed": "• Tachycardia\n• Nausea", "protocol_detailed": "**Dosage:** 2mg -> 12mg weekly.", "storage": "Refrigerate."},
    "Semaglutide": {"type": "Metabolic", "filter_cat": "Slimming & Fat Loss", "desc": "GLP-1 Weight loss standard.", "benefits_detailed": "- **Satiety:** Keeps you full longer.\n- **Sugar:** Controls glucose.", "side_effects_detailed": "• Nausea\n• Constipation", "protocol_detailed": "**Dosage:** 0.25mg -> 2.4mg weekly.", "storage": "Refrigerate."},
    "TB-500": {"type": "Regenerative", "filter_cat": "Injury & Repair", "desc": "Thymosin Beta-4 analog.", "benefits_detailed": "- **Muscle:** Heals tears/strains.\n- **Cardiac:** Reduces heart scarring.", "side_effects_detailed": "• Head rush\n• Lethargy", "protocol_detailed": "**Dosage:** 2.5mg 2x weekly.", "storage": "Refrigerate."},
    "Tesamorelin": {"type": "Growth Hormone", "filter_cat": "Slimming & Fat Loss", "desc": "FDA approved for visceral fat.", "benefits_detailed": "- **Belly:** Targets fat around organs.\n- **Brain:** Increases focus/memory.", "side_effects_detailed": "• Joint stiffness\n• Redness", "protocol_detailed": "**Dosage:** 1-2mg nightly fasted.", "storage": "Refrigerate."},
    "Tesamorelin + Ipamorelin Blend": {"type": "Growth Hormone Blend", "filter_cat": "Slimming & Fat Loss", "desc": "The 'Shred Stack'.", "benefits_detailed": "- **Recomp:** Builds muscle/burns fat.\n- **Sleep:** Deep recovery pulses.", "side_effects_detailed": "• Joint pain\n• Flushing", "protocol_detailed": "**Dosage:** 350-500mcg nightly.", "storage": "Refrigerate."},
    "Tirzepatide": {"type": "Metabolic", "filter_cat": "Slimming & Fat Loss", "desc": "GIP/GLP-1 Dual Agonist.", "benefits_detailed": "- **Loss:** Superior weight reduction.\n- **Noise:** Stops food obsessions.", "side_effects_detailed": "• Anhedonia\n• Hair shedding", "protocol_detailed": "**Dosage:** 2.5mg -> 15mg weekly.", "storage": "Refrigerate."},
}

# --- SEARCH ---
st.title("📚 Peptide Encyclopedia")
st.divider()

cats = ["All", "Slimming & Fat Loss", "Skin, Hair & Beauty", "Muscle & Workout", "Nootropics & Brain", "Injury & Repair", "Wellness & Longevity", "Libido & Sexual Health"]
c1, c2 = st.columns([3, 1])
with c1: q = st.text_input("🔍 Search Database", placeholder="Search...").lower()
with c2: f = st.selectbox("🏷️ Category", cats)

# --- FILTER & GRID ---
filtered = {n: d for n, d in PEPTIDE_PRESETS.items() if (f == "All" or d['filter_cat'] == f) and (q in n.lower() or q in d['benefits_detailed'].lower())}

cols = st.columns(3)
for i, (name, info) in enumerate(filtered.items()):
    with cols[i % 3]:
        with st.container(border=True):
            st.markdown(f"### {name}")
            st.markdown(f"<span class='db-tag'>{info['type']}</span>", unsafe_allow_html=True)
            st.markdown(f"**🌟 Benefits:**\n{info['benefits_detailed']}")
            st.markdown(f"<div class='side-effect-box'><strong>⚠️ Side Effects:</strong><br>{info['side_effects_detailed']}</div>", unsafe_allow_html=True)
            with st.expander("📋 Protocol", expanded=True): st.markdown(info['protocol_detailed'])
            with st.expander("ℹ️ Mechanism & Storage"):
                st.markdown(f"_{info['desc']}_")
                st.markdown(f"**❄️ Storage:** {info['storage']}")
