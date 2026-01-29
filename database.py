import streamlit as st

def run_database():
    # --- DATA ---
    PEPTIDE_DB = {
        "AOD-9604": {"type": "Fat Loss", "filter_cat": "Slimming & Fat Loss", "desc": "Anti-Obesity Drug 9604.", "benefits": "- **Fat Burning:** Lipolysis.\n- **Metabolic:** No insulin issues.", "side": "Redness at site.", "protocol": "300mcg daily fasted."},
        "BPC-157": {"type": "Regenerative", "filter_cat": "Injury & Repair", "desc": "Body Protection Compound.", "benefits": "- **Tendon Healing:** Soft tissue repair.\n- **Gut:** Heals lining.", "side": "Mild nausea.", "protocol": "250-500mcg daily."},
        "Tirzepatide": {"type": "Metabolic", "filter_cat": "Slimming & Fat Loss", "desc": "GIP/GLP-1 Agonist.", "benefits": "- **Weight:** 22% loss.\n- **Satiety:** Stops food noise.", "side": "Anhedonia, Constipation.", "protocol": "2.5mg-15mg weekly."},
        "GHK-Cu": {"type": "Cosmetic", "filter_cat": "Skin, Hair & Beauty", "desc": "Copper Tripeptide-1.", "benefits": "- **Collagen:** Rejuvenates skin.\n- **Hair:** Follicle growth.", "side": "Painful sting.", "protocol": "1-2mg daily."},
        "NAD+": {"type": "Cellular", "filter_cat": "Wellness & Longevity", "desc": "Coenzyme for energy.", "benefits": "- **Brain Fog:** Mental clarity.\n- **DNA:** Cellular repair.", "side": "Chest pressure.", "protocol": "25-50mg 2x/week."},
        "PT-141": {"type": "Libido", "filter_cat": "Libido & Sexual Health", "desc": "Bremelanotide.", "benefits": "- **Arousal:** Works via nervous system.\n- **ED:** Effective for both sexes.", "side": "Nausea, flushing.", "protocol": "1.5mg-2mg as needed."},
        "Retatrutide": {"type": "Metabolic", "filter_cat": "Slimming & Fat Loss", "desc": "Triple Agonist.", "benefits": "- **Potency:** Highest fat loss agent.\n- **Liver:** Clears NAFLD.", "side": "Tachycardia.", "protocol": "2mg starting dose."},
        "TB-500": {"type": "Regenerative", "filter_cat": "Injury & Repair", "desc": "Thymosin Beta-4.", "benefits": "- **Muscle:** Heals tears.\n- **Flexibility:** Systemic repair.", "side": "Lethargy.", "protocol": "2.5mg twice weekly."},
        "Tesamorelin": {"type": "GH", "filter_cat": "Slimming & Fat Loss", "desc": "GHRH for visceral fat.", "benefits": "- **Belly Fat:** Targets organ fat.\n- **Cognition:** Memory support.", "side": "Joint stiffness.", "protocol": "1-2mg nightly."},
        "Oxytocin": {"type": "Wellness", "filter_cat": "Nootropics & Brain", "desc": "Bonding hormone.", "benefits": "- **Social:** Reduces anxiety.\n- **Bonding:** Trust/Intimacy.", "side": "Headache.", "protocol": "10-25 IU as needed."},
        "Semaglutide": {"type": "Metabolic", "filter_cat": "Slimming & Fat Loss", "desc": "GLP-1 Agonist.", "benefits": "- **Control:** Blood sugar management.\n- **Weight:** Proven weight loss.", "side": "Constipation, Nausea.", "protocol": "0.25mg titration."},
        "MOTS-c": {"type": "Metabolic", "filter_cat": "Muscle & Workout", "desc": "Mitochondrial peptide.", "benefits": "- **Mitochondria:** Exercise mimetic.\n- **Endurance:** VO2 max.", "side": "Painful injection.", "protocol": "5-10mg weekly."},
    }

    st.subheader("📚 Peptide Clinical Database")
    st.divider()

    cats = ["All", "Slimming & Fat Loss", "Skin, Hair & Beauty", "Muscle & Workout", "Nootropics & Brain", "Injury & Repair", "Wellness & Longevity", "Libido & Sexual Health"]
    c1, c2 = st.columns([3, 1])
    with c1: q = st.text_input("🔍 Search Database", placeholder="Search...").lower()
    with c2: f = st.selectbox("🏷️ Filter", cats)

    filtered = {n: d for n, d in PEPTIDE_DB.items() if (f == "All" or d['filter_cat'] == f) and (q in n.lower() or q in d['benefits'].lower())}

    rows = st.columns(3)
    for i, (name, info) in enumerate(filtered.items()):
        with rows[i % 3]:
            with st.container(border=True):
                st.markdown(f"### {name} <span class='db-tag' style='background:#4b4bff; color:white; padding:2px 8px; border-radius:10px; font-size:0.7em;'>{info['type']}</span>", unsafe_allow_html=True)
                st.markdown(f"**🌟 Benefits:**\n{info['benefits']}")
                st.markdown(f"<div style='background:#3e1818; padding:8px; border-radius:4px; margin:5px 0;'><strong>⚠️ Side Effects:</strong> {info['side']}</div>", unsafe_allow_html=True)
                with st.expander("📋 Protocol", expanded=True): st.markdown(info['protocol'])
