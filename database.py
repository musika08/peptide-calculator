# database.py

FACTORS = {'mcg': 1, 'mg': 1000, 'g': 1000000, 'IU': 1}

PEPTIDE_PRESETS = {
    "AOD-9604": {
        "vial_mg": 5.0, "dose_mcg": 300.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Fat Loss", "filter_cat": "Slimming & Fat Loss",
        "desc": "Anti-Obesity Drug 9604. A modified fragment of the C-terminus of Human Growth Hormone (HGH).",
        "benefits_summary": "- Targeted fat burning (lipolysis)\n- No blood sugar spikes\n- Cartilage repair support\n- Non-hormonal (no IGF-1 impact)",
        "side_effects_summary": "- Injection site redness\n- Mild stomach upset (rare)\n- Headache (rare)",
        "protocol_summary": "300mcg daily, morning fasted.",
        "benefits_detailed": "- **Targeted Lipolysis:** Stimulates the breakdown of fat cells.\n- **Metabolic Safety:** Does not induce insulin resistance.\n- **Joint Support:** Aids in cartilage regeneration.",
        "protocol_detailed": "**Dosage:** 300mcg\n**Frequency:** Daily\n**Timing:** Morning (Fasted)\n**Cycle:** 3 to 6 Months",
        "side_effects_detailed": "• Extremely well tolerated\n• Minor injection site reactions\n• Mild headache",
        "storage": "Refrigerate. Stable."
    },
    "BPC-157": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Regenerative", "filter_cat": "Injury & Repair",
        "desc": "Body Protection Compound-157. Derived from gastric juice.",
        "benefits_summary": "- Accelerates tendon/ligament repair\n- Heals gut lining\n- Reduces neuro-inflammation",
        "side_effects_summary": "- Mild nausea\n- Injection site irritation",
        "protocol_summary": "250-500mcg daily.",
        "benefits_detailed": "- **Connective Tissue:** Speeds up soft tissue healing.\n- **Angiogenesis:** Stimulates new blood vessels.\n- **Gastroprotection:** Heals gastric ulcers.",
        "protocol_detailed": "**Dosage:** 250mcg - 500mcg\n**Frequency:** Daily\n**Timing:** SubQ near injury site\n**Cycle:** 4 to 6 Weeks",
        "side_effects_detailed": "• Generally very safe\n• Rare reports of fatigue",
        "storage": "Refrigerate. Stable for ~30-45 days."
    },
    "CJC-1295 + Ipamorelin Blend": {
        "vial_mg": 10.0, "dose_mcg": 200.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone Blend", "filter_cat": "Muscle & Workout",
        "desc": "The Gold Standard GH Stack. Combines CJC-1295 and Ipamorelin.",
        "benefits_summary": "- Max natural GH secretion\n- Superior recovery & sleep\n- No cortisol/prolactin spike",
        "side_effects_summary": "- Head rush/Flushing\n- Water retention",
        "protocol_summary": "200-300mcg total nightly, fasted.",
        "benefits_detailed": "- **Synergistic Power:** Maximizes GH secretion naturally.\n- **Visceral Fat:** Effective at mobilizing deep abdominal fat.\n- **Safety:** No trigger of stress hormones.",
        "protocol_detailed": "**Dosage:** 200mcg - 300mcg\n**Frequency:** Nightly (5 on / 2 off)\n**Timing:** Before bed (Fasted 2+ hours)",
        "side_effects_detailed": "• Head rush/Flushing\n• Numbness in hands\n• Initial water weight",
        "storage": "Refrigerate. Do not shake."
    },
    "GHK-Cu": {
        "vial_mg": 50.0, "dose_mcg": 2.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cosmetic/Repair", "filter_cat": "Skin, Hair & Beauty",
        "desc": "Copper Tripeptide-1. Genomic modulator for tissue repair.",
        "benefits_summary": "- Boosts collagen & elastin\n- Tightens loose skin\n- Regrows hair",
        "side_effects_summary": "- Painful injection (Sting)\n- Red welts\n- Zinc depletion",
        "protocol_summary": "1-2mg daily. Evening.",
        "benefits_detailed": "- **Skin:** Increases collagen synthesis by 70%.\n- **Hair:** Enlarges follicles and prolongs growth.\n- **DNA:** Resets activity of DNA repair genes.",
        "protocol_detailed": "**Dosage:** 1mg - 2mg\n**Frequency:** Daily\n**Timing:** Evening\n**Cycle:** 30 Days on / 30 Days off",
        "side_effects_detailed": "• Injection site burning\n• Large red welts\n• Requires Zinc supplementation (50mg)",
        "storage": "Refrigerate. Protect from light."
    },
    "NAD+": {
        "vial_mg": 500.0, "dose_mcg": 25.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cellular Energy", "filter_cat": "Wellness & Longevity",
        "desc": "Nicotinamide Adenine Dinucleotide. Fuel for cellular engines.",
        "benefits_summary": "- Clears brain fog\n- Repairs DNA damage\n- Anti-aging/Longevity",
        "side_effects_summary": "- Chest pressure (The Flush)\n- Nausea/Cramps",
        "protocol_summary": "25-50mg 2-3x per week. SLOW INJECTION.",
        "benefits_detailed": "- **Cognition:** Enhances mental sharpness.\n- **Mitochondria:** Restores efficient ATP production.\n- **Addiction:** Helps restore neurotransmitter balance.",
        "protocol_detailed": "**Dosage:** 25mg - 50mg\n**Frequency:** 2-3x / Week\n**Note:** Inject VERY slowly to avoid the NAD flush.",
        "side_effects_detailed": "• Intense chest pressure\n• Abdominal cramping\n• Anxiety sensation (Passes in 10 mins)",
        "storage": "Refrigerate immediately."
    },
    "Tirzepatide": {
        "vial_mg": 30.0, "dose_mcg": 2.5, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Metabolic (GLP-1/GIP)", "filter_cat": "Slimming & Fat Loss",
        "desc": "Dual Agonist (Mounjaro). GIP + GLP-1.",
        "benefits_summary": "- Massive weight loss (22%)\n- Eliminates 'Food Noise'\n- Metabolic repair",
        "side_effects_summary": "- Anhedonia (No joy)\n- Constipation\n- Cold hands/feet",
        "protocol_summary": "2.5mg weekly, titrate up.",
        "benefits_detailed": "- **Weight Loss:** 20%+ average loss.\n- **Food Noise:** Eliminates obsessive food thoughts.\n- **Tolerability:** GIP component reduces nausea severity.",
        "protocol_detailed": "**Dosage:** Start 2.5mg -> Max 15mg\n**Frequency:** Once Weekly\n**Cycle:** Continuous",
        "side_effects_detailed": "• Anhedonia\n• Cold extremities\n• Constipation\n• Hair shedding",
        "storage": "Refrigerate. Do not freeze."
    }
}

def get_peptide_data():
    return PEPTIDE_PRESETS, FACTORS
