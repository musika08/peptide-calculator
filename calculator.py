FACTORS = {'mcg': 1, 'mg': 1000, 'g': 1000000, 'IU': 1}

def calculate_dosage(vial_qty, vial_unit, water_ml, desired_dose, dose_unit, syringe_factor, peptide_info):
    """
    Core math engine for peptide reconstitution.
    Returns: draw_ml, units, doses_per_vial, display_strength
    """
    conversion = peptide_info.get("iu_conversion")
    total_stock_units = 0
    display_strength = ""

    # LOGIC BRANCH A: Peptide has defined IU conversion (e.g., Oxytocin)
    if conversion and conversion > 1:
        if vial_unit in ['mg', 'mcg', 'g']:
            # Get mass in mg first
            stock_mg = vial_qty * (FACTORS[vial_unit] / 1000)
            total_stock_units = stock_mg * conversion
            display_strength = f"{stock_mg:.1f}mg ≈ {int(total_stock_units)} IU"
        else:
            total_stock_units = vial_qty
            display_strength = f"{int(vial_qty)} IU"

        # Target must be in IU for math
        if dose_unit == 'IU': target_dose_units = desired_dose
        elif dose_unit == 'mg': target_dose_units = desired_dose * conversion
        else: target_dose_units = (desired_dose / 1000) * conversion

    # LOGIC BRANCH B: Naturally IU (e.g., HCG)
    elif conversion == 1:
        total_stock_units = vial_qty
        target_dose_units = desired_dose
        display_strength = f"{int(vial_qty)} IU"

    # LOGIC BRANCH C: Standard Mass-Based (e.g., Tirzepatide)
    else:
        total_stock_units = vial_qty * FACTORS[vial_unit]
        target_dose_units = desired_dose * FACTORS[dose_unit]
        display_strength = f"{total_stock_units/1000:.1f} mg"

    # FINAL MATH
    if total_stock_units > 0 and target_dose_units > 0:
        concentration = total_stock_units / water_ml
        draw_ml = target_dose_units / concentration
        units = draw_ml * syringe_factor
        doses_per_vial = total_stock_units / target_dose_units
        return draw_ml, units, doses_per_vial, display_strength
    
    return 0, 0, 0, ""

