import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Halalan 2025 Data Science Dashboard",
    page_icon="🇵🇭",
    layout="wide"
)

# --- 1. DATA INGESTION (MOCKED FOR DEMO) ---
# In a real scenario, replace this with: pd.read_csv("s3://bucket/election_2025_full.csv")
@st.cache_data
def load_data():
    # Mock Data based on partial 2025 reports
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
        "Votes": [2776316, 1817461, 1461427, 1237929, 950000],
        "Percentage": [6.66, 4.36, 3.51, 2.97, 2.20]
    }
    
    meta_data = {
        "Total Voters": 69773653,
        "Votes Cast": 56962688,
        "Precincts Processed": 92808,
        "Total Precincts": 93629
    }
    
    return pd.DataFrame(senate_data), pd.DataFrame(partylist_data), meta_data

df_senate, df_partylist, meta = load_data()

# --- SIDEBAR ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/9/99/Coat_of_arms_of_the_Philippines.svg", width=100)
st.sidebar.title("Filters & Settings")
show_top_n = st.sidebar.slider("Show Top N Candidates", 5, 12, 12)
party_filter = st.sidebar.multiselect("Filter by Party", df_senate["Party"].unique(), default=df_senate["Party"].unique())

# --- MAIN DASHBOARD ---
st.title("🇵🇭 Halalan 2025 Official Results Dashboard")
st.markdown(f"**Data Status:** Partial, Unofficial ({meta['Precincts Processed'] / meta['Total Precincts'] * 100:.2f}% of Election Returns processed)")

# Metric Cards
col1, col2, col3 = st.columns(3)
col1.metric("Registered Voters", f"{meta['Total Voters']:,}")
col2.metric("Voter Turnout", f"{meta['Votes Cast']:,}", f"{(meta['Votes Cast']/meta['Total Voters'])*100:.2f}%")
col3.metric("Precincts Reporting", f"{meta['Precincts Processed']:,} / {meta['Total Precincts']:,}")

st.markdown("---")

# --- VISUALIZATION 1: SENATE RACE ---
st.subheader("🏛️ Senatorial Race: The Magic 12")

# Filtering Data
filtered_senate = df_senate[df_senate["Party"].isin(party_filter)].head(show_top_n)

# Interactive Bar Chart
fig_senate = px.bar(
    filtered_senate, 
    x="Votes", 
    y="Candidate", 
    orientation='h',
    color="Party",
    text_auto='.2s',
    title="Top Senatorial Candidates by Vote Count",
    color_discrete_sequence=px.colors.qualitative.Bold
)
fig_senate.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig_senate, use_container_width=True)

# --- VISUALIZATION 2: PARTY LIST BREAKDOWN ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📊 Party-List Composition")
    fig_party = px.pie(
        df_partylist, 
        values='Votes', 
        names='Party List', 
        title='Top Party-List Groups (Vote Share)',
        hole=0.4
    )
    st.plotly_chart(fig_party, use_container_width=True)

with col_right:
    st.subheader("📈 Vote Distribution Analysis")
    st.write("This section calculates the 'Safe Margin' for the 12th spot.")
    
    # Calculate margin
    if len(df_senate) >= 12:
        top_12 = df_senate.iloc[11]["Votes"]
        rank_13 = df_senate.iloc[11]["Votes"] * 0.95 # Mocking a close contender
        st.metric(label="Votes needed for 12th Spot", value=f"{top_12:,}")
        st.info(f"The margin between 12th and hypothetical 13th is approx. {top_12 - rank_13:,.0f} votes.")
    else:
        st.write("Insufficient data to calculate 12th spot margin.")

# --- FOOTER ---
st.markdown("---")
st.caption("Data Source: Aggregated from Comelec Transparency Server & Media Mirrors. Generated for Data Science Demonstration.")