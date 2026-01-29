# calculator.py - The Calculation Engine v4.0

# Define factors locally to break circular import dependencies
FACTORS = {'mcg': 1, 'mg': 1000, 'g': 1000000, 'IU': 1}

def calculate_dosage(vial_qty, vial_unit, water_ml, desired_dose, dose_unit, syringe_factor, peptide_info):
    """
    Handles reconstitution math for mass-based and IU-based peptides.
    Returns: draw_ml, units, doses_per_vial, display_strength
    """
    conversion = peptide_info.get("iu_conversion")
    total_stock_units = 0
    display_strength = ""

    # Logic for Peptides with IU Conversion (e.g., Oxytocin: 600, HCG: 1)
    if conversion:
        if vial_unit in ['mg', 'mcg', 'g']:
            # Convert input mass to mg, then to IU
            stock_mg = vial_qty * (FACTORS[vial_unit] / 1000)
            total_stock_units = stock_mg * conversion
            display_strength = f"{stock_mg:.1f}mg ≈ {int(total_stock_units)} IU"
        else:
            # User input is already in IU
            total_stock_units = vial_qty
            display_strength = f"{int(vial_qty)} IU"

        # Calculate target dose in IU
        if dose_unit == 'IU':
            target_dose_units = desired_dose
        elif dose_unit == 'mg':
            target_dose_units = desired_dose * conversion
        else: # mcg
            target_dose_units = (desired_dose / 1000) * conversion

    # Logic for standard Mass-Based peptides (e.g., Tirzepatide, BPC-157)
    else:
        total_stock_units = vial_qty * FACTORS[vial_unit]
        target_dose_units = desired_dose * FACTORS[dose_unit]
        display_strength = f"{total_stock_units / 1000:.1f} mg"

    # Final Volume Calculations
    if total_stock_units > 0 and water_ml > 0 and target_dose_units > 0:
        # Concentration = total units / total ml
        concentration_per_ml = total_stock_units / water_ml
        
        # mL to draw = target dose / concentration
        draw_ml = target_dose_units / concentration_per_ml
        
        # Syringe units = ml * syringe type (100 or 40)
        units = draw_ml * syringe_factor
        
        # Total doses available in this vial
        doses_per_vial = total_stock_units / target_dose_units
        
        return draw_ml, units, doses_per_vial, display_strength
    
    return 0.0, 0.0, 0.0, ""
