import streamlit as st
import math

# --- 1. CONFIGURATION: WIDE MODE ---
st.set_page_config(
    page_title="PeptideCalc Pro v3.5",
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
    .contra-header {
        color: #ff4b4b;
        font-weight: bold;
        margin-top: 10px;
        display: block;
        border-top: 1px solid #555;
        padding-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- KNOWLEDGE BASE ---
PEPTIDE_PRESETS = {
    "AOD-9604": {
        "vial_mg": 5.0, "dose_mcg": 300.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
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
        "contraindications": "None specifically reported, but avoid if pregnant or breastfeeding.",
        "protocol_summary": "300mcg daily, morning fasted.",
        "benefits_detailed": "• Targeted fat burning (lipolysis)\n• No blood sugar spikes\n• Cartilage repair support\n• Non-hormonal (no IGF-1 impact)",
        "protocol_detailed": "**Dosage:** 300mcg\n**Frequency:** Daily\n**Timing:** Morning Fasted",
        "side_effects_detailed": "• Injection site redness\n• Mild stomach upset (rare)\n• Headache (rare)",
        "storage": "Refrigerate. Stable."
    },
    "BPC-157": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Regenerative", "filter_cat": "Injury & Repair",
        "desc": "Body Protection Compound-157.",
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
        "contraindications": "Known active cancer (due to angiogenesis properties).",
        "protocol_summary": "250-500mcg daily.",
        "benefits_detailed": "• Accelerates tendon/ligament repair\n• Heals gut lining (IBS/Leaky Gut)\n• Reduces neuro-inflammation\n• Protects liver and organs",
        "protocol_detailed": "**Dosage:** 250mcg - 500mcg\n**Frequency:** Daily\n**Timing:** SubQ near injury",
        "side_effects_detailed": "• Mild nausea\n• Fatigue\n• Injection site irritation",
        "storage": "Refrigerate."
    },
    "BPC-157 + TB-500 Blend": {
        "vial_mg": 10.0, "dose_mcg": 500.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Regenerative Blend", "filter_cat": "Injury & Repair",
        "desc": "The 'Wolverine Stack'.",
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
        "contraindications": "Active cancer.",
        "protocol_summary": "500mcg daily.",
        "benefits_detailed": "• Maximum surgical/injury recovery\n• Improves joint flexibility\n• Cardiovascular protection\n• Systemic anti-inflammatory",
        "protocol_detailed": "**Dosage:** 500mcg\n**Frequency:** Daily",
        "side_effects_detailed": "• Head rush\n• Fatigue\n• Stinging",
        "storage": "Refrigerate."
    },
    "CJC-1295 (No DAC)": {
        "vial_mg": 5.0, "dose_mcg": 100.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone", "filter_cat": "Muscle & Workout",
        "desc": "Modified GRF 1-29.",
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
        "contraindications": "Active cancer.",
        "protocol_summary": "100mcg nightly.",
        "benefits_detailed": "• Increases lean muscle mass\n• Promotes deep slow-wave sleep\n• Improves skin elasticity\n• Accelerates fat metabolism",
        "protocol_detailed": "**Dosage:** 100mcg\n**Frequency:** Nightly (Fasted)",
        "side_effects_detailed": "• Flushing\n• Head rush\n• Vivid dreams",
        "storage": "Refrigerate."
    },
    "CJC-1295 + Ipamorelin Blend": {
        "vial_mg": 10.0, "dose_mcg": 200.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone Blend", "filter_cat": "Muscle & Workout",
        "desc": "The Gold Standard GH Stack.",
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
        "contraindications": "Active cancer.",
        "protocol_summary": "200mcg nightly.",
        "benefits_detailed": "• Max natural GH secretion\n• Significant body recomposition\n• Superior recovery & sleep\n• No cortisol/prolactin spike",
        "protocol_detailed": "**Dosage:** 200mcg\n**Frequency:** Nightly",
        "side_effects_detailed": "• Head rush\n• Numb fingers\n• Water retention",
        "storage": "Refrigerate."
    },
    "Epithalon": {
        "vial_mg": 10.0, "dose_mcg": 5000.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Anti-Aging", "filter_cat": "Wellness & Longevity",
        "desc": "Synthetic tetrapeptide.",
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
        "contraindications": "None reported.",
        "protocol_summary": "5mg daily for 10 days.",
        "benefits_detailed": "• Extends lifespan (Telomeres)\n• Resets circadian rhythm\n• Boosts melatonin naturally\n• Anti-tumor/cancer protective",
        "protocol_detailed": "**Dosage:** 5mg\n**Frequency:** Daily",
        "side_effects_detailed": "• Drowsiness\n• Vivid dreams",
        "storage": "Refrigerate."
    },
    "GHK-Cu": {
        "vial_mg": 50.0, "dose_mcg": 2000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cosmetic/Repair", "filter_cat": "Skin, Hair & Beauty",
        "desc": "Copper Tripeptide-1.",
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
        "contraindications": "Wilson's Disease.",
        "protocol_summary": "1-2mg daily.",
        "benefits_detailed": "• Boosts collagen & elastin\n• Tightens loose skin\n• Regrows hair\n• Activates DNA repair",
        "protocol_detailed": "**Dosage:** 1-2mg\n**Frequency:** Daily",
        "side_effects_detailed": "• Injection Sting\n• Red welts\n• Zinc depletion",
        "storage": "Refrigerate."
    },
    "Glow Blend (GHK-Cu/BPC/TB)": {
        "vial_mg": 70.0, "dose_mcg": 2500.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cosmetic/Recovery Blend", "filter_cat": "Skin, Hair & Beauty",
        "desc": "70mg Tri-Blend.",
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
        "contraindications": "Wilson's Disease, Active Cancer.",
        "protocol_summary": "2.5mg daily.",
        "benefits_detailed": "• Painless GHK-Cu injection\n• Total body skin tightening\n• Rapid injury recovery\n• Gut & Heart health",
        "protocol_detailed": "**Dosage:** 2.5mg\n**Frequency:** Daily",
        "side_effects_detailed": "• Mild redness\n• Flushing\n• Fatigue",
        "storage": "Refrigerate."
    },
    "HCG": {
        "vial_mg": 5000.0, "dose_mcg": 250.0, "default_dose_unit": "IU", "default_stock_unit": "IU", "iu_conversion": 1,
        "type": "Hormonal", "filter_cat": "Libido & Sexual Health",
        "desc": "Human Chorionic Gonadotropin.",
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
        "contraindications": "Prostate cancer, androgen-dependent tumors.",
        "protocol_summary": "250-500 IU 2-3x per week.",
        "benefits_detailed": "• Prevents testicular shrinkage\n• Maintains fertility/sperm\n• Boosts libido & mood\n• TRT adjunct support",
        "protocol_detailed": "**Dosage:** 250-500 IU\n**Frequency:** 2-3x Weekly",
        "side_effects_detailed": "• Estrogen spikes\n• Acne\n• Water retention",
        "storage": "Refrigerate."
    },
    "Ipamorelin": {
        "vial_mg": 5.0, "dose_mcg": 100.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone", "filter_cat": "Muscle & Workout",
        "desc": "Selective GH Secretagogue.",
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
        "contraindications": "Active cancer.",
        "protocol_summary": "100-300mcg nightly.",
        "benefits_detailed": "• Clean GH release (No hunger)\n• Fat loss & muscle sparing\n• Improved sleep quality\n• Anti-aging support",
        "protocol_detailed": "**Dosage:** 100-300mcg\n**Frequency:** Nightly",
        "side_effects_detailed": "• Slight water retention\n• Rare dizziness",
        "storage": "Refrigerate."
    },
    "Kisspeptin": {
        "vial_mg": 10.0, "dose_mcg": 100.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Hormonal", "filter_cat": "Libido & Sexual Health",
        "desc": "A neuromodulator.",
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
        "contraindications": "None reported.",
        "protocol_summary": "100-200mcg daily.",
        "benefits_detailed": "• Restarts HPTA axis safely\n• Boosts fertility (LH/FSH)\n• Increases libido\n• No testicular desensitization",
        "protocol_detailed": "**Dosage:** 100-200mcg\n**Frequency:** Daily",
        "side_effects_detailed": "• Flushing\n• Redness\n• Headache",
        "storage": "Refrigerate."
    },
    "Klow Blend (GHK-Cu/BPC/TB/KPV)": {
        "vial_mg": 80.0, "dose_mcg": 3000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Ultimate Repair", "filter_cat": "Skin, Hair & Beauty",
        "desc": "The 80mg Master Stack.",
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
        "contraindications": "Wilson's Disease.",
        "protocol_summary": "3mg daily.",
        "benefits_detailed": "• Clears Acne/Psoriasis\n• Heals Gut\n• Systemic anti-inflammatory\n• Total tissue repair",
        "protocol_detailed": "**Dosage:** 3mg\n**Frequency:** Daily",
        "side_effects_detailed": "• Red welts\n• Fatigue\n• Flushing",
        "storage": "Refrigerate."
    },
    "Melanotan II": {
        "vial_mg": 10.0, "dose_mcg": 500.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cosmetic", "filter_cat": "Skin, Hair & Beauty",
        "desc": "Alpha-MSH analog.",
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
        "contraindications": "Melanoma history, Hypertension.",
        "protocol_summary": "100-500mcg before UV.",
        "benefits_detailed": "• Deep, rapid tan\n• Extreme libido boost\n• Appetite suppression\n• UV protection",
        "protocol_detailed": "**Dosage:** 100-500mcg\n**Timing:** Before UV",
        "side_effects_detailed": "• Nausea\n• Flushing\n• Moles darkening",
        "storage": "Refrigerate."
    },
    "MOTS-c": {
        "vial_mg": 10.0, "dose_mcg": 5000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Metabolic", "filter_cat": "Muscle & Workout",
        "desc": "Mitochondrial-Derived Peptide.",
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
        "contraindications": "None reported.",
        "protocol_summary": "5mg weekly.",
        "benefits_detailed": "• Increases VO2 Max\n• Prevents weight gain\n• Improves bone metabolism\n• Cellular energy boost",
        "protocol_detailed": "**Dosage:** 5mg\n**Frequency:** Weekly",
        "side_effects_detailed": "• Injection Sting\n• Insomnia",
        "storage": "Refrigerate."
    },
    "NAD+": {
        "vial_mg": 500.0, "dose_mcg": 25000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Cellular Energy", "filter_cat": "Wellness & Longevity",
        "desc": "Nicotinamide Adenine Dinucleotide.",
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
        "contraindications": "None reported.",
        "protocol_summary": "25-50mg 2-3x per week.",
        "benefits_detailed": "• Clears brain fog\n• Restores cellular energy\n• Repairs DNA damage\n• Anti-aging",
        "protocol_detailed": "**Dosage:** 25-50mg\n**Frequency:** 2-3x Weekly",
        "side_effects_detailed": "• Chest pressure (Flush)\n• Anxiety\n• Cramps",
        "storage": "Refrigerate."
    },
    "Oxytocin Acetate": {
        "vial_mg": 2.0, "dose_mcg": 20.0, "default_dose_unit": "IU", "default_stock_unit": "mg", "iu_conversion": 600,
        "default_water_ml": 3.0,
        "type": "Hormonal", "filter_cat": "Nootropics & Brain",
        "desc": "The 'Love Hormone'.",
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
        "contraindications": "Pregnancy, Severe cardiovascular disease.",
        "protocol_summary": "20-50 IU as needed.",
        "benefits_detailed": "• Reduces social anxiety\n• Lowers cortisol (Stress)\n• Enhances emotional bonding\n• Modulates pain perception",
        "protocol_detailed": "**Dosage:** 20-50 IU\n**Frequency:** As needed",
        "side_effects_detailed": "• Nausea\n• Headache\n• Flushing",
        "storage": "Refrigerate."
    },
    "PT-141": {
        "vial_mg": 10.0, "dose_mcg": 1000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Libido", "filter_cat": "Libido & Sexual Health",
        "desc": "Bremelanotide.",
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
        "contraindications": "Uncontrolled hypertension.",
        "protocol_summary": "1.5mg as needed.",
        "benefits_detailed": "• Treats ED & Low Libido\n• Works when Viagra fails\n• Increases physical arousal\n• For Men & Women",
        "protocol_detailed": "**Dosage:** 1.5mg\n**Frequency:** As needed",
        "side_effects_detailed": "• Nausea\n• Flushing\n• Headache",
        "storage": "Refrigerate."
    },
    "Retatrutide": {
        "vial_mg": 10.0, "dose_mcg": 2000.0, 
        "type": "Metabolic", "filter_cat": "Slimming & Fat Loss",
        "desc": "Triple Agonist.",
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
        "contraindications": "MEN2, Medullary Thyroid Cancer.",
        "protocol_summary": "2mg weekly.",
        "benefits_detailed": "• Extreme weight loss (24%+)\n• Burns liver fat (NAFLD)\n• Resets insulin sensitivity\n• Increases metabolism",
        "protocol_detailed": "**Dosage:** 2mg\n**Frequency:** Weekly",
        "side_effects_detailed": "• High Heart Rate\n• Skin sensitivity\n• Nausea",
        "storage": "Refrigerate."
    },
    "Semaglutide": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Metabolic", "filter_cat": "Slimming & Fat Loss",
        "desc": "GLP-1 Agonist.",
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
        "contraindications": "MEN2, Medullary Thyroid Cancer.",
        "protocol_summary": "0.25mg weekly.",
        "benefits_detailed": "• Significant weight loss (15%)\n• Controls blood sugar\n• Cardioprotective\n• Reduces addiction cravings",
        "protocol_detailed": "**Dosage:** 0.25mg\n**Frequency:** Weekly",
        "side_effects_detailed": "• Nausea\n• Constipation\n• Fatigue",
        "storage": "Refrigerate."
    },
    "TB-500": {
        "vial_mg": 5.0, "dose_mcg": 2500.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Regenerative", "filter_cat": "Injury & Repair",
        "desc": "Synthetic Thymosin Beta-4.",
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
        "contraindications": "Active cancer.",
        "protocol_summary": "2.5mg twice weekly.",
        "benefits_detailed": "• Heals muscle tears\n• Improves flexibility\n• Reduces scar tissue\n• Cardiac repair",
        "protocol_detailed": "**Dosage:** 2.5mg\n**Frequency:** 2x Weekly",
        "side_effects_detailed": "• Head rush\n• Lethargy\n• Flu-like symptoms",
        "storage": "Refrigerate."
    },
    "Tesamorelin": {
        "vial_mg": 2.0, "dose_mcg": 1000.0, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone", "filter_cat": "Slimming & Fat Loss",
        "desc": "GHRH for visceral fat.",
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
        "contraindications": "Active cancer.",
        "protocol_summary": "1-2mg nightly.",
        "benefits_detailed": "• Burns belly fat (Visceral)\n• Increases muscle tone\n• Nootropic effects\n• Lowers triglycerides",
        "protocol_detailed": "**Dosage:** 1-2mg\n**Frequency:** Nightly",
        "side_effects_detailed": "• Injection redness\n• Joint stiffness\n• Carpal Tunnel",
        "storage": "Refrigerate."
    },
    "Tesamorelin + Ipamorelin Blend": {
        "vial_mg": 12.0, "dose_mcg": 350.0, "default_dose_unit": "mcg", "default_stock_unit": "mg", "iu_conversion": None,
        "type": "Growth Hormone Blend", "filter_cat": "Slimming & Fat Loss",
        "desc": "The 'Shred Stack'.",
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
        "contraindications": "Active cancer.",
        "protocol_summary": "350mcg nightly.",
        "benefits_detailed": "• Max fat loss (Visceral)\n• Muscle definition\n• Deep sleep\n• Systemic anti-aging",
        "protocol_detailed": "**Dosage:** 350mcg\n**Frequency:** Nightly",
        "side_effects_detailed": "• Flushing\n• Joint stiffness\n• Water retention",
        "storage": "Refrigerate."
    },
    "Tirzepatide": {
        "vial_mg": 30.0, "dose_mcg": 2.5, "default_dose_unit": "mg", "default_stock_unit": "mg", "iu_conversion": None,
        "default_water_ml": 3.0,
        "type": "Metabolic", "filter_cat": "Slimming & Fat Loss",
        "desc": "Dual Agonist.",
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
        "contraindications": "MEN2, Medullary Thyroid Cancer.",
        "protocol_summary": "2.5mg weekly.",
        "benefits_detailed": "• Massive weight loss (22%)\n• Eliminates 'Food Noise'\n• Less nausea than Semaglutide\n• Metabolic repair",
        "protocol_detailed": "**Dosage:** 2.5mg\n**Frequency:** Weekly",
        "side_effects_detailed": "• Anhedonia\n• Constipation\n• Hair shedding",
        "storage": "Refrigerate."
    },
}

