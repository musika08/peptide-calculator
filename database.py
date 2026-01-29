# database.py

FACTORS = {'mcg': 1, 'mg': 1000, 'g': 1000000, 'IU': 1}

PEPTIDE_PRESETS = {
    "AOD-9604": {
        "vial_mg": 5.0, "dose_mcg": 300.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Fat Loss", "filter_cat": "Slimming & Fat Loss",
        "desc": "Anti-Obesity Drug 9604. A modified fragment of the C-terminus of Human Growth Hormone (HGH).",
        "benefits_summary": "- Targeted fat burning (lipolysis)\n- No blood sugar spikes\n- Cartilage repair support",
        "side_effects_summary": "- Injection site redness\n- Mild stomach upset",
        "protocol_summary": "300mcg daily, morning fasted.",
        "benefits_detailed": "- **Targeted Lipolysis:** Specifically stimulates fat cell breakdown.\n- **Metabolic Safety:** Does not induce insulin resistance.\n- **Joint Support:** Aids in cartilage regeneration.",
        "protocol_detailed": "**Dosage:** 300mcg\n**Frequency:** Daily\n**Timing:** Morning (Fasted)",
        "side_effects_detailed": "• Extremely well tolerated\n• Minor redness",
        "storage": "Refrigerate. Stable."
    },
    "BPC-157": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Regenerative", "filter_cat": "Injury & Repair",
        "desc": "Body Protection Compound-157. Derived from gastric juice.",
        "benefits_summary": "- Accelerates tendon/ligament repair\n- Heals gut lining",
        "side_effects_summary": "- Mild nausea\n- Irritation at site",
        "protocol_summary": "250-500mcg daily.",
        "benefits_detailed": "- **Connective Tissue:** Drastically speeds up healing of soft tissue.\n- **Angiogenesis:** Formation of new blood vessels.\n- **Gastroprotection:** Heals gastric ulcers.",
        "protocol_detailed": "**Dosage:** 250mcg - 500mcg\n**Frequency:** Daily\n**Timing:** SubQ near injury",
        "side_effects_detailed": "• Generally extremely safe\n• Rare reports of fatigue",
        "storage": "Refrigerate. Stable for ~30-45 days."
    },
    "Tirzepatide": {
        "vial_mg": 30.0, "dose_mcg": 2.5, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Metabolic (GLP-1/GIP)", "filter_cat": "Slimming & Fat Loss",
        "desc": "Dual Agonist (Mounjaro). GIP + GLP-1.",
        "benefits_summary": "- Massive weight loss (22%)\n- Eliminates 'Food Noise'",
        "side_effects_summary": "- Constipation\n- Nausea",
        "protocol_summary": "2.5mg weekly, titrate up.",
        "benefits_detailed": "- **Weight Loss:** 20%+ average loss in trials.\n- **Food Noise:** Eliminates obsessive thoughts about food.\n- **Metabolic Repair:** Improves insulin sensitivity.",
        "protocol_detailed": "**Dosage:** Start 2.5mg\n**Frequency:** Once Weekly\n**Cycle:** Continuous",
        "side_effects_detailed": "• Anhedonia (flat mood)\n• Cold extremities\n• Constipation",
        "storage": "Refrigerate. Do not freeze."
    }
    # (Additional peptides can be added here following the same structure)
}

def get_peptide_data():
    return PEPTIDE_PRESETS, FACTORS
