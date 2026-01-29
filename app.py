# app.py
import streamlit as st
from calculator import run_calculator, PEPTIDE_DB

st.set_page_config(page_title="PeptideCalc Pro v4.1", page_icon="🧪", layout="wide")

# Global CSS for Cards
st.markdown("""
<style>
    .db-tag { background-color: #4b4bff; color: white; padding: 4px 12px; border-radius: 15px; font-size: 0.8em; font-weight: bold; }
    .side-effect-box { background-color: #3e1818; border-left: 5px solid #ff4b4b; padding: 12px; border-radius: 5px; margin-top: 10px; }
    .contra-box { background-color: #4a3700; border-left: 5px solid #ffcc00; padding: 12px; border-radius: 5px; margin-top: 10px; font-size: 0.9em; }
</style>
""", unsafe_allow_html=True)

def run_database_ui():
    st.subheader("📚 Peptide Clinical Database")
    cats = ["All", "Slimming & Fat Loss", "Skin, Hair & Beauty", "Muscle & Workout", "Injury & Repair", "Libido & Sexual Health"]
    
    col_search, col_filter = st.columns([3, 1])
    with col_search: query = st.text_input("🔍 Search Database", placeholder="Search...").lower()
    with col_filter: cat_filter = st.selectbox("🏷️ Filter", cats)

    filtered = {n: d for n, d in PEPTIDE_DB.items() if (cat_filter == "All" or d['filter_cat'] == cat_filter) and (query in n.lower() or query in d['benefits'].lower())}

    cols = st.columns(3)
    for i, (name, info) in enumerate(filtered.items()):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"### {name} <span class='db-tag'>{info['type']}</span>", unsafe_allow_html=True)
                st.markdown(f"**🌟 Benefits:**\n{info['benefits']}")
                st.markdown(f"<div class='side-effect-box'><strong>⚠️ Side Effects:</strong><br>{info['side']}</div>", unsafe_allow_html=True)
                if info.get("contra"):
                    st.markdown(f"<div class='contra-box'><strong>🚫 Contraindications:</strong><br>{info['contra']}</div>", unsafe_allow_html=True)
                with st.expander("📋 Full Protocol"):
                    st.markdown(f"**Timing:** {info['timing']}\n\n**Food:** {info['food']}\n\n**Storage:** {info['storage']}")

def main():
    st.sidebar.title("PeptideCalc Pro")
    page = st.sidebar.radio("Go to:", ["Calculator", "Database"])
    if page == "Calculator":
        run_calculator()
    else:
        run_database_ui()

if __name__ == "__main__":
    main()
