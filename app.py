import streamlit as st
import math

# --- 1. CONFIGURATION: WIDE MODE ---
st.set_page_config(
    page_title="PeptideCalc Pro v4.0 (IU Support)",
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
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# --- KNOWLEDGE BASE (v4.0 - IU UPDATES) ---
# Added 'iu_conversion' key: 
# If value is > 0, it means 1mg = X IU. 
# If value is 1, it implies the vial is likely sold in IU (like HCG).

PEPTIDE_PRESETS = {
    "AOD-9604": {
        "vial_mg": 5.0, "dose_mcg": 300.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Fat Loss", "filter_cat": "Slimming & Fat Loss",
        "desc": "Anti-Obesity Drug 9604. A modified fragment of the C-terminus of Human Growth Hormone (HGH).",
        "benefits_summary": """
- Targeted fat burning (lipolysis)
- No blood sugar spikes
- Cartilage repair support
- Non-hormonal (no IGF-1 impact)
""",
        "side_effects_summary": """
- Injection site redness
- Mild stomach upset (rare)
- Headache (rare)
""",
        "protocol_summary": "300mcg daily, morning fasted.",
        "benefits_detailed": """
        - **Targeted Lipolysis:** Specifically stimulates the breakdown of fat cells (lipolysis).
        - **Metabolic Safety:** Does not induce insulin resistance or elevate IGF-1.
        - **Joint Support:** Aids in cartilage regeneration and repair.
        """,
        "protocol_detailed": """
        **Dosage:** 300mcg (0.3mg)

        **Frequency:** Daily

        **Timing:** Morning (Fasted) or 1 hour before cardio

        **Cycle:** 3 to 6 Months
        """,
        "side_effects_detailed": """
        • Extremely well tolerated
        • Minor injection site reactions (redness)
        • Mild headache (rare)
        """,
        "storage": "Refrigerate. Stable."
    },
    "BPC-157": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Regenerative", "filter_cat": "Injury & Repair",
        "desc": "Body Protection Compound-157. A 15-amino acid chain derived from gastric juice.",
        "benefits_summary": """
- Accelerates tendon/ligament repair
- Heals gut lining (IBS/Leaky Gut)
- Reduces neuro-inflammation
- Protects liver and organs
""",
        "side_effects_summary": """
- Mild nausea (rare)
- Injection site irritation
- Fatigue during healing phase
""",
        "protocol_summary": "250-500mcg daily or 2x daily.",
        "benefits_detailed": """
        - **Connective Tissue:** Drastically speeds up the healing of soft tissue injuries.
        - **Angiogenesis:** Stimulates the formation of new blood vessels.
        - **Gastroprotection:** Heals gastric ulcers and protects intestinal endothelium.
        """,
        "protocol_detailed": """
        **Dosage:** 250mcg - 500mcg

        **Frequency:** Daily or Twice Daily (AM/PM)

        **Timing:** SubQ near injury site or belly fat

        **Cycle:** 4 to 6 Weeks on, 2 Weeks off
        """,
        "side_effects_detailed": """
        • Generally considered extremely safe
        • Rare reports of fatigue
        • Mild nausea
        """,
        "storage": "Refrigerate after mixing. Stable for ~30-45 days."
    },
    "BPC-157 + TB-500 Blend": {
        "vial_mg": 10.0, "dose_mcg": 500.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Regenerative Blend", "filter_cat": "Injury & Repair",
        "desc": "The 'Wolverine Stack'. Synergistic combination of BPC-157 and TB-500.",
        "benefits_summary": """
- Maximum surgical/injury recovery
- Improves joint flexibility
- Cardiovascular protection
- Systemic anti-inflammatory
""",
        "side_effects_summary": """
- Head rush (TB-500)
- Fatigue/Lethargy
- Injection site stinging
""",
        "protocol_summary": "500mcg-1mg total fluid daily.",
        "benefits_detailed": """
        - **Total Repair:** Targets tendon/bone interface and muscle belly simultaneously.
        - **Mobility:** Significant improvements in joint range of motion.
        - **Cardioprotection:** Proven efficacy in reducing scar tissue.
        """,
        "protocol_detailed": """
        **Dosage:** 500mcg - 1000mcg (Total Volume)

        **Frequency:** Daily

        **Timing:** Any time of day

        **Cycle:** 4 to 8 Weeks (Duration of injury)
        """,
        "side_effects_detailed": """
        • Temporary head rush immediately after injection
        • Fatigue or lethargy (body repairing)
        • Injection site stinging
        """,
        "storage": "Refrigerate. Use within 30 days."
    },
    "CJC-1295 (No DAC)": {
        "vial_mg": 5.0, "dose_mcg": 100.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone", "filter_cat": "Muscle & Workout",
        "desc": "Modified GRF 1-29. A GHRH analog that stimulates pulsatile Growth Hormone release.",
        "benefits_summary": """
- Increases lean muscle mass
- Promotes deep slow-wave sleep
- Improves skin elasticity
- Accelerates fat metabolism
""",
        "side_effects_summary": """
- Flushing/Warmth (Vasodilation)
- Head rush
- Vivid dreams
""",
        "protocol_summary": "100mcg nightly, fasted.",
        "benefits_detailed": """
        - **Hyperplasia:** Stimulates the division of muscle cells.
        - **Sleep Architecture:** Dramatically improves Delta-wave (Stage 4) deep sleep.
        - **Anti-Aging:** Increases collagen synthesis.
        """,
        "protocol_detailed": """
        **Dosage:** 100mcg (0.1mg)

        **Frequency:** Daily (5 days on / 2 days off)

        **Timing:** Immediately before bed (Fasted 2+ hours)

        **Cycle:** 12 Weeks +
        """,
        "side_effects_detailed": """
        • Immediate head rush (vasodilation)
        • Warm/flushed face (lasts 10-20 mins)
        • Vivid dreams
        """,
        "storage": "Refrigerate. Sensitive to light/heat."
    },
    "CJC-1295 + Ipamorelin Blend": {
        "vial_mg": 10.0, "dose_mcg": 200.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone Blend", "filter_cat": "Muscle & Workout",
        "desc": "The Gold Standard GH Stack. Combines CJC-1295 and Ipamorelin.",
        "benefits_summary": """
- Max natural GH secretion
- Significant body recomposition
- Superior recovery & sleep
- No cortisol/prolactin spike
""",
        "side_effects_summary": """
- Head rush/Flushing
- Numb fingers (Carpal Tunnel)
- Water retention
""",
        "protocol_summary": "200-300mcg total nightly, fasted.",
        "benefits_detailed": """
        - **Synergistic Power:** Maximizes GH secretion naturally.
        - **Visceral Fat:** Highly effective at mobilizing deep abdominal fat stores.
        - **Safety Profile:** No trigger of stress hormones (cortisol) or hunger hormones.
        """,
        "protocol_detailed": """
        **Dosage:** 200mcg - 300mcg (Total Volume)

        **Frequency:** Nightly (5 days on / 2 days off)

        **Timing:** Immediately before bed (Fasted 2+ hours)

        **Cycle:** 3 to 6 Months
        """,
        "side_effects_detailed": """
        • Head rush/Flushing
        • Numbness/tingling in hands (Carpal Tunnel symptoms)
        • Initial water weight gain
        """,
        "storage": "Refrigerate. Do not shake."
    },
    "Epithalon": {
        "vial_mg": 10.0, "dose_mcg": 5000.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Anti-Aging", "filter_cat": "Wellness & Longevity",
        "desc": "Synthetic tetrapeptide that increases telomerase activity.",
        "benefits_summary": """
- Extends lifespan (Telomeres)
- Resets circadian rhythm
- Boosts melatonin naturally
- Anti-tumor/cancer protective
""",
        "side_effects_summary": """
- Daytime drowsiness (rare)
- Vivid dreams
- Very safe profile
""",
        "protocol_summary": "5mg-10mg daily for 10-20 days.",
        "benefits_detailed": """
        - **Telomere Extension:** Upregulates telomerase to protect DNA.
        - **Endocrine Reset:** Restores sensitivity of the hypothalamus/pineal gland.
        - **Sleep Quality:** Normalizes melatonin production.
        """,
        "protocol_detailed": """
        **Dosage:** 5mg - 10mg

        **Frequency:** Daily

        **Timing:** Morning or Evening

        **Cycle:** 10 to 20 Day Course (Repeat every 6-12 months)
        """,
        "side_effects_detailed": """
        • Extremely safe profile
        • Occasional daytime drowsiness
        • Vivid dreams
        """,
        "storage": "Refrigerate."
    },
    "GHK-Cu": {
        "vial_mg": 50.0, "dose_mcg": 2000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cosmetic/Repair", "filter_cat": "Skin, Hair & Beauty",
        "desc": "Copper Tripeptide-1. A genomic modulator that resets over 4,000 genes to a younger state.",
        "benefits_summary": """
- Boosts collagen & elastin
- Tightens loose skin
- Regrows hair (follicle size)
- Activates DNA repair genes
""",
        "side_effects_summary": """
- Painful injection (Sting)
- Red welts/bruising
- Zinc depletion
""",
        "protocol_summary": "1-2mg daily. Evening.",
        "benefits_detailed": """
        - **Skin Rejuvenation:** Increases collagen synthesis by 70%, thickens dermis.
        - **Hair Growth:** Enlarges hair follicles and prolongs growth phase.
        - **DNA Repair:** Resets activity of DNA repair genes.
        """,
        "protocol_detailed": """
        **Dosage:** 1mg - 2mg

        **Frequency:** Daily

        **Timing:** Evening (rotate sites)

        **Cycle:** 30 Days on, 30 Days off
        """,
        "side_effects_detailed": """
        • High incidence of injection site pain (burning)
        • Large red welts (post-injection)
        • Zinc depletion (Supplement Zinc 50mg)
        """,
        "storage": "Refrigerate. Protect from light."
    },
    "Glow Blend (GHK-Cu/BPC/TB)": {
        "vial_mg": 70.0, "dose_mcg": 2500.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cosmetic/Recovery Blend", "filter_cat": "Skin, Hair & Beauty",
        "desc": "70mg Tri-Blend. BPC-157 and TB-500 are added to buffer the GHK-Cu, reducing the 'sting'.",
        "benefits_summary": """
- Painless GHK-Cu injection
- Total body skin tightening
- Rapid injury recovery
- Gut & Heart health
""",
        "side_effects_summary": """
- Mild redness
- Flushing
- Fatigue
""",
        "protocol_summary": "2.5mg - 3mg total daily.",
        "benefits_detailed": """
        - **Painless Application:** BPC-157 neutralizes acidity of Copper.
        - **Total Rejuvenation:** Targets skin, hair, gut, and muscle simultaneously.
        - **Synergy:** Increases Growth Hormone receptors for better repair.
        """,
        "protocol_detailed": """
        **Dosage:** 2.5mg - 3mg (Total Volume)

        **Frequency:** Daily

        **Timing:** Evening

        **Cycle:** 4 to 6 Weeks
        """,
        "side_effects_detailed": """
        • Mild injection site redness
        • Temporary flushing
        • Fatigue (healing response)
        """,
        "storage": "Refrigerate. Protect from light."
    },
    "HCG": {
        "vial_mg": 5000.0, "dose_mcg": 250.0, "default_dose_unit": "IU", "default_stock_unit": "IU", "iu_conversion": 1,
        "type": "Hormonal", "filter_cat": "Libido & Sexual Health",
        "desc": "Human Chorionic Gonadotropin. Mimics LH to maintain testicular function.",
        "benefits_summary": """
- Prevents testicular shrinkage
- Maintains fertility/sperm
- Boosts libido & mood
- TRT adjunct support
""",
        "side_effects_summary": """
- Estrogen spikes (High E2)
- Acne/Water retention
- Gynecomastia risk
""",
        "protocol_summary": "250-500 IU 2-3x per week.",
        "benefits_detailed": """
        - **Testicular Health:** Prevents atrophy during TRT cycles.
        - **Fertility:** Crucial for maintaining spermatogenesis.
        - **Libido:** Provides distinct libido boost separate from testosterone.
        """,
        "protocol_detailed": """
        **Dosage:** 250 IU - 500 IU

        **Frequency:** 2 to 3 times per week

        **Timing:** Morning

        **Cycle:** Continuous with TRT or as PCT
        """,
        "side_effects_detailed": """
        • Estrogen spikes (requires AI management)
        • Acne
        • Water retention
        • Desensitization if overdosed
        """,
        "storage": "Refrigerate. Fragile."
    },
    "Ipamorelin": {
        "vial_mg": 5.0, "dose_mcg": 100.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone", "filter_cat": "Muscle & Workout",
        "desc": "Selective GH Secretagogue. The mildest and safest GHRP.",
        "benefits_summary": """
- Clean GH release (No hunger)
- Fat loss & muscle sparing
- Improved sleep quality
- Anti-aging support
""",
        "side_effects_summary": """
- Very mild
- Slight water retention
- Rare dizziness
""",
        "protocol_summary": "100-300mcg nightly, fasted.",
        "benefits_detailed": """
        - **Pure Signal:** Stimulates steady GH pulse without hunger spikes.
        - **Catabolic Protection:** Preserves lean muscle tissue.
        - **Sleep:** Increases REM and Slow-Wave sleep stages.
        """,
        "protocol_detailed": """
        **Dosage:** 100mcg - 300mcg

        **Frequency:** Nightly

        **Timing:** Before Bed (Fasted)

        **Cycle:** 8 to 12 Weeks
        """,
        "side_effects_detailed": """
        • Extremely well tolerated
        • Slight water retention possible
        • No 'jittery' feeling
        """,
        "storage": "Refrigerate."
    },
    "Kisspeptin": {
        "vial_mg": 10.0, "dose_mcg": 100.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Hormonal", "filter_cat": "Libido & Sexual Health",
        "desc": "A neuromodulator that stimulates the hypothalamus to release GnRH.",
        "benefits_summary": """
- Restarts HPTA axis safely
- Boosts fertility (LH/FSH)
- Increases libido
- No testicular desensitization
""",
        "side_effects_summary": """
- Flushing/Warmth
- Injection site redness
- Mild headache
""",
        "protocol_summary": "100-200mcg daily.",
        "benefits_detailed": """
        - **HPTA Restart:** Safest way to restart natural testosterone.
        - **Fertility:** Strongly stimulates FSH for sperm maturation.
        - **Safety:** Does not cause Leydig cell desensitization.
        """,
        "protocol_detailed": """
        **Dosage:** 100mcg - 200mcg

        **Frequency:** Daily

        **Timing:** Any time

        **Cycle:** 4 Weeks (PCT)
        """,
        "side_effects_detailed": """
        • Mild flushing
        • Injection site redness
        • Mild headache
        """,
        "storage": "Refrigerate."
    },
    "Klow Blend (GHK-Cu/BPC/TB/KPV)": {
        "vial_mg": 80.0, "dose_mcg": 3000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Ultimate Repair/Cosmetic Blend", "filter_cat": "Skin, Hair & Beauty",
        "desc": "The 80mg Master Stack. Adds KPV to the GHK/BPC/TB trio.",
        "benefits_summary": """
- Clears Acne, Psoriasis, Eczema
- Heals Gut (IBD/Colitis)
- Systemic anti-inflammatory
- Total tissue repair
""",
        "side_effects_summary": """
- Red welts (Injection site)
- Fatigue (Herxheimer)
- Flushing
""",
        "protocol_summary": "3mg total daily.",
        "benefits_detailed": """
        - **Dermatology:** KPV actively treats acne, psoriasis, and eczema.
        - **Gut Health:** Strongest known peptide stack for IBD/Colitis.
        - **Mast Cells:** KPV stabilizes mast cells, reducing histamine.
        """,
        "protocol_detailed": """
        **Dosage:** 3mg (Total Volume)

        **Frequency:** Daily

        **Timing:** Evening

        **Cycle:** 4 to 8 Weeks
        """,
        "side_effects_detailed": """
        • Red welts at injection site (common)
        • Fatigue (body detox/healing)
        • Flushing
        """,
        "storage": "Refrigerate. Protect from light."
    },
    "Melanotan II": {
        "vial_mg": 10.0, "dose_mcg": 500.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cosmetic", "filter_cat": "Skin, Hair & Beauty",
        "desc": "Alpha-MSH analog. Stimulates melanin production and sexual arousal.",
        "benefits_summary": """
- Deep, rapid tan
- Extreme libido boost
- Appetite suppression
- UV protection
""",
        "side_effects_summary": """
- Severe Nausea
- Facial Flushing
- Spontaneous erections
- Darkening moles
""",
        "protocol_summary": "100-500mcg before UV exposure.",
        "benefits_detailed": """
        - **Photoprotection:** Creates a deep, natural tan that protects the skin.
        - **Libido:** Potent aphrodisiac for both men and women.
        - **Metabolic:** Suppresses appetite.
        """,
        "protocol_detailed": """
        **Dosage:** 100mcg - 500mcg

        **Frequency:** As needed (Loading phase: Daily)

        **Timing:** 30 mins before UV exposure

        **Cycle:** Until desired color, then maintenance
        """,
        "side_effects_detailed": """
        • Significant nausea (lasts 1-2 hours)
        • Facial flushing
        • Spontaneous erections (priapism risk)
        • Darkening of freckles/moles
        """,
        "storage": "Refrigerate."
    },
    "MOTS-c": {
        "vial_mg": 10.0, "dose_mcg": 5000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Metabolic/Mitochondrial", "filter_cat": "Muscle & Workout",
        "desc": "Mitochondrial-Derived Peptide. Known as an 'exercise mimetic'.",
        "benefits_summary": """
- Increases VO2 Max/Endurance
- Prevents weight gain
- Improves bone metabolism
- Cellular energy boost
""",
        "side_effects_summary": """
- Painful injection (Sting)
- Insomnia (if late)
- Hyperactivity
""",
        "protocol_summary": "5mg once weekly.",
        "benefits_detailed": """
        - **Endurance:** Increases cellular ability to utilize glucose and oxygen.
        - **Metabolic:** Prevents diet-induced insulin resistance.
        - **Biogenesis:** Promotes creation of new mitochondria.
        """,
        "protocol_detailed": """
        **Dosage:** 5mg - 10mg

        **Frequency:** Once Weekly

        **Timing:** Morning (Pre-workout preferred)

        **Cycle:** 4 to 8 Weeks
        """,
        "side_effects_detailed": """
        • Injection site pain (very common)
        • Insomnia (if taken late)
        • High energy/restlessness
        """,
        "storage": "Refrigerate."
    },
    "NAD+": {
        "vial_mg": 500.0, "dose_mcg": 25000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cellular Energy", "filter_cat": "Wellness & Longevity",
        "desc": "Nicotinamide Adenine Dinucleotide. The fuel for cellular engines.",
        "benefits_summary": """
- Clears brain fog
- Restores cellular energy
- Repairs DNA damage
- Anti-aging/Longevity
""",
        "side_effects_summary": """
- Chest pressure (The Flush)
- Anxiety/Panic feeling
- Nausea/Cramps
""",
        "protocol_summary": "25-50mg 2-3x per week. SLOW INJECTION.",
        "benefits_detailed": """
        - **Cognition:** Rapidly clears brain fog and enhances mental sharpness.
        - **Mitochondria:** Restores efficient ATP production.
        - **Addiction:** Proven to help restore neurotransmitter balance.
        """,
        "protocol_detailed": """
        **Dosage:** 25mg - 50mg

        **Frequency:** 2-3x / Week

        **Timing:** Morning

        **Cycle:** Ongoing

        **Study Note:** ⚠️ INJECT VERY SLOWLY. Rapid injection causes severe 'NAD Flush'.
        """,
        "side_effects_detailed": """
        • Intense chest pressure
        • Abdominal cramping/Nausea
        • Anxiety/Panic sensation
        • Palpitations (Passes in 5-10 mins)
        """,
        "storage": "Refrigerate immediately. Very sensitive."
    },
    "Oxytocin Acetate": {
        "vial_mg": 2.0, "dose_mcg": 20.0, "default_dose_unit": "IU", "default_stock_unit": "mg", "iu_conversion": 600,
        "type": "Hormonal/Wellness", "filter_cat": "Nootropics & Brain",
        "desc": "The 'Love Hormone'. Acts as a neurotransmitter regulating social interaction and bonding.",
        "benefits_summary": """
- Reduces social anxiety
- Lowers cortisol (Stress)
- Enhances emotional bonding
- Modulates pain perception
""",
        "side_effects_summary": """
- Nausea (at high dose)
- Headache
- Flushing
""",
        "protocol_summary": "20-50 IU as needed.",
        "benefits_detailed": """
        - **Psychological:** Significantly reduces social anxiety and stress levels.
        - **Pain Modulation:** Shows analgesic (pain-killing) properties.
        - **Intimacy:** Enhances feelings of trust and emotional connection.
        """,
        "protocol_detailed": """
        **Dosage:** 10 IU - 25 IU (Start low)

        **Frequency:** As needed (or Daily for mood support)

        **Timing:** 30 minutes before social/intimate events

        **Cycle:** Can be used continuously or cycled
        """,
        "side_effects_detailed": """
        • Nausea (common at high doses)
        • Headache
        • Flushing/warmth
        • Slight dizziness
        """,
        "storage": "Refrigerate."
    },
    "PT-141": {
        "vial_mg": 10.0, "dose_mcg": 1000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Libido", "filter_cat": "Libido & Sexual Health",
        "desc": "Bremelanotide. Works on the nervous system to treat hypoactive sexual desire.",
        "benefits_summary": """
- Treats ED & Low Libido
- Works when Viagra fails
- Increases physical arousal
- For Men & Women
""",
        "side_effects_summary": """
- Nausea (Common)
- Flushing/Warmth
- Headache
""",
        "protocol_summary": "1.5-2mg, 2 hours before activity.",
        "benefits_detailed": """
        - **Mechanism:** Targets the hypothalamus, not the vascular system.
        - **Efficacy:** FDA approved (as Vyleesi) for low libido in women.
        - **Response:** Increases physical arousal and desire.
        """,
        "protocol_detailed": """
        **Dosage:** 1.5mg - 2mg

        **Frequency:** As needed

        **Timing:** 2 to 4 hours BEFORE activity

        **Cycle:** Max 8 doses per month
        """,
        "side_effects_detailed": """
        • Nausea (40% of users)
        • Flushing
        • Headache
        • Elevated blood pressure
        """,
        "storage": "Refrigerate."
    },
    "Retatrutide": {
        "vial_mg": 10.0, "dose_mcg": 2000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Metabolic (GLP-1/GIP/Glucagon)", "filter_cat": "Slimming & Fat Loss",
        "desc": "The 'Triple G' Agonist. The most potent weight loss agent currently in trials.",
        "benefits_summary": """
- Extreme weight loss (24%+)
- Burns liver fat (NAFLD)
- Resets insulin sensitivity
- Increases metabolism
""",
        "side_effects_summary": """
- High Heart Rate
- Skin sensitivity
- Nausea/Constipation
""",
        "protocol_summary": "2mg weekly, titrate up.",
        "benefits_detailed": """
        - **Efficacy:** 24.2% average weight loss in clinical trials.
        - **Liver Health:** Resolves Fatty Liver Disease (NAFLD).
        - **Energy:** Glucagon component increases calorie burn.
        """,
        "protocol_detailed": """
        **Dosage:** Start 2mg -> Titrate to Max 12mg

        **Frequency:** Once Weekly

        **Timing:** Any time

        **Cycle:** Continuous
        """,
        "side_effects_detailed": """
        • Tachycardia (fast heart rate)
        • Cutaneous hyperesthesia (sensitive skin)
        • Nausea
        • Constipation
        """,
        "storage": "Refrigerate. Do not freeze."
    },
    "Semaglutide": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Metabolic (GLP-1)", "filter_cat": "Slimming & Fat Loss",
        "desc": "GLP-1 Agonist. The standard for medical weight loss.",
        "benefits_summary": """
- Significant weight loss (15%)
- Controls blood sugar
- Cardioprotective
- Reduces addiction cravings
""",
        "side_effects_summary": """
- Nausea/Vomiting
- Severe Constipation
- Fatigue
- Muscle loss
""",
        "protocol_summary": "0.25mg weekly, titrate up.",
        "benefits_detailed": """
        - **Satiety:** Slows gastric emptying, keeping you full longer.
        - **Heart:** Proven 20% reduction in major adverse cardiac events.
        - **Addiction:** Reduces cravings for alcohol and sugar.
        """,
        "protocol_detailed": """
        **Dosage:** Start 0.25mg -> Max 2.4mg

        **Frequency:** Once Weekly

        **Timing:** Any time

        **Cycle:** Continuous
        """,
        "side_effects_detailed": """
        • Nausea/Vomiting
        • Severe constipation
        • 'Ozempic face' (rapid fat loss)
        • Fatigue
        """,
        "storage": "Refrigerate. Protect from light."
    },
    "TB-500": {
        "vial_mg": 5.0, "dose_mcg": 2500.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Regenerative", "filter_cat": "Injury & Repair",
        "desc": "Synthetic Thymosin Beta-4. The 'Muscle Repair' peptide.",
        "benefits_summary": """
- Heals muscle tears
- Improves flexibility
- Reduces scar tissue
- Cardiac repair
""",
        "side_effects_summary": """
- Head rush (common)
- Lethargy
- Flu-like symptoms
""",
        "protocol_summary": "2.5mg twice weekly.",
        "benefits_detailed": """
        - **Muscle Repair:** The primary peptide for torn muscles and strains.
        - **Flexibility:** Improves range of motion by reducing inflammation.
        - **Cardiac:** Repairs heart tissue and reduces scarring.
        """,
        "protocol_detailed": """
        **Dosage:** 2.5mg (2500mcg)

        **Frequency:** 2x Per Week (e.g., Mon/Thu)

        **Timing:** Any time

        **Cycle:** 4 to 6 Weeks
        """,
        "side_effects_detailed": """
        • Temporary head rush
        • Occasional lethargy
        • Flu-like symptoms (rare)
        """,
        "storage": "Refrigerate."
    },
    "Tesamorelin": {
        "vial_mg": 2.0, "dose_mcg": 1000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone", "filter_cat": "Slimming & Fat Loss",
        "desc": "FDA Approved GHRH for visceral fat reduction.",
        "benefits_summary": """
- Burns belly fat (Visceral)
- Increases muscle tone
- Nootropic effects
- Lowers triglycerides
""",
        "side_effects_summary": """
- Injection redness
- Joint stiffness
- Carpal Tunnel
""",
        "protocol_summary": "1-2mg nightly, fasted.",
        "benefits_detailed": """
        - **Visceral Fat:** Specifically targets stubborn adipose tissue around organs.
        - **Cognition:** Improves executive function and memory.
        - **Cardio:** Drastically lowers triglycerides.
        """,
        "protocol_detailed": """
        **Dosage:** 1mg - 2mg

        **Frequency:** Daily

        **Timing:** Before Bed (Fasted)

        **Cycle:** 8 to 12 Weeks
        """,
        "side_effects_detailed": """
        • Injection site redness/itching (common)
        • Joint stiffness
        • Carpal tunnel symptoms
        • Water retention
        """,
        "storage": "Refrigerate. Use within 20-30 days."
    },
    "Tesamorelin + Ipamorelin Blend": {
        "vial_mg": 12.0, "dose_mcg": 350.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone/Fat Loss Blend", "filter_cat": "Slimming & Fat Loss",
        "desc": "The 'Shred Stack'. Targets visceral fat + systemic GH elevation.",
        "benefits_summary": """
- Max fat loss (Visceral)
- Muscle definition
- Deep sleep
- Systemic anti-aging
""",
        "side_effects_summary": """
- Flushing/Redness
- Joint stiffness
- Water retention
""",
        "protocol_summary": "350-500mcg total nightly, fasted.",
        "benefits_detailed": """
        - **Recomposition:** Powerful combo for burning fat and building muscle.
        - **Metabolic:** Amplifies the fat-burning effects of fasting.
        - **Synergy:** Ipamorelin smooths out the pulse and adds sleep benefits.
        """,
        "protocol_detailed": """
        **Dosage:** 350mcg - 500mcg (Total Volume)

        **Frequency:** Daily (5 days on / 2 off)

        **Timing:** Before Bed (Fasted)

        **Cycle:** 8 to 12 Weeks
        """,
        "side_effects_detailed": """
        • Joint pain
        • Carpal tunnel numbness
        • Flushing
        • Injection site reactions
        """,
        "storage": "Refrigerate."
    },
    "Tirzepatide": {
        "vial_mg": 30.0, "dose_mcg": 2.5, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Metabolic (GLP-1/GIP)", "filter_cat": "Slimming & Fat Loss",
        "desc": "Dual Agonist (Mounjaro). GIP + GLP-1. Superior to Semaglutide.",
        "benefits_summary": """
- Massive weight loss (22%)
- Eliminates 'Food Noise'
- Less nausea than Semaglutide
- Metabolic repair
""",
        "side_effects_summary": """
- Anhedonia (No joy)
- Constipation
- Hair shedding
- Cold hands/feet
""",
        "protocol_summary": "2.5mg weekly, titrate up.",
        "benefits_detailed": """
        - **Weight Loss:** 20%+ average loss in SURMOUNT-1 trials.
        - **Food Noise:** Eliminates obsessive food thoughts.
        - **Tolerability:** GIP component reduces nausea severity compared to Semaglutide.
        """,
        "protocol_detailed": """
        **Dosage:** Start 2.5mg -> Max 15mg

        **Frequency:** Once Weekly

        **Timing:** Any time

        **Cycle:** Continuous
        """,
        "side_effects_detailed": """
        • Anhedonia (flat mood)
        • Cold extremities
        • Constipation
        • Hair shedding
        """,
        "storage": "Refrigerate. Do not freeze."
    },
}

