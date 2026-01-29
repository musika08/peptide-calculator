# database.py

PEPTIDE_DB = {
    # --- METABOLIC & WEIGHT LOSS ---
    "Tirzepatide": {
        "vial_mg": 30.0, "dose_val": 2.5, "unit": "mg", "freq": "Once Weekly", "timing": "Any time", "food": "With or without",
        "type": "GLP-1/GIP Agonist", "filter_cat": "Slimming & Fat Loss", "iu_conversion": None,
        "desc": "Dual agonist (Mounjaro/Zepbound) for superior weight loss and insulin control.",
        "benefits": "- 22%+ average weight loss\n- Eliminates 'food noise'\n- Resets insulin sensitivity\n- Significant visceral fat reduction",
        "side": "• Nausea/Vomiting\n• Constipation\n• Fatigue\n• Sulfur burps",
        "contra": "History of Medullary Thyroid Carcinoma (MTC) or MEN 2 syndrome.",
        "protocol": "**Cycle:** Continuous or until goal.\n**Note:** Titrate every 4 weeks by 2.5mg increments.",
        "storage": "Refrigerate. Do not freeze."
    },
    "Retatrutide": {
        "vial_mg": 10.0, "dose_val": 2.0, "unit": "mg", "freq": "Once Weekly", "timing": "Any time", "food": "With or without",
        "type": "Triple G Agonist", "filter_cat": "Slimming & Fat Loss", "iu_conversion": None,
        "desc": "The 'Triple G' (GLP-1/GIP/Glucagon) currently in Phase 3 trials.",
        "benefits": "- Highest weight loss efficacy recorded (24%+)\n- Drastic reduction in liver fat\n- Increased resting energy expenditure",
        "side": "• Tachycardia (High Heart Rate)\n• Skin sensitivity\n• Intense GI upset",
        "contra": "Pre-existing heart conditions or tachycardia.",
        "protocol": "**Cycle:** Ongoing.\n**Note:** Monitor pulse regularly due to glucagon component.",
        "storage": "Refrigerate."
    },
    "Semaglutide": {
        "vial_mg": 5.0, "dose_val": 0.25, "unit": "mg", "freq": "Once Weekly", "timing": "Any time", "food": "With or without",
        "type": "GLP-1 Agonist", "filter_cat": "Slimming & Fat Loss", "iu_conversion": None,
        "desc": "Standard GLP-1 agonist (Ozempic/Wegovy) for weight management.",
        "benefits": "- 15% average weight loss\n- Improved cardiovascular markers\n- Blood glucose stabilization",
        "side": "• Nausea\n• Fatigue\n• Gastrointestinal reflux",
        "contra": "History of pancreatitis or thyroid tumors.",
        "protocol": "**Cycle:** Ongoing.\n**Note:** Titrate from 0.25mg to 2.4mg max over several months.",
        "storage": "Refrigerate."
    },
    "AOD-9604": {
        "vial_mg": 5.0, "dose_val": 300.0, "unit": "mcg", "freq": "Daily", "timing": "Morning", "food": "Without (Empty stomach)",
        "type": "Fat Loss", "filter_cat": "Slimming & Fat Loss", "iu_conversion": None,
        "desc": "Anti-Obesity Drug 9604. A modified fragment of the HGH molecule.",
        "benefits": "- Targeted lipolysis (fat breakdown)\n- No impact on blood sugar\n- Bone and cartilage repair properties",
        "side": "• Injection site redness\n• Rare headache\n• Mild stomach upset",
        "contra": "No known major contraindications; general safety profile is high.",
        "protocol": "**Cycle:** 3-6 Months.\n**Note:** Must remain fasted for 30-60 mins post-injection.",
        "storage": "Refrigerate."
    },

    # --- REPAIR & REGENERATIVE ---
    "BPC-157": {
        "vial_mg": 5.0, "dose_val": 250.0, "unit": "mcg", "freq": "1-2x Daily", "timing": "Morning/Night", "food": "With or without",
        "type": "Repair Peptide", "filter_cat": "Injury & Repair", "iu_conversion": None,
        "desc": "Body Protection Compound. Derived from human gastric juice.",
        "benefits": "- Heals tendons/ligaments/bone\n- Seals 'Leaky Gut' and IBD\n- Angiogenesis (blood vessel growth)",
        "side": "• Rare nausea\n• Dizziness\n• Site irritation",
        "contra": "Active malignancies (due to angiogenesis).",
        "protocol": "**Cycle:** 4-6 Weeks on, 2 Weeks off.\n**Note:** Can be injected near injury (local) or belly fat (systemic).",
        "storage": "Refrigerate. Sensitive to shaking."
    },
    "TB-500": {
        "vial_mg": 5.0, "dose_val": 2.5, "unit": "mg", "freq": "2x Weekly", "timing": "Any time", "food": "With or without",
        "type": "Regenerative", "filter_cat": "Injury & Repair", "iu_conversion": None,
        "desc": "Thymosin Beta-4. Promotes cell migration and tissue repair.",
        "benefits": "- Systemic tissue healing\n- Reduced inflammation/scar tissue\n- Improves range of motion",
        "side": "• Temporary lethargy\n• Flu-like symptoms (rare)\n• Injection site redness",
        "contra": "Active cancer (growth factor mechanism).",
        "protocol": "**Cycle:** 4-6 Weeks.\n**Note:** Often stacked with BPC-157.",
        "storage": "Refrigerate."
    },
    "Wolverine Stack (BPC/TB)": {
        "vial_mg": 10.0, "dose_val": 500.0, "unit": "mcg", "freq": "Daily", "timing": "Morning", "food": "With or without",
        "type": "Repair Blend", "filter_cat": "Injury & Repair", "iu_conversion": None,
        "desc": "A 1:1 blend of BPC-157 and TB-500 for maximum recovery.",
        "benefits": "- Synergistic healing of soft tissue\n- Rapid post-surgical recovery\n- Joint health & flexibility",
        "side": "• Head rush (TB-500)\n• Fatigue",
        "contra": "Active malignancies.",
        "protocol": "**Cycle:** 4-8 Weeks.\n**Note:** Dose reflects total volume of blend.",
        "storage": "Refrigerate."
    },

    # --- GROWTH HORMONE & NOOTROPICS ---
    "Ipamorelin": {
        "vial_mg": 5.0, "dose_val": 250.0, "unit": "mcg", "freq": "Daily", "timing": "Nightly", "food": "Without (Empty stomach)",
        "type": "GH Secretagogue", "filter_cat": "Muscle & Workout", "iu_conversion": None,
        "desc": "Selective Growth Hormone Releasing Peptide (GHRP).",
        "benefits": "- Lean muscle preservation\n- Improved sleep quality\n- No hunger spikes (unlike GHRP-6)",
        "side": "• Warm flushing\n• Water retention\n• Tingling in hands",
        "contra": "Tumors of the pituitary gland.",
        "protocol": "**Cycle:** 8-12 Weeks.\n**Note:** Fast 2+ hours before bed for best results.",
        "storage": "Refrigerate."
    },
    "CJC-1295 (No DAC)": {
        "vial_mg": 5.0, "dose_val": 100.0, "unit": "mcg", "freq": "Daily", "timing": "Nightly", "food": "Without (Empty stomach)",
        "type": "GHRH Analog", "filter_cat": "Muscle & Workout", "iu_conversion": None,
        "desc": "Stimulates pulsatile GH release.",
        "benefits": "- Enhanced fat metabolism\n- Skin rejuvenation\n- Stage 4 deep sleep improvement",
        "side": "• Facial flushing\n• Vivid dreams\n• Head rush",
        "contra": "Pituitary adenomas.",
        "protocol": "**Cycle:** 3+ Months.\n**Note:** Best paired with Ipamorelin.",
        "storage": "Refrigerate."
    },
    "Sermorelin": {
        "vial_mg": 5.0, "dose_val": 300.0, "unit": "mcg", "freq": "Daily (5 on/2 off)", "timing": "Nightly", "food": "Without (Empty stomach)",
        "type": "GHRH Analog", "filter_cat": "Muscle & Workout", "iu_conversion": None,
        "desc": "A GHRH analog used to increase natural growth hormone output.",
        "benefits": "- Faster workout recovery\n- Improved hair and skin quality\n- Bone density support",
        "side": "• Flushing\n• Headache\n• Hyperactivity",
        "contra": "Untreated hypothyroidism.",
        "protocol": "**Cycle:** 3-6 Months.\n**Note:** Take immediately before bed.",
        "storage": "Refrigerate."
    },

    # --- LONGEVITY & WELLNESS ---
    "Epithalon": {
        "vial_mg": 10.0, "dose_val": 5.0, "unit": "mg", "freq": "Daily", "timing": "Morning or Night", "food": "With or without",
        "type": "Anti-Aging", "filter_cat": "Wellness & Longevity", "iu_conversion": None,
        "desc": "Pineal gland tetrapeptide for telomere lengthening.",
        "benefits": "- Telomerase activation\n- Circadian rhythm reset\n- Increases Melatonin levels",
        "side": "• Vivid dreams\n• Drowsiness",
        "contra": "No specific contraindications reported.",
        "protocol": "**Cycle:** 10-20 Day course, repeated every 6 months.",
        "storage": "Refrigerate."
    },
    "NAD+": {
        "vial_mg": 500.0, "dose_val": 50.0, "unit": "mg", "freq": "2-3x Weekly", "timing": "Morning", "food": "With or without",
        "type": "Cellular Energy", "filter_cat": "Wellness & Longevity", "iu_conversion": None,
        "desc": "Coenzyme for mitochondrial health and DNA repair.",
        "benefits": "- Clears brain fog\n- Massive energy boost\n- Reduces cravings (addiction support)",
        "side": "• Intense chest pressure (The Flush)\n• Nausea/Cramping\n• Anxiety sensation",
        "contra": "History of specific malignancies (consult MD).",
        "protocol": "**Cycle:** Ongoing.\n**Note:** ⚠️ INJECT SLOWLY to avoid the 'NAD Flush'.",
        "storage": "Refrigerate immediately."
    },
    "GHK-Cu": {
        "vial_mg": 50.0, "dose_val": 2.0, "unit": "mg", "freq": "Daily", "timing": "Evening", "food": "With or without",
        "type": "Cosmetic/Repair", "filter_cat": "Skin, Hair & Beauty", "iu_conversion": None,
        "desc": "Copper Tripeptide-1 for skin and hair rejuvenation.",
        "benefits": "- Increases collagen synthesis by 70%\n- Thickens dermis/tightens skin\n- Hair follicle enlargement",
        "side": "• Significant injection stinging\n• Red welts\n• Zinc depletion",
        "contra": "Known copper toxicity (Wilson's Disease).",
        "protocol": "**Cycle:** 30 Days on/off.\n**Note:** Supplement 50mg Zinc to balance copper intake.",
        "storage": "Refrigerate. Protect from light."
    },

    # --- HORMONAL & SEXUAL HEALTH ---
    "HCG": {
        "vial_mg": 5000.0, "dose_val": 250.0, "unit": "IU", "freq": "2-3x Weekly", "timing": "Morning", "food": "With or without",
        "type": "Hormonal", "filter_cat": "Libido & Sexual Health", "iu_conversion": 1,
        "desc": "Mimics LH to keep testes active during TRT.",
        "benefits": "- Prevents testicular shrinkage\n- Maintains fertility\n- Boosts libido and mood",
        "side": "• High Estrogen (E2)\n• Acne\n• Water retention",
        "contra": "Androgen-sensitive tumors.",
        "protocol": "**Cycle:** Continuous with TRT.\n**Note:** Essential for anyone on TRT wishing to remain fertile.",
        "storage": "Refrigerate after mixing."
    },
    "PT-141 (Bremelanotide)": {
        "vial_mg": 10.0, "dose_val": 1.75, "unit": "mg", "freq": "As needed", "timing": "2-4 hrs pre-activity", "food": "With or without",
        "type": "Libido", "filter_cat": "Libido & Sexual Health", "iu_conversion": None,
        "desc": "Works via the CNS to increase sexual desire.",
        "benefits": "- Treats ED and HSDD\n- Increases arousal for Men & Women\n- Works where Viagra fails",
        "side": "• Intense nausea\n• Flushing\n• High blood pressure",
        "contra": "Uncontrolled hypertension.",
        "protocol": "**Cycle:** Max 8 doses per month.\n**Note:** Use anti-nausea meds prior to injection.",
        "storage": "Refrigerate."
    },
    "Oxytocin": {
        "vial_mg": 2.0, "dose_val": 20.0, "unit": "IU", "freq": "As needed", "timing": "Any time", "food": "With or without",
        "type": "Hormonal", "filter_cat": "Libido & Sexual Health", "iu_conversion": 600,
        "desc": "The 'Love Hormone' for bonding and social trust.",
        "benefits": "- Reduces social anxiety\n- Lowers cortisol levels\n- Enhances intimacy",
        "side": "• Nausea\n• Headache\n• Dizziness",
        "contra": "No specific major contraindications.",
        "protocol": "**Cycle:** As needed.\n**Note:** Can be taken as nasal spray or injection.",
        "storage": "Refrigerate."
    }
}
