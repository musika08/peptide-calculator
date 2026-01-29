import streamlit as st

# --- CONFIGURATION ---
st.set_page_config(
    page_title="PeptideCalc Pro - Database",
    page_icon="📚",
    layout="wide"
)

# --- CSS FOR DATABASE CARDS ---
st.markdown("""
<style>
    .db-tag { background-color: #4b4bff; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.8em; font-weight: bold; display: inline-block; margin-bottom: 10px; }
    .side-effect-box { background-color: #3e1818; border-left: 4px solid #ff4b4b; padding: 10px; margin-top: 10px; border-radius: 4px; font-size: 0.9em; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# --- CLINICAL DATABASE ---
PEPTIDE_DB = {
    "AOD-9604": {"type": "Fat Loss", "filter_cat": "Slimming & Fat Loss", "desc": "Anti-Obesity Drug 9604. Fragment of HGH.", "benefits": "- **Targeted Lipolysis:** Breaks fat cells.\n- **Metabolic Safety:** No insulin spike.", "side": "• Injection redness\n• Rare headache", "protocol": "**Dosage:** 300mcg daily fasted.", "storage": "Refrigerate."},
    "BPC-157": {"type": "Regenerative", "filter_cat": "Injury & Repair", "desc": "Body Protection Compound. Derived from gastric juice.", "benefits": "- **Healing:** Speeds up tendon/ligament repair.\n- **Gut:** Heals ulcers/IBS.", "side": "• Rare nausea\n• Fatigue", "protocol": "**Dosage:** 250-500mcg daily.", "storage": "Refrigerate."},
    "CJC-1295 (No DAC)": {"type": "Growth Hormone", "filter_cat": "Muscle & Workout", "desc": "GHRH analog for pulsatile GH.", "benefits": "- **Sleep:** Improves deep Stage 4 sleep.\n- **Aging:** Increases collagen synthesis.", "side": "• Warm flushing\n• Vivid dreams", "protocol": "**Dosage:** 100mcg nightly fasted.", "storage": "Refrigerate."},
    "GHK-Cu": {"type": "Cosmetic", "filter_cat": "Skin, Hair & Beauty", "desc": "Copper Tripeptide-1.", "benefits": "- **Skin:** 70% increase in collagen.\n- **Hair:** Increases follicle size.", "side": "• Painful sting\n• Zinc depletion", "protocol": "**Dosage:** 1mg-2mg daily.", "storage": "Refrigerate."},
    "NAD+": {"type": "Cellular", "filter_cat": "Wellness & Longevity", "desc": "Fuel for cellular engines.", "benefits": "- **Brain Fog:** Mental clarity.\n- **DNA:** Cellular repair.", "side": "• Chest pressure\n• Anxiety", "protocol": "**Dosage:** 25-50mg 2-3x weekly (Slow).", "storage": "Refrigerate."},
    "Oxytocin Acetate": {"type": "Wellness", "filter_cat": "Nootropics & Brain", "desc": "The 'Love Hormone' neurotransmitter.", "benefits": "- **Social:** Reduces social anxiety.\n- **Bonding:** Enhances emotional trust.\n- **Pain:** Shows analgesic properties.", "side": "• Nausea\n• Headache\n• Flushing", "protocol": "**Dosage:** 10-25 IU as needed.", "storage": "Refrigerate."},
    "Tirzepatide": {"type": "Metabolic", "filter_cat": "Slimming & Fat Loss", "desc": "GIP/GLP-1 Dual Agonist.", "benefits": "- **Loss:** Superior weight reduction.\n- **Noise:** Stops food obsessions.", "side": "• Anhedonia\n• Hair shedding", "protocol": "**Dosage:** 2.5mg -> 15mg weekly.", "storage": "Refrigerate."},
    # ... [Includes all other peptides from the v4.0 list]
}

def run_database():
    st.subheader("📚 Peptide Clinical Database")
    st.divider()

    cats = ["All", "Slimming & Fat Loss", "Skin, Hair & Beauty", "Muscle & Workout", "Nootropics & Brain", "Injury & Repair", "Wellness & Longevity", "Libido & Sexual Health"]
    c1, c2 = st.columns([3, 1])
    with c1: query = st.text_input("🔍 Search Database", placeholder="Search...").lower()
    with c2: cat_filter = st.selectbox("🏷️ Category", cats)

    filtered = {n: d for n, d in PEPTIDE_DB.items() if (cat_filter == "All" or d['filter_cat'] == cat_filter) and (query in n.lower() or query in d['benefits'].lower())}

    cols = st.columns(3)
    for i, (name, info) in enumerate(filtered.items()):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"### {name} <span class='db-tag'>{info['type']}</span>", unsafe_allow_html=True)
                st.markdown(f"**🌟 Benefits:**\n{info['benefits']}")
                st.markdown(f"<div class='side-effect-box'><strong>⚠️ Side Effects:</strong><br>{info['side']}</div>", unsafe_allow_html=True)
                with st.expander("📋 Protocol", expanded=True): st.markdown(info['protocol'])
                with st.expander("ℹ️ Mechanism"):
                    st.markdown(f"_{info['desc']}_")
                    st.markdown(f"**❄️ Storage:** {info['storage']}")

if __name__ == "__main__":
    run_database()
