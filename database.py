# database.py - Peptide Knowledge Base v4.0 (Full Clinical Version)

FACTORS = {'mcg': 1, 'mg': 1000, 'g': 1000000, 'IU': 1}

PEPTIDE_PRESETS = {
    "AOD-9604": {
        "vial_mg": 5.0, "dose_mcg": 300.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Fat Loss", "filter_cat": "Slimming & Fat Loss",
        "desc": "Anti-Obesity Drug 9604. A modified fragment of HGH (Human Growth Hormone).",
        "benefits_summary": "- Targeted fat burning (lipolysis)\n- No blood sugar spikes\n- Cartilage repair support",
        "benefits_detailed": """
- **Targeted Lipolysis:** Stimulates the breakdown of fat cells without affecting blood sugar or insulin.
- **Joint Support:** Aids in cartilage regeneration and systemic repair of connective tissues.
- **Non-Hormonal:** Does not elevate IGF-1 levels, making it safer for long-term use.
""",
        "side_effects_detailed": """
• **Injection Site:** Mild redness or itching at the site.
• **Headache:** Rare reports of mild tension headaches.
• **Gastro:** Occasional stomach upset if not taken on an empty stomach.
""",
        "protocol_detailed": """
**Dosage:** 300mcg (0.3mg) daily.
**Timing:** Morning (Fasted) or 1 hour before cardio for maximum lipolysis.
**Cycle:** 3 to 6 Months.
""",
        "storage": "Refrigerate. Stable after reconstitution for 30-45 days."
    },
    "BPC-157": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Regenerative", "filter_cat": "Injury & Repair",
        "desc": "Body Protection Compound-157. Derived from gastric juice.",
        "benefits_summary": "- Accelerates tendon/ligament repair\n- Heals gut lining (IBS)\n- Reduces neuro-inflammation",
        "benefits_detailed": """
- **Connective Tissue:** Drastically speeds up the healing of soft tissue, tendons, and bone-to-tendon interfaces.
- **Angiogenesis:** Stimulates the formation of new blood vessels to bypass damaged tissue.
- **Gastroprotection:** Proven to heal gastric ulcers and intestinal endothelium (Leaky Gut).
""",
        "side_effects_detailed": """
• **Lethargy:** Some users report mild fatigue during the initial healing phase.
• **Nausea:** Occasional stomach discomfort if taken at high doses.
• **Interaction:** Generally considered extremely safe with no known major contraindications.
""",
        "protocol_detailed": """
**Dosage:** 250mcg - 500mcg daily.
**Frequency:** Once or twice daily (AM/PM).
**Cycle:** 4 to 8 weeks, followed by a 2-week break.
""",
        "storage": "Refrigerate. Sensitive to heat. Stable for ~30 days after mixing."
    },
    "BPC-157 + TB-500 Blend": {
        "vial_mg": 10.0, "dose_mcg": 500.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Regenerative Blend", "filter_cat": "Injury & Repair",
        "desc": "The 'Wolverine Stack'. Synergistic combination for total body repair.",
        "benefits_summary": "- Maximum surgical/injury recovery\n- Improves joint flexibility\n- Systemic anti-inflammatory",
        "benefits_detailed": """
- **Synergy:** BPC-157 handles the localized repair, while TB-500 provides systemic healing and inflammation reduction.
- **Mobility:** Significant improvements in joint range of motion and reduction in scar tissue.
- **Cardio:** Some evidence of heart tissue repair and protection.
""",
        "side_effects_detailed": """
• **Head Rush:** TB-500 can cause a temporary rush or flushing immediately after injection.
• **Lethargy:** Body repairs faster, which can cause increased sleep requirements.
• **Stinging:** The blend may cause mild stinging depending on the concentration.
""",
        "protocol_detailed": """
**Dosage:** 500mcg - 1000mcg (total fluid volume).
**Frequency:** Daily for acute injuries, or 3x per week for maintenance.
**Cycle:** 4 to 6 weeks.
""",
        "storage": "Refrigerate. Use within 30 days for maximum potency."
    },
    "CJC-1295 (No DAC)": {
        "vial_mg": 5.0, "dose_mcg": 100.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone", "filter_cat": "Muscle & Workout",
        "desc": "Modified GRF 1-29. A GHRH analog that stimulates pulsatile GH release.",
        "benefits_summary": "- Increases lean muscle mass\n- Promotes deep slow-wave sleep\n- Improves skin elasticity",
        "benefits_detailed": """
- **Sleep Quality:** Dramatically improves Delta-wave (Stage 4) deep sleep, leading to faster recovery.
- **Hyperplasia:** Stimulates the division of muscle cells for long-term growth.
- **Anti-Aging:** Increases natural collagen synthesis and skin thickness.
""",
        "side_effects_detailed": """
• **Flushing:** Warmth/redness in the face lasting 10-20 mins (vasodilation).
• **Vivid Dreams:** Increased REM sleep can lead to very intense dreaming.
• **Head Rush:** Occasional lightheadedness immediately after injection.
""",
        "protocol_detailed": """
**Dosage:** 100mcg (0.1mg).
**Frequency:** Daily (5 days on / 2 days off).
**Timing:** Immediately before bed (Fasted 2+ hours).
""",
        "storage": "Refrigerate. Very sensitive to light and heat."
    },
    "CJC-1295 + Ipamorelin Blend": {
        "vial_mg": 10.0, "dose_mcg": 200.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone Blend", "filter_cat": "Muscle & Workout",
        "desc": "The Gold Standard GH Stack. Combines a GHRH and a GHRP.",
        "benefits_summary": "- Max natural GH secretion\n- Significant body recomposition\n- No cortisol or prolactin spike",
        "benefits_detailed": """
- **Synergy:** CJC-1295 sends the signal, Ipamorelin amplifies the pulse size.
- **Fat Loss:** Highly effective at mobilizing deep visceral abdominal fat.
- **Safety:** Unlike older GHRPs, it does not cause hunger or stress hormone spikes.
""",
        "side_effects_detailed": """
• **Carpal Tunnel:** High doses can cause tingling or numbness in the hands.
• **Water Retention:** Initial water weight gain is common (subsides in 2 weeks).
• **Flushing:** Temporary facial warmth post-injection.
""",
        "protocol_detailed": """
**Dosage:** 200mcg - 300mcg (Total Volume).
**Timing:** Nightly before bed on a completely empty stomach.
**Cycle:** 3 to 6 months for best results.
""",
        "storage": "Refrigerate. Do not shake the vial."
    },
    "Epithalon": {
        "vial_mg": 10.0, "dose_mcg": 5.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Anti-Aging", "filter_cat": "Wellness & Longevity",
        "desc": "Synthetic tetrapeptide that increases telomerase activity.",
        "benefits_summary": "- Extends lifespan (Telomeres)\n- Resets circadian rhythm\n- Anti-tumor/cancer protective",
        "benefits_detailed": """
- **DNA Repair:** Upregulates telomerase to protect and repair DNA strands.
- **Endocrine Reset:** Restores sensitivity of the hypothalamus and pineal gland.
- **Sleep Quality:** Normalizes natural melatonin production and sleep-wake cycles.
""",
        "side_effects_detailed": """
• **Drowsiness:** Can cause daytime sleepiness in some users.
• **Vivid Dreams:** Significant impact on dream intensity.
• **Safety:** No known toxicities or major contraindications in human trials.
""",
        "protocol_detailed": """
**Dosage:** 5mg - 10mg daily.
**Cycle:** 10 to 20 Day Course (Repeat every 6-12 months).
**Timing:** Any time, but evening is preferred for sleep benefits.
""",
        "storage": "Refrigerate."
    },
    "GHK-Cu": {
        "vial_mg": 50.0, "dose_mcg": 2.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cosmetic/Repair", "filter_cat": "Skin, Hair & Beauty",
        "desc": "Copper Tripeptide-1. Genomic modulator.",
        "benefits_summary": "- Boosts collagen & elastin\n- Tightens loose skin\n- Regrows hair (follicle size)",
        "benefits_detailed": """
- **Skin Rejuvenation:** Increases collagen synthesis by 70%; thickens the dermis.
- **Hair Growth:** Enlarges hair follicles and prolongs the growth (Anagen) phase.
- **DNA Repair:** Resets activity of over 4,000 genes to a younger state.
""",
        "side_effects_detailed": """
• **Pain:** Significant injection site pain (burning sensation).
• **Welts:** Common to see red welts or bruising that lasts several days.
• **Zinc Depletion:** Blocks zinc absorption; supplement 50mg Zinc daily.
""",
        "protocol_detailed": """
**Dosage:** 1mg - 2mg daily.
**Timing:** Evening (rotate injection sites frequently).
**Cycle:** 30 Days on, 30 Days off.
""",
        "storage": "Refrigerate. Protect from light."
    },
    "Glow Blend (GHK-Cu/BPC/TB)": {
        "vial_mg": 70.0, "dose_mcg": 2.5, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cosmetic/Recovery Blend", "filter_cat": "Skin, Hair & Beauty",
        "desc": "70mg Tri-Blend. Buffered GHK-Cu for reduced pain.",
        "benefits_summary": "- Painless GHK-Cu injection\n- Total body skin tightening\n- Rapid injury recovery",
        "benefits_detailed": """
- **Neutralization:** BPC-157 acts as a buffer to stop the GHK-Cu acidity/sting.
- **Synergy:** Simultaneously repairs the gut, skin, and connective tissue.
- **Rejuvenation:** High-dose repair for those with multiple injuries or aging skin.
""",
        "side_effects_detailed": """
• **Redness:** Mild redness at the site, though much less than pure GHK-Cu.
• **Flushing:** Temporary warmth.
• **Fatigue:** Healing response can cause sleepiness.
""",
        "protocol_detailed": """
**Dosage:** 2.5mg - 3mg total fluid daily.
**Timing:** Evening preferred.
**Cycle:** 4 to 6 weeks.
""",
        "storage": "Refrigerate. Protect from light."
    },
    "HCG": {
        "vial_mg": 5000.0, "dose_mcg": 250.0, "default_dose_unit": "IU", "default_stock_unit": "IU", "iu_conversion": 1,
        "type": "Hormonal", "filter_cat": "Libido & Sexual Health",
        "desc": "Human Chorionic Gonadotropin. Mimics LH.",
        "benefits_summary": "- Prevents testicular shrinkage\n- Maintains fertility/sperm\n- Boosts libido & mood",
        "benefits_detailed": """
- **Testicular Health:** Maintains natural function and volume during TRT cycles.
- **Fertility:** Essential for maintaining spermatogenesis (sperm production).
- **Libido:** Provides a unique mood and libido boost separate from testosterone.
""",
        "side_effects_detailed": """
• **Estrogen:** Can cause significant spikes in Estradiol (E2).
• **Gyno:** Risk of breast tissue growth if E2 is not managed.
• **Acne:** Hormonal fluctuations can cause skin breakouts.
""",
        "protocol_detailed": """
**Dosage:** 250 IU - 500 IU.
**Frequency:** 2 to 3 times per week.
**Cycle:** Continuous with TRT or used as part of a PCT protocol.
""",
        "storage": "Refrigerate. Extremely fragile; do not shake."
    },
    "Ipamorelin": {
        "vial_mg": 5.0, "dose_mcg": 100.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone", "filter_cat": "Muscle & Workout",
        "desc": "Selective GH Secretagogue. The mildest and safest GHRP.",
        "benefits_summary": "- Clean GH release (No hunger)\n- Fat loss & muscle sparing\n- Improved sleep quality",
        "benefits_detailed": """
- **Pure Signal:** Stimulates steady GH pulse without affecting hunger (ghrelin).
- **Catabolic Protection:** Helps maintain muscle tissue during calorie deficits.
- **Sleep:** Increases both REM and Slow-Wave (Deep) sleep cycles.
""",
        "side_effects_detailed": """
• **Water Retention:** Minimal compared to other GHRPs.
• **Headache:** Rare reports of mild headaches.
• **Dizziness:** Can occur if blood sugar is very low at time of injection.
""",
        "protocol_detailed": """
**Dosage:** 100mcg - 300mcg nightly.
**Timing:** Before bed on an empty stomach.
**Cycle:** 8 to 12 weeks.
""",
        "storage": "Refrigerate."
    },
    "Kisspeptin": {
        "vial_mg": 10.0, "dose_mcg": 100.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Hormonal", "filter_cat": "Libido & Sexual Health",
        "desc": "A neuromodulator that stimulates GnRH release.",
        "benefits_summary": "- Restarts HPTA axis safely\n- Boosts fertility (LH/FSH)\n- Increases libido",
        "benefits_detailed": """
- **HPTA Restart:** One of the safest methods to restart natural testosterone production.
- **Fertility:** Strongly stimulates FSH for sperm maturation.
- **Neurological:** Influences emotional processing and sexual desire.
""",
        "side_effects_detailed": """
• **Flushing:** Temporary warmth/redness post-injection.
• **Injection Site:** Mild irritation or itching.
• **Headache:** Rare but reported in higher doses.
""",
        "protocol_detailed": """
**Dosage:** 100mcg - 200mcg daily.
**Cycle:** 4 weeks during Post-Cycle Therapy (PCT).
""",
        "storage": "Refrigerate."
    },
    "Klow Blend (GHK-Cu/BPC/TB/KPV)": {
        "vial_mg": 80.0, "dose_mcg": 3.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Ultimate Repair/Cosmetic Blend", "filter_cat": "Skin, Hair & Beauty",
        "desc": "The 80mg Master Stack. Adds KPV for skin/gut health.",
        "benefits_summary": "- Clears Acne, Psoriasis, Eczema\n- Heals Gut (IBD/Colitis)\n- Systemic anti-inflammatory",
        "benefits_detailed": """
- **Dermatology:** KPV is a potent anti-inflammatory for chronic skin conditions.
- **Gut Health:** Strongest known blend for treating IBD or Ulcerative Colitis.
- **Mast Cell:** KPV stabilizes mast cells to reduce systemic histamine.
""",
        "side_effects_detailed": """
• **Red Welts:** Common at injection site due to GHK-Cu concentration.
• **Healing Crisis:** Temporary fatigue (Herxheimer) as the body repairs.
• **Flushing:** Facial warmth.
""",
        "protocol_detailed": """
**Dosage:** 3mg total volume daily.
**Timing:** Evening preferred.
**Cycle:** 4 to 8 weeks.
""",
        "storage": "Refrigerate. Protect from light."
    },
    "Melanotan II": {
        "vial_mg": 10.0, "dose_mcg": 500.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cosmetic", "filter_cat": "Skin, Hair & Beauty",
        "desc": "Alpha-MSH analog. Stimulates melanin and arousal.",
        "benefits_summary": "- Deep, rapid tan\n- Extreme libido boost\n- Appetite suppression",
        "benefits_detailed": """
- **Tanning:** Stimulates melanin for a deep tan even with minimal UV.
- **Libido:** Very potent aphrodisiac for both men and women.
- **Photoprotection:** Melanin provides a natural barrier against UV damage.
""",
        "side_effects_detailed": """
• **Nausea:** Significant nausea for 1-2 hours after injection (Common).
• **Mole Darkening:** Freckles and moles will get darker.
• **Erections:** Can cause spontaneous, long-lasting erections (Priapism risk).
""",
        "protocol_detailed": """
**Dosage:** 100mcg - 500mcg.
**Frequency:** Start low! Daily until tan achieved, then 1-2x weekly.
**Timing:** 30 mins before UV exposure.
""",
        "storage": "Refrigerate."
    },
    "MOTS-c": {
        "vial_mg": 10.0, "dose_mcg": 5.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Metabolic/Mitochondrial", "filter_cat": "Muscle & Workout",
        "desc": "Mitochondrial-Derived Peptide. An 'exercise mimetic'.",
        "benefits_summary": "- Increases VO2 Max/Endurance\n- Prevents weight gain\n- Cellular energy boost",
        "benefits_detailed": """
- **Endurance:** Dramatically increases cellular capacity for glucose and oxygen utilization.
- **Metabolic:** Prevents diet-induced insulin resistance and weight gain.
- **Biogenesis:** Promotes the creation of new mitochondria in cells.
""",
        "side_effects_detailed": """
• **Stinging:** Known for being a very painful injection.
• **Insomnia:** Can cause extreme hyperactivity if taken late in the day.
• **Heart Rate:** May slightly elevate resting heart rate.
""",
        "protocol_detailed": """
**Dosage:** 5mg - 10mg.
**Frequency:** Once per week.
**Timing:** Morning (Pre-workout).
""",
        "storage": "Refrigerate."
    },
    "NAD+": {
        "vial_mg": 500.0, "dose_mcg": 50.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cellular Energy", "filter_cat": "Wellness & Longevity",
        "desc": "Nicotinamide Adenine Dinucleotide. Cellular fuel.",
        "benefits_summary": "- Clears brain fog\n- Restores cellular energy\n- Repairs DNA damage",
        "benefits_detailed": """
- **Cognition:** Rapidly restores mental clarity and sharp focus.
- **Anti-Aging:** Repairs DNA and regulates Sirtuins (longevity genes).
- **Mitochondria:** Directly fuels the ATP production process.
""",
        "side_effects_detailed": """
• **NAD Flush:** Rapid injection causes intense chest pressure and anxiety.
• **Cramps:** Abdominal cramping and nausea if injected too fast.
• **Palpitations:** Temporary racing heart (lasts 5-10 mins).
""",
        "protocol_detailed": """
**Dosage:** 25mg - 50mg.
**Frequency:** 2-3x per week.
**Warning:** INJECT VERY SLOWLY (over 60+ seconds).
""",
        "storage": "Refrigerate immediately. Highly sensitive."
    },
    "Oxytocin Acetate": {
        "vial_mg": 2.0, "dose_mcg": 20.0, "default_dose_unit": "IU", "default_stock_unit": "mg", "iu_conversion": 600,
        "type": "Hormonal/Wellness", "filter_cat": "Nootropics & Brain",
        "desc": "The 'Love Hormone'. social interaction regulator.",
        "benefits_summary": "- Reduces social anxiety\n- Lowers cortisol (Stress)\n- Enhances emotional bonding",
        "benefits_detailed": """
- **Social Anxiety:** Significantly reduces fear and stress in social settings.
- **Analgesia:** Shows natural pain-killing properties.
- **Trust:** Enhances feelings of empathy, trust, and connection.
""",
        "side_effects_detailed": """
• **Nausea:** Common at higher doses.
• **Headache:** Occasional tension.
• **Flushing:** Mild facial warmth.
""",
        "protocol_detailed": """
**Dosage:** 10 IU - 25 IU.
**Timing:** 30 minutes before social or intimate events.
**Frequency:** As needed.
""",
        "storage": "Refrigerate."
    },
    "PT-141": {
        "vial_mg": 10.0, "dose_mcg": 1.5, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Libido", "filter_cat": "Libido & Sexual Health",
        "desc": "Bremelanotide. Targets the nervous system for arousal.",
        "benefits_summary": "- Treats ED & Low Libido\n- Works when PDE5i fails\n- For Men & Women",
        "benefits_detailed": """
- **Mechanism:** Works on the brain (hypothalamus), not the blood vessels.
- **Efficacy:** FDA approved (Vyleesi) for female sexual arousal disorder.
- **Libido:** Direct stimulation of sexual desire and physical arousal.
""",
        "side_effects_detailed": """
• **Nausea:** Occurs in about 40% of users; can be intense.
• **Blood Pressure:** Temporary elevation in blood pressure.
• **Flushing:** Facial warmth and redness.
""",
        "protocol_detailed": """
**Dosage:** 1.5mg - 2mg.
**Timing:** 2 to 4 hours BEFORE activity.
**Frequency:** Max 8 doses per month.
""",
        "storage": "Refrigerate."
    },
    "Retatrutide": {
        "vial_mg": 10.0, "dose_mcg": 2.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Metabolic (GLP-1/GIP/Glucagon)", "filter_cat": "Slimming & Fat Loss",
        "desc": "The 'Triple G' Agonist. Most potent weight loss agent.",
        "benefits_summary": "- Extreme weight loss (24%+)\n- Burns liver fat (NAFLD)\n- Resets metabolism",
        "benefits_detailed": """
- **Weight Loss:** Average 24.2% loss in clinical trials (unprecedented).
- **Liver Health:** Resolves Fatty Liver Disease by clearing hepatic fat.
- **Energy Burn:** Glucagon component increases calorie expenditure.
""",
        "side_effects_detailed": """
• **Tachycardia:** Significant increase in heart rate.
• **Skin Sensitivity:** Cutaneous hyperesthesia (skin hurts to touch).
• **Gastro:** Nausea and constipation.
""",
        "protocol_detailed": """
**Dosage:** Start 2mg -> Titrate up to 12mg.
**Frequency:** Once weekly.
**Cycle:** Continuous.
""",
        "storage": "Refrigerate. Do not freeze."
    },
    "Semaglutide": {
        "vial_mg": 5.0, "dose_mcg": 0.25, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Metabolic (GLP-1)", "filter_cat": "Slimming & Fat Loss",
        "desc": "GLP-1 Agonist. Standard medical weight loss.",
        "benefits_summary": "- 15% weight loss\n- Controls blood sugar\n- Cardioprotective",
        "benefits_detailed": """
- **Satiety:** Slows gastric emptying, making you feel full longer.
- **Heart:** 20% reduction in major adverse cardiac events.
- **Addiction:** Reduces cravings for alcohol, sugar, and nicotine.
""",
        "side_effects_detailed": """
• **Gastro:** Nausea, vomiting, and severe constipation.
• **Fatigue:** Common during initial titration.
• **Ozempic Face:** Rapid fat loss in facial area.
""",
        "protocol_detailed": """
**Dosage:** Start 0.25mg -> Max 2.4mg.
**Frequency:** Once weekly.
**Cycle:** Continuous.
""",
        "storage": "Refrigerate. Protect from light."
    },
    "TB-500": {
        "vial_mg": 5.0, "dose_mcg": 2.5, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Regenerative", "filter_cat": "Injury & Repair",
        "desc": "Synthetic Thymosin Beta-4. Muscle repair peptide.",
        "benefits_summary": "- Heals muscle tears\n- Improves flexibility\n- Cardiac repair",
        "benefits_detailed": """
- **Muscle Repair:** Primary peptide for torn muscles, strains, and pulls.
- **Inflammation:** Systemic reduction of inflammatory markers.
- **Flexibility:** Softens scar tissue and increases joint mobility.
""",
        "side_effects_detailed": """
• **Head Rush:** Temporary feeling of pressure in the head post-injection.
• **Lethargy:** Intense fatigue as the body focuses on repair.
• **Flu-like Symptoms:** Occasional reports of mild malaise.
""",
        "protocol_detailed": """
**Dosage:** 2.5mg (2500mcg).
**Frequency:** 2x per week.
**Cycle:** 4 to 6 weeks.
""",
        "storage": "Refrigerate."
    },
    "Tesamorelin": {
        "vial_mg": 2.0, "dose_mcg": 1.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone", "filter_cat": "Slimming & Fat Loss",
        "desc": "FDA Approved GHRH for visceral fat reduction.",
        "benefits_summary": "- Burns visceral belly fat\n- Increases muscle tone\n- Nootropic effects",
        "benefits_detailed": """
- **Visceral Fat:** Specifically targets the "hard" fat around internal organs.
- **Cognition:** Improves executive function and memory in aging adults.
- **Triglycerides:** Significantly improves lipid profiles.
""",
        "side_effects_detailed": """
• **Joint Stiffness:** "Achy" joints are a common side effect of GH elevation.
• **Injection Site:** Itching or redness (more common than others).
• **Water Retention:** Mild swelling in extremities.
""",
        "protocol_detailed": """
**Dosage:** 1mg - 2mg nightly.
**Timing:** Before bed (Fasted).
**Cycle:** 8 to 12 weeks.
""",
        "storage": "Refrigerate. Use within 20-30 days."
    },
    "Tesamorelin + Ipamorelin Blend": {
        "vial_mg": 12.0, "dose_mcg": 350.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone/Fat Loss Blend", "filter_cat": "Slimming & Fat Loss",
        "desc": "The 'Shred Stack'. High potency fat burner.",
        "benefits_summary": "- Max visceral fat loss\n- Muscle definition\n- Deep sleep",
        "benefits_detailed": """
- **Recomposition:** Powerful combo for burning abdominal fat while maintaining muscle.
- **Fasting Synergy:** Amplifies the fat-burning effects of overnight fasting.
- **Sleep:** Ipamorelin component improves sleep depth.
""",
        "side_effects_detailed": """
• **Numbness:** Carpal tunnel-like tingling in hands.
• **Joint Pain:** Mild aches in knees and wrists.
• **Flushing:** Post-injection warmth.
""",
        "protocol_detailed": """
**Dosage:** 350mcg - 500mcg (Total Volume).
**Frequency:** Daily (5 on / 2 off).
**Timing:** Nightly (Fasted).
""",
        "storage": "Refrigerate."
    },
    "Tirzepatide": {
        "vial_mg": 30.0, "dose_mcg": 2.5, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Metabolic (GLP-1/GIP)", "filter_cat": "Slimming & Fat Loss",
        "desc": "Dual Agonist (Mounjaro). GIP + GLP-1. Superior to Semaglutide.",
        "benefits_summary": "- Massive weight loss (22%)\n- Eliminates 'Food Noise'\n- Metabolic repair",
        "benefits_detailed": """
- **Weight Loss:** 22%+ average loss in clinical trials.
- **Food Noise:** Complete suppression of obsessive food thoughts.
- **Tolerability:** GIP component reduces nausea compared to Semaglutide.
""",
        "side_effects_detailed": """
• **Anhedonia:** Feeling "flat" or losing joy in hobbies/food.
• **Cold Extremities:** Hands and feet feeling unusually cold.
• **Constipation:** Can be severe; requires high fiber/water intake.
• **Hair Shedding:** Telogen effluvium due to rapid weight loss.
""",
        "protocol_detailed": """
**Dosage:** Start 2.5mg -> Max 15mg.
**Frequency:** Once weekly.
**Cycle:** Continuous.
""",
        "storage": "Refrigerate. Do not freeze."
    }
}
