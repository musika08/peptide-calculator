# database.py

PEPTIDE_DB = {
    "AOD-9604": {
        "type": "Fat Loss", 
        "filter_cat": "Slimming & Fat Loss", 
        "desc": "Advanced Obesity Drug 9604. A modified fragment of the HGH molecule (C-terminal fragment).", 
        "benefits": "- **Lipolysis:** Specifically triggers the breakdown of fat cells.\n- **Anti-Lipogenesis:** Blocks the transformation of non-fatty foods into body fat.\n- **Metabolic Safety:** Does not affect blood sugar or insulin sensitivity.", 
        "side": "• Injection site redness/pain\n• Occasional headache\n• Rare upset stomach", 
        "protocol": "**Dosage:** 300mcg daily.\n**Timing:** Best taken in the morning on an empty stomach (30 mins before food).", 
        "storage": "Refrigerate after reconstitution."
    },
    "BPC-157": {
        "type": "Regenerative", 
        "filter_cat": "Injury & Repair", 
        "desc": "Body Protection Compound. A 15-amino acid peptide derived from human gastric juice.", 
        "benefits": "- **Soft Tissue Repair:** Speeds healing of tendons, ligaments, and muscle tears.\n- **Gut Health:** Heals leaky gut, IBS, and gastric ulcers.\n- **Angiogenesis:** Promotes new blood vessel growth to damaged areas.", 
        "side": "• Mild nausea\n• Dizziness\n• Changes in bowel movements", 
        "protocol": "**Dosage:** 250mcg - 500mcg twice daily.\n**Timing:** Can be taken anytime; often injected near the site of injury.", 
        "storage": "Refrigerate. Sensitive to vigorous shaking."
    },
    "CJC-1295 + Ipamorelin": {
        "type": "Growth Hormone", 
        "filter_cat": "Muscle & Workout", 
        "desc": "A combination of GHRH (CJC) and Ghrelin mimetic (Ipamorelin) for a synergistic GH pulse.", 
        "benefits": "- **Lean Muscle:** Increases protein synthesis and muscle mass.\n- **Fat Loss:** Enhances metabolic rate and fat oxidation.\n- **Sleep Quality:** Significantly improves deep Stage 4 REM sleep.", 
        "side": "• Facial flushing\n• Water retention (if dose is too high)\n• Tingling in hands/feet", 
        "protocol": "**Dosage:** 100mcg/100mcg (total 200mcg) daily.\n**Timing:** Nightly on an empty stomach (2 hours post-meal).", 
        "storage": "Refrigerate."
    },
    "GHK-Cu": {
        "type": "Cosmetic", 
        "filter_cat": "Skin, Hair & Beauty", 
        "desc": "Copper Tripeptide-1. A naturally occurring copper-binding tripeptide.", 
        "benefits": "- **Collagen Boost:** 70% increase in collagen and elastin production.\n- **Hair Growth:** Increases hair follicle size and density.\n- **Wound Healing:** Reduces scarring and inflammatory markers.", 
        "side": "• Significant injection site stinging\n• Potential zinc depletion (with long-term use)\n• Lethargy if dose is high", 
        "protocol": "**Dosage:** 1mg - 2mg daily.\n**Timing:** Usually injected subcutaneously in the evening.", 
        "storage": "Refrigerate. Protect from light."
    },
    "TB-500": {
        "type": "Regenerative", 
        "filter_cat": "Injury & Repair", 
        "desc": "Thymosin Beta-4. A peptide that plays a vital role in cell migration and tissue repair.", 
        "benefits": "- **Flexibility:** Reduces joint inflammation and increases range of motion.\n- **Systemic Repair:** Unlike BPC-157, it travels effectively throughout the whole body.\n- **Cardiovascular:** Supports heart tissue repair and blood vessel growth.", 
        "side": "• Temporary lethargy\n• Mild headache\n• Injection site irritation", 
        "protocol": "**Dosage:** 2mg - 5mg twice weekly (Loading phase for 4-6 weeks).\n**Maintenance:** 2mg - 5mg once a month.", 
        "storage": "Refrigerate."
    },
    "PT-141 (Bremelanotide)": {
        "type": "Wellness", 
        "filter_cat": "Libido & Sexual Health", 
        "desc": "Melanocortin receptor agonist. Primarily used for sexual dysfunction.", 
        "benefits": "- **Libido:** Increases sexual desire in both men and women.\n- **Performance:** Effective for ED that doesn't respond to PDE5 inhibitors (Viagra).\n- **Mood:** Can enhance overall sense of well-being.", 
        "side": "• Nausea (very common)\n• Facial flushing\n• Increased blood pressure (briefly)", 
        "protocol": "**Dosage:** 1mg - 1.75mg as needed.\n**Timing:** 2 to 4 hours before sexual activity. Limit to 8 doses per month.", 
        "storage": "Refrigerate."
    },
    "Melanotan II": {
        "type": "Wellness", 
        "filter_cat": "Skin, Hair & Beauty", 
        "desc": "A synthetic analog of the alpha-melanocyte stimulating hormone.", 
        "benefits": "- **Tanning:** Darkens skin pigment without heavy UV exposure.\n- **Appetite:** Significant appetite suppression properties.\n- **Libido:** Often causes spontaneous erections.", 
        "side": "• Nausea and 'flushing' episodes\n• Darkening of existing moles/freckles\n• Fatigue", 
        "protocol": "**Dosage:** 250mcg - 500mcg every other day.\n**Timing:** Best taken before bedtime to 'sleep through' potential nausea.", 
        "storage": "Refrigerate. Protect from light."
    },
    "Tesamorelin": {
        "type": "Fat Loss", 
        "filter_cat": "Slimming & Fat Loss", 
        "desc": "Growth hormone-releasing hormone (GHRH) analog used for visceral fat.", 
        "benefits": "- **Visceral Fat:** Specifically targets 'hard' belly fat around organs.\n- **Cognition:** Some evidence for improving memory in aging adults.\n- **Muscle:** Modest increases in lean mass.", 
        "side": "• Joint pain/stiffness\n• Night sweats\n• Peripheral edema (swelling)", 
        "protocol": "**Dosage:** 1mg - 2mg daily.\n**Timing:** Best in the morning or before bed on an empty stomach.", 
        "storage": "Refrigerate."
    },
    "Selank": {
        "type": "Nootropic", 
        "filter_cat": "Nootropics & Brain", 
        "desc": "Synthetic analog of the immunomodulatory peptide Tuftsin.", 
        "benefits": "- **Anxiolytic:** Reduces anxiety without sedation or addiction.\n- **Cognition:** Enhances focus and memory under stress.\n- **Immune:** Modulates the immune system response.", 
        "side": "• Rare nasal irritation (if using spray)\n• Mild headache\n• Restlessness", 
        "protocol": "**Dosage:** 250mcg - 500mcg per dose.\n**Timing:** As needed or up to 3 times daily.", 
        "storage": "Refrigerate. Can be used via injection or nasal spray."
    },
    "Semax": {
        "type": "Nootropic", 
        "filter_cat": "Nootropics & Brain", 
        "desc": "A fragment of ACTH. Known as a potent neuroprotective agent.", 
        "benefits": "- **Brain Fog:** Rapidly clears mental fatigue.\n- **Neurogenesis:** Increases BDNF levels in the brain.\n- **Stroke Recovery:** Used clinically for nerve regeneration and recovery.", 
        "side": "• Irritability (if dose is too high)\n• Hair shedding (rare/anecdotal)\n• Transient insomnia", 
        "protocol": "**Dosage:** 100mcg - 500mcg daily.\n**Timing:** Morning use is best to avoid sleep interference.", 
        "storage": "Refrigerate."
    },
    "Tirzepatide": {
        "type": "Metabolic", 
        "filter_cat": "Slimming & Fat Loss", 
        "desc": "Dual GIP and GLP-1 receptor agonist.", 
        "benefits": "- **Weight Loss:** Superior fat reduction compared to Semaglutide.\n- **Food Noise:** Eliminates obsessive thoughts about eating.\n- **Blood Sugar:** Dramatically improves A1C and insulin sensitivity.", 
        "side": "• Gastrointestinal upset (nausea, constipation)\n• Fatigue\n• Anhedonia (mild lack of pleasure)", 
        "protocol": "**Dosage:** Starts at 2.5mg weekly, titrating up to 15mg.\n**Timing:** Weekly injection on the same day.", 
        "storage": "Refrigerate. Avoid freezing."
    },
    "HCG": {
        "type": "Hormonal", 
        "filter_cat": "Libido & Sexual Health", 
        "desc": "Human Chorionic Gonadotropin. Mimics Luteinizing Hormone (LH).", 
        "benefits": "- **Fertility:** Maintains sperm production during TRT.\n- **Testosterone:** Stimulates natural testosterone production in the testes.\n- **Neurosteroids:** Supports upstream hormones like pregnenolone.", 
        "side": "• Elevated Estrogen (E2)\n• Water retention\n• Gynecomastia risk (if dose is unmanaged)", 
        "protocol": "**Dosage:** 250 IU - 500 IU 2-3 times per week.\n**Timing:** Injected subcutaneously at any time.", 
        "storage": "Must be refrigerated after reconstitution."
    }
}