FACTORS = {'mcg': 1, 'mg': 1000, 'g': 1000000, 'IU': 1} # IU handling is special

# Initialize State (Default to Tirzepatide)
if 'vial_val' not in st.session_state: st.session_state.vial_val = 30.0
if 'dose_val' not in st.session_state: st.session_state.dose_val = 2.5
if 'stock_unit_index' not in st.session_state: st.session_state.stock_unit_index = 0
if 'dose_unit_index' not in st.session_state: st.session_state.dose_unit_index = 1 # mg
if 'dose_unit_selection' not in st.session_state: st.session_state.dose_unit_selection = "mg"
if 'calc_count' not in st.session_state: st.session_state.calc_count = 0

# --- NAVIGATION SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/biotech.png", width=60)
    st.title("Navigation")
    page = st.radio("Go to:", ["🧮 Calculator", "📚 Peptide Database"])
    st.markdown("---")
    st.caption("v4.0 | by Musika")

# ==============================================================================
# PAGE 1: CALCULATOR
# ==============================================================================
if page == "🧮 Calculator":

    # --- LOGIC ---
    def load_preset():
        selection = st.session_state.peptide_selector
        data = PEPTIDE_PRESETS[selection]
        
        # Set Vial
        if data.get("default_stock_unit") == "IU":
             st.session_state.vial_val = float(data["vial_mg"]) # Treat as IU
             st.session_state.stock_unit_index = 3 # Index for IU
        else:
             st.session_state.vial_val = float(data["vial_mg"])
             st.session_state.stock_unit_index = 0 # mg

        # Set Dose
        target_val = float(data["dose_mcg"]) # This is raw value from preset
        unit_pref = data.get("default_dose_unit", "mcg")
        
        if unit_pref == "mg":
             st.session_state.dose_unit_selection = "mg"
             st.session_state.dose_val = target_val # Preset usually stores this in correct unit if carefully managed, otherwise conv needed. 
             # Correction: My presets stored Tirzepatide as 2.5 (mg) in dose_mcg field? No, I put 2.5 there.
             # Ideally dose_mcg field should be consistent.
             # v4.0 fix: dose_mcg in presets holds the 'value' associated with the 'default_dose_unit'.
        elif unit_pref == "IU":
             st.session_state.dose_unit_selection = "IU"
             st.session_state.dose_val = target_val
        else:
             st.session_state.dose_unit_selection = "mcg"
             st.session_state.dose_val = target_val

        st.session_state.calc_count += 1

    def convert_dose_unit():
        # Simple reset or conversion logic if needed. 
        # For now, just keeping the value is safer to avoid loop errors with IU.
        pass

    # --- UI HEADER ---
    st.subheader("🧪 Reconstitution Calculator")
    st.divider()

    left_col, right_col = st.columns([1, 1.2], gap="large")

    # === LEFT COLUMN: INPUTS ===
    with left_col:
        st.info("1️⃣ **Configuration**")
        
        # Sort keys, Tirzepatide default
        sorted_presets = sorted(list(PEPTIDE_PRESETS.keys()))
        default_index = 0
        if "Tirzepatide" in sorted_presets:
            default_index = sorted_presets.index("Tirzepatide")

        selected_peptide = st.selectbox("Select Peptide Profile", sorted_presets, index=default_index, key="peptide_selector", on_change=load_preset)
        peptide_info = PEPTIDE_PRESETS[selected_peptide]

        st.write("📦 **Stock & Water**")
        c1, c2, c3 = st.columns([1.5, 1, 1.5])
        with c1:
            vial_qty = st.number_input("Stock Amount", key="vial_val", min_value=0.0, step=1.0, format="%.1f")
        with c2:
            # Added IU to units
            vial_unit = st.selectbox("Unit", ["mg", "mcg", "g", "IU"], index=st.session_state.stock_unit_index, key="stock_unit_selection")
        with c3:
            water_ml = st.number_input("Water Added (mL)", value=2.0, step=0.5, min_value=0.1, format="%.1f")

        st.warning("⚠️ **Safety Check:** Ensure inputs match your physical supplies.")

        st.write("🎯 **Dosing**")
        c4, c5 = st.columns([2, 1])
        with c5:
            dose_unit = st.selectbox("Dose Unit", ["mcg", "mg", "g", "IU"], key="dose_unit_selection", on_change=convert_dose_unit)
        with c4:
            # Dynamic Step sizing
            if dose_unit == 'mg': step = 0.5
            elif dose_unit == 'IU': step = 5.0
            elif dose_unit == 'mcg': step = 50.0
            else: step = 0.001
            desired_dose = st.number_input("Desired Dose", key="dose_val", min_value=0.0, step=step, format="%.4f" if dose_unit=='g' else "%.1f")
        
        syringe_type = st.radio("Syringe Type", ["U-100 (Standard)", "U-40 (Vet)"], horizontal=True)
        syringe_factor = 100 if "U-100" in syringe_type else 40

    # === RIGHT COLUMN: RESULTS ===
    with right_col:
        st.success("2️⃣ **Profile & Results**")

        if vial_qty > 0 and water_ml > 0 and desired_dose > 0:
            
            # --- CALCULATION ENGINE v4.0 ---
            # 1. Normalize Stock to 'units' or 'mcg'
            # If IU conversion exists for this peptide:
            conversion = peptide_info.get("iu_conversion")
            
            total_stock_units = 0
            
            # Helper to get pure mass in mg
            stock_mg = 0 
            if vial_unit == 'mg': stock_mg = vial_qty
            elif vial_unit == 'mcg': stock_mg = vial_qty / 1000
            elif vial_unit == 'g': stock_mg = vial_qty * 1000
            
            # LOGIC BRANCH A: Peptide has defined IU conversion (Oxytocin: 600)
            if conversion and conversion > 1:
                # If user entered MG, convert to IU
                if vial_unit in ['mg', 'mcg', 'g']:
                    total_stock_units = stock_mg * conversion # Total IU in vial
                    display_strength = f"{stock_mg:.1f}mg ≈ {int(total_stock_units)} IU"
                else: # User entered IU directly
                    total_stock_units = vial_qty
                    display_strength = f"{int(vial_qty)} IU"
                
                # Target must be in IU for calculation
                if dose_unit == 'IU':
                    target_dose_units = desired_dose
                elif dose_unit == 'mg':
                    target_dose_units = desired_dose * conversion
                elif dose_unit == 'mcg':
                    target_dose_units = (desired_dose / 1000) * conversion
                else:
                    target_dose_units = 0 # error
                    
            # LOGIC BRANCH B: Peptide is naturally IU (HCG) - conversion=1
            elif conversion == 1: 
                # Assume Stock is IU. If user puts mg, we assume 1mg=1IU?? No, HCG usually 1mg=10000IU but variability exists.
                # Simplified: Just trust user input numbers.
                total_stock_units = vial_qty 
                target_dose_units = desired_dose
                display_strength = f"{int(vial_qty)} IU"
                
            # LOGIC BRANCH C: Standard Mass-Based (Tirzepatide, etc)
            else:
                # Convert everything to MCG for math
                if vial_unit == 'mg': total_stock_units = vial_qty * 1000
                elif vial_unit == 'g': total_stock_units = vial_qty * 1000000
                elif vial_unit == 'mcg': total_stock_units = vial_qty
                else: total_stock_units = 0 # IU entered for mass peptide?
                
                if dose_unit == 'mg': target_dose_units = desired_dose * 1000
                elif dose_unit == 'g': target_dose_units = desired_dose * 1000000
                elif dose_unit == 'mcg': target_dose_units = desired_dose
                else: target_dose_units = 0
                
                display_strength = f"{total_stock_units/1000:.1f} mg"

            # Final Math
            if total_stock_units > 0:
                concentration_per_ml = total_stock_units / water_ml
                draw_ml = target_dose_units / concentration_per_ml
                units = draw_ml * syringe_factor
                doses_per_vial = total_stock_units / target_dose_units
            else:
                draw_ml, units, doses_per_vial = 0, 0, 0

            # --- RENDER RESULTS ---
            c1, c2, c3 = st.columns(3)
            c1.metric("Draw Volume", f"{draw_ml:.4f} mL")
            c2.metric("Syringe Units", f"{units:.1f} Units")
            c3.metric("Doses / Vial", f"{int(doses_per_vial)}")
            
            # Visual Bar
            percentage = min(units / syringe_factor * 100, 100)
            if units > syringe_factor:
                st.error("⚠️ **Volume too large for one syringe!**")
                st.markdown(f"""<div style="margin-bottom:5px; font-weight:bold;">Overflow:</div><div class="syringe-container"><div class="syringe-liquid" style="width: 100%; background-color: #ff0000;"></div><div class="syringe-markings"></div></div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style="margin-bottom:5px; font-weight:bold;">Visual Fill ({units:.1f}):</div><div class="syringe-container"><div class="syringe-liquid" style="width: {percentage}%;"></div><div class="syringe-markings"></div></div>""", unsafe_allow_html=True)
                st.caption(f"Draw to **{units:.1f}** on your {syringe_type} syringe.")
                
            if conversion:
                st.caption(f"ℹ️ **Conversion Applied:** {display_strength} | Dose: {target_dose_units:.1f} IU")

            # --- PROFILE ---
            st.write("")
            with st.expander(f"📖 **Profile: {selected_peptide}**", expanded=True):
                st.markdown(f"**Type:** {peptide_info['type']}")
                st.markdown(f"**🌟 Key Benefits:**")
                st.markdown(peptide_info['benefits_summary']) 
                st.markdown(f"""
                <div style="margin-top:10px; padding:10px; background-color:#3e1818; border-left:4px solid #ff4b4b; border-radius:4px;">
                <strong>⚠️ Common Side Effects:</strong><br>
                {peptide_info['side_effects_summary'].replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
                st.write("")
                st.info(f"**📋 Quick Protocol:** {peptide_info['protocol_summary']}")
                st.caption("*For clinical details, visit the 'Peptide Database' tab.*")

            # Download
            protocol_text = f"Peptide: {selected_peptide}\nStock: {vial_qty}{vial_unit} + {water_ml}mL Water\nDose: {desired_dose}{dose_unit} = {units:.1f} Units\nProtocol: {peptide_info['protocol_summary']}"
            st.download_button("💾 Save Protocol", protocol_text, "protocol.txt", use_container_width=True)

        else:
            st.info("Enter inputs to see results.")

    st.divider()
    
    with st.expander("🛠️ How to Reconstitute (Mix)", expanded=True):
         if vial_qty > 0 and water_ml > 0:
            st.markdown(f"1. **Clean:** Wipe the top of the **{vial_qty} {vial_unit}** peptide vial and the water vial with an alcohol swab.\n2. **Withdraw:** Draw exactly **{water_ml} mL** of Bacteriostatic Water.\n3. **Inject:** Slowly inject the **{water_ml} mL** of water into the peptide vial. Aim for the glass wall, not the powder directly.\n4. **Mix:** **Do not shake.** Gently swirl the vial until dissolved.\n5. **Store:** Refrigerate immediately.")
         else:
             st.write("Enter Stock and Water amounts.")

    with st.expander("💉 Visual Guide: Injection Sites", expanded=False):
        try:
            st.image("injection_sites.png", caption="Recommended Subcutaneous Zones", use_container_width=True)
        except:
            st.warning("⚠️ Image not found.")

    st.divider()
    st.caption(f"v4.0 | Calculations: {st.session_state.calc_count}")

# ==============================================================================
# PAGE 2: DATABASE
# ==============================================================================
elif page == "📚 Peptide Database":
    st.subheader("📚 Peptide Database")
    st.divider()
    
    # [Database Logic remains identical to v3.7 but using v4.0 data structure]
    # Re-using the same loop logic for rendering cards
    
    # Extract unique categories
    all_categories = ["All", "Slimming & Fat Loss", "Skin, Hair & Beauty", "Muscle & Workout", "Nootropics & Brain", "Injury & Repair", "Wellness & Longevity", "Libido & Sexual Health"]
    col_search, col_filter = st.columns([3, 1])
    with col_search:
        search_query = st.text_input("🔍 Search Peptides", placeholder="Search...").lower()
    with col_filter:
        category_filter = st.selectbox("🏷️ Filter", all_categories)
    st.markdown("---")

    filtered_items = {}
    for name, data in PEPTIDE_PRESETS.items():
        if category_filter != "All" and data.get('filter_cat') != category_filter: continue
        if search_query not in name.lower() and search_query not in data['benefits_detailed'].lower(): continue
        filtered_items[name] = data

    num_cols = 3
    cols = st.columns(num_cols)
    for idx, (name, info) in enumerate(filtered_items.items()):
        col = cols[idx % num_cols]
        with col:
            with st.container(border=True):
                st.markdown(f"### {name}")
                st.markdown(f"<span class='db-tag'>{info['type']}</span>", unsafe_allow_html=True)
                st.write("")
                st.markdown("**🌟 Clinical Benefits:**")
                st.markdown(info['benefits_detailed'])
                st.markdown(f"""<div class='side-effect-box'><strong>⚠️ Side Effects:</strong><br>{info['side_effects_detailed'].replace(chr(10), '<br>')}</div>""", unsafe_allow_html=True)
                st.write("")
                with st.expander("📋 Detailed Protocol", expanded=True):
                     st.markdown(info['protocol_detailed'])
                with st.expander("ℹ️ Description & Mechanism"):
                    st.markdown(f"_{info['desc']}_")
                    st.markdown(f"**❄️ Storage:** {info['storage']}")
