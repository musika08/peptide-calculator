# calculator.py
def perform_calc(vial_qty, vial_unit, water_ml, desired_dose, dose_unit, syringe_factor, peptide_info):
    conversion = peptide_info.get("iu_conversion")
    total_stock_units = 0
    
    # Helper to get pure mass in mg
    stock_mg = 0 
    if vial_unit == 'mg': stock_mg = vial_qty
    elif vial_unit == 'mcg': stock_mg = vial_qty / 1000
    elif vial_unit == 'g': stock_mg = vial_qty * 1000
    
    # LOGIC BRANCH A: Peptide has defined IU conversion (Oxytocin/HCG)
    if conversion and conversion > 0:
        if vial_unit in ['mg', 'mcg', 'g']:
            total_stock_units = stock_mg * (conversion if conversion > 1 else 1)
        else:
            total_stock_units = vial_qty
        
        if dose_unit == 'IU': target_dose_units = desired_dose
        elif dose_unit == 'mg': target_dose_units = desired_dose * conversion
        elif dose_unit == 'mcg': target_dose_units = (desired_dose / 1000) * conversion
        else: target_dose_units = 0
            
    # LOGIC BRANCH B: Standard Mass-Based
    else:
        if vial_unit == 'mg': total_stock_units = vial_qty * 1000
        elif vial_unit == 'g': total_stock_units = vial_qty * 1000000
        elif vial_unit == 'mcg': total_stock_units = vial_qty
        else: total_stock_units = 0
        
        if dose_unit == 'mg': target_dose_units = desired_dose * 1000
        elif dose_unit == 'g': target_dose_units = desired_dose * 1000000
        elif dose_unit == 'mcg': target_dose_units = desired_dose
        else: target_dose_units = 0

    if total_stock_units > 0 and target_dose_units > 0:
        concentration_per_ml = total_stock_units / water_ml
        draw_ml = target_dose_units / concentration_per_ml
        units = draw_ml * syringe_factor
        per_vial = total_stock_units / target_dose_units
        return draw_ml, units, per_vial
    
    return 0, 0, 0
