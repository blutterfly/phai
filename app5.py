import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PH Halalan AI",
    page_icon="🇵🇭",
    layout="wide"
)

# --- SESSION STATE & NAVIGATION LOGIC ---
if 'current_view' not in st.session_state:
    st.session_state.current_view = "Senatorial Race" # Default Home

def set_view(view_name):
    """Callback to update the current view"""
    st.session_state.current_view = view_name

# --- HELPER FUNCTIONS ---
@st.cache_data
def load_data():
    # Mock Election Data
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
    meta_data = {"Total Voters": 69773653, "Votes Cast": 56962688, "Precincts Processed": 92808, "Total Precincts": 93629}
    return pd.DataFrame(senate_data), meta_data

@st.cache_data
def load_geo_data():
    # Mock Geo Data (Lat/Lon for Philippines)
    # Generating random points around major PH cities for demo
    base_lat, base_lon = 12.8797, 121.7740
    lat = np.random.normal(base_lat, 2, 100)
    lon = np.random.normal(base_lon, 1, 100)
    return pd.DataFrame({'lat': lat, 'lon': lon, 'votes': np.random.randint(1000, 50000, 100)})

# --- VIEW RENDERERS ---

def render_dashboard_charts():
    df_senate, meta = load_data()
    st.title("🇵🇭 Senatorial Race Leaders")
    st.markdown(f"**Status:** Unofficial ({meta['Precincts Processed'] / meta['Total Precincts'] * 100:.2f}% Processed)")
    
    top_n = st.slider("Show Top Candidates", 5, 12, 12)
    fig = px.bar(df_senate.head(top_n), x="Votes", y="Candidate", orientation='h', color="Party", 
                 color_discrete_sequence=px.colors.qualitative.Bold)
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, width='stretch')

def render_govs_reps():
    st.title("🏛️ Local Winners (Govs & Reps)")
    target_file = "data/govs_reps_winners.csv"
    if os.path.exists(target_file):
        df = pd.read_csv(target_file)
        st.dataframe(df, width='stretch', hide_index=True)
    else:
        st.info("No local data found.")
        if st.button("Generate Demo Data"):
            os.makedirs("data", exist_ok=True)
            pd.DataFrame({"Position": ["Governor", "Rep"], "Province": ["Cebu", "Manila"], "Name": ["GARCIA, GWEN", "LACUNA, JOEL"]}).to_csv(target_file, index=False)
            st.rerun()

def render_geo_map():
    st.title("🗺️ Election Heatmap")
    st.markdown("Geographic distribution of votes processed.")
    df_geo = load_geo_data()
    st.map(df_geo)

def render_markdown_page(title, filepath):
    st.title(title)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            st.markdown(f.read())
    else:
        st.warning(f"File not found: `{filepath}`")
        if st.button(f"Create {filepath}"):
            os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
            with open(filepath, "w") as f: f.write(f"# {title}\nPlaceholder content.")
            st.rerun()

# --- MAIN LAYOUT & ROUTING ---
def main():
    st.sidebar.title("PH Halalan AI")

    # 1. DASH EXPANDER
    with st.sidebar.expander("Dash", expanded=True):
        # We use buttons for navigation to avoid 'radio button conflict' visual states
        if st.button("Senatorial Race", use_container_width=True): set_view("Senatorial Race")
        if st.button("Govs/Reps Race", use_container_width=True): set_view("Govs/Reps Race")
        if st.button("Geo Map", use_container_width=True): set_view("Geo Map")
        if st.button("Build Notes", use_container_width=True): set_view("Build Notes")

    # 2. DOCS EXPANDER
    with st.sidebar.expander("Docs", expanded=False):
        if st.button("Overview", use_container_width=True): set_view("Overview")
        if st.button("Project Details", use_container_width=True): set_view("Project")
        if st.button("More Info", use_container_width=True): set_view("More")

    # 3. CHAT EXPANDER
    with st.sidebar.expander("Chat", expanded=False):
        if st.button("Chat Session 1", use_container_width=True): set_view("Chat 1")
        if st.button("Chat Session 2", use_container_width=True): set_view("Chat 2")
        if st.button("Chat Session 3", use_container_width=True): set_view("Chat 3")

    # --- CONTENT ROUTER ---
    view = st.session_state.current_view

    # Dash Routes
    if view == "Senatorial Race":
        render_dashboard_charts()
    elif view == "Govs/Reps Race":
        render_govs_reps()
    elif view == "Geo Map":
        render_geo_map()
    elif view == "Build Notes":
        render_markdown_page("📝 Build Notes", "doc/build.md") # Preserving original path
    
    # Docs Routes
    elif view == "Overview":
        render_markdown_page("📄 Overview", "docs/overview.md")
    elif view == "Project":
        render_markdown_page("🚀 Project Details", "docs/project.md")
    elif view == "More":
        render_markdown_page("ℹ️ More Information", "More.md")
    
    # Chat Routes
    elif view == "Chat 1":
        render_markdown_page("💬 Chat Session 1", "docs/chat1")
    elif view == "Chat 2":
        render_markdown_page("💬 Chat Session 2", "docs/chat2")
    elif view == "Chat 3":
        render_markdown_page("💬 Chat Session 3", "docs/chat3")

if __name__ == "__main__":
    main()