FACTORS = {'mcg': 1, 'mg': 1000, 'g': 1000000}

# Initialize State
if 'vial_val' not in st.session_state: st.session_state.vial_val = 30.0
if 'dose_val' not in st.session_state: st.session_state.dose_val = 2.5
if 'stock_unit_index' not in st.session_state: st.session_state.stock_unit_index = 0
if 'dose_unit_index' not in st.session_state: st.session_state.dose_unit_index = 0
if 'dose_unit_selection' not in st.session_state: st.session_state.dose_unit_selection = "mg"
if 'water_input' not in st.session_state: st.session_state.water_input = 3.0
if 'calc_count' not in st.session_state: st.session_state.calc_count = 0

# --- NAVIGATION SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/biotech.png", width=60)
    st.title("Navigation")
    page = st.radio("Go to:", ["🧮 Calculator", "📚 Peptide Database"])
    st.markdown("---")
    st.caption("v3.5 | by Musika")

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
             st.session_state.vial_val = float(data["vial_mg"]) 
             st.session_state.stock_unit_index = 3 # Index for IU in ["mg", "mcg", "g", "IU"]
        else:
             st.session_state.vial_val = float(data["vial_mg"])
             st.session_state.stock_unit_index = 0 # mg

        # Set Water
        if "default_water_ml" in data:
             st.session_state.water_input = data["default_water_ml"]
        else:
             st.session_state.water_input = 2.0

        # Set Dose
        target_val = float(data["dose_mcg"]) 
        unit_pref = data.get("default_dose_unit", "mcg")
        
        if unit_pref == "mg":
             st.session_state.dose_unit_selection = "mg"
             st.session_state.dose_val = target_val 
        elif unit_pref == "IU":
             st.session_state.dose_unit_selection = "IU"
             st.session_state.dose_val = target_val
        else:
             st.session_state.dose_unit_selection = "mcg"
             st.session_state.dose_val = target_val

        st.session_state.calc_count += 1

    def convert_dose_unit():
        pass

    # --- UI HEADER ---
    st.subheader("🧪 Reconstitution Calculator")
    st.divider()

    # --- MAIN LAYOUT ---
    left_col, right_col = st.columns([1, 1.2], gap="large")

    # === LEFT COLUMN: INPUTS ===
    with left_col:
        st.info("1️⃣ **Configuration**")
        
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
            vial_unit = st.selectbox("Unit", ["mg", "mcg", "g", "IU"], index=st.session_state.stock_unit_index, key="stock_unit_selection")
        with c3:
            water_ml = st.number_input("Water Added (mL)", key="water_input", step=0.5, min_value=0.1, format="%.1f")

        st.warning("⚠️ **Safety Check:** Ensure inputs match your physical supplies.")

        st.write("🎯 **Dosing**")
        c4, c5 = st.columns([2, 1])
        with c5:
            dose_unit = st.selectbox("Dose Unit", ["mcg", "mg", "g", "IU"], key="dose_unit_selection", on_change=convert_dose_unit)
        with c4:
            if dose_unit == 'mg': step = 0.5
            elif dose_unit == 'IU': step = 5.0
            elif dose_unit == 'mcg': step = 50.0
            else: step = 0.001
            desired_dose = st.number_input("Desired Dose", key="dose_val", min_value=0.0, step=step, format="%.4f" if dose_unit=='g' else "%.1f")
        
        syringe_type = st.radio("Syringe Type", ["U-100 (Standard)", "U-40 (Vet)"], horizontal=True)
        syringe_factor = 100 if "U-100" in syringe_type else 40

        # MOVED TO LEFT COLUMN
        st.divider()
        with st.expander("🛠️ How to Reconstitute (Mix)", expanded=True):
             if vial_qty > 0 and water_ml > 0:
                st.markdown(f"1. **Clean:** Wipe the top of the **{vial_qty} {vial_unit}** peptide vial and the water vial with an alcohol swab.\n2. **Withdraw:** Draw exactly **{water_ml} mL** of Bacteriostatic Water.\n3. **Inject:** Slowly inject the **{water_ml} mL** of water into the peptide vial. Aim for the glass wall, not the powder directly.\n4. **Mix:** **Do not shake.** Gently swirl the vial until dissolved.\n5. **Store:** Refrigerate immediately.")
             else:
                 st.write("Enter Stock and Water amounts to see specific instructions.")

    # === RIGHT COLUMN: RESULTS + PROFILE ===
    with right_col:
        st.success("2️⃣ **Profile & Results**")

        if vial_qty > 0 and water_ml > 0 and desired_dose > 0:
            
            conversion = peptide_info.get("iu_conversion")
            total_stock_units = 0
            stock_mg = 0 
            if vial_unit == 'mg': stock_mg = vial_qty
            elif vial_unit == 'mcg': stock_mg = vial_qty / 1000
            elif vial_unit == 'g': stock_mg = vial_qty * 1000
            
            if conversion and conversion > 1:
                if vial_unit in ['mg', 'mcg', 'g']:
                    total_stock_units = stock_mg * conversion 
                    display_strength = f"{stock_mg:.1f}mg ≈ {int(total_stock_units)} IU"
                else: 
                    total_stock_units = vial_qty
                    display_strength = f"{int(vial_qty)} IU"
                
                if dose_unit == 'IU': target_dose_units = desired_dose
                elif dose_unit == 'mg': target_dose_units = desired_dose * conversion
                elif dose_unit == 'mcg': target_dose_units = (desired_dose / 1000) * conversion
                else: target_dose_units = 0
                    
            elif conversion == 1: 
                total_stock_units = vial_qty 
                target_dose_units = desired_dose
                display_strength = f"{int(vial_qty)} IU"
                
            else:
                if vial_unit == 'mg': total_stock_units = vial_qty * 1000
                elif vial_unit == 'g': total_stock_units = vial_qty * 1000000
                elif vial_unit == 'mcg': total_stock_units = vial_qty
                else: total_stock_units = 0 
                
                if dose_unit == 'mg': target_dose_units = desired_dose * 1000
                elif dose_unit == 'g': target_dose_units = desired_dose * 1000000
                elif dose_unit == 'mcg': target_dose_units = desired_dose
                else: target_dose_units = 0
                
                display_strength = f"{total_stock_units/1000:.1f} mg"

            if total_stock_units > 0:
                concentration_per_ml = total_stock_units / water_ml
                draw_ml = target_dose_units / concentration_per_ml
                units = draw_ml * syringe_factor
                doses_per_vial = total_stock_units / target_dose_units
            else:
                draw_ml, units, doses_per_vial = 0, 0, 0

            c1, c2, c3 = st.columns(3)
            c1.metric("Draw Volume", f"{draw_ml:.4f} mL")
            c2.metric("Syringe Units", f"{units:.1f} Units")
            c3.metric("Doses / Vial", f"{int(doses_per_vial)}")
            
            percentage = min(units / syringe_factor * 100, 100)
            if units > syringe_factor:
                st.error("⚠️ **Volume too large for one syringe!**")
                st.markdown(f"""<div style="margin-bottom:5px; font-weight:bold;">Overflow:</div><div class="syringe-container"><div class="syringe-liquid" style="width: 100%; background-color: #ff0000;"></div><div class="syringe-markings"></div></div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style="margin-bottom:5px; font-weight:bold;">Visual Fill ({units:.1f}):</div><div class="syringe-container"><div class="syringe-liquid" style="width: {percentage}%;"></div><div class="syringe-markings"></div></div>""", unsafe_allow_html=True)
                st.caption(f"Draw to **{units:.1f}** on your {syringe_type} syringe.")
                
            if conversion:
                st.caption(f"ℹ️ **Conversion Applied:** {display_strength} | Dose: {target_dose_units:.1f} IU")

            st.write("")
            with st.expander(f"📖 **Profile: {selected_peptide}**", expanded=True):
                st.markdown(f"**Type:** {peptide_info['type']}")
                st.markdown(f"**🌟 Key Benefits:**")
                st.markdown(peptide_info['benefits_detailed'])
                
                st.markdown(f"""
                <div style="margin-top:10px; padding:10px; background-color:#3e1818; border-left:4px solid #ff4b4b; border-radius:4px;">
                <strong>⚠️ Common Side Effects:</strong><br>
                {peptide_info['side_effects_detailed'].strip().replace(chr(10), '<br>')}
                <br><br>
                <span class='contra-header'>⛔ Contraindications:</span>
                {peptide_info['contraindications']}
                </div>
                """, unsafe_allow_html=True)
                
                st.write("")
                st.info(f"**📋 Quick Protocol:** {peptide_info['protocol_summary']}")
                st.markdown(f"**❄️ Storage:** {peptide_info['storage']}")
                st.caption("*For clinical details, visit the 'Peptide Database' tab.*")

            protocol_text = f"Peptide: {selected_peptide}\nType: {peptide_info['type']}\nStock: {vial_qty}{vial_unit} + {water_ml}mL Water\nDose: {desired_dose}{dose_unit} = {units:.1f} Units\nProtocol: {peptide_info['protocol_summary']}"
            st.download_button("💾 Save Protocol", protocol_text, "protocol.txt", use_container_width=True)

        else:
            st.info("Enter inputs to see results.")

    # 3. BOTTOM: VISUAL GUIDE
    st.divider()
    with st.expander("💉 Visual Guide: Injection Sites", expanded=False):
        try:
            st.image("Sites.jpeg", caption="Recommended Subcutaneous Zones", use_container_width=True)
        except:
            st.warning("⚠️ Image 'Sites.jpeg' not found.")

    st.caption(f"v3.5 | Calculations: {st.session_state.calc_count}")

# ==============================================================================
# PAGE 2: DATABASE
# ==============================================================================
elif page == "📚 Peptide Database":
    st.subheader("📚 Peptide Database")
    st.divider()
    
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
                
                st.markdown(f"""
                <div class='side-effect-box'>
                <strong>⚠️ Side Effects:</strong><br>
                {info['side_effects_detailed'].strip().replace(chr(10), '<br>')}
                <br><br>
                <span class='contra-header'>⛔ Contraindications:</span>
                {info['contraindications']}
                </div>
                """, unsafe_allow_html=True)
                
                st.write("")
                with st.expander("📋 Detailed Protocol", expanded=True):
                     st.markdown(info['protocol_detailed'])
                with st.expander("ℹ️ Description & Mechanism"):
                    st.markdown(f"_{info['desc']}_")
                    st.markdown(f"**❄️ Storage:** {info['storage']}")
