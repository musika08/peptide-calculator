import streamlit as st
import math

# --- 1. CONFIGURATION: WIDE MODE ---
st.set_page_config(
    page_title="PeptideCalc Pro v4.0",
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
    .contraindication-box {
        background-color: #2e0000;
        border: 1px solid #ff0000;
        color: #ffcccc;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 15px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- EXPANDED KNOWLEDGE BASE (v4.0 - Contraindications & IU Factors) ---
# conversion_factor: used if vial is MG but dose is IU. (1mg = X IU)
PEPTIDE_PRESETS = {
    "AOD-9604": {
        "vial_mg": 5.0, "dose_amount": 300.0, "dose_u": "mcg",
        "type": "Fat Loss", "filter_cat": "Slimming & Fat Loss",
        "desc": "Anti-Obesity Drug 9604. A modified fragment of the C-terminus of Human Growth Hormone (HGH) designed specifically to burn fat without the blood sugar effects of full HGH.",
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
        "contraindications": "None significant reported. Safe for most users.",
        "protocol_summary": "300mcg daily, morning fasted.",
        "benefits_detailed": """
        - **Targeted Lipolysis:** Specifically stimulates the breakdown of fat cells (lipolysis) and inhibits the formation of new fat (lipogenesis).
        - **Metabolic Safety:** Unlike full HGH, it does not induce insulin resistance or elevate IGF-1.
        - **Joint Support:** Originally researched for osteoarthritis, it aids in cartilage regeneration.
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
        "vial_mg": 5.0, "dose_amount": 250.0, "dose_u": "mcg",
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
        "contraindications": "Theoretical risk with active malignancy (due to angiogenesis).",
        "protocol_summary": "250-500mcg daily or 2x daily.",
        "benefits_detailed": """
        - **Connective Tissue:** Drastically speeds up the healing of soft tissue injuries.
        - **Angiogenesis:** Stimulates the formation of new blood vessels.
        - **Gastroprotection:** Heals gastric ulcers and protects intestinal endothelium.
        """,
        "protocol_detailed": """
        **Dosage:** 250mcg - 500mcg

        **Frequency:** Daily or Twice Daily

        **Timing:** SubQ near injury (local) or belly fat (systemic)

        **Cycle:** 4 to 6 Weeks on, 2 Weeks off
        """,
        "side_effects_detailed": """
        • Generally considered extremely safe
        • Rare reports of fatigue
        • Mild nausea
        """,
        "storage": "Refrigerate. Stable."
    },
    "BPC-157 + TB-500 Blend": {
        "vial_mg": 10.0, "dose_amount": 500.0, "dose_u": "mcg",
        "type": "Regenerative Blend", "filter_cat": "Injury & Repair",
        "desc": "The 'Wolverine Stack'. Synergistic combination for total repair.",
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
        "contraindications": "Active Cancer (due to angiogenesis/cell migration from TB-500).",
        "protocol_summary": "500mcg-1mg total fluid daily.",
        "benefits_detailed": """
        - **Total Repair:** Targets tendon/bone interface and muscle belly simultaneously.
        - **Mobility:** Significant improvements in joint range of motion.
        - **Speed:** Often halves recovery time compared to natural healing.
        """,
        "protocol_detailed": """
        **Dosage:** 500mcg - 1000mcg (Total Volume)

        **Frequency:** Daily

        **Timing:** Any time

        **Cycle:** 4 to 8 Weeks
        """,
        "side_effects_detailed": """
        • Temporary head rush
        • Fatigue (healing phase)
        • Injection site stinging
        """,
        "storage": "Refrigerate. Use within 30 days."
    },
    "CJC-1295 (No DAC)": {
        "vial_mg": 5.0, "dose_amount": 100.0, "dose_u": "mcg",
        "type": "Growth Hormone", "filter_cat": "Muscle & Workout",
        "desc": "Modified GRF 1-29. A GHRH analog that acts on the pituitary gland.",
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
        "contraindications": "Active Cancer. History of intracranial hypertension.",
        "protocol_summary": "100mcg nightly, fasted.",
        "benefits_detailed": """
        - **Hyperplasia:** Stimulates the division of muscle cells.
        - **Sleep Architecture:** Dramatically improves Delta-wave deep sleep.
        - **Anti-Aging:** Increases collagen synthesis.
        """,
        "protocol_detailed": """
        **Dosage:** 100mcg

        **Frequency:** Daily (5 days on / 2 days off)

        **Timing:** Bedtime (Fasted 2+ hours)

        **Cycle:** 12 Weeks +
        """,
        "side_effects_detailed": """
        • Immediate head rush (vasodilation)
        • Warm/flushed face
        • Vivid dreams
        """,
        "storage": "Refrigerate. Sensitive."
    },
    "CJC-1295 + Ipamorelin Blend": {
        "vial_mg": 10.0, "dose_amount": 200.0, "dose_u": "mcg",
        "type": "Growth Hormone Blend", "filter_cat": "Muscle & Workout",
        "desc": "The Gold Standard GH Stack. GHRH + GHRP for max synergy.",
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
        "contraindications": "Active Cancer. History of intracranial hypertension.",
        "protocol_summary": "200-300mcg total nightly, fasted.",
        "benefits_detailed": """
        - **Synergistic Power:** Maximizes GH secretion naturally.
        - **Visceral Fat:** Effective at mobilizing deep abdominal fat.
        - **Wellness:** Improves hair density and nail strength.
        """,
        "protocol_detailed": """
        **Dosage:** 200mcg - 300mcg (Total Volume)

        **Frequency:** Nightly (5 days on / 2 off)

        **Timing:** Bedtime (Fasted 2+ hours)

        **Cycle:** 3 to 6 Months
        """,
        "side_effects_detailed": """
        • Head rush/Flushing
        • Numbness in hands (Carpal Tunnel)
        • Water weight gain
        """,
        "storage": "Refrigerate. Do not shake."
    },
    "Epithalon": {
        "vial_mg": 10.0, "dose_amount": 5000.0, "dose_u": "mcg",
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
        "contraindications": "None significant reported.",
        "protocol_summary": "5mg-10mg daily for 10-20 days.",
        "benefits_detailed": """
        - **Telomere Extension:** Prevents DNA cap shortening.
        - **Endocrine Reset:** Restores pineal gland sensitivity.
        - **Sleep Quality:** Normalizes melatonin production.
        """,
        "protocol_detailed": """
        **Dosage:** 5mg - 10mg

        **Frequency:** Daily

        **Timing:** Morning or Evening

        **Cycle:** 10-20 Days (Repeat every 6-12 mos)
        """,
        "side_effects_detailed": """
        • Extremely safe profile
        • Occasional drowsiness
        • Vivid dreams
        """,
        "storage": "Refrigerate."
    },
    "GHK-Cu": {
        "vial_mg": 50.0, "dose_amount": 2000.0, "dose_u": "mcg",
        "type": "Cosmetic/Repair", "filter_cat": "Skin, Hair & Beauty",
        "desc": "Copper Tripeptide-1. A genomic modulator for skin and hair.",
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
        "contraindications": "Wilson's Disease. Copper Hypersensitivity.",
        "protocol_summary": "1-2mg daily. Evening.",
        "benefits_detailed": """
        - **Skin Rejuvenation:** Increases collagen synthesis by 70%.
        - **Hair Growth:** Enlarges hair follicles.
        - **DNA Repair:** Resets activity of DNA repair genes.
        """,
        "protocol_detailed": """
        **Dosage:** 1mg - 2mg

        **Frequency:** Daily

        **Timing:** Evening

        **Cycle:** 30 Days on, 30 Days off
        """,
        "side_effects_detailed": """
        • Injection site pain (burning)
        • Large red welts
        • Zinc depletion (Supplement Zinc)
        """,
        "storage": "Refrigerate. Protect from light."
    },
    "Glow Blend (GHK-Cu/BPC/TB)": {
        "vial_mg": 70.0, "dose_amount": 2500.0, "dose_u": "mcg",
        "type": "Cosmetic/Recovery Blend", "filter_cat": "Skin, Hair & Beauty",
        "desc": "70mg Tri-Blend. Buffered GHK-Cu for painless injection.",
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
        "contraindications": "Active Cancer (due to TB-500). Wilson's Disease.",
        "protocol_summary": "2.5mg - 3mg total daily.",
        "benefits_detailed": """
        - **Painless Application:** BPC-157 neutralizes Copper acidity.
        - **Total Rejuvenation:** Targets skin, hair, and joints.
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
        "vial_mg": 5000.0, "dose_amount": 250.0, "dose_u": "IU", "vial_u": "IU", # HCG usually sold in IU
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
        "contraindications": "Prostate Cancer. Androgen-dependent tumors.",
        "protocol_summary": "250-500iu 2-3x per week.",
        "benefits_detailed": """
        - **Testicular Health:** Prevents atrophy during TRT.
        - **Fertility:** Crucial for maintaining spermatogenesis.
        - **Neurosteroids:** Supports DHEA and Pregnenolone synthesis.
        """,
        "protocol_detailed": """
        **Dosage:** 250iu - 500iu

        **Frequency:** 2 to 3 times per week

        **Timing:** Morning

        **Cycle:** Continuous with TRT or PCT
        """,
        "side_effects_detailed": """
        • Estrogen spikes (requires AI)
        • Acne
        • Water retention
        """,
        "storage": "Refrigerate. Fragile."
    },
    "Ipamorelin": {
        "vial_mg": 5.0, "dose_amount": 100.0, "dose_u": "mcg",
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
        "contraindications": "Active Cancer.",
        "protocol_summary": "100-300mcg nightly, fasted.",
        "benefits_detailed": """
        - **Pure Signal:** Stimulates GH without extreme hunger.
        - **Catabolic Protection:** Preserves lean muscle.
        - **Sleep:** Increases REM and Slow-Wave sleep.
        """,
        "protocol_detailed": """
        **Dosage:** 100mcg - 300mcg

        **Frequency:** Nightly

        **Timing:** Bedtime (Fasted)

        **Cycle:** 8 to 12 Weeks
        """,
        "side_effects_detailed": """
        • Extremely well tolerated
        • Slight water retention possible
        """,
        "storage": "Refrigerate."
    },
    "Kisspeptin": {
        "vial_mg": 10.0, "dose_amount": 100.0, "dose_u": "mcg",
        "type": "Hormonal", "filter_cat": "Libido & Sexual Health",
        "desc": "Stimulates hypothalamus to release GnRH, restarting HPTA.",
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
        "contraindications": "None significant reported.",
        "protocol_summary": "100-200mcg daily.",
        "benefits_detailed": """
        - **HPTA Restart:** Safely restarts testosterone post-cycle.
        - **Fertility:** Strongly stimulates FSH.
        - **Psychogenic:** Linked to emotional arousal.
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
        "vial_mg": 80.0, "dose_amount": 3000.0, "dose_u": "mcg",
        "type": "Ultimate Repair/Cosmetic Blend", "filter_cat": "Skin, Hair & Beauty",
        "desc": "The 80mg Master Stack. Adds **KPV** for powerful anti-inflammation.",
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
        "contraindications": "Active Cancer (due to TB-500). Wilson's Disease.",
        "protocol_summary": "3mg total daily.",
        "benefits_detailed": """
        - **Dermatology:** KPV treats acne and psoriasis.
        - **Gut Health:** Strongest stack for IBD/Colitis.
        - **Mast Cells:** Stabilizes mast cells (histamine).
        """,
        "protocol_detailed": """
        **Dosage:** 3mg (Total Volume)

        **Frequency:** Daily

        **Timing:** Evening

        **Cycle:** 4 to 8 Weeks
        """,
        "side_effects_detailed": """
        • Red welts at injection site
        • Fatigue (healing/detox)
        • Flushing
        """,
        "storage": "Refrigerate. Protect from light."
    },
    "Melanotan II": {
        "vial_mg": 10.0, "dose_amount": 500.0, "dose_u": "mcg",
        "type": "Cosmetic", "filter_cat": "Skin, Hair & Beauty",
        "desc": "Alpha-MSH analog. Stimulates tanning and arousal.",
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
        "contraindications": "Melanoma history. Uncontrolled Hypertension.",
        "protocol_summary": "100-500mcg before UV exposure.",
        "benefits_detailed": """
        - **Photoprotection:** Creates a deep, natural tan.
        - **Libido:** Potent CNS aphrodisiac.
        - **Metabolic:** Suppresses appetite.
        """,
        "protocol_detailed": """
        **Dosage:** 100mcg - 500mcg

        **Frequency:** As needed

        **Timing:** 30 mins before UV

        **Cycle:** Until desired color
        """,
        "side_effects_detailed": """
        • Significant nausea
        • Facial flushing
        • Spontaneous erections
        • Darkening of moles
        """,
        "storage": "Refrigerate."
    },
    "MOTS-c": {
        "vial_mg": 10.0, "dose_amount": 5000.0, "dose_u": "mcg",
        "type": "Metabolic/Mitochondrial", "filter_cat": "Muscle & Workout",
        "desc": "Mitochondrial-Derived Peptide. 'Exercise mimetic'.",
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
        "contraindications": "None significant reported.",
        "protocol_summary": "5mg once weekly.",
        "benefits_detailed": """
        - **Endurance:** Increases glucose/oxygen utilization.
        - **Metabolic:** Prevents diet-induced obesity.
        - **Bone Health:** Promotes bone metabolism.
        """,
        "protocol_detailed": """
        **Dosage:** 5mg - 10mg

        **Frequency:** Once Weekly

        **Timing:** Morning (Pre-workout)

        **Cycle:** 4 to 8 Weeks
        """,
        "side_effects_detailed": """
        • Injection site pain
        • Insomnia (if late)
        • Restlessness
        """,
        "storage": "Refrigerate."
    },
    "NAD+": {
        "vial_mg": 500.0, "dose_amount": 25000.0, "dose_u": "mcg",
        "type": "Cellular Energy", "filter_cat": "Wellness & Longevity",
        "desc": "Nicotinamide Adenine Dinucleotide. Fuel for mitochondria.",
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
        "contraindications": "None. Caution with anxiety disorders (triggers flush).",
        "protocol_summary": "25-50mg 2-3x per week. SLOW INJECTION.",
        "benefits_detailed": """
        - **Cognition:** Rapidly clears brain fog.
        - **Mitochondria:** Restores ATP production.
        - **DNA Repair:** Essential for PARP enzymes.
        """,
        "protocol_detailed": """
        **Dosage:** 25mg - 50mg

        **Frequency:** 2-3x / Week

        **Timing:** Morning

        **Cycle:** Ongoing
        """,
        "side_effects_detailed": """
        • Intense chest pressure
        • Abdominal cramping
        • Anxiety/Panic sensation
        """,
        "storage": "Refrigerate immediately."
    },
    "Oxytocin Acetate": {
        "vial_mg": 2.0, "dose_amount": 20.0, "dose_u": "IU", "conversion_factor": 600, # 1mg = 600 IU
        "type": "Hormonal/Wellness", "filter_cat": "Nootropics & Brain",
        "desc": "The 'Love Hormone'. Regulates bonding and anxiety.",
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
        "contraindications": "Pregnancy (induces labor).",
        "protocol_summary": "20-50mcg as needed.",
        "benefits_detailed": """
        - **Psychological:** Significantly reduces social anxiety and cortisol.
        - **Pain Modulation:** Analgesic properties.
        - **Intimacy:** Enhances trust and bonding.
        """,
        "protocol_detailed": """
        **Dosage:** 20 IU - 50 IU

        **Frequency:** As needed

        **Timing:** 30 mins before event

        **Cycle:** Continuous or Cycled
        """,
        "side_effects_detailed": """
        • Nausea (high doses)
        • Headache
        • Flushing
        """,
        "storage": "Refrigerate."
    },
    "PT-141": {
        "vial_mg": 10.0, "dose_amount": 1000.0, "dose_u": "mcg",
        "type": "Libido", "filter_cat": "Libido & Sexual Health",
        "desc": "Bremelanotide. Treats hypoactive sexual desire via nervous system.",
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
        "contraindications": "Uncontrolled Hypertension. Cardiovascular Disease.",
        "protocol_summary": "1.5-2mg, 2 hours before activity.",
        "benefits_detailed": """
        - **Mechanism:** Targets hypothalamus, not blood flow.
        - **Efficacy:** FDA approved for low libido.
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
        "vial_mg": 10.0, "dose_amount": 2000.0, "dose_u": "mcg",
        "type": "Metabolic (GLP-1/GIP/Glucagon)", "filter_cat": "Slimming & Fat Loss",
        "desc": "The 'Triple G' Agonist. Most potent weight loss agent.",
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
        "contraindications": "Medullary Thyroid Cancer (MTC). MEN 2 Syndrome.",
        "protocol_summary": "2mg weekly, titrate up.",
        "benefits_detailed": """
        - **Efficacy:** 24.2% average weight loss in trials.
        - **Liver Health:** Resolves Fatty Liver.
        - **Energy:** Glucagon increases calorie burn.
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
        "vial_mg": 5.0, "dose_amount": 250.0, "dose_u": "mcg",
        "type": "Metabolic (GLP-1)", "filter_cat": "Slimming & Fat Loss",
        "desc": "GLP-1 Agonist. Standard for medical weight loss.",
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
        "contraindications": "Medullary Thyroid Cancer (MTC). MEN 2 Syndrome. Pancreatitis history.",
        "protocol_summary": "0.25mg weekly, titrate up.",
        "benefits_detailed": """
        - **Satiety:** Slows gastric emptying.
        - **Heart:** 20% reduction in cardiac events.
        - **Addiction:** Modulates dopamine reward.
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
        • 'Ozempic face'
        • Fatigue
        """,
        "storage": "Refrigerate. Protect from light."
    },
    "TB-500": {
        "vial_mg": 5.0, "dose_amount": 2500.0, "dose_u": "mcg",
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
        "contraindications": "Active Cancer (promotes angiogenesis).",
        "protocol_summary": "2.5mg twice weekly.",
        "benefits_detailed": """
        - **Muscle Repair:** Best for tears and strains.
        - **Flexibility:** Improves range of motion.
        - **Cardiac:** Repairs heart tissue.
        """,
        "protocol_detailed": """
        **Dosage:** 2.5mg (2500mcg)

        **Frequency:** 2x Per Week

        **Timing:** Any time

        **Cycle:** 4 to 6 Weeks
        """,
        "side_effects_detailed": """
        • Temporary head rush
        • Occasional lethargy
        • Flu-like symptoms
        """,
        "storage": "Refrigerate."
    },
    "Tesamorelin": {
        "vial_mg": 2.0, "dose_amount": 1000.0, "dose_u": "mcg",
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
        "contraindications": "Active Cancer. Pregnancy.",
        "protocol_summary": "1-2mg nightly, fasted.",
        "benefits_detailed": """
        - **Visceral Fat:** Destroys stubborn organ fat.
        - **Cognition:** Improves executive function.
        - **Cardio:** Lowers triglycerides.
        """,
        "protocol_detailed": """
        **Dosage:** 1mg - 2mg

        **Frequency:** Daily

        **Timing:** Bedtime (Fasted)

        **Cycle:** 8 to 12 Weeks
        """,
        "side_effects_detailed": """
        • Injection site redness (common)
        • Joint stiffness
        • Carpal tunnel
        """,
        "storage": "Refrigerate. Use within 20-30 days."
    },
    "Tesamorelin + Ipamorelin Blend": {
        "vial_mg": 12.0, "dose_amount": 350.0, "dose_u": "mcg",
        "type": "Growth Hormone/Fat Loss Blend", "filter_cat": "Slimming & Fat Loss",
        "desc": "The 'Shred Stack'. Targets visceral fat + systemic GH.",
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
        "contraindications": "Active Cancer.",
        "protocol_summary": "350-500mcg total nightly, fasted.",
        "benefits_detailed": """
        - **Recomposition:** Burns fat while building muscle.
        - **Metabolic:** Amplifies fasting effects.
        - **Synergy:** Ipamorelin smooths the pulse.
        """,
        "protocol_detailed": """
        **Dosage:** 350mcg - 500mcg (Total)

        **Frequency:** Daily (5 on / 2 off)

        **Timing:** Bedtime (Fasted)

        **Cycle:** 8 to 12 Weeks
        """,
        "side_effects_detailed": """
        • Joint pain
        • Carpal tunnel
        • Flushing
        """,
        "storage": "Refrigerate."
    },
    "Tirzepatide": {
        "vial_mg": 30.0, "dose_amount": 2.5, "dose_u": "mg",
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
        "contraindications": "Medullary Thyroid Cancer (MTC). MEN 2 Syndrome. Pancreatitis.",
        "protocol_summary": "2.5mg weekly, titrate up.",
        "benefits_detailed": """
        - **Weight Loss:** 20%+ average loss in trials.
        - **Food Noise:** Eliminates food obsession.
        - **Tolerability:** Less nausea than GLP-1 alone.
        """,
        "protocol_detailed": """
        **Dosage:** Start 2.5mg -> Max 15mg

        **Frequency:** Once Weekly

        **Timing:** Any time

        **Cycle:** Continuous
        """,
        "side_effects_detailed": """
        • Anhedonia
        • Cold extremities
        • Constipation
        • Hair shedding
        """,
        "storage": "Refrigerate. Do not freeze."
    },
}

FACTORS = {'mcg': 1, 'mg': 1000, 'g': 1000000, 'IU': 1} # IU handling is special

# Initialize State
if 'vial_val' not in st.session_state: st.session_state.vial_val = 30.0 
if 'dose_val' not in st.session_state: st.session_state.dose_val = 2.5 
if 'stock_unit_index' not in st.session_state: st.session_state.stock_unit_index = 0
if 'dose_unit_index' not in st.session_state: st.session_state.dose_unit_index = 0
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
        
        # 1. Set Vial (Stock)
        # If the preset has a defined vial_u (e.g. HCG is IU), use it. Default to mg.
        preset_vial_u = data.get("vial_u", "mg") 
        st.session_state.vial_val = float(data["vial_mg"])
        
        # Map string unit to index for selectbox
        unit_options = ["mg", "mcg", "g", "IU"]
        try:
            st.session_state.stock_unit_index = unit_options.index(preset_vial_u)
        except:
            st.session_state.stock_unit_index = 0 # Default to mg if error

        # 2. Set Dose
        st.session_state.dose_val = float(data["dose_amount"])
        st.session_state.dose_unit_selection = data.get("dose_u", "mcg")

        st.session_state.calc_count += 1

    # --- UI HEADER ---
    st.subheader("🧪 Reconstitution Calculator")
    st.divider()

    # --- MAIN LAYOUT LOGIC (MOBILE OPTIMIZED) ---
    left_col, right_col = st.columns([1, 1.2], gap="large")

    # === LEFT COLUMN: INPUTS ONLY ===
    with left_col:
        st.info("1️⃣ **Configuration**")
        
        # Determine default index for Tirzepatide
        sorted_presets = sorted(list(PEPTIDE_PRESETS.keys()))
        default_index = 0
        if "Tirzepatide" in sorted_presets:
            default_index = sorted_presets.index("Tirzepatide")

        selected_peptide = st.selectbox("Select Peptide Profile", sorted_presets, index=default_index, key="peptide_selector", on_change=load_preset)
        
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
            # Added IU to units
            dose_unit = st.selectbox("Dose Unit", ["mcg", "mg", "g", "IU"], key="dose_unit_selection")
        with c4:
            if dose_unit == 'mg': step, fmt = 1.0, "%.1f"
            elif dose_unit == 'mcg': step, fmt = 50.0, "%.1f"
            elif dose_unit == 'IU': step, fmt = 10.0, "%.1f" # IU step
            else: step, fmt = 0.001, "%.4f"
            desired_dose = st.number_input("Desired Dose", key="dose_val", min_value=0.0, step=step, format=fmt)
        
        syringe_type = st.radio("Syringe Type", ["U-100 (Standard)", "U-40 (Vet)"], horizontal=True)
        syringe_factor = 100 if "U-100" in syringe_type else 40

    # === RIGHT COLUMN: RESULTS + PROFILE ===
    with right_col:
        st.success("2️⃣ **Profile & Results**")

        # --- CALCULATION ENGINE v4.0 (IU & CONVERSION) ---
        if vial_qty > 0 and water_ml > 0 and desired_dose > 0:
            
            # 1. Determine Total Quantity in 'Standard' Units
            # If vial is mg, convert to mcg. If IU, keep as IU.
            peptide_data = PEPTIDE_PRESETS[selected_peptide]
            conversion_factor = peptide_data.get("conversion_factor", None)

            total_qty_standard = 0.0
            
            # Logic A: Vial is Mass (mg/mcg/g)
            if vial_unit in ['mg', 'mcg', 'g']:
                total_mass_mcg = vial_qty * FACTORS[vial_unit] # Convert all to mcg first
                
                # Check if we need to convert Mass -> IU (e.g. Oxytocin)
                if dose_unit == 'IU' and conversion_factor:
                    # 1 mg = Factor IU. So 1 mcg = Factor/1000 IU.
                    # Total IU = (Total mcg / 1000) * Factor
                    total_qty_standard = (total_mass_mcg / 1000) * conversion_factor
                    calc_base_unit = 'IU'
                else:
                    total_qty_standard = total_mass_mcg
                    calc_base_unit = 'mcg'

            # Logic B: Vial is already IU (e.g. HCG)
            else: # vial_unit == 'IU'
                total_qty_standard = vial_qty
                calc_base_unit = 'IU'

            # 2. Determine Dose in 'Standard' Units
            dose_standard = 0.0
            if dose_unit == 'IU':
                dose_standard = desired_dose
            elif dose_unit in ['mg', 'mcg', 'g']:
                dose_standard = desired_dose * FACTORS[dose_unit] # to mcg
            
            # 3. Calculate Volume
            # Concentration = Total Qty / Water
            concentration = total_qty_standard / water_ml
            draw_ml = dose_standard / concentration
            units = draw_ml * syringe_factor
            
            # Doses per vial
            doses_per_vial = total_qty_standard / dose_standard

            # --- RENDER RESULTS ---
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

            # --- CONTRAINDICATION WARNING ---
            if "contraindications" in peptide_data:
                st.markdown(f"""
                <div class='contraindication-box'>
                ⛔ CONTRAINDICATIONS: {peptide_data['contraindications']}
                </div>
                """, unsafe_allow_html=True)

            # --- B. PEPTIDE PROFILE (Second) ---
            st.write("") # Spacer
            with st.expander(f"📖 **Profile: {selected_peptide}**", expanded=True):
                st.markdown(f"**Type:** {peptide_data['type']}")
                st.markdown(f"**🌟 Key Benefits:**")
                st.markdown(peptide_data['benefits_summary']) 
                
                st.markdown(f"""
                <div style="margin-top:10px; padding:10px; background-color:#3e1818; border-left:4px solid #ff4b4b; border-radius:4px;">
                <strong>⚠️ Common Side Effects:</strong><br>
                {peptide_data['side_effects_summary'].replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
                st.write("")
                st.info(f"**📋 Quick Protocol:** {peptide_data['protocol_summary']}")
                st.markdown(f"**❄️ Storage:** {peptide_data['storage']}")
                st.caption("*For clinical details, visit the 'Peptide Database' tab.*")

            protocol_text = f"Peptide: {selected_peptide}\nType: {peptide_data['type']}\nStock: {vial_qty}{vial_unit} + {water_ml}mL Water\nConc: {concentration:.2f} {calc_base_unit}/mL\nDose: {desired_dose}{dose_unit} = {units:.1f} Units ({syringe_type})\nSupply: 1 vial lasts approx {int(doses_per_vial)} doses.\n\nQuick Protocol: {peptide_data['protocol_summary']}\nBenefits: {peptide_data['benefits_summary']}\nStorage: {peptide_data['storage']}"
            st.download_button("💾 Save Protocol", protocol_text, "protocol.txt", use_container_width=True)
        else:
            st.info("Enter inputs to see results.")

    # 2. BOTTOM SECTION: GUIDES (Rendered AFTER results on all devices)
    st.divider()
    
    with st.expander("🛠️ How to Reconstitute (Mix)", expanded=True):
         st.markdown(f"1. **Clean:** Wipe the top of the **{vial_qty} {vial_unit}** peptide vial and the water vial with an alcohol swab.\n2. **Withdraw:** Draw exactly **{water_ml} mL** of Bacteriostatic Water.\n3. **Inject:** Slowly inject the **{water_ml} mL** of water into the peptide vial. Aim for the glass wall, not the powder directly.\n4. **Mix:** **Do not shake.** Gently swirl the vial until dissolved.\n5. **Store:** Refrigerate immediately.")

    with st.expander("💉 Visual Guide: Injection Sites", expanded=False):
        try:
            st.image("injection_sites.png", caption="Recommended Subcutaneous Zones", use_container_width=True)
        except:
            st.warning("⚠️ Image not found. Please upload 'injection_sites.png' to your GitHub repository.")

    st.divider()
    c_foot1, c_foot2 = st.columns([1,1])
    with c_foot1:
        st.caption(f"🔢 Calculations performed this session: **{st.session_state.calc_count}**")
    with c_foot2:
        st.markdown("[![Hits](https://hits.sh/peptide-calculator.streamlit.app.svg?style=flat-square&label=Total%20Visits&extraCount=2023&color=79c83d)](https://hits.sh/peptide-calculator.streamlit.app/)")

# ==============================================================================
# PAGE 2: PEPTIDE DATABASE (Notion-Style / v4.0)
# ==============================================================================
elif page == "📚 Peptide Database":
    st.subheader("📚 Peptide Database")
    st.caption("Comprehensive clinical data, mechanisms, and protocols. *Disclaimer: For educational purposes only.*")
    st.divider()

    db_items = PEPTIDE_PRESETS
    all_categories = ["All", "Slimming & Fat Loss", "Skin, Hair & Beauty", "Muscle & Workout", "Nootropics & Brain", "Injury & Repair", "Wellness & Longevity", "Libido & Sexual Health"]

    col_search, col_filter = st.columns([3, 1])
    with col_search:
        search_query = st.text_input("🔍 Search Peptides", placeholder="Search by name, benefit, or type...").lower()
    with col_filter:
        category_filter = st.selectbox("🏷️ Filter by Category", all_categories)

    st.markdown("---")

    filtered_items = {}
    for name, data in db_items.items():
        if category_filter != "All" and data['filter_cat'] != category_filter: continue
        if search_query not in name.lower() and search_query not in data['benefits_detailed'].lower() and search_query not in data['desc'].lower(): continue
        filtered_items[name] = data

    num_cols = 3
    cols = st.columns(num_cols)
    
    for idx, (name, info) in enumerate(filtered_items.items()):
        col = cols[idx % num_cols]
        with col:
            with st.container(border=True):
                st.markdown(f"### {name}")
                st.markdown(f"<span class='db-tag'>{info['type']}</span>", unsafe_allow_html=True)
                
                # CONTRAINDICATION (In DB View)
                if "contraindications" in info:
                    st.markdown(f"<div style='color: #ff4b4b; font-size:0.8em; margin-top:5px;'><strong>⛔ {info['contraindications']}</strong></div>", unsafe_allow_html=True)

                st.write("") 
                
                st.markdown("**🌟 Clinical Benefits:**")
                st.markdown(info['benefits_detailed'])
                
                st.markdown(f"""
                <div class='side-effect-box'>
                <strong>⚠️ Side Effects:</strong><br>
                {info['side_effects_detailed'].replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
                
                st.write("")

                with st.expander("📋 Detailed Protocol", expanded=True):
                     st.markdown(info['protocol_detailed'])

                with st.expander("ℹ️ Description & Mechanism"):
                    st.markdown(f"_{info['desc']}_")
                    st.markdown(f"**❄️ Storage:** {info['storage']}")

    if len(filtered_items) == 0:
        st.warning("No peptides match your search criteria. Try clearing the filters.")

# --- UNIVERSAL DISCLAIMER ---
st.markdown("---")
st.caption("⚠️ **Medical Disclaimer:** This tool is for educational and informational purposes only and does not constitute medical advice. Always verify calculations with a professional. The developers assume no liability for errors or misuse.")
