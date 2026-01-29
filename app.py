# app.py
import streamlit as st
from database import PEPTIDE_PRESETS, FACTORS
from calculator import perform_calc

st.set_page_config(page_title="PeptideCalc Pro v4.0", page_icon="🧪", layout="wide", initial_sidebar_state="expanded")

# CSS Styling
st.markdown("""
<style>
    .syringe-container { border: 2px solid #333; border-radius: 4px; background-color: #f0f0f0; height: 30px; width: 100%; position: relative; margin: 10px 0; }
    .syringe-liquid { background-color: #ff4b4b; height: 100%; border-radius: 2px 0 0 2px; transition: width 0.5s; }
    .syringe-markings { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: repeating-linear-gradient(90deg, transparent, transparent 19%, #000 20%); opacity: 0.1; }
    .db-tag { background-color: #4b4bff; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.8em; font-weight: bold; display: inline-block; margin-bottom: 10px; }
    .side-effect-box { background-color: #3e1818; border-left: 4px solid #ff4b4b; padding: 10px; margin-top: 10px; border-radius: 4px; font-size: 0.9em; line-height: 1.6; color: #ffd1d1; }
</style>
""", unsafe_allow_html=True)

if 'vial_val' not in st.session_state: st.session_state.vial_val = 30.0
if 'dose_val' not in st.session_state: st.session_state.dose_val = 2.5
if 'stock_unit_index' not in st.session_state: st.session_state.stock_unit_index = 0
if 'dose_unit_selection' not in st.session_state: st.session_state.dose_unit_selection = "mg"
if 'water_val' not in st.session_state: st.session_state.water_val = 2.0

def load_preset():
    sel = st.session_state.peptide_selector
    data = PEPTIDE_PRESETS[sel]
    
    # 1. Handle Vial Quantity & Units
    st.session_state.vial_val = float(data["vial_mg"])
    st.session_state.stock_unit_index = 3 if data.get("default_stock_unit") == "IU" else 0
    
    # 2. Handle Dose Quantity & Units
    st.session_state.dose_unit_selection = data.get("default_dose_unit", "mcg")
    st.session_state.dose_val = float(data["dose_mcg"])
    
    # 3. Handle Default Water (Special for Oxytocin)
    if sel == "Oxytocin Acetate":
        st.session_state.water_val = 3.0
    else:
        st.session_state.water_val = 2.0

with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/biotech.png", width=60)
    page = st.radio("Navigation", ["🧮 Calculator", "📚 Peptide Database"])

if page == "🧮 Calculator":
    st.subheader("🧪 Reconstitution Calculator")
    l, r = st.columns([1, 1.2], gap="large")

    with l:
        st.info("1️⃣ **Configuration**")
        sorted_keys = sorted(list(PEPTIDE_PRESETS.keys()))
        sel_peptide = st.selectbox("Select Peptide", sorted_keys, index=sorted_keys.index("Tirzepatide"), key="peptide_selector", on_change=load_preset)
        info = PEPTIDE_PRESETS[sel_peptide]
        
        c1, c2, c3 = st.columns([1.5, 1, 1.5])
        v_qty = c1.number_input("Stock Amount", key="vial_val", format="%.1f")
        v_unit = c2.selectbox("Unit", ["mg", "mcg", "g", "IU"], index=st.session_state.stock_unit_index, key="stock_unit_selection")
        water = c3.number_input("Water Added (mL)", key="water_val", min_value=0.1, format="%.1f")

        c4, c5 = st.columns([2, 1])
        d_unit = c5.selectbox("Dose Unit", ["mcg", "mg", "g", "IU"], key="dose_unit_selection")
        d_qty = c4.number_input("Desired Dose", key="dose_val", format="%.1f")
        
        syringe = st.radio("Syringe Type", ["U-100 (Standard)", "U-40 (Vet)"], horizontal=True)
        s_factor = 100 if "U-100" in syringe else 40

    with r:
        st.success("2️⃣ **Results**")
        if v_qty > 0 and water > 0 and d_qty > 0:
            d_ml, units, per_vial = perform_calc(v_qty, v_unit, water, d_qty, d_unit, s_factor, info)
            
            rc1, rc2, rc3 = st.columns(3)
            rc1.metric("Draw Volume", f"{d_ml:.4f} mL")
            rc2.metric("Syringe Units", f"{units:.1f} Units")
            rc3.metric("Doses / Vial", int(per_vial))
            
            pct = min(units / s_factor * 100, 100)
            st.markdown(f'<div class="syringe-container"><div class="syringe-liquid" style="width: {pct}%;"></div><div class="syringe-markings"></div></div>', unsafe_allow_html=True)
            
            with st.expander(f"📖 Profile: {sel_peptide}", expanded=True):
                st.write(f"**Type:** {info['type']}")
                st.markdown(f"**🌟 Comprehensive Benefits:**\n{info['benefits_detailed']}")
                # Render vertical bullets for side effects
                se_list = info['side_effects_detailed'].replace("•", "").replace("-", "").strip().split("\n")
                se_formatted = "<br>".join([f"• {item.strip()}" for item in se_list if item.strip()])
                st.markdown(f'<div class="side-effect-box"><strong>⚠️ Vertical Side Effects:</strong><br>{se_formatted}</div>', unsafe_allow_html=True)
                st.info(f"**📋 Quick Protocol:** {info['protocol_summary']}")

    st.divider()
    with st.expander("🛠️ How to Reconstitute (Mix)", expanded=False):
        st.markdown(f"1. **Clean:** Wipe the top of the **{v_qty} {v_unit}** peptide vial and the water vial.\n2. **Withdraw:** Draw exactly **{water} mL** of Bacteriostatic Water.\n3. **Inject:** Slowly aim for the glass wall.\n4. **Mix:** Swirl gently.\n5. **Store:** Refrigerate immediately.")
    
    with st.expander("💉 Visual Guide: Injection Sites", expanded=False):
        st.write("Common subcutaneous injection zones: Abdomen, Upper Thigh, and Back of Arm.")
        

elif page == "📚 Peptide Database":
    st.subheader("📚 Peptide Database")
    sc, fc = st.columns([3, 1])
    query = sc.text_input("🔍 Search").lower()
    cat = fc.selectbox("🏷️ Filter", ["All", "Slimming & Fat Loss", "Skin, Hair & Beauty", "Muscle & Workout", "Nootropics & Brain", "Injury & Repair", "Wellness & Longevity", "Libido & Sexual Health"])
    
    items = {n: d for n, d in PEPTIDE_PRESETS.items() if (cat == "All" or d['filter_cat'] == cat) and (query in n.lower() or query in d['benefits_detailed'].lower())}
    
    cols = st.columns(3)
    for idx, (name, i) in enumerate(items.items()):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"### {name}\n<span class='db-tag'>{i['type']}</span>", unsafe_allow_html=True)
                st.markdown(f"**🌟 Clinical Benefits:**\n{i['benefits_detailed']}")
                # Render vertical bullets for database view
                se_list_db = i['side_effects_detailed'].replace("•", "").replace("-", "").strip().split("\n")
                se_formatted_db = "<br>".join([f"• {item.strip()}" for item in se_list_db if item.strip()])
                st.markdown(f'<div class="side-effect-box"><strong>⚠️ Side Effects:</strong><br>{se_formatted_db}</div>', unsafe_allow_html=True)
                with st.expander("Detailed Protocol"): st.markdown(i['protocol_detailed'])
                with st.expander("ℹ️ Description & Mechanism"): st.write(f"_{i['desc']}_")
