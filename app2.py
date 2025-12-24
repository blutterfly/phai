import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Halalan 2025 ",
    page_icon="🇵🇭",
    layout="wide"
)

# --- HELPER FUNCTIONS ---
@st.cache_data
def load_data():
    # Mock Data for demo purposes
    senate_data = {
        "Candidate": ["AQUINO, BAM (KNP)", "TULFO, ERWIN (LAKAS)", "PANGILINAN, KIKO (LP)", 
                      "GO, BONG (PDPLBN)", "REVILLA, BONG (LAKAS)", "SOTTO, TITO (NPC)",
                      "CAYETANO, PIA (NP)", "DELA ROSA, BATO (PDPLBN)", "ONG, DOC WILLIE (AKSYON)",
                      "MANALAC, PHILIP (IND)", "QUIRINO, CORY (IND)", "TEODORO, GIBO (LAKAS)"],
        "Votes": [20895171, 17065384, 15290525, 14500100, 13980220, 13500000, 
                  13100000, 12900000, 12500000, 11000000, 10500000, 10200000],
        "Party": ["KNP", "LAKAS", "LP", "PDP-Laban", "LAKAS", "NPC", 
                  "NP", "PDP-Laban", "Aksyon", "Independent", "Independent", "LAKAS"]
    }
    partylist_data = {
        "Party List": ["ACT-CIS", "TINGOG", "4PS", "AKO BICOL", "USWAG ILONGGO"],
        "Votes": [2776316, 1817461, 1461427, 1237929, 950000]
    }
    meta_data = {"Total Voters": 69773653, "Votes Cast": 56962688, "Precincts Processed": 92808, "Total Precincts": 93629}
    return pd.DataFrame(senate_data), pd.DataFrame(partylist_data), meta_data

# --- PAGE 1: DASHBOARD ---
def page_dashboard():
    df_senate, df_partylist, meta = load_data()

    st.title("🇵🇭 Halalan 2025 Official Results")
    st.markdown(f"**Data Status:** Partial, Unofficial ({meta['Precincts Processed'] / meta['Total Precincts'] * 100:.2f}% of Election Returns processed)")

    # Sidebar Filters specific to Dashboard
    st.sidebar.header("Dashboard Filters")
    show_top_n = st.sidebar.slider("Show Top N Candidates", 5, 12, 12)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Registered Voters", f"{meta['Total Voters']:,}")
    col2.metric("Voter Turnout", f"{(meta['Votes Cast']/meta['Total Voters'])*100:.2f}%")
    col3.metric("Precincts Reporting", f"{meta['Precincts Processed']:,} / {meta['Total Precincts']:,}")
    st.markdown("---")

    # Visualizations
    filtered_senate = df_senate.head(show_top_n)
    fig_senate = px.bar(filtered_senate, x="Votes", y="Candidate", orientation='h', color="Party", title="Senatorial Race")
    fig_senate.update_layout(yaxis={'categoryorder':'total ascending'})
    
    # FIX APPLIED: Replaced use_container_width=True with width='stretch'
    st.plotly_chart(fig_senate, width='stretch')

# --- PAGE 2: DOCUMENTATION VIEWER ---
def page_documentation():
    st.title("📂 Dashboard Doc")
    
    target_file = 'docs/05-gemini-response.md'

    
    # Sidebar controls for the document viewer
    st.sidebar.header("Doc Settings")
    show_raw = st.sidebar.checkbox("Show Raw Markdown", value=False)

    # Check if file exists to prevent errors
    if os.path.exists(target_file):
        with open(target_file, "r", encoding="utf-8") as f:
            markdown_content = f.read()
            
        if show_raw:
            st.code(markdown_content, language="markdown")
        else:
            st.markdown(markdown_content)
    else:
        st.error(f"File not found: `{target_file}`")
        st.info("Please ensure you have a folder named `doc` and a file named `build.md` inside it.")
        
        # Create a dummy file button for testing
        if st.button("Create Demo File (doc/build.md)"):
            os.makedirs("doc", exist_ok=True)
            with open(target_file, "w", encoding="utf-8") as f:
                f.write("# Build Instructions\n\n## 1. Setup\nRun `pip install streamlit pandas plotly`.\n\n## 2. Methodology\nData scraped from...")
            st.rerun()

# --- MAIN NAVIGATION ---
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Read Docs"])

    if page == "Dashboard":
        page_dashboard()
    elif page == "Read Docs":
        page_documentation()

if __name__ == "__main__":
    main()