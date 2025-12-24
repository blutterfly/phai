import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Halalan 2025 AI & Data Project",
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

# --- VIEW 1: SENATORIAL RACE (Formerly Dashboard) ---
def page_senatorial():
    df_senate, df_partylist, meta = load_data()

    st.title("🇵🇭 Halalan 2025: Senatorial Race")
    st.markdown(f"**Data Status:** Partial, Unofficial ({meta['Precincts Processed'] / meta['Total Precincts'] * 100:.2f}% of Election Returns processed)")

    # Sidebar Filters specific to Dashboard
    st.sidebar.markdown("---")
    st.sidebar.header("Race Filters")
    show_top_n = st.sidebar.slider("Show Top N Candidates", 5, 12, 12)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Registered Voters", f"{meta['Total Voters']:,}")
    col2.metric("Voter Turnout", f"{(meta['Votes Cast']/meta['Total Voters'])*100:.2f}%")
    col3.metric("Precincts Reporting", f"{meta['Precincts Processed']:,} / {meta['Total Precincts']:,}")
    st.markdown("---")

    # Visualizations
    filtered_senate = df_senate.head(show_top_n)
    fig_senate = px.bar(filtered_senate, x="Votes", y="Candidate", orientation='h', color="Party", title="Senatorial Race Leaders")
    fig_senate.update_layout(yaxis={'categoryorder':'total ascending'})
    
    # FIX: Replaced use_container_width=True with width='stretch'
    st.plotly_chart(fig_senate, width='stretch')

# --- VIEW 2: GOVS/REPS RACE ---
def page_govs_reps():
    st.title("🏛️ Local Winners: Governors & Representatives")
    st.markdown("Searchable database of declared winners for local executive and legislative posts.")

    target_file = "data/govs_reps_winners.csv"

    if os.path.exists(target_file):
        df = pd.read_csv(target_file)
        
        st.subheader("🏆 Winner Database")
        st.caption("Tip: Click headers to sort. Use the search icon to filter.")
        # FIX: Replaced use_container_width=True with width='stretch'
        st.dataframe(df, width='stretch', hide_index=True)

        st.markdown("---")

        # Aggregation Widget
        st.subheader("📊 Party Aggregation Stats")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("##### Wins by Party")
            if "Party" in df.columns:
                agg_df = df["Party"].value_counts().reset_index()
                agg_df.columns = ["Party", "Total Wins"]
                st.dataframe(agg_df, width='stretch', hide_index=True)
            else:
                st.warning("Column 'Party' not found for aggregation.")

        with col2:
            st.markdown("##### Visual Breakdown")
            if "Party" in df.columns:
                fig_agg = px.bar(agg_df, x="Party", y="Total Wins", color="Party", title="Total Wins per Party")
                st.plotly_chart(fig_agg, width='stretch')

    else:
        st.error(f"Data file not found: `{target_file}`")
        if st.button("Create Demo Data (data/govs_reps_winners.csv)"):
            os.makedirs("data", exist_ok=True)
            mock_data = {
                "Position": ["Governor", "Governor", "Representative", "Representative", "Governor", "Representative"],
                "Province/District": ["Cebu", "Ilocos Norte", "Quezon City - 1st Dist", "Cavite - 1st Dist", "Davao del Sur", "Manila - 3rd Dist"],
                "Name": ["GARCIA, GWEN", "MANOTOC, MATTHEW", "ARJO ATAYDE", "JOLO REVILLA", "CAGAS, YVONNE", "LACUNA, JOEL"],
                "Party": ["1CEBU", "NP", "NP", "LAKAS", "NP", "AKSYON"]
            }
            pd.DataFrame(mock_data).to_csv(target_file, index=False)
            st.rerun()

# --- VIEW 3: BUILD NOTES (Formerly Read Docs) ---
def page_build_notes():
    st.title("📝 Build Notes & Documentation")
    
    target_file = "doc/build.md"
    
    st.sidebar.markdown("---")
    st.sidebar.header("Doc Settings")
    show_raw = st.sidebar.checkbox("Show Raw Markdown", value=False)

    if os.path.exists(target_file):
        with open(target_file, "r", encoding="utf-8") as f:
            markdown_content = f.read()
        if show_raw:
            st.code(markdown_content, language="markdown")
        else:
            st.markdown(markdown_content)
    else:
        st.error(f"File not found: `{target_file}`")
        if st.button("Create Demo File (doc/build.md)"):
            os.makedirs("doc", exist_ok=True)
            with open(target_file, "w", encoding="utf-8") as f:
                f.write("# Build Instructions\n\n## 1. Setup\nRun `pip install streamlit pandas plotly`.\n\n## 2. Methodology\nData scraped from...")
            st.rerun()

# --- VIEW 4: PHILIPPINE HALALAN AI (PDF Viewer) ---
def page_ph_ai():
    st.title("🤖 Philippine Halalan AI")
    st.markdown("Project Proposal and Architecture Overview.")
    
    # Note: Using 'docs' folder as requested for this specific file
    target_file = "docs/phai.pdf"
    
    if os.path.exists(target_file):
        with open(target_file, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')

        # Embed PDF using HTML iframe
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.error(f"PDF Document not found: `{target_file}`")
        st.info("Please place the `phai.pdf` file inside the `docs/` folder.")
        
        # Helper to create a dummy PDF for testing if needed
        if st.button("Create Dummy PDF structure"):
            os.makedirs("docs", exist_ok=True)
            st.warning("Folder `docs/` created. Please upload your actual PDF file there.")

# --- MAIN NAVIGATION ---
def main():
    st.sidebar.title("Navigation")
    
    # Level 1 Navigation
    nav_mode = st.sidebar.radio("Project Section", ["Election Data", "PH AI"])

    if nav_mode == "Election Data":
        # Level 2 Navigation (Sub-bullets)
        st.sidebar.markdown("### Dashboard Views")
        sub_page = st.sidebar.radio(
            "Select View", 
            ["Senatorial Race", "Govs/Reps Race", "Build Notes"],
            label_visibility="collapsed" # Hides label to look more like sub-bullets
        )
        
        if sub_page == "Senatorial Race":
            page_senatorial()
        elif sub_page == "Govs/Reps Race":
            page_govs_reps()
        elif sub_page == "Build Notes":
            page_build_notes()
            
    elif nav_mode == "PH AI":
        page_ph_ai()

if __name__ == "__main__":
    main()