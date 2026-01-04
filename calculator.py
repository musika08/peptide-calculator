def convert_to_mcg(value, unit):
    """Converts g or mg to mcg."""
    unit = unit.lower()
    if unit == 'g':
        return value * 1_000_000
    elif unit == 'mg':
        return value * 1_000
    elif unit == 'mcg':
        return value
    else:
        raise ValueError("Unknown unit. Please use g, mg, or mcg.")

def calculate_dosage(vial_amount, vial_unit, water_amount_ml, desired_dose, dose_unit):
    """
    Calculates how much liquid to draw.
    
    Args:
        vial_amount (float): Total peptide in the vial (e.g., 5).
        vial_unit (str): Unit of the vial (e.g., 'mg').
        water_amount_ml (float): Amount of bacteriostatic water added (e.g., 2.0).
        desired_dose (float): How much you want to take (e.g., 250).
        dose_unit (str): Unit of the desired dose (e.g., 'mcg').
    
    Returns:
        dict: Contains volume in mL and Units (for insulin syringes).
    """
    
    # 1. Standardize everything to mcg
    total_peptide_mcg = convert_to_mcg(vial_amount, vial_unit)
    desired_dose_mcg = convert_to_mcg(desired_dose, dose_unit)
    
    # 2. Calculate Concentration (mcg per mL)
    concentration_mcg_per_ml = total_peptide_mcg / water_amount_ml
    
    # 3. Calculate Volume to Draw (mL)
    volume_to_draw_ml = desired_dose_mcg / concentration_mcg_per_ml
    
    # 4. Convert to "Units" (assuming standard U-100 insulin syringe)
    # 1 mL = 100 Units
    units_to_draw = volume_to_draw_ml * 100
    
    return {
        "draw_ml": round(volume_to_draw_ml, 4),
        "draw_units": round(units_to_draw, 2),
        "concentration": concentration_mcg_per_ml
    }

# --- Example Usage (Testing the logic) ---
if __name__ == "__main__":
    # Scenario: 5mg Vial, 2ml Water, want 250mcg dose
    result = calculate_dosage(5, 'mg', 2, 250, 'mcg')
    
    print(f"--- Dosage Result ---")
    print(f"Draw Amount: {result['draw_ml']} mL")
    print(f"Insulin Syringe Ticks: {result['draw_units']} Units")