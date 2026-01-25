import streamlit as st
import math

# --- 1. CONFIGURATION: WIDE MODE ---
st.set_page_config(
    page_title="PeptideCalc Pro v2.3",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS FOR VISUAL SYRINGE & CARDS ---
st.markdown("""
<style>
    .syringe-container {
        border: 2px solid #333;
        border-radius: 4px;
        background-color: #f0f0f0;
        height: 30px;
        width: 100%;
        position: relative;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .syringe-liquid {
        background-color: #ff4b4b;
        height: 100%;
        border-radius: 2px 0 0 2px;
        transition: width 0.5s ease-in-out;
    }
    .syringe-markings {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: repeating-linear-gradient(90deg, transparent, transparent 19%, #000 20%);
        opacity: 0.1;
    }
    .db-tag {
        background-color: #4b4bff;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.8em;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    .side-effect-box {
        background-color: #3e1818;
        border-left: 4px solid #ff4b4b;
        padding: 10px;
        margin-top: 10px;
        border-radius: 4px;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

# --- EXPANDED KNOWLEDGE BASE (v2.3) ---
PEPTIDE_PRESETS = {
    "Custom (Enter manually)": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "type": "N/A", "desc": "Manual calculation.",
        "benefits_summary": "N/A", "side_effects_summary": "Unknown.", "protocol_summary": "As directed.",
        "benefits_detailed": "N/A", "protocol_detailed": "N/A", "side_effects_detailed": "N/A", "storage": "Dependant on compound."
    },
    "AOD-9604": {
        "vial_mg": 5.0, "dose_mcg": 300.0,
        "type": "Fat Loss",
        "desc": "Anti-Obesity Drug 9604. A modified fragment of the C-terminus of Human Growth Hormone (HGH) designed specifically to burn fat without the blood sugar effects of full HGH.",
        "benefits_summary": "Fat burning, no blood sugar spike, cartilage repair.",
        "side_effects_summary": "Very mild. Injection site redness.",
        "protocol_summary": "300mcg daily, fasted.",
        "benefits_detailed": """
        - **Targeted Fat Loss:** Stimulates lipolysis (fat breakdown) and inhibits lipogenesis (fat storage).
        - **Safety:** Does not affect insulin or IGF-1 levels, making it safer than HGH for some users.
        - **Cartilage:** Originally developed for osteoarthritis; aids in cartilage regeneration.
        """,
        "protocol_detailed": """
        **Dosage:** 300mcg (0.3mg)

        **Frequency:** Daily

        **Timing:** Morning (Fasted)

        **Cycle:** 3 Months

        **Study Note:** Clinical trials showed efficacy in weight management with a distinct lack of HGH-related side effects.
        """,
        "side_effects_detailed": "Extremely well tolerated. Minor injection site reactions.",
        "storage": "Refrigerate."
    },
    "BPC-157": {
        "vial_mg": 5.0, "dose_mcg": 250.0, 
        "type": "Regenerative",
        "desc": "Body Protection Compound-157. A 15-amino acid chain derived from gastric juice. It modulates the nitric oxide system and promotes angiogenesis.",
        "benefits_summary": "Heals tendons/ligaments, protects gut health (IBS), reduces inflammation.",
        "side_effects_summary": "Rare. Mild nausea or injection site irritation.",
        "protocol_summary": "250-500mcg daily or 2x daily.",
        "benefits_detailed": """
        - **Soft Tissue Repair:** Rapidly accelerates healing of tendons, ligaments, and bone fractures.
        - **Gut Health:** Potent cytoprotective effects on the GI tract; used for IBS, leaky gut, and ulcers.
        - **Neuroprotection:** Modulates serotonergic and dopaminergic systems (brain health).
        """,
        "protocol_detailed": """
        **Dosage:** 250mcg - 500mcg (0.25mg - 0.5mg)

        **Frequency:** Daily or Twice Daily (AM/PM)

        **Timing:** SubQ near injury site (local) or belly fat (systemic)

        **Cycle:** 4 to 6 Weeks on, 2 Weeks off

        **Study Note:** Extensive pre-clinical trials demonstrate accelerated tendon-to-bone healing.
        """,
        "side_effects_detailed": "Generally considered extremely safe. Rare reports of fatigue, mild nausea, or temporary anhedonia.",
        "storage": "Refrigerate after mixing. Stable for ~30-45 days."
    },
    "BPC-157 + TB-500 Blend": {
        "vial_mg": 10.0, "dose_mcg": 500.0, 
        "type": "Regenerative Blend",
        "desc": "The 'Wolverine Stack'. Synergistic combination where BPC-157 works on connective tissue/gut, while TB-500 works on muscle tissue.",
        "benefits_summary": "Maximum tissue repair, flexibility, anti-inflammatory, cardiac health.",
        "side_effects_summary": "Head rush, fatigue, lethargy.",
        "protocol_summary": "500mcg-1mg total fluid daily.",
        "benefits_detailed": """
        - **Synergy:** BPC repairs the structure (tendon/bone) while TB-500 aids muscle contractile tissue.
        - **Flexibility:** Significant improvements in joint range of motion.
        - **Cardiac:** TB-500 has documented cardioprotective effects post-injury.
        """,
        "protocol_detailed": """
        **Dosage:** 500mcg - 1000mcg (Total Volume)

        **Frequency:** Daily

        **Timing:** Any time of day

        **Cycle:** 4 to 8 Weeks (Duration of injury)

        **Study Note:** Pre-clinical models show faster wound closure rates when these two are combined vs used alone.
        """,
        "side_effects_detailed": "Temporary head rush immediately after injection (common with TB-500). Fatigue or lethargy during the healing phase.",
        "storage": "Refrigerate. Use within 30 days."
    },
    "CJC-1295 (No DAC)": {
        "vial_mg": 5.0, "dose_mcg": 100.0, 
        "type": "Growth Hormone",
        "desc": "Modified GRF 1-29. A GHRH analog that acts on the pituitary gland to stimulate pulsatile Growth Hormone release.",
        "benefits_summary": "Lean muscle, fat loss, deep sleep, anti-aging.",
        "side_effects_summary": "Head rush, flushing, vivid dreams.",
        "protocol_summary": "100mcg nightly, fasted.",
        "benefits_detailed": """
        - **Hyperplasia:** Increases the actual number of muscle cells.
        - **Sleep Architecture:** Increases slow-wave (Delta) deep sleep.
        - **Cosmetic:** Improves skin elasticity and collagen density.
        """,
        "protocol_detailed": """
        **Dosage:** 100mcg (0.1mg)

        **Frequency:** Daily (5 days on / 2 days off)

        **Timing:** Immediately before bed (Fasted 2+ hours)

        **Cycle:** 12 Weeks +

        **Study Note:** Mimics natural pulsatile GH secretion rather than the 'constant bleed' of synthetic HGH.
        """,
        "side_effects_detailed": "Immediate head rush (vasodilation) lasting 10-20 mins. Warm/flushed face. Vivid dreams.",
        "storage": "Refrigerate. Sensitive to light/heat."
    },
    "CJC-1295 + Ipamorelin Blend": {
        "vial_mg": 10.0, "dose_mcg": 200.0, 
        "type": "Growth Hormone Blend",
        "desc": "The Gold Standard GH Stack. Combines a Releasing Hormone (CJC) with a Releasing Peptide (Ipamorelin) for a synergistic 5x-10x GH pulse.",
        "benefits_summary": "Max natural GH release, fat loss, muscle preservation, recovery.",
        "side_effects_summary": "Head rush, numb fingers, water retention.",
        "protocol_summary": "200-300mcg total nightly, fasted.",
        "benefits_detailed": """
        - **Maximum Pulse:** The strongest natural GH release signal possible without synthetic HGH.
        - **Safety:** Ipamorelin ensures no spike in cortisol or prolactin.
        - **Recomposition:** Simultaneously burns visceral fat and builds lean tissue.
        """,
        "protocol_detailed": """
        **Dosage:** 200mcg - 300mcg (Total Volume)

        **Frequency:** Nightly (5 days on / 2 days off)

        **Timing:** Immediately before bed (Fasted 2+ hours)

        **Cycle:** 3 to 6 Months

        **Study Note:** Clinical data suggests GHRH+GHRP combinations are far superior to monotherapy for IGF-1 elevation.
        """,
        "side_effects_detailed": "Head rush. Numbness/tingling in hands (carpal tunnel-like symptoms) if dose is too high. Water weight gain.",
        "storage": "Refrigerate. Do not shake."
    },
    "Epithalon": {
        "vial_mg": 10.0, "dose_mcg": 5000.0, 
        "type": "Anti-Aging",
        "desc": "Synthetic tetrapeptide that increases telomerase activity, potentially lengthening telomeres.",
        "benefits_summary": "Longevity, telomere lengthening, circadian rhythm reset.",
        "side_effects_summary": "None reported/Very mild.",
        "protocol_summary": "5mg-10mg daily for 10-20 days.",
        "benefits_detailed": """
        - **Life Extension:** Increases telomere length, a marker of biological age.
        - **Endocrine Health:** Restores sensitivity of the pineal gland.
        - **Sleep:** Normalizes melatonin production and circadian rhythms.
        """,
        "protocol_detailed": """
        **Dosage:** 5mg - 10mg

        **Frequency:** Daily

        **Timing:** Morning or Evening

        **Cycle:** 10 to 20 Day Course (Repeat every 6-12 months)

        **Study Note:** Based on the Khavinson Protocol (Gerontology trials).
        """,
        "side_effects_detailed": "Extremely safe profile. Occasional daytime drowsiness.",
        "storage": "Refrigerate."
    },
    "GHK-Cu": {
        "vial_mg": 50.0, "dose_mcg": 2000.0, 
        "type": "Cosmetic/Repair",
        "desc": "Copper Tripeptide-1. A naturally occurring peptide that declines with age. It modulates over 4,000 genes to a younger state.",
        "benefits_summary": "Collagen boost, wrinkle reduction, hair regrowth, wound healing.",
        "side_effects_summary": "Painful injection sting, redness, potential zinc depletion.",
        "protocol_summary": "1-2mg daily. Evening.",
        "benefits_detailed": """
        - **Skin Architecture:** Increases collagen (70%) and elastin levels. Tightens loose skin.
        - **Hair Restoration:** Enlarges hair follicles and stimulates growth.
        - **Wound Healing:** Powerful antioxidant and anti-inflammatory properties.
        """,
        "protocol_detailed": """
        **Dosage:** 1mg - 2mg

        **Frequency:** Daily

        **Timing:** Evening (rotate sites)

        **Cycle:** 30 Days on, 30 Days off

        **Study Note:** Monitor copper/zinc balance. Supplement Zinc if using long-term.
        """,
        "side_effects_detailed": "High incidence of injection site pain (burning) and redness. Systemic copper toxicity risk if overdosed.",
        "storage": "Refrigerate. Protect from light."
    },
    "Glow Blend (GHK-Cu/BPC/TB)": {
        "vial_mg": 70.0, "dose_mcg": 2500.0, 
        "type": "Cosmetic/Recovery Blend",
        "desc": "70mg Tri-Blend. BPC-157 and TB-500 are added to buffer the GHK-Cu, significantly reducing the 'sting' while adding systemic recovery benefits.",
        "benefits_summary": "Painless GHK-Cu, skin tightening, total body recovery.",
        "side_effects_summary": "Mild redness, flushing.",
        "protocol_summary": "2.5mg - 3mg total daily.",
        "benefits_detailed": """
        - **Painless Application:** BPC-157 neutralizes the acidity of Copper, making injections tolerable.
        - **Total Rejuvenation:** Targets skin, hair, gut, and muscle simultaneously.
        - **Collagen Matrix:** Synergistic upregulation of collagen synthesis.
        """,
        "protocol_detailed": """
        **Dosage:** 2.5mg - 3mg (Total Volume)

        **Frequency:** Daily

        **Timing:** Evening

        **Cycle:** 4 to 6 Weeks

        **Study Note:** Combined protocol targets both aesthetic markers (skin) and biological markers (inflammation).
        """,
        "side_effects_detailed": "Mild injection site redness. Temporary flushing.",
        "storage": "Refrigerate. Protect from light."
    },
    "HCG": {
        "vial_mg": 5.0, "dose_mcg": 250.0, 
        "type": "Hormonal",
        "desc": "Human Chorionic Gonadotropin. Mimics LH to maintain testicular function.",
        "benefits_summary": "Maintains testicular size, fertility, libido.",
        "side_effects_summary": "High estrogen, acne, gynecomastia risk.",
        "protocol_summary": "250-500iu 2-3x per week.",
        "benefits_detailed": """
        - **On-Cycle Support:** Prevents testicular atrophy during TRT.
        - **Fertility:** Restores spermatogenesis and intratesticular testosterone.
        - **Mood:** Upstream pathways support DHEA and Pregnenolone synthesis.
        """,
        "protocol_detailed": """
        **Dosage:** 250iu - 500iu (Check vial concentration!)

        **Frequency:** 2 to 3 times per week

        **Timing:** Morning

        **Cycle:** Continuous with TRT or as PCT

        **Study Note:** Essential for maintaining the HPTA axis during exogenous testosterone use.
        """,
        "side_effects_detailed": "Estrogen spikes (requires AI management), acne, water retention, desensitization if overdosed.",
        "storage": "Refrigerate. Fragile."
    },
    "Ipamorelin": {
        "vial_mg": 5.0, "dose_mcg": 100.0, 
        "type": "Growth Hormone",
        "desc": "Selective GH Secretagogue. The mildest and safest GHRP.",
        "benefits_summary": "Fat loss, sleep, no hunger spike.",
        "side_effects_summary": "Very mild. Rare dizziness.",
        "protocol_summary": "100-300mcg nightly, fasted.",
        "benefits_detailed": """
        - **Pure Signal:** Stimulates GH release without the extreme hunger of GHRP-6.
        - **Deep Sleep:** Increases REM cycles.
        - **Anabolic:** Preserves lean tissue during caloric restriction.
        """,
        "protocol_detailed": """
        **Dosage:** 100mcg - 300mcg

        **Frequency:** Nightly

        **Timing:** Before Bed (Fasted)

        **Cycle:** 8 to 12 Weeks

        **Study Note:** Does not elevate cortisol or prolactin levels in clinical trials.
        """,
        "side_effects_detailed": "Extremely well tolerated. Slight water retention possible.",
        "storage": "Refrigerate."
    },
    "Kisspeptin": {
        "vial_mg": 10.0, "dose_mcg": 100.0, 
        "type": "Hormonal",
        "desc": "A neuromodulator that stimulates the hypothalamus to release GnRH, restarting the HPTA axis.",
        "benefits_summary": "Safe testosterone restart, fertility, libido.",
        "side_effects_summary": "Flushing, injection site reaction.",
        "protocol_summary": "100-200mcg daily.",
        "benefits_detailed": """
        - **HPTA Restart:** Safely restarts natural testosterone production post-cycle.
        - **Libido:** Enhances psychogenic sexual desire and mood.
        - **Safety:** Unlike HCG, does not cause testicular desensitization.
        """,
        "protocol_detailed": """
        **Dosage:** 100mcg - 200mcg

        **Frequency:** Daily

        **Timing:** Any time

        **Cycle:** 4 Weeks (PCT)

        **Study Note:** Acts upstream of HCG, mimicking natural pulsatile GnRH release.
        """,
        "side_effects_detailed": "Rare. Slight flushing. Short half-life means effects do not linger.",
        "storage": "Refrigerate."
    },
    "Klow Blend (GHK-Cu/BPC/TB/KPV)": {
        "vial_mg": 80.0, "dose_mcg": 3000.0, 
        "type": "Ultimate Repair/Cosmetic Blend",
        "desc": "The 80mg Master Stack. Adds **KPV** to the GHK/BPC/TB trio. KPV is a potent anti-inflammatory.",
        "benefits_summary": "Clear skin (acne/psoriasis), gut healing, anti-inflammatory.",
        "side_effects_summary": "Injection site redness, fatigue.",
        "protocol_summary": "3mg total daily.",
        "benefits_detailed": """
        - **Dermatology:** KPV actively treats acne, psoriasis, and eczema.
        - **Gut Health:** Strongest known stack for IBD and Colitis.
        - **Systemic:** Mast cell stabilization (histamine control).
        """,
        "protocol_detailed": """
        **Dosage:** 3mg (Total Volume)

        **Frequency:** Daily

        **Timing:** Evening

        **Cycle:** 4 to 8 Weeks

        **Study Note:** KPV data shows significant reduction in inflammatory cytokines.
        """,
        "side_effects_detailed": "Red welts at injection site (common). Fatigue possible as body detoxes.",
        "storage": "Refrigerate. Protect from light."
    },
    "Melanotan II": {
        "vial_mg": 10.0, "dose_mcg": 500.0, 
        "type": "Cosmetic",
        "desc": "Alpha-MSH analog. Stimulates melanin production and sexual arousal centers.",
        "benefits_summary": "Deep tan, high libido, appetite suppression.",
        "side_effects_summary": "Nausea, flushing, darkening moles.",
        "protocol_summary": "100-500mcg before UV exposure.",
        "benefits_detailed": """
        - **Tanning:** Activates melanocytes to produce protective melanin (tan) with minimal UV.
        - **Libido:** Potent central nervous system aphrodisiac for men and women.
        - **Metabolic:** Suppresses appetite and increases energy expenditure.
        """,
        "protocol_detailed": """
        **Dosage:** 100mcg - 500mcg

        **Frequency:** As needed (Loading phase: Daily)

        **Timing:** 30 mins before UV exposure

        **Cycle:** Until desired color, then maintenance

        **Study Note:** Start very low (50-100mcg) to assess nausea tolerance.
        """,
        "side_effects_detailed": "Significant nausea (lasts 1-2 hours), facial flushing, spontaneous erections, darkening of freckles.",
        "storage": "Refrigerate."
    },
    "MOTS-c": {
        "vial_mg": 10.0, "dose_mcg": 5000.0,
        "type": "Metabolic/Mitochondrial",
        "desc": "Mitochondrial-Derived Peptide. Known as an 'exercise mimetic', it regulates metabolic functions and promotes endurance.",
        "benefits_summary": "Endurance, insulin sensitivity, weight control, energy.",
        "side_effects_summary": "Injection site pain (sting), insomnia if taken late.",
        "protocol_summary": "5mg once weekly.",
        "benefits_detailed": """
        - **Endurance:** Increases cellular ability to utilize glucose and oxygen (VO2 Max).
        - **Metabolic:** Prevents diet-induced insulin resistance and obesity in studies.
        - **Cellular Energy:** Promotes mitochondrial biogenesis (creation of new power plants in cells).
        """,
        "protocol_detailed": """
        **Dosage:** 5mg - 10mg

        **Frequency:** Once Weekly

        **Timing:** Morning (Pre-workout preferred)

        **Cycle:** 4 to 8 Weeks

        **Study Note:** Research indicates it mimics the physiological effects of aerobic exercise at a cellular level.
        """,
        "side_effects_detailed": "Injection site pain is very common. Insomnia/high energy if taken too late in the day.",
        "storage": "Refrigerate."
    },
    "NAD+": {
        "vial_mg": 500.0, "dose_mcg": 25000.0, 
        "type": "Cellular Energy",
        "desc": "Nicotinamide Adenine Dinucleotide. The fuel for cellular engines (mitochondria).",
        "benefits_summary": "Mental clarity, energy, DNA repair, detox.",
        "side_effects_summary": "Chest pressure, anxiety, nausea (The 'Flush').",
        "protocol_summary": "25-50mg 2-3x per week. SLOW INJECTION.",
        "benefits_detailed": """
        - **Cognition:** Clears brain fog and improves focus.
        - **Cellular:** Restores mitochondrial function (ATP production).
        - **Anti-Aging:** Activates Sirtuins (longevity genes).
        """,
        "protocol_detailed": """
        **Dosage:** 25mg - 50mg

        **Frequency:** 2-3x / Week

        **Timing:** Morning

        **Cycle:** Ongoing

        **Study Note:** ⚠️ INJECT VERY SLOWLY. Rapid injection causes severe discomfort.
        """,
        "side_effects_detailed": "Intense chest pressure, abdominal cramping, anxiety, palpitations. Lasts 5-10 minutes.",
        "storage": "Refrigerate immediately."
    },
    "PT-141": {
        "vial_mg": 10.0, "dose_mcg": 1000.0, 
        "type": "Libido",
        "desc": "Bremelanotide. Works on the nervous system to treat hypoactive sexual desire.",
        "benefits_summary": "Treats ED, increases libido in men/women.",
        "side_effects_summary": "Nausea, flushing, headache.",
        "protocol_summary": "1.5-2mg, 2 hours before activity.",
        "benefits_detailed": """
        - **Mechanism:** Targets the hypothalamus, not the vascular system.
        - **Efficacy:** FDA approved (Vyleesi) for low libido in women.
        - **Response:** Increases physical arousal and desire.
        """,
        "protocol_detailed": """
        **Dosage:** 1.5mg - 2mg

        **Frequency:** As needed

        **Timing:** 2 to 4 hours BEFORE activity

        **Cycle:** Max 8 doses per month

        **Study Note:** Effects can last up to 24 hours.
        """,
        "side_effects_detailed": "Nausea (40% of users), flushing, headache, elevated blood pressure.",
        "storage": "Refrigerate."
    },
    "Retatrutide": {
        "vial_mg": 10.0, "dose_mcg": 2000.0, 
        "type": "Metabolic (GLP-1/GIP/Glucagon)",
        "desc": "The 'Triple G' Agonist. The most potent weight loss agent currently in trials.",
        "benefits_summary": "Extreme weight loss, liver fat reduction, metabolic reset.",
        "side_effects_summary": "Increased heart rate, skin sensitivity, nausea.",
        "protocol_summary": "2mg weekly, titrate up.",
        "benefits_detailed": """
        - **Efficacy:** 24.2% average weight loss in clinical trials.
        - **Liver Health:** Resolves NAFLD (fatty liver) by actively burning liver fat via Glucagon.
        - **Metabolic:** Massive improvements in insulin sensitivity and lipids.
        """,
        "protocol_detailed": """
        **Dosage:** Start 2mg -> Titrate to Max 12mg

        **Frequency:** Once Weekly

        **Timing:** Any time

        **Cycle:** Continuous

        **Study Note:** Glucagon component increases resting energy expenditure.
        """,
        "side_effects_detailed": "Tachycardia (fast heart rate), cutaneous hyperesthesia (sensitive skin), nausea, constipation.",
        "storage": "Refrigerate. Do not freeze."
    },
    "Semaglutide": {
        "vial_mg": 5.0, "dose_mcg": 250.0, 
        "type": "Metabolic (GLP-1)",
        "desc": "GLP-1 Agonist. The standard for medical weight loss.",
        "benefits_summary": "Weight loss, appetite control, cardioprotection.",
        "side_effects_summary": "Nausea, constipation, fatigue, muscle loss.",
        "protocol_summary": "0.25mg weekly, titrate up.",
        "benefits_detailed": """
        - **Satiety:** Slows gastric emptying, keeping you full longer.
        - **Heart:** 20% reduction in major adverse cardiac events.
        - **Addiction:** Reduces cravings for alcohol and sugar.
        """,
        "protocol_detailed": """
        **Dosage:** Start 0.25mg -> Max 2.4mg

        **Frequency:** Once Weekly

        **Timing:** Any time

        **Cycle:** Continuous

        **Study Note:** Requires protein prioritization to prevent muscle wasting.
        """,
        "side_effects_detailed": "Nausea, vomiting, severe constipation, 'Ozempic face', fatigue.",
        "storage": "Refrigerate. Protect from light."
    },
    "TB-500": {
        "vial_mg": 5.0, "dose_mcg": 2500.0, 
        "type": "Regenerative",
        "desc": "Synthetic Thymosin Beta-4. The 'Muscle Repair' peptide.",
        "benefits_summary": "Muscle healing, flexibility, heart health.",
        "side_effects_summary": "Rare. Head rush.",
        "protocol_summary": "2.5mg twice weekly.",
        "benefits_detailed": """
        - **Actin Regulation:** Upregulates actin for faster cellular migration to wounds.
        - **Musculoskeletal:** Best choice for muscle tears and strains.
        - **Cardiac:** Repairs heart tissue after ischemic events.
        """,
        "protocol_detailed": """
        **Dosage:** 2.5mg (2500mcg)

        **Frequency:** 2x Per Week (e.g., Mon/Thu)

        **Timing:** Any time

        **Cycle:** 4 to 6 Weeks

        **Study Note:** Do not use if active cancer is present.
        """,
        "side_effects_detailed": "Very rare. Temporary head rush.",
        "storage": "Refrigerate."
    },
    "Tesamorelin": {
        "vial_mg": 2.0, "dose_mcg": 1000.0, 
        "type": "Growth Hormone",
        "desc": "FDA Approved GHRH for visceral fat reduction.",
        "benefits_summary": "Belly fat loss, nootropic, muscle tone.",
        "side_effects_summary": "Injection redness, joint pain, water retention.",
        "protocol_summary": "1-2mg nightly, fasted.",
        "benefits_detailed": """
        - **Visceral Fat:** Specifically targets stubborn adipose tissue around organs.
        - **Cognition:** Improves executive function in older adults.
        - **Lipids:** Lowers triglycerides significantly.
        """,
        "protocol_detailed": """
        **Dosage:** 1mg - 2mg

        **Frequency:** Daily

        **Timing:** Before Bed (Fasted)

        **Cycle:** 8 to 12 Weeks

        **Study Note:** FDA approved as Egrifta.
        """,
        "side_effects_detailed": "High rate of injection site redness/itching. Joint stiffness. Carpal tunnel symptoms.",
        "storage": "Refrigerate. Use within 20-30 days."
    },
    "Tesamorelin + Ipamorelin Blend": {
        "vial_mg": 12.0, "dose_mcg": 350.0, 
        "type": "Growth Hormone/Fat Loss Blend",
        "desc": "The 'Shred Stack'. Targets visceral fat + systemic GH elevation.",
        "benefits_summary": "Max fat loss, muscle definition, deep sleep.",
        "side_effects_summary": "Flushing, joint stiffness, water retention.",
        "protocol_summary": "350-500mcg total nightly, fasted.",
        "benefits_detailed": """
        - **Recomposition:** Powerful combo for changing body composition.
        - **Metabolic:** Amplifies the fat-burning effects of fasting.
        - **Synergy:** Ipamorelin extends the pulse duration of Tesamorelin.
        """,
        "protocol_detailed": """
        **Dosage:** 350mcg - 500mcg (Total Volume)

        **Frequency:** Daily (5 days on / 2 off)

        **Timing:** Before Bed (Fasted)

        **Cycle:** 8 to 12 Weeks

        **Study Note:** Monitor for water retention.
        """,
        "side_effects_detailed": "Joint pain, carpal tunnel numbness, flushing.",
        "storage": "Refrigerate."
    },
    "Tirzepatide": {
        "vial_mg": 30.0, "dose_mcg": 2500.0, 
        "type": "Metabolic (GLP-1/GIP)",
        "desc": "Dual Agonist (Mounjaro). GIP + GLP-1. Superior to Semaglutide.",
        "benefits_summary": "Massive weight loss, no food noise, less nausea.",
        "side_effects_summary": "Anhedonia, constipation, hair shedding.",
        "protocol_summary": "2.5mg weekly, titrate up.",
        "benefits_detailed": """
        - **Weight Loss:** 20%+ average loss in SURMOUNT-1 trials.
        - **Food Noise:** Eliminates obsessive food thoughts.
        - **Tolerability:** GIP component reduces nausea compared to Semaglutide.
        """,
        "protocol_detailed": """
        **Dosage:** Start 2.5mg -> Max 15mg

        **Frequency:** Once Weekly

        **Timing:** Any time

        **Cycle:** Continuous

        **Study Note:** Watch for 'anhedonia' (loss of interest in hobbies).
        """,
        "side_effects_detailed": "Anhedonia, cold extremities, constipation, hair shedding.",
        "storage": "Refrigerate. Do not freeze."
    },
}

FACTORS = {'mcg': 1, 'mg': 1000, 'g': 1000000}

# Initialize State
if 'vial_val' not in st.session_state: st.session_state.vial_val = 5.0
if 'dose_val' not in st.session_state: st.session_state.dose_val = 250.0
if 'stock_unit_index' not in st.session_state: st.session_state.stock_unit_index = 0
if 'dose_unit_index' not in st.session_state: st.session_state.dose_unit_index = 0
if 'dose_unit_selection' not in st.session_state: st.session_state.dose_unit_selection = "mcg"
if 'calc_count' not in st.session_state: st.session_state.calc_count = 0

# --- NAVIGATION SIDEBAR (v2.3 UI) ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/biotech.png", width=60) # Placeholder logo
    st.title("Navigation")
    page = st.radio("Go to:", ["🧮 Calculator", "📚 Peptide Database"])
    st.markdown("---")
    st.caption("v2.3 | by Musika")

# ==============================================================================
# PAGE 1: CALCULATOR
# ==============================================================================
if page == "🧮 Calculator":

    # --- LOGIC ---
    def load_preset():
        selection = st.session_state.peptide_selector
        data = PEPTIDE_PRESETS[selection]
        st.session_state.vial_val = float(data["vial_mg"])
        st.session_state.stock_unit_index = 0 
        target_mcg = float(data["dose_mcg"])
        if target_mcg < 1000:
            st.session_state.dose_unit_selection = "mcg"
            st.session_state.dose_val = target_mcg
        else:
            st.session_state.dose_unit_selection = "mg"
            st.session_state.dose_val = target_mcg / 1000
        st.session_state.calc_count += 1

    def convert_dose_unit():
        new_unit = st.session_state.dose_unit_selection
        old_unit = st.session_state.get("_prev_dose_unit", "mcg")
        current_val = st.session_state.dose_val
        val_in_mcg = current_val * FACTORS[old_unit]
        new_val = val_in_mcg / FACTORS[new_unit]
        st.session_state.dose_val = new_val
        st.session_state._prev_dose_unit = new_unit

    def get_mcg(value, unit):
        return value * FACTORS[unit]

    # --- UI HEADER ---
    st.subheader("🧪 Reconstitution Calculator")
    st.divider()

    # --- MAIN DASHBOARD ---
    left_col, right_col = st.columns([1, 1.2], gap="large")

    # === LEFT COLUMN: INPUTS & GUIDES ===
    with left_col:
        st.info("1️⃣ **Configuration**")
        
        selected_peptide = st.selectbox("Select Peptide Profile", list(PEPTIDE_PRESETS.keys()), key="peptide_selector", on_change=load_preset)
        
        st.write("📦 **Stock & Water**")
        c1, c2, c3 = st.columns([1.5, 1, 1.5])
        with c1:
            vial_qty = st.number_input("Stock Amount", key="vial_val", min_value=0.0, step=1.0, format="%.1f")
        with c2:
            vial_unit = st.selectbox("Unit", ["mg", "mcg", "g"], index=st.session_state.stock_unit_index, key="stock_unit_selection")
        with c3:
            water_ml = st.number_input("Water Added (mL)", value=2.0, step=0.5, min_value=0.1, format="%.1f")

        st.warning("⚠️ **Safety Check:** Ensure inputs match your physical supplies.")

        st.write("🎯 **Dosing**")
        c4, c5 = st.columns([2, 1])
        with c5:
            dose_unit = st.selectbox("Dose Unit", ["mcg", "mg", "g"], key="dose_unit_selection", on_change=convert_dose_unit)
            if "_prev_dose_unit" not in st.session_state: st.session_state._prev_dose_unit = dose_unit
        with c4:
            if dose_unit == 'mg':
                step, fmt = 1.0, "%.1f"
            elif dose_unit == 'mcg':
                step, fmt = 50.0, "%.1f"
            else:
                step, fmt = 0.001, "%.4f"
            desired_dose = st.number_input("Desired Dose", key="dose_val", min_value=0.0, step=step, format=fmt)
        
        syringe_type = st.radio("Syringe Type", ["U-100 (Standard)", "U-40 (Vet)"], horizontal=True)
        syringe_factor = 100 if "U-100" in syringe_type else 40

        st.divider()

        with st.expander("🛠️ How to Reconstitute (Mix)"):
            st.markdown(f"1. **Clean:** Wipe the top of the **{vial_qty} {vial_unit}** peptide vial and the water vial with an alcohol swab.\n2. **Withdraw:** Draw exactly **{water_ml} mL** of Bacteriostatic Water.\n3. **Inject:** Slowly inject the **{water_ml} mL** of water into the peptide vial. Aim for the glass wall, not the powder directly.\n4. **Mix:** **Do not shake.** Gently swirl the vial until dissolved.\n5. **Store:** Refrigerate immediately.")

        with st.expander("💉 Visual Guide: Injection Sites", expanded=True):
            try:
                st.image("injection_sites.png", caption="Recommended Subcutaneous Zones", use_container_width=True)
            except:
                st.warning("⚠️ Image not found. Please upload 'injection_sites.png' to your GitHub repository.")

    # === RIGHT COLUMN: RESULTS ===
    with right_col:
        st.success("2️⃣ **Profile & Results**")

        if vial_qty > 0 and water_ml > 0 and desired_dose > 0:
            total_peptide_mcg = get_mcg(vial_qty, vial_unit)
            desired_dose_mcg = get_mcg(desired_dose, dose_unit)
            concentration_mcg_ml = total_peptide_mcg / water_ml
            concentration_mg_ml = concentration_mcg_ml / 1000
            draw_ml = desired_dose_mcg / concentration_mcg_ml
            units = draw_ml * syringe_factor
            doses_per_vial = total_peptide_mcg / desired_dose_mcg
            peptide_info = PEPTIDE_PRESETS[selected_peptide]

            # --- CALCULATOR VIEW (SUMMARIZED) ---
            with st.expander(f"📖 **Profile: {selected_peptide}**", expanded=True):
                if selected_peptide == "Custom (Enter manually)":
                     st.write("Manual mode selected.")
                else:
                    st.markdown(f"**Type:** {peptide_info['type']}")
                    # Use Summarized Data for Calc View
                    st.markdown(f"**🌟 Key Benefits:** {peptide_info['benefits_summary']}")
                    st.warning(f"**⚠️ Common Side Effects:** {peptide_info['side_effects_summary']}")
                    st.info(f"**📋 Quick Protocol:** {peptide_info['protocol_summary']}")
                    st.markdown(f"**❄️ Storage:** {peptide_info['storage']}")
                    st.caption("*For full details, visit the 'Peptide Database' tab.*")

            st.divider()

            c1, c2, c3 = st.columns(3)
            c1.metric("Draw Volume", f"{draw_ml:.4f} mL")
            c2.metric("Syringe Units", f"{units:.1f} Units")
            c3.metric("Doses / Vial", f"{int(doses_per_vial)}")
            
            percentage = min(units / syringe_factor * 100, 100)
            
            if units > syringe_factor:
                num_injections = math.ceil(units / syringe_factor)
                dose_per = units / num_injections
                st.error(f"⚠️ **Volume too large for one syringe!**")
                st.warning(f"💡 **Recommendation:** Split into **{num_injections}** injections of **{dose_per:.1f} Units** each.")
                st.markdown(f"""<div style="margin-bottom:5px; font-weight:bold;">Visual Fill (1 Full Syringe + Overflow):</div><div class="syringe-container"><div class="syringe-liquid" style="width: 100%; background-color: #ff0000;"></div><div class="syringe-markings"></div></div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style="margin-bottom:5px; font-weight:bold;">Visual Syringe Fill ({units:.1f} Units):</div><div class="syringe-container"><div class="syringe-liquid" style="width: {percentage}%;"></div><div class="syringe-markings"></div></div>""", unsafe_allow_html=True)
                st.caption(f"Draw to the **{units:.1f}** mark on your {syringe_type} syringe.")

            protocol_text = f"Peptide: {selected_peptide}\nType: {peptide_info['type']}\nStock: {vial_qty}{vial_unit} + {water_ml}mL Water\nConc: {concentration_mg_ml:.2f} mg/mL\nDose: {desired_dose}{dose_unit} = {units:.1f} Units ({syringe_type})\nSupply: 1 vial lasts approx {int(doses_per_vial)} doses.\n\nQuick Protocol: {peptide_info['protocol_summary']}\nBenefits: {peptide_info['benefits_summary']}\nStorage: {peptide_info['storage']}"
            st.download_button("💾 Save Protocol", protocol_text, "protocol.txt", use_container_width=True)
        else:
            st.info("Enter inputs to see results.")

    st.divider()
    c_foot1, c_foot2 = st.columns([1,1])
    with c_foot1:
        st.caption(f"🔢 Calculations performed this session: **{st.session_state.calc_count}**")
    with c_foot2:
        st.markdown("[![Hits](https://hits.sh/peptide-calculator.streamlit.app.svg?style=flat-square&label=Total%20Visits&extraCount=2023&color=79c83d)](https://hits.sh/peptide-calculator.streamlit.app/)")

# ==============================================================================
# PAGE 2: PEPTIDE DATABASE (Notion-Style / v2.3)
# ==============================================================================
elif page == "📚 Peptide Database":
    st.subheader("📚 Peptide Database")
    st.caption("Comprehensive clinical data, mechanisms, and protocols. *Disclaimer: For educational purposes only.*")
    st.divider()

    # Get all peptides except the "Custom" entry
    db_items = {k: v for k, v in PEPTIDE_PRESETS.items() if k != "Custom (Enter manually)"}

    # Extract unique categories for the filter
    all_types = sorted(list(set([v['type'] for v in db_items.values()])))
    all_types.insert(0, "All")

    # Filters
    col_search, col_filter = st.columns([3, 1])
    with col_search:
        search_query = st.text_input("🔍 Search Peptides", placeholder="Search by name, benefit, or type...").lower()
    with col_filter:
        category_filter = st.selectbox("🏷️ Filter by Category", all_types)

    st.markdown("---")

    # Filter Logic
    filtered_items = {}
    for name, data in db_items.items():
        # Match Category
        if category_filter != "All" and data['type'] != category_filter:
            continue
        # Match Search
        if search_query not in name.lower() and search_query not in data['benefits_detailed'].lower() and search_query not in data['desc'].lower():
            continue
        filtered_items[name] = data

    # Display Grid (3 columns)
    num_cols = 3
    cols = st.columns(num_cols)
    
    for idx, (name, info) in enumerate(filtered_items.items()):
        col = cols[idx % num_cols]
        with col:
            # Replicating Notion Card Style
            with st.container(border=True):
                st.markdown(f"### {name}")
                st.markdown(f"<span class='db-tag'>{info['type']}</span>", unsafe_allow_html=True)
                st.write("") # Spacer
                
                # VISIBLE IMMEDIATELY: Benefits & Side Effects
                st.markdown("**🌟 Clinical Benefits:**")
                st.markdown(info['benefits_detailed'])
                
                st.markdown(f"""
                <div class='side-effect-box'>
                <strong>⚠️ Side Effects:</strong><br>{info['side_effects_detailed']}
                </div>
                """, unsafe_allow_html=True)
                
                st.write("")

                # COLLAPSIBLE: Description & Mechanism
                with st.expander("ℹ️ Description & Mechanism"):
                    st.markdown(f"_{info['desc']}_")
                    st.markdown(f"**❄️ Storage:** {info['storage']}")
                
                # COLLAPSIBLE: Detailed Protocol
                with st.expander("📋 Detailed Protocol"):
                     st.markdown(info['protocol_detailed'])

    if len(filtered_items) == 0:
        st.warning("No peptides match your search criteria. Try clearing the filters.")

# --- UNIVERSAL DISCLAIMER ---
st.markdown("---")
st.caption("⚠️ **Medical Disclaimer:** This tool is for educational and informational purposes only and does not constitute medical advice. Always verify calculations with a professional. The developers assume no liability for errors or misuse.")
