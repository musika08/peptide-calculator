# database.py - Full Clinical Library v4.1

FACTORS = {'mcg': 1, 'mg': 1000, 'g': 1000000, 'IU': 1}

PEPTIDE_PRESETS = {
    "AOD-9604": {
        "vial_mg": 5.0, "dose_mcg": 300.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Fat Loss", "filter_cat": "Slimming & Fat Loss",
        "desc": "Anti-Obesity Drug 9604. A modified fragment of the C-terminus of Human Growth Hormone (HGH).",
        "benefits_detailed": "- **Targeted Lipolysis:** Specifically stimulates the breakdown of fat cells (lipolysis) in stubborn areas.\n- **Metabolic Safety:** Does not induce insulin resistance or elevate IGF-1, making it safer than GH.\n- **Joint Support:** Clinical studies suggest it aids in cartilage regeneration and repair of connective tissue.\n- **Weight Management:** Effectively burns visceral fat stores without affecting blood sugar levels.\n- **Hyperlipidemic Action:** May assist in improving lipid profiles and reducing cholesterol.\n- **Non-Tumorigenic:** Does not promote the growth of existing tumors unlike full-length HGH.",
        "side_effects_detailed": "• Injection site redness\n• Mild stomach upset\n• Rare headaches\n• Mild nausea",
        "contraindications": "• Active malignancy (cancer)\n• Pregnancy or breastfeeding\n• Known hypersensitivity to GH fragments",
        "protocol_detailed": "**Dosage:** 300mcg (0.3mg)\n\n**Frequency:** Daily\n\n**Timing:** Morning (Fasted) or 1 hour before cardio\n\n**Cycle:** 3 to 6 Months",
        "storage": "Refrigerate. Stable."
    },
    "BPC-157": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Regenerative", "filter_cat": "Injury & Repair",
        "desc": "Body Protection Compound-157. A 15-amino acid chain derived from gastric juice.",
        "benefits_detailed": "- **Connective Tissue:** Drastically speeds up the healing of soft tissue injuries including tendons and ligaments.\n- **Angiogenesis:** Stimulates the formation of new blood vessels (VEGF) for faster tissue oxygenation.\n- **Gastroprotection:** Heals gastric ulcers, IBS, Crohn's, and intestinal endothelium (Leaky Gut).\n- **Anti-Inflammatory:** Systemically reduces inflammation and protects vital organ health.\n- **Neuroprotection:** Protects neurons and can help repair nerve damage in the brain and limbs.\n- **Liver Protection:** Shown to protect the liver from toxic insults and promote liver cell regeneration.",
        "side_effects_detailed": "• Mild nausea\n• Injection site irritation\n• Fatigue during the healing phase\n• Rare headaches",
        "contraindications": "• History of neovascularization-related eye disorders\n• Active cancer (due to blood vessel growth stimulation)\n• Pregnancy",
        "protocol_detailed": "**Dosage:** 250mcg - 500mcg\n\n**Frequency:** Daily or Twice Daily (AM/PM)\n\n**Timing:** SubQ near injury site or belly fat\n\n**Cycle:** 4 to 6 Weeks on, 2 Weeks off",
        "storage": "Refrigerate after mixing. Stable for ~30-45 days."
    },
    "BPC-157 + TB-500 Blend": {
        "vial_mg": 10.0, "dose_mcg": 500.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Regenerative Blend", "filter_cat": "Injury & Repair",
        "desc": "The 'Wolverine Stack'. Synergistic combination of BPC-157 and TB-500.",
        "benefits_detailed": "- **Total Body Repair:** Targets tendon/bone interface and muscle belly simultaneously.\n- **Mobility Enhancement:** Significant improvements in joint range of motion and reduction of scar tissue.\n- **Cardioprotection:** Proven efficacy in reducing myocardial scar tissue and protecting heart health.\n- **Recovery Synergy:** Combines systemic repair with localized healing for maximal efficiency.\n- **Systemic Anti-Inflammatory:** Drastically lowers systemic inflammatory markers (CRP).\n- **Wound Healing:** Accelerates closure of dermal wounds and prevents infection.",
        "side_effects_detailed": "• Temporary head rush immediately after injection\n• Lethargy/Excessive sleepiness\n• Injection site stinging\n• Mild facial flushing",
        "contraindications": "• Active malignancy (Cancer)\n• History of heart palpitations or tachycardia\n• Congestive heart failure",
        "protocol_detailed": "**Dosage:** 500mcg - 1000mcg (Total Volume)\n\n**Frequency:** Daily\n\n**Timing:** Any time of day\n\n**Cycle:** 4 to 8 Weeks (Duration of injury)",
        "storage": "Refrigerate. Use within 30 days."
    },
    "CJC-1295 (No DAC)": {
        "vial_mg": 5.0, "dose_mcg": 100.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone", "filter_cat": "Muscle & Workout",
        "desc": "Modified GRF 1-29. A GHRH analog that stimulates pulsatile Growth Hormone release.",
        "benefits_detailed": "- **Hyperplasia:** Stimulates the division of muscle cells for actual lean tissue growth.\n- **Sleep Architecture:** Dramatically improves Delta-wave (Stage 4) deep sleep for recovery.\n- **Anti-Aging:** Increases collagen synthesis, leading to improved skin thickness and hair quality.\n- **Metabolic Fire:** Enhances fat metabolism and ensures muscle recovery during calorie deficits.\n- **Bone Density:** Increases bone mineralization and prevents osteoporosis long-term.\n- **Immune Support:** Aids in the production of T-cells and general immune system resilience.",
        "side_effects_detailed": "• Facial flushing (lasts 10-20 mins)\n• Immediate head rush\n• Vivid or lucid dreams\n• Mild water retention",
        "contraindications": "• Active cancer (GH promotes cell growth)\n• History of GH-related pituitary adenoma\n• Diabetes (requires close monitoring)",
        "protocol_detailed": "**Dosage:** 100mcg (0.1mg)\n\n**Frequency:** Daily (5 days on / 2 days off)\n\n**Timing:** Immediately before bed (Fasted 2+ hours)\n\n**Cycle:** 12 Weeks +",
        "storage": "Refrigerate. Sensitive to light/heat."
    },
    "CJC-1295 + Ipamorelin Blend": {
        "vial_mg": 10.0, "dose_mcg": 200.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone Blend", "filter_cat": "Muscle & Workout",
        "desc": "The Gold Standard GH Stack. Combines CJC-1295 and Ipamorelin.",
        "benefits_detailed": "- **Synergistic Secretion:** Maximizes natural GH output by using two different metabolic pathways.\n- **Visceral Fat Mobilization:** Highly effective at targeting deep abdominal fat stores.\n- **Safety Profile:** Unlike GHRP-2 or 6, it does not trigger hunger, cortisol, or prolactin.\n- **Cellular Repair:** Enhances whole-body recovery, physical performance, and injury resistance.\n- **Recomposition:** Accelerates the ability to build muscle while losing body fat simultaneously.\n- **Nervous System:** Supports nerve regeneration and improves overall mental focus.",
        "side_effects_detailed": "• Head rush post-injection\n• Numbness or tingling in fingers (Carpal Tunnel symptoms)\n• Water weight retention\n• Temporary lethargy",
        "contraindications": "• Existing Carpal Tunnel Syndrome\n• Active malignancy\n• Severe insulin resistance",
        "protocol_detailed": "**Dosage:** 200mcg - 300mcg (Total Volume)\n\n**Frequency:** Nightly (5 days on / 2 off)\n\n**Timing:** Immediately before bed (Fasted 2+ hours)\n\n**Cycle:** 3 to 6 Months",
        "storage": "Refrigerate. Do not shake."
    },
    "Epithalon": {
        "vial_mg": 10.0, "dose_mcg": 5000.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Anti-Aging", "filter_cat": "Wellness & Longevity",
        "desc": "Synthetic tetrapeptide that increases telomerase activity.",
        "benefits_detailed": "- **Telomere Extension:** Upregulates telomerase to protect and repair DNA strands from aging.\n- **Endocrine Normalization:** Restores sensitivity of the hypothalamus and pineal gland.\n- **Circadian Reset:** Normalizes melatonin production and regulates sleep-wake cycles effectively.\n- **Anti-Tumor Action:** Has been shown in Russian trials to reduce the risk of spontaneous tumor growth.\n- **Longevity:** Potent life-extension effects by maintaining cellular integrity and DNA health.\n- **Immune Rejuvenation:** Increases the efficiency of the thymus gland for better infection resistance.",
        "side_effects_detailed": "• Daytime drowsiness\n• Very vivid dreams\n• Extremely safe profile\n• Occasional mild fatigue",
        "contraindications": "• Pregnancy (not studied)\n• Pediatric use (unless specifically indicated)",
        "protocol_detailed": "**Dosage:** 5mg - 10mg\n\n**Frequency:** Daily\n\n**Timing:** Morning or Evening\n\n**Cycle:** 10 to 20 Day Course (Repeat every 6-12 months)",
        "storage": "Refrigerate."
    },
    "GHK-Cu": {
        "vial_mg": 50.0, "dose_mcg": 2000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cosmetic/Repair", "filter_cat": "Skin, Hair & Beauty",
        "desc": "Copper Tripeptide-1. A genomic modulator that resets over 4,000 genes to a younger state.",
        "benefits_detailed": "- **Skin Rejuvenation:** Increases collagen synthesis by 70%, tightens loose skin and thickens dermis.\n- **Hair Growth:** Enlarges hair follicles, prevents thinning, and prolongs the growth phase.\n- **DNA Gene Repair:** Resets activity of DNA repair genes to a youthful, healthy state.\n- **Genomic Remodeling:** Modulates over 4,000 human genes for systemic anti-aging.\n- **Stem Cell Activation:** Promotes the proliferation of adult stem cells in the skin and organs.\n- **Wound Repair:** Accelerates healing and reduces the appearance of old scar tissue.",
        "side_effects_detailed": "• High incidence of injection site pain (burning)\n• Large red welts or bruising (post-injection)\n• Zinc depletion (requires 50mg Zinc daily)\n• Mild site itching",
        "contraindications": "• Wilson's Disease\n• Known copper toxicity or allergy\n• Severe kidney disease",
        "protocol_detailed": "**Dosage:** 1mg - 2mg\n\n**Frequency:** Daily\n\n**Timing:** Evening (rotate sites)\n\n**Cycle:** 30 Days on, 30 Days off",
        "storage": "Refrigerate. Protect from light."
    },
    "HCG": {
        "vial_mg": 5000.0, "dose_mcg": 250.0, "default_dose_unit": "IU", "default_stock_unit": "IU", "iu_conversion": 1,
        "type": "Hormonal", "filter_cat": "Libido & Sexual Health",
        "desc": "Human Chorionic Gonadotropin. Mimics LH to maintain testicular function.",
        "benefits_detailed": "- **Testicular Health:** Prevents atrophy and maintains natural function/size during TRT.\n- **Fertility Maintenance:** Crucial for maintaining spermatogenesis and reproductive health.\n- **Libido Boost:** Provides a distinct libido and mood boost separate from pure testosterone.\n- **Neurosteroid Production:** Stimulates the production of DHEA and pregnenolone in the body.\n- **HPTA Support:** Essential for bridging the gap during a restart (PCT) or cruise.\n- **Thyroid Synergy:** May assist in regulating thyroid function and metabolic rate.",
        "side_effects_detailed": "• Estrogen spikes (Elevated E2)\n• Acne breakouts\n• Water weight retention\n• Testicular desensitization (if overdosed)\n• Irritability",
        "contraindications": "• Prostate cancer\n• History of Estrogen-sensitive conditions\n• Severe polycythemia (thick blood)",
        "protocol_detailed": "**Dosage:** 250 IU - 500 IU\n\n**Frequency:** 2 to 3 times per week\n\n**Timing:** Morning\n\n**Cycle:** Continuous with TRT or as PCT",
        "storage": "Refrigerate. Fragile."
    },
    "NAD+": {
        "vial_mg": 500.0, "dose_mcg": 25.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cellular Energy", "filter_cat": "Wellness & Longevity",
        "desc": "Nicotinamide Adenine Dinucleotide. The fuel for cellular engines.",
        "benefits_detailed": "- **Cognitive Enhancement:** Rapidly clears brain fog and enhances mental sharpness and recall.\n- **Mitochondrial Restoration:** Directly fuels ATP production for extreme physical vitality.\n- **Addiction Recovery:** Proven to help restore neurotransmitter balance and reduce cravings.\n- **Sirtuin Fuel:** Essential for the function of longevity genes that maintain DNA.\n- **Cellular Detox:** Assists the body in clearing metabolic waste and cellular debris.\n- **Stress Resilience:** Improves the body's ability to recover from environmental and oxidative stress.",
        "side_effects_detailed": "• Intense chest pressure (The Flush)\n• Anxiety or panic sensation\n• Abdominal cramping and nausea\n• Dizziness or lightheadedness",
        "contraindications": "• Active cancer (GH/NAD standard precaution)\n• Severe anxiety or panic disorder\n• History of arrhythmia",
        "protocol_detailed": "**Dosage:** 25mg - 50mg\n\n**Frequency:** 2-3x / Week\n\n**Timing:** Morning\n\n**Cycle:** Ongoing\n\n**Study Note:** ⚠️ INJECT VERY SLOWLY. Rapid injection causes severe 'NAD Flush'.",
        "storage": "Refrigerate immediately. Very sensitive."
    },
    "Oxytocin Acetate": {
        "vial_mg": 2.0, "dose_mcg": 20.0, "default_dose_unit": "IU", "default_stock_unit": "mg", "iu_conversion": 600,
        "type": "Hormonal/Wellness", "filter_cat": "Nootropics & Brain",
        "desc": "The 'Love Hormone'. social interaction regulator.",
        "benefits_detailed": "- **Social Anxiety Reduction:** Significantly reduces fear and social stress in public settings.\n- **Cortisol Suppression:** Lowers systemic stress hormones and promotes relaxation.\n- **Emotional Bonding:** Enhances feelings of trust, empathy, and connection with others.\n- **Analgesic Properties:** Natural pain-killing effects for chronic pain management.\n- **Mood Regulation:** Helps regulate emotional responses and promotes general wellbeing.\n- **Sexual Wellness:** Enhances physical sensitivity and emotional intimacy.",
        "side_effects_detailed": "• Nausea (common at high doses)\n• Headache\n• Facial flushing\n• Slight dizziness\n• Rare mild palpitations",
        "contraindications": "• Pregnancy (may induce labor)\n• History of uterine issues\n• Severe electrolyte imbalance",
        "protocol_detailed": "**Dosage:** 10 IU - 25 IU (Start low)\n\n**Frequency:** As needed\n\n**Timing:** 30 minutes before social or intimate events\n\n**Cycle:** Can be used continuously or cycled",
        "storage": "Refrigerate."
    },
    "Tirzepatide": {
        "vial_mg": 30.0, "dose_mcg": 2.5, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Metabolic (GLP-1/GIP)", "filter_cat": "Slimming & Fat Loss",
        "desc": "Dual Agonist (Mounjaro). GIP + GLP-1. Superior to Semaglutide.",
        "benefits_detailed": "- **Max Weight Loss:** Average 22%+ loss in SURMOUNT clinical trials.\n- **Food Noise Eradication:** Completely eliminates obsessive and intrusive food thoughts.\n- **Nausea Resistance:** GIP component significantly reduces nausea compared to older GLP-1s.\n- **Metabolic Reset:** Restores insulin sensitivity and metabolic flexibility long-term.\n- **Blood Sugar Control:** Powerful regulation of A1C and blood glucose levels.\n- **Cardiovascular Health:** Improves lipid profiles and lowers systemic blood pressure.",
        "side_effects_detailed": "• Anhedonia (flat mood/loss of joy)\n• Cold extremities (hands/feet)\n• Severe constipation\n• Hair shedding (Telogen Effluvium)\n• Fatigue",
        "contraindications": "• History of Medullary Thyroid Carcinoma (MTC)\n• Type 1 Diabetes\n• Severe Gastroparesis\n• History of pancreatitis",
        "protocol_detailed": "**Dosage:** Start 2.5mg -> Max 15mg\n\n**Frequency:** Once Weekly\n\n**Timing:** Any time\n\n**Cycle:** Continuous",
        "storage": "Refrigerate. Do not freeze."
    }
    # (Rest of peptides continue in this detailed format)
}
