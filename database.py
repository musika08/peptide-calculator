# database.py - Full Clinical Library v4.0

FACTORS = {'mcg': 1, 'mg': 1000, 'g': 1000000, 'IU': 1}

PEPTIDE_PRESETS = {
    "AOD-9604": {
        "vial_mg": 5.0, "dose_mcg": 300.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Fat Loss", "filter_cat": "Slimming & Fat Loss",
        "desc": "Anti-Obesity Drug 9604. A modified fragment of the C-terminus of Human Growth Hormone (HGH).",
        "benefits_summary": "- Targeted fat burning (lipolysis)\n- No blood sugar spikes\n- Cartilage repair support\n- Non-hormonal (no IGF-1 impact)",
        "benefits_detailed": "- **Targeted Lipolysis:** Specifically stimulates the breakdown of fat cells (lipolysis).\n- **Metabolic Safety:** Does not induce insulin resistance or elevate IGF-1.\n- **Joint Support:** Aids in cartilage regeneration and repair.\n- **Weight Management:** Effectively burns stubborn visceral fat without the typical GH side effects.",
        "side_effects_detailed": "• Injection site redness\n• Mild stomach upset\n• Rare headaches\n• Mild nausea",
        "contraindications": "• Active malignancy\n• Pregnancy or breastfeeding\n• Known hypersensitivity to GH fragments",
        "protocol_detailed": "**Dosage:** 300mcg (0.3mg)\n\n**Frequency:** Daily\n\n**Timing:** Morning (Fasted) or 1 hour before cardio\n\n**Cycle:** 3 to 6 Months",
        "storage": "Refrigerate. Stable."
    },
    "BPC-157": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Regenerative", "filter_cat": "Injury & Repair",
        "desc": "Body Protection Compound-157. A 15-amino acid chain derived from gastric juice.",
        "benefits_summary": "- Accelerates tendon/ligament repair\n- Heals gut lining (IBS/Leaky Gut)\n- Reduces neuro-inflammation\n- Protects liver and organs",
        "benefits_detailed": "- **Connective Tissue:** Drastically speeds up the healing of soft tissue injuries (tendons, ligaments).\n- **Angiogenesis:** Stimulates the formation of new blood vessels for faster recovery.\n- **Gastroprotection:** Heals gastric ulcers and protects intestinal endothelium.\n- **Anti-Inflammatory:** Systemically reduces inflammation and protects organ health.",
        "side_effects_detailed": "• Mild nausea\n• Injection site irritation\n• Fatigue during healing\n• Rare headaches",
        "contraindications": "• Active cancer (due to angiogenesis properties)\n• Pregnancy",
        "protocol_detailed": "**Dosage:** 250mcg - 500mcg\n\n**Frequency:** Daily or Twice Daily (AM/PM)\n\n**Timing:** SubQ near injury site or belly fat\n\n**Cycle:** 4 to 6 Weeks on, 2 Weeks off",
        "storage": "Refrigerate after mixing. Stable for ~30-45 days."
    },
    "BPC-157 + TB-500 Blend": {
        "vial_mg": 10.0, "dose_mcg": 500.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Regenerative Blend", "filter_cat": "Injury & Repair",
        "desc": "The 'Wolverine Stack'. Synergistic combination of BPC-157 and TB-500.",
        "benefits_summary": "- Maximum surgical/injury recovery\n- Improves joint flexibility\n- Cardiovascular protection\n- Systemic anti-inflammatory",
        "benefits_detailed": "- **Total Repair:** Targets tendon/bone interface and muscle belly simultaneously.\n- **Mobility:** Significant improvements in joint range of motion and tissue flexibility.\n- **Cardioprotection:** Proven efficacy in reducing scar tissue and protecting heart health.\n- **Recovery Synergy:** Combines systemic repair with localized healing.",
        "side_effects_detailed": "• Temporary head rush\n• Lethargy\n• Injection site stinging\n• Mild facial flushing",
        "contraindications": "• History of heart palpitations (for TB-500 component)\n• Active malignancy",
        "protocol_detailed": "**Dosage:** 500mcg - 1000mcg (Total Volume)\n\n**Frequency:** Daily\n\n**Timing:** Any time of day\n\n**Cycle:** 4 to 8 Weeks (Duration of injury)",
        "storage": "Refrigerate. Use within 30 days."
    },
    "CJC-1295 (No DAC)": {
        "vial_mg": 5.0, "dose_mcg": 100.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone", "filter_cat": "Muscle & Workout",
        "desc": "Modified GRF 1-29. A GHRH analog that stimulates pulsatile Growth Hormone release.",
        "benefits_summary": "- Increases lean muscle mass\n- Promotes deep slow-wave sleep\n- Improves skin elasticity\n- Accelerates fat metabolism",
        "benefits_detailed": "- **Hyperplasia:** Stimulates the division of muscle cells for actual tissue growth.\n- **Sleep Architecture:** Dramatically improves Delta-wave (Stage 4) deep sleep.\n- **Anti-Aging:** Increases collagen synthesis and improves skin thickness.\n- **Metabolic Rate:** Enhances fat metabolism and muscle recovery.",
        "side_effects_detailed": "• Facial flushing\n• Head rush\n• Vivid dreams\n• Mild water retention",
        "contraindications": "• Active cancer\n• History of GH-related pituitary issues",
        "protocol_detailed": "**Dosage:** 100mcg (0.1mg)\n\n**Frequency:** Daily (5 days on / 2 days off)\n\n**Timing:** Immediately before bed (Fasted 2+ hours)\n\n**Cycle:** 12 Weeks +",
        "storage": "Refrigerate. Sensitive to light/heat."
    },
    "CJC-1295 + Ipamorelin Blend": {
        "vial_mg": 10.0, "dose_mcg": 200.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone Blend", "filter_cat": "Muscle & Workout",
        "desc": "The Gold Standard GH Stack. Combines CJC-1295 and Ipamorelin.",
        "benefits_summary": "- Max natural GH secretion\n- Significant body recomposition\n- Superior recovery & sleep\n- No cortisol/prolactin spike",
        "benefits_detailed": "- **Synergistic Power:** Maximizes GH secretion naturally by using two pathways.\n- **Visceral Fat:** Highly effective at mobilizing deep abdominal fat stores.\n- **Safety Profile:** No trigger of stress hormones (cortisol) or hunger hormones.\n- **Cellular Repair:** Enhances whole-body recovery and physical performance.",
        "side_effects_detailed": "• Head rush post-injection\n• Numbness/Tingling in hands\n• Water retention\n• Temporary lethargy",
        "contraindications": "• Carpal Tunnel Syndrome (may worsen)\n• Active malignancy",
        "protocol_detailed": "**Dosage:** 200mcg - 300mcg (Total Volume)\n\n**Frequency:** Nightly (5 days on / 2 off)\n\n**Timing:** Immediately before bed (Fasted 2+ hours)\n\n**Cycle:** 3 to 6 Months",
        "storage": "Refrigerate. Do not shake."
    },
    "Epithalon": {
        "vial_mg": 10.0, "dose_mcg": 5000.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Anti-Aging", "filter_cat": "Wellness & Longevity",
        "desc": "Synthetic tetrapeptide that increases telomerase activity.",
        "benefits_summary": "- Extends lifespan (Telomeres)\n- Resets circadian rhythm\n- Boosts melatonin naturally\n- Anti-tumor/cancer protective",
        "benefits_detailed": "- **Telomere Extension:** Upregulates telomerase to protect and repair DNA strands.\n- **Endocrine Reset:** Restores sensitivity of the hypothalamus/pineal gland.\n- **Sleep Quality:** Normalizes melatonin production and regulates circadian rhythms.\n- **Longevity:** Potent anti-aging effects by protecting cellular integrity.",
        "side_effects_detailed": "• Daytime drowsiness\n• Vivid dreams\n• Extremely safe profile\n• Mild fatigue",
        "contraindications": "• Generally none known in clinical doses\n• Pregnancy (standard caution)",
        "protocol_detailed": "**Dosage:** 5mg - 10mg\n\n**Frequency:** Daily\n\n**Timing:** Morning or Evening\n\n**Cycle:** 10 to 20 Day Course (Repeat every 6-12 months)",
        "storage": "Refrigerate."
    },
    "GHK-Cu": {
        "vial_mg": 50.0, "dose_mcg": 2000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cosmetic/Repair", "filter_cat": "Skin, Hair & Beauty",
        "desc": "Copper Tripeptide-1. A genomic modulator that resets over 4,000 genes to a younger state.",
        "benefits_summary": "- Boosts collagen & elastin\n- Tightens loose skin\n- Regrows hair (follicle size)\n- Activates DNA repair genes",
        "benefits_detailed": "- **Skin Rejuvenation:** Increases collagen synthesis by 70%, thickens the dermis.\n- **Hair Growth:** Enlarges hair follicles and prolongs the growth phase.\n- **DNA Repair:** Resets activity of DNA repair genes to a youthful state.\n- **Genomic Remodeling:** Modulates thousands of genes for systemic anti-aging.",
        "side_effects_detailed": "• Painful injection (Sting)\n• Red welts/bruising\n• Zinc depletion\n• Mild site itching",
        "contraindications": "• Wilson's Disease\n• Known copper toxicity",
        "protocol_detailed": "**Dosage:** 1mg - 2mg\n\n**Frequency:** Daily\n\n**Timing:** Evening (rotate sites)\n\n**Cycle:** 30 Days on, 30 Days off",
        "storage": "Refrigerate. Protect from light."
    },
    "Glow Blend (GHK-Cu/BPC/TB)": {
        "vial_mg": 70.0, "dose_mcg": 2500.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cosmetic/Recovery Blend", "filter_cat": "Skin, Hair & Beauty",
        "desc": "70mg Tri-Blend. BPC-157 and TB-500 are added to buffer the GHK-Cu, reducing the 'sting'.",
        "benefits_summary": "- Painless GHK-Cu injection\n- Total body skin tightening\n- Rapid injury recovery\n- Gut & Heart health",
        "benefits_detailed": "- **Painless Application:** BPC-157 effectively neutralizes the acidity of Copper.\n- **Total Rejuvenation:** Targets skin, hair, gut, and muscle health simultaneously.\n- **GH Synergy:** Increases Growth Hormone receptors for better repair capacity.\n- **Systemic Health:** Provides a balanced approach to cosmetic and physical recovery.",
        "side_effects_detailed": "• Mild redness\n• Flushing\n• Healing fatigue\n• Rare mild nausea",
        "contraindications": "• Copper sensitivity\n• Active cancer",
        "protocol_detailed": "**Dosage:** 2.5mg - 3mg (Total Volume)\n\n**Frequency:** Daily\n\n**Timing:** Evening\n\n**Cycle:** 4 to 6 Weeks",
        "storage": "Refrigerate. Protect from light."
    },
    "HCG": {
        "vial_mg": 5000.0, "dose_mcg": 250.0, "default_dose_unit": "IU", "default_stock_unit": "IU", "iu_conversion": 1,
        "type": "Hormonal", "filter_cat": "Libido & Sexual Health",
        "desc": "Human Chorionic Gonadotropin. Mimics LH to maintain testicular function.",
        "benefits_summary": "- Prevents testicular shrinkage\n- Maintains fertility/sperm\n- Boosts libido & mood\n- TRT adjunct support",
        "benefits_detailed": "- **Testicular Health:** Prevents atrophy and maintains natural function during TRT.\n- **Fertility:** Crucial for maintaining spermatogenesis and reproductive health.\n- **Libido:** Provides a distinct libido and mood boost separate from testosterone.\n- **HPTA Support:** Helps bridge the gap between exogenous and endogenous hormones.",
        "side_effects_detailed": "• Estrogen spikes\n• Acne breakouts\n• Water retention\n• Testicular desensitization if overdosed",
        "contraindications": "• Prostate cancer\n• History of Estrogen-sensitive conditions",
        "protocol_detailed": "**Dosage:** 250 IU - 500 IU\n\n**Frequency:** 2 to 3 times per week\n\n**Timing:** Morning\n\n**Cycle:** Continuous with TRT or as PCT",
        "storage": "Refrigerate. Fragile."
    },
    "Ipamorelin": {
        "vial_mg": 5.0, "dose_mcg": 100.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone", "filter_cat": "Muscle & Workout",
        "desc": "Selective GH Secretagogue. The mildest and safest GHRP.",
        "benefits_summary": "- Clean GH release (No hunger)\n- Fat loss & muscle sparing\n- Improved sleep quality\n- Anti-aging support",
        "benefits_detailed": "- **Pure Signal:** Stimulates steady GH pulse without the ghrelin-induced hunger spikes.\n- **Catabolic Protection:** Preserves lean muscle mass even during caloric restriction.\n- **Sleep:** Increases deep slow-wave and REM sleep for better recovery.\n- **Safety:** Does not impact cortisol, prolactin, or insulin levels.",
        "side_effects_detailed": "• Mild water retention\n• Rare dizziness\n• Very low side effect profile\n• Rare mild headache",
        "contraindications": "• Active malignancy\n• Pituitary tumors",
        "protocol_detailed": "**Dosage:** 100mcg - 300mcg\n\n**Frequency:** Nightly\n\n**Timing:** Before Bed (Fasted)\n\n**Cycle:** 8 to 12 Weeks",
        "storage": "Refrigerate."
    },
    "Kisspeptin": {
        "vial_mg": 10.0, "dose_mcg": 100.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Hormonal", "filter_cat": "Libido & Sexual Health",
        "desc": "A neuromodulator that stimulates the hypothalamus to release GnRH.",
        "benefits_summary": "- Restarts HPTA axis safely\n- Boosts fertility (LH/FSH)\n- Increases libido\n- No testicular desensitization",
        "benefits_detailed": "- **HPTA Restart:** The safest way to restart natural testosterone production post-cycle.\n- **Fertility:** Strongly stimulates FSH for improved sperm quality and count.\n- **Arousal:** Directly influences the brain's sexual arousal and emotional pathways.\n- **Natural Signal:** Acts high up in the endocrine chain for a physiological response.",
        "side_effects_detailed": "• Facial flushing\n• Injection site redness\n• Mild headache\n• Temporary warmth",
        "contraindications": "• History of sex-hormone driven cancers\n• Pituitary disorders",
        "protocol_detailed": "**Dosage:** 100mcg - 200mcg\n\n**Frequency:** Daily\n\n**Timing:** Any time\n\n**Cycle:** 4 Weeks (PCT)",
        "storage": "Refrigerate."
    },
    "Klow Blend (GHK-Cu/BPC/TB/KPV)": {
        "vial_mg": 80.0, "dose_mcg": 3000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Ultimate Repair/Cosmetic Blend", "filter_cat": "Skin, Hair & Beauty",
        "desc": "The 80mg Master Stack. Adds KPV to the GHK/BPC/TB trio.",
        "benefits_summary": "- Clears Acne, Psoriasis, Eczema\n- Heals Gut (IBD/Colitis)\n- Systemic anti-inflammatory\n- Total tissue repair",
        "benefits_detailed": "- **Dermatology:** KPV component treats chronic acne, psoriasis, and severe eczema.\n- **Gut Health:** The most powerful known peptide stack for IBD and Ulcerative Colitis.\n- **Mast Cells:** KPV stabilizes mast cells to reduce systemic histamine levels.\n- **Holistic Recovery:** Integrates gut-brain-skin repair for comprehensive wellness.",
        "side_effects_detailed": "• Red welts\n• Healing fatigue\n• Temporary flushing\n• Occasional mild nausea",
        "contraindications": "• Wilson's Disease\n• Active cancer",
        "protocol_detailed": "**Dosage:** 3mg (Total Volume)\n\n**Frequency:** Daily\n\n**Timing:** Evening\n\n**Cycle:** 4 to 8 Weeks",
        "storage": "Refrigerate. Protect from light."
    },
    "Melanotan II": {
        "vial_mg": 10.0, "dose_mcg": 500.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cosmetic", "filter_cat": "Skin, Hair & Beauty",
        "desc": "Alpha-MSH analog. Stimulates melanin production and sexual arousal.",
        "benefits_summary": "- Deep, rapid tan\n- Extreme libido boost\n- Appetite suppression\n- UV protection",
        "benefits_detailed": "- **Photoprotection:** Creates a deep tan that acts as a natural barrier against UV damage.\n- **Libido:** Acts as a potent aphrodisiac for both men and women.\n- **Metabolic:** Helps suppress appetite and may assist in body fat reduction.\n- **Skin Health:** Reduces the amount of sun exposure needed to achieve a tan.",
        "side_effects_detailed": "• Severe Nausea\n• Facial Flushing\n• Spontaneous erections\n• Darkening of freckles/moles",
        "contraindications": "• History of melanoma\n• Dysplastic Nevus Syndrome (many moles)",
        "protocol_detailed": "**Dosage:** 100mcg - 500mcg\n\n**Frequency:** As needed (Loading phase: Daily)\n\n**Timing:** 30 mins before UV exposure\n\n**Cycle:** Until desired color, then maintenance",
        "storage": "Refrigerate."
    },
    "MOTS-c": {
        "vial_mg": 10.0, "dose_mcg": 5000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Metabolic/Mitochondrial", "filter_cat": "Muscle & Workout",
        "desc": "Mitochondrial-Derived Peptide. Known as an 'exercise mimetic'.",
        "benefits_summary": "- Increases VO2 Max/Endurance\n- Prevents weight gain\n- Improves bone metabolism\n- Cellular energy boost",
        "benefits_detailed": "- **Endurance:** Dramatically increases cellular capacity for glucose and oxygen utilization.\n- **Metabolic:** Prevents diet-induced insulin resistance and weight gain.\n- **Biogenesis:** Promotes the creation of new mitochondria for cellular energy.\n- **Recovery:** Enhances physical performance and skeletal muscle integrity.",
        "side_effects_detailed": "• Painful injection\n• Insomnia\n• Hyperactivity\n• Rare mild tachycardia",
        "contraindications": "• Severe hypertension\n• Chronic heart failure",
        "protocol_detailed": "**Dosage:** 5mg - 10mg\n\n**Frequency:** Once Weekly\n\n**Timing:** Morning (Pre-workout preferred)\n\n**Cycle:** 4 to 8 Weeks",
        "storage": "Refrigerate."
    },
    "NAD+": {
        "vial_mg": 500.0, "dose_mcg": 25000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cellular Energy", "filter_cat": "Wellness & Longevity",
        "desc": "Nicotinamide Adenine Dinucleotide. The fuel for cellular engines.",
        "benefits_summary": "- Clears brain fog\n- Restores cellular energy\n- Repairs DNA damage\n- Anti-aging/Longevity",
        "benefits_detailed": "- **Cognition:** Rapidly clears brain fog and enhances mental sharpness and memory.\n- **Mitochondria:** Restores efficient ATP production for physical vitality.\n- **Addiction:** Proven to help restore neurotransmitter balance and reduce cravings.\n- **DNA Repair:** Essential for Sirtuin function and longevity-related DNA maintenance.",
        "side_effects_detailed": "• Intense chest pressure\n• Anxiety/Panic feeling\n• Nausea/Cramps\n• Dizziness if injected too quickly",
        "contraindications": "• Active cancer (standard anti-aging precaution)\n• Pregnancy",
        "protocol_detailed": "**Dosage:** 25mg - 50mg\n\n**Frequency:** 2-3x / Week\n\n**Timing:** Morning\n\n**Cycle:** Ongoing\n\n**Study Note:** ⚠️ INJECT VERY SLOWLY. Rapid injection causes severe 'NAD Flush'.",
        "storage": "Refrigerate immediately. Very sensitive."
    },
    "Oxytocin Acetate": {
        "vial_mg": 2.0, "dose_mcg": 20.0, "default_dose_unit": "IU", "default_stock_unit": "mg", "iu_conversion": 600,
        "type": "Hormonal/Wellness", "filter_cat": "Nootropics & Brain",
        "desc": "The 'Love Hormone'. Acts as a neurotransmitter regulating social interaction and bonding.",
        "benefits_summary": "- Reduces social anxiety\n- Lowers cortisol (Stress)\n- Enhances emotional bonding\n- Modulates pain perception",
        "benefits_detailed": "- **Psychological:** Significantly reduces social anxiety and lowers systemic stress levels.\n- **Pain Modulation:** Shows analgesic properties that help manage chronic pain.\n- **Intimacy:** Enhances trust, empathy, and emotional connection in social settings.\n- **Mood Support:** Helps regulate emotional responses and promotes general wellbeing.",
        "side_effects_detailed": "• Nausea\n• Headache\n• Flushing\n• Slight dizziness",
        "contraindications": "• History of uterine issues (if female)\n• Severe electrolyte imbalance",
        "protocol_detailed": "**Dosage:** 10 IU - 25 IU (Start low)\n\n**Frequency:** As needed (or Daily for mood support)\n\n**Timing:** 30 minutes before social/intimate events\n\n**Cycle:** Can be used continuously or cycled",
        "storage": "Refrigerate."
    },
    "PT-141": {
        "vial_mg": 10.0, "dose_mcg": 1000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Libido", "filter_cat": "Libido & Sexual Health",
        "desc": "Bremelanotide. Works on the nervous system to treat hypoactive sexual desire.",
        "benefits_summary": "- Treats ED & Low Libido\n- Works when Viagra fails\n- Increases physical arousal\n- For Men & Women",
        "benefits_detailed": "- **Mechanism:** Targets the brain's melanocortin receptors, not the vascular system.\n- **Efficacy:** FDA approved for low libido; works independently of sexual stimulation.\n- **Response:** Increases physical arousal and genuine sexual desire.\n- **Versatility:** Effective for both men and women with no vascular side effects.",
        "side_effects_detailed": "• Nausea (Common)\n• Flushing/Warmth\n• Headache\n• Elevated blood pressure",
        "contraindications": "• Uncontrolled hypertension\n• Severe cardiovascular disease",
        "protocol_detailed": "**Dosage:** 1.5mg - 2mg\n\n**Frequency:** As needed\n\n**Timing:** 2 to 4 hours BEFORE activity\n\n**Cycle:** Max 8 doses per month",
        "storage": "Refrigerate."
    },
    "Retatrutide": {
        "vial_mg": 10.0, "dose_mcg": 2000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Metabolic (GLP-1/GIP/Glucagon)", "filter_cat": "Slimming & Fat Loss",
        "desc": "The 'Triple G' Agonist. The most potent weight loss agent currently in trials.",
        "benefits_summary": "- Extreme weight loss (24%+)\n- Burns liver fat (NAFLD)\n- Resets insulin sensitivity\n- Increases metabolism",
        "benefits_detailed": "- **Efficacy:** Most potent weight loss agent with over 24% loss in clinical trials.\n- **Liver Health:** Resolves NAFLD by directly mobilizing and burning hepatic fat.\n- **Metabolic Fire:** Glucagon component increases caloric burn even at rest.\n- **Insulin Repair:** Resets sensitivity and improves blood glucose control.",
        "side_effects_detailed": "• High Heart Rate\n• Skin sensitivity\n• Nausea\n• Constipation",
        "contraindications": "• History of pancreatitis\n• Thyroid cancer (MTC)\n• Severe gastroparesis",
        "protocol_detailed": "**Dosage:** Start 2mg -> Titrate to Max 12mg\n\n**Frequency:** Once Weekly\n\n**Timing:** Any time\n\n**Cycle:** Continuous",
        "storage": "Refrigerate. Do not freeze."
    },
    "Semaglutide": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Metabolic (GLP-1)", "filter_cat": "Slimming & Fat Loss",
        "desc": "GLP-1 Agonist. The standard for medical weight loss.",
        "benefits_summary": "- Significant weight loss (15%)\n- Controls blood sugar\n- Cardioprotective\n- Reduces addiction cravings",
        "benefits_detailed": "- **Satiety:** Slows gastric emptying to keep you full longer and reduce intake.\n- **Heart Health:** Proven to reduce major adverse cardiac events by 20%.\n- **Addiction:** Helps suppress cravings for alcohol, sugar, and nicotine.\n- **Glycemic Control:** Effective for managing and reversing Type 2 Diabetes symptoms.",
        "side_effects_detailed": "• Nausea/Vomiting\n• Severe Constipation\n• Fatigue\n• Muscle loss",
        "contraindications": "• History of pancreatitis\n• Multiple Endocrine Neoplasia type 2 (MEN 2)\n• Retinopathy",
        "protocol_detailed": "**Dosage:** Start 0.25mg -> Max 2.4mg\n\n**Frequency:** Once Weekly\n\n**Timing:** Any time\n\n**Cycle:** Continuous",
        "storage": "Refrigerate. Protect from light."
    },
    "TB-500": {
        "vial_mg": 5.0, "dose_mcg": 2500.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Regenerative", "filter_cat": "Injury & Repair",
        "desc": "Synthetic Thymosin Beta-4. The 'Muscle Repair' peptide.",
        "benefits_summary": "- Heals muscle tears\n- Improves flexibility\n- Reduces scar tissue\n- Cardiac repair",
        "benefits_detailed": "- **Muscle Repair:** The primary choice for healing torn muscles and severe strains.\n- **Flexibility:** Enhances joint range of motion by reducing internal inflammation.\n- **Cardiac:** Helps repair damaged heart tissue and reduce scar tissue formation.\n- **Systemic Healing:** Promotes cell migration and tissue regeneration body-wide.",
        "side_effects_detailed": "• Temporary head rush\n• Lethargy\n• Rare flu-like symptoms\n• Mild site itching",
        "contraindications": "• Active cancer\n• History of cardiac palpitations",
        "protocol_detailed": "**Dosage:** 2.5mg (2500mcg)\n\n**Frequency:** 2x Per Week (e.g., Mon/Thu)\n\n**Timing:** Any time\n\n**Cycle:** 4 to 6 Weeks",
        "storage": "Refrigerate."
    },
    "Tesamorelin": {
        "vial_mg": 2.0, "dose_mcg": 1000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone", "filter_cat": "Slimming & Fat Loss",
        "desc": "FDA Approved GHRH for visceral fat reduction.",
        "benefits_summary": "- Burns belly fat (Visceral)\n- Increases muscle tone\n- Nootropic effects\n- Lowers triglycerides",
        "benefits_detailed": "- **Visceral Fat:** Specifically targets stubborn adipose tissue around internal organs.\n- **Cognition:** Enhances executive function and memory in aging adults.\n- **Lipids:** Drastically lowers systemic triglycerides for better heart health.\n- **Muscle Definition:** Improves tone and recomposition without major water gain.",
        "side_effects_detailed": "• Injection site redness\n• Joint stiffness\n• Carpal Tunnel\n• Water retention",
        "contraindications": "• Active cancer\n• Diabetes with severe retinopathy",
        "protocol_detailed": "**Dosage:** 1mg - 2mg\n\n**Frequency:** Daily\n\n**Timing:** Before Bed (Fasted)\n\n**Cycle:** 8 to 12 Weeks",
        "storage": "Refrigerate. Use within 20-30 days."
    },
    "Tesamorelin + Ipamorelin Blend": {
        "vial_mg": 12.0, "dose_mcg": 350.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone/Fat Loss Blend", "filter_cat": "Slimming & Fat Loss",
        "desc": "The 'Shred Stack'. Targets visceral fat + systemic GH elevation.",
        "benefits_summary": "- Max fat loss (Visceral)\n- Muscle definition\n- Deep sleep\n- Systemic anti-aging",
        "benefits_detailed": "- **Recomposition:** The ultimate combination for burning fat while building muscle.\n- **Metabolic Fire:** Amplifies the fat-burning effects of overnight fasting.\n- **Sleep:** Ipamorelin component ensures deep sleep for better hormone regulation.\n- **Synergy:** High-volume GH release with focused abdominal fat mobilization.",
        "side_effects_detailed": "• Joint pain\n• Numbness\n• Flushing\n• Water retention",
        "contraindications": "• Carpal Tunnel Syndrome\n• Active malignancy",
        "protocol_detailed": "**Dosage:** 350mcg - 500mcg (Total Volume)\n\n**Frequency:** Daily (5 days on / 2 off)\n\n**Timing:** Before Bed (Fasted)\n\n**Cycle:** 8 to 12 Weeks",
        "storage": "Refrigerate."
    },
    "Tirzepatide": {
        "vial_mg": 30.0, "dose_mcg": 2.5, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Metabolic (GLP-1/GIP)", "filter_cat": "Slimming & Fat Loss",
        "desc": "Dual Agonist (Mounjaro). GIP + GLP-1. Superior to Semaglutide.",
        "benefits_summary": "- Massive weight loss (22%)\n- Eliminates 'Food Noise'\n- Less nausea than Semaglutide\n- Metabolic repair",
        "benefits_detailed": "- **Weight Loss:** Over 22% average loss in SURMOUNT clinical trials.\n- **Food Noise:** Completely eliminates obsessive and intrusive food thoughts.\n- **Tolerability:** GIP component significantly reduces nausea compared to Semaglutide.\n- **Repair:** Restores metabolic flexibility and insulin sensitivity for long-term health.",
        "side_effects_detailed": "• Anhedonia\n• Constipation\n• Cold hands/feet\n• Hair shedding",
        "contraindications": "• History of Medullary Thyroid Carcinoma\n• Type 1 Diabetes\n• History of severe depression/anhedonia",
        "protocol_detailed": "**Dosage:** Start 2.5mg -> Max 15mg\n\n**Frequency:** Once Weekly\n\n**Timing:** Any time\n\n**Cycle:** Continuous",
        "storage": "Refrigerate. Do not freeze."
    },
}
