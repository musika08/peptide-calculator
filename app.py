import streamlit as st
import math
import pandas as pd

# --- 1. CONFIGURATION: WIDE MODE ---
st.set_page_config(
    page_title="PeptideCalc Pro v2.0",
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
</style>
""", unsafe_allow_html=True)

# --- EXPANDED HIGH-DETAIL KNOWLEDGE BASE (v2.0 - Cleaned MG Conversions) ---
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
    "BPC-157": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "freq": "Daily (or 2x Daily)", 
        "type": "Regenerative",
        "desc": "Body Protection Compound-157. A 15-amino acid chain derived from gastric juice. It modulates the nitric oxide system and promotes angiogenesis (creation of new blood vessels).", 
        "benefits": "- **Soft Tissue:** Rapidly heals tendons, ligaments, and bones.\n- **GI Tract:** Heals gastric ulcers, IBS, leaky gut, and Crohn's disease symptoms.\n- **Neurological:** Neuroprotective properties; heals dopamine and serotonin systems (often used post-substance abuse).\n- **Systemic:** Lowers blood pressure slightly and reduces overall inflammation.",
        "note": "**Protocol:** 250mcg - 500mcg injected 1 to 2 times daily. SubQ injections have a systemic effect, but injecting near the injury site (if applicable) is preferred by many. **Cycle:** 4 to 6 weeks, then 2 weeks off. **Half-life:** ~4-6 hours.",
        "side_effects": "Generally considered extremely safe. Rare side effects include fatigue, lethargy, temporary anhedonia (blunting of emotions due to dopaminergic resetting), or mild injection site reactions.",
        "storage": "Refrigerate after mixing. Highly stable. Use within 30-45 days."
    },
    "BPC-157 + TB-500 Blend": {
        "vial_mg": 10.0, "dose_mcg": 500.0, "freq": "Daily (or 2x Daily)", 
        "type": "Regenerative Blend",
        "desc": "The 'Wolverine Stack'. Synergistic combination where BPC-157 works on tendons/ligaments/gut, while TB-500 works on muscle tissue and promotes actin regulation for cellular migration.", 
        "benefits": "- **Maximum Healing:** The ultimate protocol for post-surgery or acute physical injury.\n- **Flexibility:** Noticeable improvement in joint and muscle flexibility.\n- **Hair & Heart:** TB-500 promotes hair growth and protects cardiac tissue post-injury.",
        "note": "**Protocol:** 500mcg - 1mg total fluid daily (yielding 250mcg-500mcg of EACH compound). Injected SubQ. **Cycle:** Run for the duration of injury recovery (typically 4-8 weeks).",
        "side_effects": "Head rush upon injection (from TB-500), fatigue, lethargy. Angiogenic properties mean this should NOT be used by individuals with active cancers.",
        "storage": "Refrigerate after mixing. Use within 30 days."
    },
    "CJC-1295 (No DAC)": {
        "vial_mg": 5.0, "dose_mcg": 100.0, "freq": "Daily (PM)", 
        "type": "Growth Hormone",
        "desc": "A GHRH (Growth Hormone Releasing Hormone) analog that acts on the pituitary gland to release bursts of natural GH.", 
        "benefits": "- **Hyperplasia:** Increases the number of muscle cells (not just size).\n- **Recovery:** Significantly improves Stage 4 deep sleep (slow-wave sleep).\n- **Anti-Aging:** Plumps skin, thickens hair, and improves bone density over long durations.",
        "note": "⚠️ **FASTED ONLY.** Inject immediately **before bed** on an empty stomach (No food for at least 2 hours prior, especially carbs/fats, as insulin blunts GH release). **Cycle:** 5 days on, 2 days off to prevent pituitary downregulation. **Half-life:** ~30 minutes.",
        "side_effects": "Head rush/throbbing immediately post-injection (normal), facial flushing, vivid dreams, mild water retention, tingling in hands/feet (carpal tunnel-like symptoms if dosed too high).",
        "storage": "Refrigerate. Sensitive to light/heat."
    },
    "CJC-1295 + Ipamorelin Blend": {
        "vial_mg": 10.0, "dose_mcg": 200.0, "freq": "Daily (PM)", 
        "type": "Growth Hormone Blend",
        "desc": "The Gold Standard for GH enhancement. Synergistic pairing of a GHRH (CJC) and a GHRP (Ipamorelin). Together, they release 5x to 10x more GH than either used alone.", 
        "benefits": "- **Synergy:** Creates a massive GH pulse while maintaining the body's natural feedback loop (unlike synthetic HGH).\n- **Fat Loss:** Mobilizes stored visceral fat while sleeping.\n- **Safe:** Ipamorelin does not spike cortisol or prolactin (unlike GHRP-6 or GHRP-2).",
        "note": "⚠️ **FASTED ONLY.** 200mcg to 300mcg total daily, right before bed. Must be 2 hours fasted. **Cycle:** 5 days on, 2 days off. Can be run for 3-6 months safely.",
        "side_effects": "Intense head rush, deep sleep, vivid dreams, water weight gain, numb fingers.",
        "storage": "Refrigerate. Do not shake vigorously—roll gently to mix."
    },
    "Epithalon": {
        "vial_mg": 10.0, "dose_mcg": 5000.0, "freq": "Daily (Course)", 
        "type": "Anti-Aging",
        "desc": "Synthetic tetrapeptide derived from the pineal gland. It up-regulates telomerase production to elongate telomeres (the protective caps on DNA).", 
        "benefits": "- **True Anti-Aging:** Shown to reduce all-cause mortality in Russian human trials.\n- **Sleep:** Resets circadian rhythm and boosts natural melatonin.\n- **Immunity:** Dramatically improves thymus function and T-cell count.",
        "note": "**Protocol (Russian Khavinson):** 5mg to 10mg daily for 10-20 consecutive days. Do not repeat for 6-12 months. Can be taken AM or PM.",
        "side_effects": "Very few reported. Occasional vivid dreams or daytime sleepiness.",
        "storage": "Refrigerate after mixing."
    },
    "GHK-Cu": {
        "vial_mg": 50.0, "dose_mcg": 2000.0, "freq": "Daily", 
        "type": "Cosmetic/Repair",
        "desc": "Copper Tripeptide-1. Found naturally in human plasma but drops by 60%+ by age 60. Modulates over 4,000 human genes back to a younger state.", 
        "benefits": "- **Skin:** Increases collagen (by 70%), elastin, and glycosaminoglycans.\n- **Hair:** Enlarges hair follicles and stops hair loss (often outperforming Minoxidil).\n- **Healing:** Accelerates wound contraction.",
        "note": "**Protocol:** 1mg - 2mg daily SubQ. 🌙 **EVENING PREFERRED.** Dilute with extra bacteriostatic water to reduce sting. **Cycle:** 30 days on, then monitor systemic copper levels.",
        "side_effects": "Notorious injection site pain (stinging and large red welts). Potential for systemic copper toxicity or zinc depletion if used long-term without zinc supplementation.",
        "storage": "Refrigerate. Keep away from strong light."
    },
    "Glow Blend (GHK-Cu/BPC/TB)": {
        "vial_mg": 70.0, "dose_mcg": 2500.0, "freq": "Daily", 
        "type": "Cosmetic/Recovery Blend",
        "desc": "A 70mg tri-blend of GHK-Cu, BPC-157, and TB-500. The BPC and TB eliminate the painful injection sting of GHK-Cu while amplifying the tissue regenerative effects.", 
        "benefits": "- **Painless GHK-Cu:** BPC neutralizes the acidic sting of the copper.\n- **Total Rejuvenation:** Combines the systemic healing of BPC/TB with the cosmetic power of GHK-Cu.\n- Targets hair, skin elasticity, gut health, and muscle recovery all at once.",
        "note": "**Protocol:** 2.5mg to 3mg daily SubQ. **Cycle:** 4 to 6 weeks. Rotate injection sites daily. Inject at night.",
        "side_effects": "Mild redness at injection site. Requires zinc supplementation if run for longer than 30 days.",
        "storage": "Refrigerate strictly. Protect from light."
    },
    "HCG": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "freq": "2-3x / Week", 
        "type": "Hormonal",
        "desc": "Human Chorionic Gonadotropin. Mimics Luteinizing Hormone (LH) to stimulate Leydig cells in the testes to produce testosterone and sperm.", 
        "benefits": "- **TRT Essential:** Prevents testicular shrinkage while on TRT.\n- **Fertility:** Restores spermatogenesis in infertile men.\n- **Neurosteroids:** Keeps pathways open for DHEA and Pregnenolone, aiding mood.",
        "note": "**Protocol:** 250iu to 500iu SubQ, 2 to 3 times per week. (Note: Calculator uses mcg/mg logic, ensure conversion matches your IU ratio).",
        "side_effects": "Can spike estradiol (E2) causing gynecomastia, mood swings, or acne if not managed with an AI. Testicular desensitization if overdosed.",
        "storage": "MUST Refrigerate immediately. Very fragile peptide—do not shake."
    },
    "Ipamorelin": {
        "vial_mg": 5.0, "dose_mcg": 100.0, "freq": "Daily (PM)", 
        "type": "Growth Hormone",
        "desc": "The cleanest, mildest GHRP (Growth Hormone Releasing Peptide). Mimics Ghrelin but does NOT stimulate appetite.", 
        "benefits": "- **Anabolism:** Preserves muscle mass during calorie deficits.\n- **Sleep:** Increases REM and Deep Sleep.\n- **Recovery:** Speeds up recovery from intense workouts.",
        "note": "⚠️ **FASTED ONLY.** 100mcg - 300mcg immediately before bed. **Half-life:** ~2 hours.",
        "side_effects": "Extremely mild compared to others. Rare dizziness or water retention.",
        "storage": "Refrigerate. Do not shake vigorously."
    },
    "Kisspeptin": {
        "vial_mg": 10.0, "dose_mcg": 100.0, "freq": "As needed", 
        "type": "Hormonal",
        "desc": "A neuromodulator that sits at the very top of the HPTA axis. Stimulates the hypothalamus to release GnRH.", 
        "benefits": "- **HPTA Restart:** Safely restarts natural testosterone production post-steroid cycle.\n- **Libido:** Enhances psychogenic sexual desire and mood.\n- **Safe:** Unlike HCG, does not cause testicular desensitization or extreme estrogen spikes.",
        "note": "**Protocol:** 100mcg - 200mcg daily or every other day. SubQ.",
        "side_effects": "Rare. Slight flushing. Short half-life means effects do not linger.",
        "storage": "Refrigerate after mixing."
    },
    "Klow Blend (GHK-Cu/BPC/TB/KPV)": {
        "vial_mg": 80.0, "dose_mcg": 3000.0, "freq": "Daily", 
        "type": "Ultimate Repair/Cosmetic Blend",
        "desc": "The Master Stack. GHK-Cu, BPC-157, TB-500, plus **KPV**. KPV acts as a master anti-inflammatory agent and antimicrobial, specifically targeting mast cells and gut flora.", 
        "benefits": "- **Skin Clearing:** KPV drastically reduces acne, psoriasis, and eczema.\n- **IBD/Gut:** KPV + BPC-157 is the strongest known peptide combo for Ulcerative Colitis, SIBO, and Crohn's.\n- **Total Healing:** Connective tissue repair and anti-aging in one.",
        "note": "**Protocol:** ~3mg total daily SubQ. This is a high-volume injection. Rotate sites religiously.",
        "side_effects": "Temporary red welts (from the copper/volume). Fatigue from systemic healing activation.",
        "storage": "Refrigerate strictly. Keep away from strong light."
    },
    "Melanotan II": {
        "vial_mg": 10.0, "dose_mcg": 500.0, "freq": "Daily (Loading)", 
        "type": "Cosmetic",
        "desc": "Alpha-MSH analog. Stimulates melanin production (tanning) and activates melanocortin receptors in the brain linked to sexual arousal.", 
        "benefits": "- **Photoprotection:** Creates a deep tan that protects against UV burning.\n- **Libido:** Extreme, often spontaneous erections and heightened arousal in both sexes.\n- **Weight Loss:** Strong appetite suppression.",
        "note": "☀️ **BEFORE SUN:** Take 100mcg - 500mcg, 30 minutes before UV exposure. **Titration:** Start at 100mcg to assess nausea. Once desired tan is reached, drop to 1x weekly maintenance.",
        "side_effects": "Intense nausea/vomiting upon injection (common at high doses), facial flushing, darkening of existing freckles/moles, spontaneous erections (can be uncomfortable).",
        "storage": "Refrigerate. Stable for ~30-60 days."
    },
    "NAD+": {
        "vial_mg": 500.0, "dose_mcg": 25000.0, "freq": "2-3x / Week", 
        "type": "Cellular Energy",
        "desc": "A critical coenzyme found in every living cell. Required for ATP (energy) production and Sirtuin activation (DNA repair).", 
        "benefits": "- **Mental:** Rapidly clears brain fog and enhances cognition.\n- **Energy:** Restores cellular energy levels (fights chronic fatigue).\n- **Detox:** Proven to aid in receptor repair post-alcohol/opiate addiction.",
        "note": "**Protocol:** 25mg - 50mg SubQ, 2 to 3 times per week. ⚠️ **SLOW INJECTION:** Take 60+ seconds to depress the plunger. Rapid injection causes the 'NAD flush' (anxiety, chest pain).",
        "side_effects": "Intense chest pressure, abdominal cramping, nausea, shortness of breath, and palpitations. These effects pass within 5-10 minutes but are very unpleasant.",
        "storage": "Refrigerate immediately. Very sensitive to heat degradation."
    },
    "PT-141": {
        "vial_mg": 10.0, "dose_mcg": 1000.0, "freq": "As needed", 
        "type": "Libido",
        "desc": "Bremelanotide. An active metabolite of Melanotan II that focuses purely on the sexual pathways in the hypothalamus, rather than the vascular system (like Viagra).", 
        "benefits": "- **Non-Vascular ED:** Works when Cialis/Viagra fail because it targets the brain, not blood flow.\n- **Women's Health:** FDA approved (Vyleesi) for Hypoactive Sexual Desire Disorder in premenopausal women.",
        "note": "⏰ **TIMING:** Onset takes 1 to 4 hours. Inject 1.5mg to 2mg roughly 2 hours before planned activity. Effects last up to 24 hours.",
        "side_effects": "High risk of initial nausea. Rise in blood pressure, flushing, headache. Can cause hyperpigmentation if used daily.",
        "storage": "Refrigerate after mixing."
    },
    "Retatrutide": {
        "vial_mg": 10.0, "dose_mcg": 2000.0, "freq": "Once Weekly", 
        "type": "Metabolic (GLP-1/GIP/Glucagon)",
        "desc": "The 'Triple G' Agonist. Binds to GLP-1 (satiety), GIP (insulin control), and Glucagon (energy expenditure). The inclusion of Glucagon actively burns stored fat.", 
        "benefits": "- **Fat Burn:** Clinical trials show an average of 24.2% body weight loss in 48 weeks.\n- **NAFLD:** Actively clears fat from the liver (often 80%+ reduction in fatty liver).\n- **Lipids:** Dramatic reductions in LDL cholesterol and triglycerides.",
        "note": "🕒 **WEEKLY.** Start at 2mg once per week. Titrate up by 2mg every 4 weeks to a max of 12mg based on tolerance. Half-life is 6 days.",
        "side_effects": "Heart rate increase (tachycardia) is common, skin hyperesthesia (skin sensitivity to touch), nausea, gastrointestinal stalling, appetite ablation.",
        "storage": "Refrigerate strictly. Do not freeze once mixed."
    },
    "Semaglutide": {
        "vial_mg": 5.0, "dose_mcg": 250.0, "freq": "Once Weekly", 
        "type": "Metabolic (GLP-1)",
        "desc": "Long-acting GLP-1 receptor agonist. Slows gastric emptying and signals the hypothalamus that you are full.", 
        "benefits": "- **Weight Loss:** 15%+ body weight reduction on average.\n- **Cardioprotective:** Reduces risk of major adverse cardiovascular events by 20%.\n- **Addiction:** Suppresses cravings for alcohol and gambling (dopamine modulation).",
        "note": "🕒 **WEEKLY.** Start at 0.25mg (250mcg) once weekly for 4 weeks. Increase to 0.5mg, then 1mg, up to 2.4mg. Half-life is ~7 days.",
        "side_effects": "Sulphur burps, severe constipation or diarrhea, nausea/vomiting, fatigue, potential muscle loss (if protein intake is low), 'Ozempic face' (fat loss from face).",
        "storage": "Refrigerate. Protect from light."
    },
    "TB-500": {
        "vial_mg": 5.0, "dose_mcg": 2500.0, "freq": "2x / Week", 
        "type": "Regenerative",
        "desc": "Synthetic version of Thymosin Beta-4. It acts as an actin-sequestering protein, guiding stem cells and immune cells directly to the site of damage.", 
        "benefits": "- **Muscular Repair:** Best peptide for torn muscles and deep tissue bruising.\n- **Flexibility:** Noticeably improves range of motion and joint suppleness.\n- **Cardiac Health:** Repairs heart tissue post-infarction.",
        "note": "**Protocol:** 2.5mg twice per week (e.g., Mon/Thurs) SubQ. **Half-life:** Long (hence the 2x/week dosing). Cycle: 4-6 weeks.",
        "side_effects": "Very rare. Occasional flu-like symptoms, lethargy, or minor head rush. Do not use if active cancer is present (promotes tumor angiogenesis).",
        "storage": "Refrigerate after mixing."
    },
    "Tesamorelin": {
        "vial_mg": 2.0, "dose_mcg": 1000.0, "freq": "Daily (PM)", 
        "type": "Growth Hormone",
        "desc": "The most potent GHRH analog. Specifically formulated and FDA approved (as Egrifta) for the reduction of HIV-associated lipodystrophy (visceral belly fat).", 
        "benefits": "- **Belly Fat:** Targets and destroys visceral adipose tissue around the organs.\n- **Lipid Profile:** Drastically lowers triglycerides.\n- **Nootropic:** Shows promise in improving cognitive function in older adults.",
        "note": "⚠️ **FASTED ONLY.** 1mg to 2mg injected SubQ immediately before bed. Must be 2 hours fasted. Cycle length: 8-12 weeks.",
        "side_effects": "High instances of injection site erythema (redness/itching). Water retention, joint stiffness, carpal tunnel symptoms, increased resting heart rate.",
        "storage": "Refrigerate. Use within 20-30 days."
    },
    "Tesamorelin + Ipamorelin Blend": {
        "vial_mg": 12.0, "dose_mcg": 350.0, "freq": "Daily (PM)", 
        "type": "Growth Hormone/Fat Loss Blend",
        "desc": "The Ultimate Shred Stack. Combines the deep visceral fat targeting of Tesamorelin with the broad pulse amplification and anti-aging benefits of Ipamorelin.", 
        "benefits": "- **Body Recomposition:** The strongest natural combo for simultaneously burning fat and building muscle.\n- **Metabolic Reset:** Lowers A1C, lipids, and systemic inflammation while sleeping.",
        "note": "⚠️ **FASTED ONLY.** ~350mcg to 500mcg total immediately before bed (2 hours post-meal). Cycle length: 5 days on, 2 days off for 8-12 weeks.",
        "side_effects": "Flushing, joint stiffness, vivid dreams, carpal tunnel numbness, injection site redness.",
        "storage": "Refrigerate strictly. Protect from light."
    },
    "Tirzepatide": {
        "vial_mg": 30.0, "dose_mcg": 2500.0, "freq": "Once Weekly", 
        "type": "Metabolic (GLP-1/GIP)",
        "desc": "Dual Agonist (Mounjaro/Zepbound). Combines GLP-1 with GIP. GIP improves insulin sensitivity directly in fat cells and mitigates the nausea often caused by GLP-1.", 
        "benefits": "- **Superior Efficacy:** Outperforms Semaglutide, averaging 20-22% weight loss.\n- **Food Noise:** Completely eliminates obsessive thoughts about food.\n- **Less GI Distress:** GIP smooths out the severe nausea seen with Semaglutide.",
        "note": "🕒 **WEEKLY.** Standard Titration: 2.5mg for 4 weeks -> 5mg for 4 weeks -> 7.5mg, up to max of 15mg. Half-life is 5 days.",
        "side_effects": "Anhedonia (general disinterest in activities/dopamine depression), constipation, cold extremities, hair shedding (Telogen effluvium due to rapid weight loss).",
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

# --- NAVIGATION SIDEBAR (v2.0 UI) ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/biotech.png", width=60) # Placeholder logo
    st.title("Navigation")
    page = st.radio("Go to:", ["🧮 Calculator", "📚 Peptide Database"])
    st.markdown("---")
    
    # NEW: Ko-fi Button inside the sidebar
    st.link_button("☕ Support my work (Ko-fi)", "https://ko-fi.com/musika", use_container_width=True)
    st.caption("v2.0 | by Musika")

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
    
    for idx, (name, info) in enumerate(filtered_items.items()):
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
                    st.markdown(f"**Frequency:** {info['freq']}")
                    st.markdown(f"{info['note']}")
                    st.markdown(f"**⚠️ Side Effects:** {info['side_effects']}")
                    st.markdown(f"**❄️ Storage:** {info['storage']}")

    if len(filtered_items) == 0:
        st.warning("No peptides match your search criteria. Try clearing the filters.")

# --- UNIVERSAL DISCLAIMER ---
st.markdown("---")
st.caption("⚠️ **Medical Disclaimer:** This tool is for educational and informational purposes only and does not constitute medical advice. Always verify calculations with a professional. The developers assume no liability for errors or misuse.")
