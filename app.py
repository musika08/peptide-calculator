import streamlit as st
from database import PEPTIDE_DB
from calculator import run_calculator

# --- CONFIGURATION ---
st.set_page_config(
    page_title="PeptideCalc Pro - Multi-Tool",
    page_icon="🧪",
    layout="wide"
)

# --- GLOBAL STYLING ---
st.markdown("""
<style>
    .db-tag { background-color: #4b4bff; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.8em; font-weight: bold; display: inline-block; margin-bottom: 10px; }
    .side-effect-box { background-color: #3e1818; border-left: 4px solid #ff4b4b; padding: 10px; margin-top: 10px; border-radius: 4px; font-size: 0.9em; line-height: 1.6; }
    .stApp { background-color: #0e1117; color: white; }
</style>
""", unsafe_allow_html=True)

def run_database_ui():
    st.subheader("📚 Peptide Clinical Database")
    st.divider()

    cats = ["All", "Slimming & Fat Loss", "Skin, Hair & Beauty", "Muscle & Workout", "Nootropics & Brain", "Injury & Repair", "Wellness & Longevity", "Libido & Sexual Health"]
    
    c1, c2 = st.columns([3, 1])
    with c1: 
        query = st.text_input("🔍 Search Peptides", placeholder="Search by name or benefit...").lower()
    with c2: 
        cat_filter = st.selectbox("🏷️ Filter by Category", cats)

    # Filter Logic
    filtered = {
        name: data for name, data in PEPTIDE_DB.items() 
        if (cat_filter == "All" or data['filter_cat'] == cat_filter) 
        and (query in name.lower() or query in data['benefits'].lower() or query in data['desc'].lower())
    }

    # Grid Display
    if not filtered:
        st.warning("No peptides found matching your search.")
    else:
        cols = st.columns(3)
        for i, (name, info) in enumerate(filtered.items()):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"### {name} <span class='db-tag'>{info['type']}</span>", unsafe_allow_html=True)
                    st.markdown(f"**🌟 Benefits:**\n{info['benefits']}")
                    st.markdown(f"<div class='side-effect-box'><strong>⚠️ Side Effects:</strong><br>{info['side']}</div>", unsafe_allow_html=True)
                    
                    with st.expander("📋 Suggested Protocol"):
                        st.markdown(info['protocol'])
                    
                    with st.expander("ℹ️ Mechanism & Storage"):
                        st.markdown(f"_{info['desc']}_")
                        st.markdown(f"**❄️ Storage:** {info['storage']}")

def main():
    # Sidebar Navigation
    st.sidebar.title("PeptideCalc Pro v4.1")
    st.sidebar.caption("Modular Clinical Suite")
    
    page = st.sidebar.radio("Navigate to:", ["Dosage Calculator", "Clinical Database"])
    
    st.sidebar.divider()
    st.sidebar.info("Disclaimer: This tool is for educational purposes only. Always consult a medical professional.")

    if page == "Dosage Calculator":
        run_calculator()
    elif page == "Clinical Database":
        run_database_ui()

if __name__ == "__main__":
    main()
