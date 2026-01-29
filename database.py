# database.py - Full Clinical Master Library v4.1

FACTORS = {'mcg': 1, 'mg': 1000, 'g': 1000000, 'IU': 1}

PEPTIDE_PRESETS = {
    "AOD-9604": {
        "vial_mg": 5.0, "dose_mcg": 300.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Fat Loss", "filter_cat": "Slimming & Fat Loss",
        "desc": "Anti-Obesity Drug 9604. A modified fragment of the Human Growth Hormone C-terminus.",
        "benefits_detailed": """
• **Lipolytic Activity:** Triggers fat release from obese fat cells specifically.
• **Anti-Lipogenic:** Prevents the transformation of non-fatty foods into body fat.
• **Metabolic Safety:** Does not affect blood sugar or insulin sensitivity.
• **Joint Health:** Clinical studies show potential for cartilage and bone repair.
• **Non-Hormonal:** Unlike HGH, it does not cause bone growth or organ enlargement.""",
        "side_effects_detailed": "• Mild injection site redness\n• Occasional headaches\n• Rare stomach upset\n• Temporary site itching",
        "contraindications": "• History of active malignancy\n• Known sensitivity to HGH fragments\n• Pregnancy or breastfeeding",
        "protocol_detailed": "**Dosage:** 300mcg - 500mcg\n**Frequency:** Daily (Fasted AM)\n**Cycle:** 3 to 6 Months",
        "storage": "Refrigerate after mixing. Use within 45 days."
    },
    "BPC-157": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Regenerative", "filter_cat": "Injury & Repair",
        "desc": "Body Protection Compound-157. Derived from gastric juices.",
        "benefits_detailed": """
• **Tissue Repair:** Accelerates healing of tendons, ligaments, and muscle tears.
• **Gut Restoration:** Heals Leaky Gut, IBD, and gastric ulcers.
• **Angiogenesis:** Improves blood flow to damaged sites for faster recovery.
• **Neurological Support:** Reduces neuro-inflammation and protects brain health.
• **Systemic Healing:** Powerful anti-inflammatory for joints and bone health.""",
        "side_effects_detailed": "• Rare reports of lethargy\n• Mild nausea\n• Injection site irritation\n• Temporary fatigue",
        "contraindications": "• Active cancer (due to blood vessel growth stimulation)\n• Known hypersensitivity",
        "protocol_detailed": "**Dosage:** 250mcg - 500mcg\n**Frequency:** Twice Daily (AM/PM)\n**Cycle:** 4 to 8 Weeks",
        "storage": "Refrigerate. Stable for ~30 days post-mixing."
    },
    "BPC-157 + TB-500 Blend": {
        "vial_mg": 10.0, "dose_mcg": 500.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Regenerative Blend", "filter_cat": "Injury & Repair",
        "desc": "The 'Wolverine Stack'. Synergistic combination of BPC-157 and TB-500.",
        "benefits_detailed": """
• **Total Systemic Repair:** Combines localized healing (BPC) with systemic tissue migration (TB).
• **Acute Injury Recovery:** Faster recovery from surgeries or severe muscle tears.
• **Reduced Scar Tissue:** Prevents the buildup of restrictive scar tissue in muscles.
• **Cardioprotection:** Promotes blood vessel growth and heart tissue health.
• **Anti-Inflammatory:** Synergistic reduction of joint and tendon inflammation.""",
        "side_effects_detailed": "• Temporary head rush\n• Lethargy during healing\n• Injection site stinging\n• Mild facial flushing",
        "contraindications": "• Active malignancy\n• History of heart palpitations",
        "protocol_detailed": "**Dosage:** 500mcg - 1000mcg\n**Frequency:** Daily\n**Cycle:** 4 to 8 Weeks",
        "storage": "Refrigerate. Use within 30 days."
    },
    "CJC-1295 (No DAC)": {
        "vial_mg": 5.0, "dose_mcg": 100.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone", "filter_cat": "Muscle & Workout",
        "desc": "Modified GRF 1-29. A GHRH analog that stimulates pulsatile GH release.",
        "benefits_detailed": """
• **Muscle Hyperplasia:** Stimulates the creation of new muscle cells.
• **Sleep Architecture:** Increases Delta-wave (Stage 4) deep sleep.
• **Anti-Aging:** Enhances collagen production for skin and hair health.
• **Fat Loss:** Increases metabolic rate and visceral fat mobilization.
• **Injury Recovery:** Speeds up the repair of bone and muscle tissue.""",
        "side_effects_detailed": "• Facial flushing\n• Head rush\n• Vivid dreams\n• Mild water retention",
        "contraindications": "• Active cancer\n• Pituitary disorders",
        "protocol_detailed": "**Dosage:** 100mcg\n**Frequency:** Daily (5 on / 2 off)\n**Cycle:** 12 Weeks +",
        "storage": "Refrigerate. Sensitive to light/heat."
    },
    "CJC-1295 + Ipamorelin Blend": {
        "vial_mg": 10.0, "dose_mcg": 200.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone Blend", "filter_cat": "Muscle & Workout",
        "desc": "The Gold Standard GH Stack. Combines CJC-1295 and Ipamorelin.",
        "benefits_detailed": """
• **GH Synergy:** Maximizes natural Growth Hormone pulses safely.
• **Body Recomposition:** Burns fat while simultaneously building lean mass.
• **Deep Recovery:** Superior physical recovery and improved sleep depth.
• **Safety Profile:** Does not trigger hunger (ghrelin) or cortisol spikes.
• **Longevity:** Supports cellular repair and youthful skin elasticity.""",
        "side_effects_detailed": "• Numbness in hands\n• Water retention\n• Flushing\n• Lethargy",
        "contraindications": "• Carpal Tunnel Syndrome\n• Active malignancy",
        "protocol_detailed": "**Dosage:** 200mcg - 300mcg\n**Frequency:** Nightly (Fasted)\n**Cycle:** 3 to 6 Months",
        "storage": "Refrigerate. Do not shake."
    },
    "Epithalon": {
        "vial_mg": 10.0, "dose_mcg": 5000.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Anti-Aging", "filter_cat": "Wellness & Longevity",
        "desc": "Synthetic tetrapeptide that increases telomerase activity.",
        "benefits_detailed": """
• **Telomere Protection:** Protects and repairs DNA to extend cellular life.
• **Circadian Rhythm:** Resets the pineal gland for natural sleep-wake cycles.
• **Melatonin Boost:** Enhances natural melatonin production.
• **Cancer Protection:** Clinical history of anti-tumor properties.
• **Life Extension:** Potential for increasing overall lifespan and vitality.""",
        "side_effects_detailed": "• Daytime drowsiness\n• Vivid dreams\n• Rare fatigue",
        "contraindications": "• Pregnancy\n• History of cancer (standard precaution)",
        "protocol_detailed": "**Dosage:** 5mg - 10mg\n**Frequency:** Daily\n**Cycle:** 10-20 Days",
        "storage": "Refrigerate. High stability."
    },
    "GHK-Cu": {
        "vial_mg": 50.0, "dose_mcg": 2000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cosmetic/Repair", "filter_cat": "Skin, Hair & Beauty",
        "desc": "Copper Tripeptide-1. Genomic modulator.",
        "benefits_detailed": """
• **Collagen Synthesis:** Increases collagen by 70% for skin tightening.
• **Hair Follicle Repair:** Reverses hair thinning and follicle miniaturization.
• **Gene Reset:** Resets 4,000+ genes to a younger state.
• **DNA Repair:** Enhances cellular repair and wound healing.
• **Skin Thickness:** Increases dermis thickness and reduces wrinkles.""",
        "side_effects_detailed": "• Painful injection\n• Red welts\n• Zinc depletion\n• Bruising",
        "contraindications": "• Wilson's Disease\n• Copper toxicity",
        "protocol_detailed": "**Dosage:** 1mg - 2mg\n**Frequency:** Daily (Evening)\n**Cycle:** 30 Days on/off",
        "storage": "Refrigerate. Protect from light."
    },
    "Glow Blend (GHK-Cu/BPC/TB)": {
        "vial_mg": 70.0, "dose_mcg": 2500.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cosmetic/Recovery Blend", "filter_cat": "Skin, Hair & Beauty",
        "desc": "70mg Tri-Blend. Buffered GHK-Cu.",
        "benefits_detailed": """
• **Painless Skin Repair:** BPC-157 buffers the GHK-Cu for a pain-free experience.
• **Total Rejuvenation:** Tightens skin, heals gut, and repairs joints.
• **Hair & Scalp Health:** Promotes follicle size and scalp vascularization.
• **Wolverine Healing:** Systemic recovery for skin and connective tissues.
• **Anti-Aging Synergy:** Multi-pathway approach to genomic age reversal.""",
        "side_effects_detailed": "• Mild site redness\n• Flushing\n• Fatigue\n• Rare nausea",
        "contraindications": "• Copper sensitivity\n• Active cancer",
        "protocol_detailed": "**Dosage:** 2.5mg - 3mg\n**Frequency:** Daily\n**Cycle:** 4 to 6 Weeks",
        "storage": "Refrigerate. Protect from light."
    },
    "HCG": {
        "vial_mg": 5000.0, "dose_mcg": 250.0, "default_dose_unit": "IU", "default_stock_unit": "IU", "iu_conversion": 1,
        "type": "Hormonal", "filter_cat": "Libido & Sexual Health",
        "desc": "Human Chorionic Gonadotropin. Mimics LH.",
        "benefits_detailed": """
• **Gonadal Function:** Prevents testicular atrophy during TRT or cycles.
• **Fertility Maintenance:** Essential for sustaining sperm production (spermatogenesis).
• **Libido Boost:** Provides a distinct increase in sexual desire and well-being.
• **Hormonal Balance:** Helps maintain natural hormone pathways.
• **Post-Cycle Recovery:** Aids in restarting the natural HPTA axis.""",
        "side_effects_detailed": "• Increased Estradiol (E2)\n• Bloating\n• Acne\n• Gynecomastia risk",
        "contraindications": "• Prostate cancer\n• History of blood clots",
        "protocol_detailed": "**Dosage:** 250 IU - 500 IU\n**Frequency:** 2-3x per week\n**Cycle:** Continuous with TRT",
        "storage": "Refrigerate. Extremely fragile."
    },
    "Ipamorelin": {
        "vial_mg": 5.0, "dose_mcg": 100.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone", "filter_cat": "Muscle & Workout",
        "desc": "Selective GH Secretagogue. Safe and mild.",
        "benefits_detailed": """
• **Selective GH Pulse:** Increases GH without hunger or cortisol spikes.
• **Body Recomposition:** Helps keep muscle while cutting body fat.
• **Sleep Improvement:** Increases REM and deep slow-wave sleep stages.
• **Anti-Aging:** Improves skin tone and bone density.
• **Safe Long-Term:** Low impact on blood glucose or stress hormones.""",
        "side_effects_detailed": "• Mild water weight\n• Dizziness\n• Rare headache",
        "contraindications": "• Pituitary tumors\n• Active malignancy",
        "protocol_detailed": "**Dosage:** 100mcg - 300mcg\n**Frequency:** Nightly\n**Cycle:** 8 to 12 Weeks",
        "storage": "Refrigerate."
    },
    "Kisspeptin": {
        "vial_mg": 10.0, "dose_mcg": 100.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Hormonal", "filter_cat": "Libido & Sexual Health",
        "desc": "Hypothalamic GnRH stimulator.",
        "benefits_detailed": """
• **HPTA Restart:** One of the safest methods to restart natural testosterone.
• **Fertility stimulation:** Strongly increases LH and FSH levels.
• **Sexual Desire:** Directly influences the brain's arousal centers.
• **Natural Pathway:** Acts higher up in the endocrine chain for a physiological reset.
• **Non-Suppressive:** Does not lead to testicular desensitization.""",
        "side_effects_detailed": "• Facial flushing\n• Site redness\n• Mild headache",
        "contraindications": "• History of sex-hormone driven cancers",
        "protocol_detailed": "**Dosage:** 100mcg - 200mcg\n**Frequency:** Daily\n**Cycle:** 4 Weeks (PCT)",
        "storage": "Refrigerate."
    },
    "Klow Blend (GHK-Cu/BPC/TB/KPV)": {
        "vial_mg": 80.0, "dose_mcg": 3000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Ultimate Repair Blend", "filter_cat": "Skin, Hair & Beauty",
        "desc": "The 80mg Master Stack. Adds KPV for dermatology.",
        "benefits_detailed": """
• **Dermatology Breakthrough:** Treats acne, psoriasis, and eczema via KPV.
• **Advanced Gut Health:** Strongest blend for IBD and Ulcerative Colitis.
• **Mast Cell Stabilization:** Reduces systemic histamine and allergic responses.
• **Genomic Skin Repair:** Deep skin tightening and DNA repair synergy.
• **Systemic Detox:** Powerful anti-inflammatory for the whole body.""",
        "side_effects_detailed": "• Red welts\n• Detox fatigue\n• Flushing\n• Rare nausea",
        "contraindications": "• Wilson's Disease\n• Active malignancy",
        "protocol_detailed": "**Dosage:** 3mg\n**Frequency:** Daily\n**Cycle:** 4 to 8 Weeks",
        "storage": "Refrigerate. Protect from light."
    },
    "Melanotan II": {
        "vial_mg": 10.0, "dose_mcg": 500.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cosmetic", "filter_cat": "Skin, Hair & Beauty",
        "desc": "Alpha-MSH analog for tanning.",
        "benefits_detailed": """
• **Rapid Tanning:** Deep tan achieved with minimal UV exposure.
• **Potent Libido:** Drastic increase in sexual desire and arousal.
• **UV Defense:** Melanin provides a natural barrier against skin damage.
• **Appetite Suppression:** Helps reduce cravings during tanning cycles.
• **Erectile Health:** Can treat ED independently of the vascular system.""",
        "side_effects_detailed": "• Severe Nausea\n• Flushing\n• Spontaneous erections\n• Mole darkening",
        "contraindications": "• History of melanoma\n• Dysplastic Nevus Syndrome",
        "protocol_detailed": "**Dosage:** 100mcg - 500mcg\n**Frequency:** As needed\n**Cycle:** Until tan goal met",
        "storage": "Refrigerate."
    },
    "MOTS-c": {
        "vial_mg": 10.0, "dose_mcg": 5000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Metabolic", "filter_cat": "Muscle & Workout",
        "desc": "Mitochondrial-Derived Peptide.",
        "benefits_detailed": """
• **Exercise Mimetic:** Mimics the benefits of endurance exercise.
• **VO2 Max Boost:** Increases oxygen utilization and physical endurance.
• **Metabolic Fire:** Prevents diet-induced obesity and weight gain.
• **Mitochondrial Biogenesis:** Promotes the creation of new cellular engines.
• **Insulin Sensitivity:** Resets blood sugar handling in skeletal muscle.""",
        "side_effects_detailed": "• Painful injection\n• Insomnia\n• Hyperactivity\n• Tachycardia",
        "contraindications": "• Severe hypertension",
        "protocol_detailed": "**Dosage:** 5mg - 10mg\n**Frequency:** Once Weekly\n**Cycle:** 4 to 8 Weeks",
        "storage": "Refrigerate."
    },
    "NAD+": {
        "vial_mg": 500.0, "dose_mcg": 25000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cellular Energy", "filter_cat": "Wellness & Longevity",
        "desc": "Cellular fuel (NAD+).",
        "benefits_detailed": """
• **Brain Clarity:** Rapidly eliminates brain fog and cognitive fatigue.
• **ATP Production:** Fuels the mitochondria for systemic physical energy.
• **DNA Repair:** Essential for repairing cellular DNA damage.
• **Addiction Recovery:** Balances neurotransmitters and reduces cravings.
• **Longevity Activation:** Direct fuel for Sirtuins (the 'aging' genes).""",
        "side_effects_detailed": "• Intense chest pressure\n• Panic feeling\n• Nausea\n• Dizziness",
        "contraindications": "• Active cancer\n• Pregnancy",
        "protocol_detailed": "**Dosage:** 25mg - 50mg\n**Frequency:** 2-3x per week\n**Note:** Inject VERY slowly.",
        "storage": "Refrigerate immediately."
    },
    "Oxytocin Acetate": {
        "vial_mg": 2.0, "dose_mcg": 20.0, "default_dose_unit": "IU", "default_stock_unit": "mg", "iu_conversion": 600,
        "type": "Hormonal/Wellness", "filter_cat": "Nootropics & Brain",
        "desc": "The 'Love Hormone' neurotransmitter.",
        "benefits_detailed": """
• **Social Ease:** Significantly reduces fear and social anxiety.
• **Stress Management:** Lowers systemic cortisol and heart rate.
• **Deep Intimacy:** Enhances emotional trust and bonding.
• **Pain Management:** Natural analgesic and pain modulator.
• **Emotional Regulation:** Stabilizes mood during stressful events.""",
        "side_effects_detailed": "• Nausea\n• Headache\n• Flushing\n• Dizziness",
        "contraindications": "• Pregnancy (standard precaution)\n• Severe heart disease",
        "protocol_detailed": "**Dosage:** 10 IU - 25 IU\n**Frequency:** As needed\n**Water:** 3.0 mL default",
        "storage": "Refrigerate."
    },
    "PT-141": {
        "vial_mg": 10.0, "dose_mcg": 1000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Libido", "filter_cat": "Libido & Sexual Health",
        "desc": "Bremelanotide. Nervous system arousal.",
        "benefits_detailed": """
• **Neurological Arousal:** Works on the brain, not the vascular system.
• **Libido Rescue:** Effective when Viagra/Cialis fail to work.
• **Sexual Desire:** Increases genuine physical arousal and desire.
• **Versatility:** Effective for both male ED and female HSDD.
• **Duration:** Benefits often last up to 24-72 hours post-injection.""",
        "side_effects_detailed": "• Nausea (Common)\n• Flushing\n• Headache\n• High blood pressure",
        "contraindications": "• Uncontrolled hypertension",
        "protocol_detailed": "**Dosage:** 1.5mg - 2mg\n**Frequency:** As needed\n**Timing:** 2-4 hours before activity",
        "storage": "Refrigerate."
    },
    "Retatrutide": {
        "vial_mg": 10.0, "dose_mcg": 2000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Metabolic", "filter_cat": "Slimming & Fat Loss",
        "desc": "The 'Triple G' Agonist (GLP/GIP/Glucagon).",
        "benefits_detailed": """
• **Unrivaled Weight Loss:** 24% average body weight loss in trials.
• **Liver Rescue:** Directly clears fat from the liver (NAFLD).
• **Metabolic Overdrive:** Glucagon component burns calories at rest.
• **Insulin Sensitivity:** Drastically improves blood sugar handling.
• **Fat Mobilization:** Aggressively targets stubborn visceral fat.""",
        "side_effects_detailed": "• High Heart Rate\n• Skin sensitivity\n• Nausea\n• Constipation",
        "contraindications": "• History of pancreatitis\n• Thyroid cancer (MTC)",
        "protocol_detailed": "**Dosage:** 2mg -> 12mg\n**Frequency:** Weekly\n**Cycle:** Continuous",
        "storage": "Refrigerate. Do not freeze."
    },
    "Semaglutide": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Metabolic", "filter_cat": "Slimming & Fat Loss",
        "desc": "GLP-1 Agonist (Ozempic/Wegovy).",
        "benefits_detailed": """
• **Proven Fat Loss:** 15% average weight loss in clinical use.
• **Fullness Sensation:** Slows stomach emptying to kill hunger.
• **Cardiac Protection:** Reduces major heart event risk by 20%.
• **Blood Sugar:** Reverses pre-diabetes and manages T2D.
• **Craving Control:** Reduces desire for alcohol and junk food.""",
        "side_effects_detailed": "• Nausea\n• Vomiting\n• Constipation\n• Fatigue\n• Muscle loss",
        "contraindications": "• MTC History\n• Pancreatitis history",
        "protocol_detailed": "**Dosage:** 0.25mg -> 2.4mg\n**Frequency:** Weekly\n**Cycle:** Continuous",
        "storage": "Refrigerate. Protect from light."
    },
    "TB-500": {
        "vial_mg": 5.0, "dose_mcg": 2500.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Regenerative", "filter_cat": "Injury & Repair",
        "desc": "Thymosin Beta-4. Muscle repair.",
        "benefits_detailed": """
• **Muscle Repair:** The gold standard for healing torn muscle fibers.
• **Flexibility:** Softens scar tissue to increase joint range of motion.
• **Systemic Anti-Inflammatory:** Reduces inflammation body-wide.
• **Heart Recovery:** Promotes repair of damaged cardiac tissue.
• **Tissue Migration:** Recruits cells to travel to damaged sites for repair.""",
        "side_effects_detailed": "• Head rush\n• Lethargy\n• Rare flu symptoms\n• Site itching",
        "contraindications": "• Active cancer\n• History of palpitations",
        "protocol_detailed": "**Dosage:** 2.5mg\n**Frequency:** 2x per week\n**Cycle:** 4 to 6 Weeks",
        "storage": "Refrigerate."
    },
    "Tesamorelin": {
        "vial_mg": 2.0, "dose_mcg": 1000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone", "filter_cat": "Slimming & Fat Loss",
        "desc": "Visceral fat burner (FDA Approved).",
        "benefits_detailed": """
• **Visceral Fat Focus:** Specifically melts fat around internal organs.
• **Muscle Tone:** Hardens muscle definition and increases tone.
• **Brain Health:** Enhances memory and executive function in trials.
• **Lipid Health:** Significantly lowers systemic triglycerides.
• **GH elevation:** Increases natural GH without increasing prolactin.""",
        "side_effects_detailed": "• Site redness\n• Joint stiffness\n• Carpal Tunnel\n• Water retention",
        "contraindications": "• Active cancer\n• Severe retinopathy",
        "protocol_detailed": "**Dosage:** 1mg - 2mg\n**Frequency:** Nightly\n**Cycle:** 8 to 12 Weeks",
        "storage": "Refrigerate. Use within 30 days."
    },
    "Tesamorelin + Ipamorelin Blend": {
        "vial_mg": 12.0, "dose_mcg": 350.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Fat Loss Stack", "filter_cat": "Slimming & Fat Loss",
        "desc": "The 'Shred Stack'. Visceral fat focus.",
        "benefits_detailed": """
• **Max Shred:** Combines visceral fat burn with systemic GH pulses.
• **Muscle Definition:** Improves tone while burning stubborn abdominal fat.
• **Fast recovery:** Enhances muscle repair while in a calorie deficit.
• **Deep sleep:** Ensures recovery pulses occur during Stage 4 sleep.
• **Synergistic Recomp:** The ideal stack for leaning out safely.""",
        "side_effects_detailed": "• Joint pain\n• Numbness\n• Flushing\n• Water retention",
        "contraindications": "• Carpal Tunnel\n• Active malignancy",
        "protocol_detailed": "**Dosage:** 350mcg - 500mcg\n**Frequency:** 5 on / 2 off\n**Cycle:** 8 to 12 Weeks",
        "storage": "Refrigerate."
    },
    "Tirzepatide": {
        "vial_mg": 30.0, "dose_mcg": 2.5, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Metabolic", "filter_cat": "Slimming & Fat Loss",
        "desc": "GIP/GLP-1 Dual Agonist.",
        "benefits_detailed": """
• **World Class Weight Loss:** Proven 22%+ average body weight reduction.
• **Mental Silence:** Eradicates the 'food noise' and food obsession.
• **Metabolic Health:** Resets insulin response and glucose handling.
• **Less Nausea:** GIP component makes it more tolerable than Semaglutide.
• **Systemic Health:** Lowers heart disease risk markers and liver fat.""",
        "side_effects_detailed": "• Anhedonia\n• Constipation\n• Cold hands/feet\n• Hair shedding",
        "contraindications": "• MTC History\n• Type 1 Diabetes\n• Severe depression history",
        "protocol_detailed": "**Dosage:** 2.5mg -> 15mg\n**Frequency:** Weekly\n**Cycle:** Continuous",
        "storage": "Refrigerate. Do not freeze."
    }
}
