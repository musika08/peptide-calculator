import streamlit as st
import math
import pandas as pd

# --- 1. CONFIGURATION: WIDE MODE ---
st.set_page_config(
    page_title="PeptideCalc Pro v2.1",
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
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        font-weight: bold;
    }
    /* Improve Expanders in Database */
    .streamlit-expanderHeader {
        font-weight: bold;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# --- EXPANDED HIGH-DETAIL KNOWLEDGE BASE (v2.1) ---
PEPTIDE_PRESETS = {
    "Custom (Enter manually)": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "freq": "As directed", 
        "type": "N/A",
        "desc": "Manual calculation for custom compounds.", 
        "benefits": "N/A",
        "note": "Verify molecular weight and concentration if applicable.",
        "side_effects": "Unknown.",
        "storage": "Dependant on compound."
    },
    "AOD-9604": {
        "vial_mg": 5.0, "dose_mcg": 300.0, "freq": "Daily (AM)", 
        "type": "Fat Loss",
        "desc": "Anti-Obesity Drug 9604. A modified fragment (C-terminal) of Human Growth Hormone (HGH) that retains the lipolytic (fat burning) properties of HGH without the insulin or growth effects.", 
        "benefits": "- **Pure Fat Loss:** Specifically targets adipose tissue reduction.\n- **No Blood Sugar Impact:** Does not induce hyperglycemia like full HGH.\n- **Joint Health:** Some users report mild cartilage repair benefits.",
        "note": "🔹 **Dosage:** 300mcg daily.\n🔹 **Frequency:** Once per day.\n🔹 **Timing:** Immediately upon waking, completely fasted. Wait 1-2 hours before eating.\n🔹 **Cycle:** 12 weeks on, 4 weeks off.",
        "side_effects": "Very mild. Occasional stomach upset or headache initially.",
        "storage": "Refrigerate. Stable."
    },
    "BPC-157": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "freq": "Daily (or 2x Daily)", 
        "type": "Regenerative",
        "desc": "Body Protection Compound-157. A 15-amino acid chain derived from gastric juice. It modulates the nitric oxide system and promotes angiogenesis (creation of new blood vessels).", 
        "benefits": "- **Soft Tissue:** Rapidly heals tendons, ligaments, and bones.\n- **GI Tract:** Heals gastric ulcers, leaky gut, and IBS symptoms.\n- **Neurological:** Neuroprotective; heals dopamine/serotonin systems.",
        "note": "🔹 **Dosage:** 250mcg to 500mcg.\n🔹 **Frequency:** 1-2 times daily.\n🔹 **Timing:** Anytime. Can be taken with food.\n🔹 **Cycle:** 4-6 weeks for injury, then 2 weeks off.",
        "side_effects": "Extremely safe. Rare fatigue or temporary anhedonia (dopamine regulation).",
        "storage": "Refrigerate after mixing. Highly stable."
    },
    "BPC-157 + TB-500 Blend": {
        "vial_mg": 10.0, "dose_mcg": 500.0, "freq": "Daily (or 2x Daily)", 
        "type": "Regenerative Blend",
        "desc": "The 'Wolverine Stack'. Synergistic combination where BPC-157 works on tendons/ligaments/gut, while TB-500 works on muscle tissue and promotes actin regulation for cellular migration.", 
        "benefits": "- **Maximum Healing:** The ultimate protocol for post-surgery or acute injury.\n- **Flexibility:** Noticeable improvement in joint range of motion.\n- **Cardio-Protection:** TB-500 aids in cardiac tissue repair.",
        "note": "🔹 **Dosage:** 500mcg - 1mg total fluid (yields 250-500mcg of each).\n🔹 **Frequency:** Daily.\n🔹 **Cycle:** Run for duration of injury (4-8 weeks).\n🔹 **Pro-Tip:** If you feel a head rush, inject slower.",
        "side_effects": "Head rush (from TB-500), fatigue. Do not use if active cancer is present.",
        "storage": "Refrigerate after mixing."
    },
    "CJC-1295 (No DAC)": {
        "vial_mg": 5.0, "dose_mcg": 100.0, "freq": "Daily (PM)", 
        "type": "Growth Hormone",
        "desc": "A GHRH (Growth Hormone Releasing Hormone) analog that acts on the pituitary gland to release bursts of natural GH. 'No DAC' means it has a short half-life, mimicking natural pulses.", 
        "benefits": "- **Hyperplasia:** Increases number of muscle cells.\n- **Recovery:** Improves deep wave sleep.\n- **Cosmetic:** Plumps skin and thickens hair.",
        "note": "🔹 **Dosage:** 100mcg.\n🔹 **Frequency:** 1-3 times daily (Pre-bed is best).\n🔹 **Timing:** ⚠️ **FASTED ONLY.** 2+ hours after food.\n🔹 **Cycle:** 5 days on, 2 days off.",
        "side_effects": "Head rush, flushing, vivid dreams. Carpal tunnel symptoms if overdosed.",
        "storage": "Refrigerate. Sensitive to light/heat."
    },
    "CJC-1295 + Ipamorelin Blend": {
        "vial_mg": 10.0, "dose_mcg": 200.0, "freq": "Daily (PM)", 
        "type": "Growth Hormone Blend",
        "desc": "The Gold Standard for GH enhancement. Synergistic pairing of a GHRH (CJC) and a GHRP (Ipamorelin). Together, they release 5x to 10x more GH than either used alone.", 
        "benefits": "- **Synergy:** Creates a massive GH pulse without shutting down natural production.\n- **Fat Loss:** Mobilizes visceral fat while sleeping.\n- **Safety:** No cortisol/prolactin spikes.",
        "note": "🔹 **Dosage:** 200mcg - 300mcg total fluid.\n🔹 **Timing:** ⚠️ **FASTED ONLY.** Immediately before bed.\n🔹 **Cycle:** 5 days on, 2 days off (12-16 weeks).",
        "side_effects": "Intense head rush, deep sleep, vivid dreams, mild water retention.",
        "storage": "Refrigerate. Do not shake vigorously."
    },
    "Epithalon": {
        "vial_mg": 10.0, "dose_mcg": 5000.0, "freq": "Daily (Course)", 
        "type": "Anti-Aging",
        "desc": "Synthetic tetrapeptide derived from the pineal gland. It up-regulates telomerase production to elongate telomeres (the protective caps on DNA).", 
        "benefits": "- **Longevity:** Increases lifespan in animal models.\n- **Circadian Rhythm:** Resets sleep cycles/melatonin.\n- **Immunity:** Restores thymus function.",
        "note": "🔹 **Dosage:** 5mg - 10mg.\n🔹 **Frequency:** Daily for 10-20 days.\n🔹 **Cycle:** Run this short course once every 6-12 months.\n🔹 **Pro-Tip:** Can be taken AM or PM.",
        "side_effects": "Very rare. Vivid dreams.",
        "storage": "Refrigerate after mixing."
    },
    "GHK-Cu": {
        "vial_mg": 50.0, "dose_mcg": 2000.0, "freq": "Daily", 
        "type": "Cosmetic/Repair",
        "desc": "Copper Tripeptide-1. Modulates over 4,000 human genes back to a younger state. Powerful remodeling agent for skin and scar tissue.", 
        "benefits": "- **Skin:** Increases collagen by 70%, tightens loose skin.\n- **Hair:** Enlarges hair follicles (reverses miniaturization).\n- **Wounds:** Accelerates healing.",
        "note": "🔹 **Dosage:** 1mg - 2mg.\n🔹 **Timing:** Evening preferred.\n🔹 **Warning:** **STINGS.** Dilute with extra water or mix with BPC-157.\n🔹 **Cycle:** 30 days on, then break to monitor copper levels.",
        "side_effects": "Painful injection site (red welts), potential zinc depletion (take Zinc supplement).",
        "storage": "Refrigerate. Protect from light."
    },
    "Glow Blend (GHK-Cu/BPC/TB)": {
        "vial_mg": 70.0, "dose_mcg": 2500.0, "freq": "Daily", 
        "type": "Cosmetic/Recovery Blend",
        "desc": "A 70mg tri-blend. BPC and TB buffer the acidic sting of GHK-Cu while adding systemic repair properties.", 
        "benefits": "- **Painless:** BPC neutralizes the GHK sting.\n- **Total Package:** Skin elasticity, hair regrowth, and muscle recovery.",
        "note": "🔹 **Dosage:** 2.5mg - 3mg total fluid.\n🔹 **Frequency:** Daily (Evening).\n🔹 **Cycle:** 4-6 weeks.",
        "side_effects": "Mild redness. Take Zinc supplement during cycle.",
        "storage": "Refrigerate strictly."
    },
    "HCG": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "freq": "2-3x / Week", 
        "type": "Hormonal",
        "desc": "Human Chorionic Gonadotropin. Mimics LH to stimulate Leydig cells in the testes.", 
        "benefits": "- **TRT:** Prevents testicular atrophy.\n- **Fertility:** Increases sperm count.\n- **Mood:** Upregulates neurosteroids (DHEA/Pregnenolone).",
        "note": "🔹 **Dosage:** 250iu - 500iu (approx 250-500mcg equivalent).\n🔹 **Frequency:** 2-3 times per week.\n🔹 **Timing:** Morning.",
        "side_effects": "Estrogen spikes (gynecomastia risk), acne. Monitor E2 levels.",
        "storage": "MUST Refrigerate. Fragile."
    },
    "IGF-1 LR3": {
        "vial_mg": 1.0, "dose_mcg": 50.0, "freq": "Pre-Workout", 
        "type": "Anabolic",
        "desc": "Insulin-like Growth Factor 1 (Long Arg3). A modified version of IGF-1 with a longer half-life (20-30 hours). It forces nutrients into muscle cells causing hyperplasia (new cell growth).", 
        "benefits": "- **Hyperplasia:** Splits muscle cells creating new fibers.\n- **Pumps:** Extreme muscle fullness.\n- **Nutrient Partitioning:** Shuttles carbs into muscle, not fat.",
        "note": "🔹 **Dosage:** 20mcg - 50mcg (Start low!).\n🔹 **Timing:** Pre or Post workout.\n🔹 **Cycle:** 4 weeks on, 4 weeks off (receptors downregulate fast).\n⚠️ **WARNING:** Risk of hypoglycemia. Consume carbs immediately after.",
        "side_effects": "Hypoglycemia (low blood sugar), gut growth (if abused), headaches.",
        "storage": "Refrigerate. Very delicate."
    },
    "Ipamorelin": {
        "vial_mg": 5.0, "dose_mcg": 100.0, "freq": "Daily (PM)", 
        "type": "Growth Hormone",
        "desc": "The mildest GHRP. Mimics Ghrelin but without the extreme hunger side effect.", 
        "benefits": "- **Lean Mass:** Preserves muscle in deficits.\n- **Sleep:** Increases REM sleep.\n- **Safe:** No cortisol elevation.",
        "note": "🔹 **Dosage:** 100mcg - 300mcg.\n🔹 **Timing:** ⚠️ **FASTED ONLY.** Before bed.\n🔹 **Cycle:** 12+ weeks.",
        "side_effects": "Very rare. Mild water retention.",
        "storage": "Refrigerate. Do not shake."
    },
    "Kisspeptin": {
        "vial_mg": 10.0, "dose_mcg": 100.0, "freq": "As needed", 
        "type": "Hormonal",
        "desc": "Neuromodulator that stimulates GnRH release. A safer alternative to HCG for restarting natural testosterone.", 
        "benefits": "- **HPTA:** Restarts natural production safely.\n- **Libido:** Enhances sexual desire via brain pathways.",
        "note": "🔹 **Dosage:** 100mcg - 200mcg.\n🔹 **Frequency:** Daily or EOD.\n🔹 **Timing:** Evening.",
        "side_effects": "Flushing. Safe profile.",
        "storage": "Refrigerate."
    },
    "Klow Blend (GHK-Cu/BPC/TB/KPV)": {
        "vial_mg": 80.0, "dose_mcg": 3000.0, "freq": "Daily", 
        "type": "Ultimate Repair/Cosmetic Blend",
        "desc": "The Master Stack. Adds **KPV** to the Glow blend. KPV is a potent anti-inflammatory and antimicrobial peptide.", 
        "benefits": "- **Skin:** KPV clears acne, psoriasis, and eczema.\n- **Gut:** KPV + BPC is the strongest stack for IBD/Colitis.\n- **Systemic:** Total body repair.",
        "note": "🔹 **Dosage:** ~3mg total fluid.\n🔹 **Frequency:** Daily (Evening).\n🔹 **Pro-Tip:** Rotate injection sites religiously to prevent welts.",
        "side_effects": "Red welts (common), fatigue. Zinc supplementation recommended.",
        "storage": "Refrigerate strictly."
    },
    "Melanotan II": {
        "vial_mg": 10.0, "dose_mcg": 500.0, "freq": "Daily (Loading)", 
        "type": "Cosmetic",
        "desc": "Alpha-MSH analog. Stimulates melanin (tanning) and libido.", 
        "benefits": "- **Tan:** Deep tan with minimal sun.\n- **Libido:** Extreme sexual arousal.\n- **Diet:** Suppresses appetite.",
        "note": "🔹 **Dosage:** 100mcg - 500mcg.\n🔹 **Timing:** 30 mins before UV exposure.\n🔹 **Protocol:** Load daily until tanned, then 1x weekly maintenance.",
        "side_effects": "Nausea (severe if dosed high), facial flushing, spontaneous erections, darkening of moles.",
        "storage": "Refrigerate. Stable."
    },
    "MOTS-c": {
        "vial_mg": 10.0, "dose_mcg": 5000.0, "freq": "Weekly", 
        "type": "Mitochondrial",
        "desc": "Mitochondrial Open Reading Frame of the 12S rRNA-c. A peptide encoded in the mitochondria that regulates metabolic homeostasis. Often called 'Exercise in a Bottle'.", 
        "benefits": "- **Endurance:** drastically increases exercise capacity and energy.\n- **Metabolism:** Improves glucose metabolism and insulin sensitivity.\n- **Cellular:** Promotes mitochondrial biogenesis (new mitochondria creation).",
        "note": "🔹 **Dosage:** 5mg - 10mg.\n🔹 **Frequency:** Once weekly (or 2mg every 3 days).\n🔹 **Timing:** Immediately before endurance exercise.\n⚠️ **WARNING:** The injection **STINGS** significantly. Warm the syringe in hands before injecting.",
        "side_effects": "Injection site pain (burning), flu-like symptoms for a few hours after injection.",
        "storage": "Refrigerate. Use vial quickly after mixing (less stable than others)."
    },
    "NAD+": {
        "vial_mg": 500.0, "dose_mcg": 25000.0, "freq": "2-3x / Week", 
        "type": "Cellular Energy",
        "desc": "Essential coenzyme for ATP production and DNA repair.", 
        "benefits": "- **Mental:** Clears brain fog.\n- **Energy:** Restores cellular ATP.\n- **Anti-Aging:** Activates Sirtuins.",
        "note": "🔹 **Dosage:** 25mg - 50mg.\n🔹 **Frequency:** 2-3x weekly.\n⚠️ **WARNING:** Inject **VERY SLOWLY** (over 60 seconds) to avoid the 'NAD Flush' (chest pressure/anxiety).",
        "side_effects": "Chest tightness, palpitations, nausea (if injected fast).",
        "storage": "Refrigerate immediately. Degrades in heat."
    },
    "PEG-MGF": {
        "vial_mg": 2.0, "dose_mcg": 200.0, "freq": "Post-Workout", 
        "type": "Anabolic/Repair",
        "desc": "Pegylated Mechano Growth Factor. A variant of IGF-1 that triggers satellite cells to repair damaged muscle tissue. The PEGylation increases half-life from minutes to days.", 
        "benefits": "- **Recovery:** Accelerates repair of torn muscle fibers.\n- **Lagging Parts:** Often used to bring up lagging muscle groups.\n- **Neuro:** Neuroprotective effects.",
        "note": "🔹 **Dosage:** 200mcg - 400mcg.\n🔹 **Timing:** Post-workout or on Rest Days.\n🔹 **Cycle:** 4-6 weeks.\n🔹 **Site:** Can be injected SubQ or IM into the target muscle.",
        "side_effects": "Injection site pain, potential hypoglycemia (rare compared to IGF-1).",
        "storage": "Refrigerate. Do not shake."
    },
    "PT-141": {
        "vial_mg": 10.0, "dose_mcg": 1000.0, "freq": "As needed", 
        "type": "Libido",
        "desc": "Bremelanotide. Targets brain receptors to increase sexual desire.", 
        "benefits": "- **ED:** Works on non-vascular ED.\n- **Libido:** Increases desire in men and women.",
        "note": "🔹 **Dosage:** 1mg - 2mg.\n🔹 **Timing:** 2-4 hours BEFORE activity.\n🔹 **Duration:** Effects last up to 24h.",
        "side_effects": "Nausea (common), flushing, headache.",
        "storage": "Refrigerate."
    },
    "Retatrutide": {
        "vial_mg": 10.0, "dose_mcg": 2000.0, "freq": "Once Weekly", 
        "type": "Metabolic (GLP-1/GIP/Glucagon)",
        "desc": "Triple Agonist. The most potent weight loss agent currently available.", 
        "benefits": "- **Weight Loss:** 24%+ average loss.\n- **Liver:** Clears fatty liver disease.\n- **Metabolism:** Actively burns fat (Glucagon).",
        "note": "🔹 **Dosage:** Start 2mg. Titrate +2mg every 4 weeks.\n🔹 **Max Dose:** 12mg.\n🔹 **Frequency:** Once weekly.",
        "side_effects": "Rapid heart rate, skin sensitivity (allodynia), nausea.",
        "storage": "Refrigerate. Do not freeze."
    },
    "Selank": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "freq": "Daily", 
        "type": "Nootropic",
        "desc": "Synthetic analog of the immunomodulatory peptide Tuftsin. Known for its pronounced anxiolytic (anti-anxiety) and nootropic effects.", 
        "benefits": "- **Anxiety:** Reduces stress without sedation.\n- **Focus:** Improves mental clarity and memory.\n- **Immunity:** Modulates the immune system.",
        "note": "🔹 **Dosage:** 250mcg - 500mcg.\n🔹 **Frequency:** Daily or as needed for stress.\n🔹 **Route:** SubQ (injectable version).",
        "side_effects": "Very rare. Fatigue if dosed too high.",
        "storage": "Refrigerate."
    },
    "Semaglutide": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "freq": "Once Weekly", 
        "type": "Metabolic (GLP-1)",
        "desc": "GLP-1 Agonist. Slows digestion and signals fullness.", 
        "benefits": "- **Weight Loss:** 15% average loss.\n- **Heart:** Cardioprotective.\n- **Habits:** Breaks addiction loops.",
        "note": "🔹 **Dosage:** Start 0.25mg. Titrate every 4 weeks.\n🔹 **Max Dose:** 2.4mg.\n🔹 **Frequency:** Once weekly.",
        "side_effects": "Nausea, constipation, fatigue, 'Ozempic face'.",
        "storage": "Refrigerate. Protect from light."
    },
    "Semax": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "freq": "Daily", 
        "type": "Nootropic",
        "desc": "Derived from Adrenocorticotropic Hormone (ACTH). Highly potent nootropic used for cognitive enhancement and stroke recovery.", 
        "benefits": "- **Cognition:** Enhances attention, memory, and learning.\n- **Neuroprotection:** Protects neurons from oxidative stress.\n- **Mood:** Mild elevation in mood and motivation.",
        "note": "🔹 **Dosage:** 250mcg - 500mcg.\n🔹 **Frequency:** Daily (Morning).\n🔹 **Route:** SubQ (injectable version).",
        "side_effects": "Mild stimulation, difficulty sleeping if taken too late.",
        "storage": "Refrigerate."
    },
    "TB-500": {
        "vial_mg": 5.0, "dose_mcg": 2500.0, "freq": "2x / Week", 
        "type": "Regenerative",
        "desc": "Synthetic Thymosin Beta-4. Directs stem cells to damage.", 
        "benefits": "- **Muscle:** Heals tears and strains.\n- **Joints:** Improves flexibility.\n- **Heart:** Repairs cardiac tissue.",
        "note": "🔹 **Dosage:** 2.5mg.\n🔹 **Frequency:** 2x per week (e.g., Mon/Thu).\n🔹 **Cycle:** 4-6 weeks.",
        "side_effects": "Head rush. Avoid if active cancer present.",
        "storage": "Refrigerate."
    },
    "Tesamorelin": {
        "vial_mg": 2.0, "dose_mcg": 1000.0, "freq": "Daily (PM)", 
        "type": "Growth Hormone",
        "desc": "Potent GHRH for visceral fat reduction.", 
        "benefits": "- **Belly Fat:** specifically targets visceral fat.\n- **Lipids:** Lowers triglycerides.",
        "note": "🔹 **Dosage:** 1mg - 2mg.\n🔹 **Timing:** ⚠️ **FASTED ONLY.** Before bed.\n🔹 **Cycle:** 8-12 weeks.",
        "side_effects": "Injection site redness, water retention, joint stiffness.",
        "storage": "Refrigerate."
    },
    "Tesamorelin + Ipamorelin Blend": {
        "vial_mg": 12.0, "dose_mcg": 350.0, "freq": "Daily (PM)", 
        "type": "Growth Hormone/Fat Loss Blend",
        "desc": "The Ultimate Shred Stack.", 
        "benefits": "- **Recomp:** Burn fat and build muscle simultaneously.\n- **Metabolic:** Lowers inflammation.",
        "note": "🔹 **Dosage:** 350mcg - 500mcg total.\n🔹 **Timing:** ⚠️ **FASTED ONLY.** Before bed.\n🔹 **Cycle:** 5 on / 2 off.",
        "side_effects": "Joint stiffness, flushing, vivid dreams.",
        "storage": "Refrigerate."
    },
    "Thymalin": {
        "vial_mg": 10.0, "dose_mcg": 5000.0, "freq": "Daily (Course)", 
        "type": "Immune/Anti-Aging",
        "desc": "A polypeptide extract from the thymus gland. It regulates the immune system and has profound anti-aging effects when combined with Epithalon.", 
        "benefits": "- **Immunity:** Corrects immunodeficiency and autoimmune conditions.\n- **Longevity:** Reduces all-cause mortality in trials.\n- **Balance:** Normalizes T-cell/B-cell ratios.",
        "note": "🔹 **Dosage:** 5mg - 10mg.\n🔹 **Frequency:** Daily for 10 days.\n🔹 **Cycle:** Repeat every 6-12 months.\n🔹 **Stack:** Often cycled with Epithalon.",
        "side_effects": "None reported. Very safe.",
        "storage": "Refrigerate."
    },
    "Tirzepatide": {
        "vial_mg": 30.0, "dose_mcg": 2500.0, "freq": "Once Weekly", 
        "type": "Metabolic (GLP-1/GIP)",
        "desc": "Dual Agonist. The GIP component reduces nausea vs Semaglutide.", 
        "benefits": "- **Weight Loss:** 20%+ average.\n- **Satiety:** Silences food noise.",
        "note": "🔹 **Dosage:** Start 2.5mg. Titrate +2.5mg every 4 weeks.\n🔹 **Max Dose:** 15mg.\n🔹 **Frequency:** Once weekly.",
        "side_effects": "Anhedonia, constipation, cold extremities, hair shedding.",
        "storage": "Refrigerate."
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

# --- NAVIGATION SIDEBAR (v2.1 UI) ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/biotech.png", width=60) # Placeholder logo
    st.title("Navigation")
    page = st.radio("Go to:", ["🧮 Calculator", "📚 Peptide Database"])
    st.markdown("---")
    
    # Ko-fi Button
    st.link_button("☕ Support my work (Ko-fi)", "https://ko-fi.com/musika", use_container_width=True)
    st.caption("v2.1 | by Musika")

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
        
        # Sort keys alphabetically
        sorted_peptides = sorted(list(PEPTIDE_PRESETS.keys()))
        # Ensure Custom is first
        if "Custom (Enter manually)" in sorted_peptides:
            sorted_peptides.insert(0, sorted_peptides.pop(sorted_peptides.index("Custom (Enter manually)")))

        selected_peptide = st.selectbox("Select Peptide Profile", sorted_peptides, key="peptide_selector", on_change=load_preset)
        
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

            with st.expander(f"📖 **Profile: {selected_peptide}**", expanded=True):
                if selected_peptide == "Custom (Enter manually)":
                     st.write("Manual mode selected.")
                else:
                    st.markdown(f"**Type:** {peptide_info['type']}")
                    st.markdown(f"**Description:** {peptide_info['desc']}")
                    st.markdown(f"**🌟 Benefits:** {peptide_info['benefits']}")
                    st.markdown(f"**Frequency:** {peptide_info['freq']}")
                    st.warning(f"**⚠️ Side Effects:** {peptide_info['side_effects']}")
                    st.info(f"**📋 Instructions:** {peptide_info['note']}")
                    st.markdown(f"**❄️ Storage:** {peptide_info['storage']}")

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

            protocol_text = f"Peptide: {selected_peptide}\nFreq: {peptide_info['freq']}\nStock: {vial_qty}{vial_unit} + {water_ml}mL Water\nConc: {concentration_mg_ml:.2f} mg/mL\nDose: {desired_dose}{dose_unit} = {units:.1f} Units ({syringe_type})\nSupply: 1 vial lasts approx {int(doses_per_vial)} doses.\n\nDetails:\n{peptide_info['desc']}\nBenefits: {peptide_info['benefits']}\nStorage: {peptide_info['storage']}\nInstructions: {peptide_info['note']}"
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
# PAGE 2: PEPTIDE DATABASE (Notion-Style)
# ==============================================================================
elif page == "📚 Peptide Database":
    st.subheader("📚 Peptide Database")
    st.caption("A comprehensive guide to the compounds available in our system, inspired by the Foofyrka Notion database.")
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
        if search_query not in name.lower() and search_query not in data['benefits'].lower() and search_query not in data['desc'].lower():
            continue
        filtered_items[name] = data

    # Display Grid (3 columns)
    num_cols = 3
    cols = st.columns(num_cols)
    
    # Sort items alphabetically
    sorted_items = dict(sorted(filtered_items.items()))
    
    for idx, (name, info) in enumerate(sorted_items.items()):
        col = cols[idx % num_cols]
        with col:
            # Replicating Notion Card Style
            with st.container(border=True):
                st.markdown(f"### {name}")
                st.markdown(f"<span class='db-tag'>{info['type']}</span>", unsafe_allow_html=True)
                st.write("") # Spacer
                st.markdown(f"**Description:** {info['desc']}")
                
                with st.expander("🌟 View Benefits"):
                    st.markdown(info['benefits'])
                with st.expander("📋 Protocol & Side Effects"):
                    st.markdown(f"{info['note']}")
                    st.markdown(f"**⚠️ Side Effects:** {info['side_effects']}")
                    st.markdown(f"**❄️ Storage:** {info['storage']}")

    if len(filtered_items) == 0:
        st.warning("No peptides match your search criteria. Try clearing the filters.")

# --- UNIVERSAL DISCLAIMER ---
st.markdown("---")
st.caption("⚠️ **Medical Disclaimer:** This tool is for educational and informational purposes only and does not constitute medical advice. Always verify calculations with a professional. The developers assume no liability for errors or misuse.")
