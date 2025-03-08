import streamlit as st
from pymongo import MongoClient

client = MongoClient("mongodb+srv://itz4mealone:SportsMentor@cluster0.gcagz.mongodb.net/test?retryWrites=true&w=majority&appName=Cluster0")  # MongoDB connection string
db = client['test']  # Replace with your database name
athletes_collection = db['users']  # Replace with your collection name

# Enhanced Search Function
def search_athletes(sport, sponsorship_type, sort_option, results_col):
    # Query MongoDB based on inputs
    query = {}
    if sport:
        query['athleteSport'] = sport
    if sponsorship_type:
        query['athleteSponsorshipType'] = sponsorship_type
    
    try:
        athletes = list(athletes_collection.find(query))

        if not athletes:
            results_col.warning("❌ No athletes found.")
        else:
            # Sorting Logic
            if sort_option == "Skill Level":
                athletes.sort(key=lambda x: x.get('athleteSkillLevel', '').lower())
            elif sort_option == "Region":
                athletes.sort(key=lambda x: x.get('athleteRegion', '').lower())

            # Display Result Counter
            results_col.success(f"✅ Found {len(athletes)} athlete(s) matching your criteria.")

            # Display Athlete Cards
            for athlete in athletes:
                with results_col:
                    st.markdown(
                        f"""
                        <div style="
                            background-color: #f0f2f6;
                            border-left: 5px solid #4CAF50;
                            border-radius: 12px;
                            padding: 15px;
                            margin-bottom: 10px;
                            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                        ">
                        <h4> {athlete.get('name', 'N/A')}</h4>
                        <p> <b>Sport:</b> {athlete.get('athleteSport', 'N/A')}</p>
                        <p> <b>Sponsorship Type:</b> {athlete.get('athleteSponsorshipType', 'N/A')}</p>
                        <p><b>Region:</b> {athlete.get('athleteRegion', 'N/A')}</p>
                        <p> <b>Email:</b> {athlete.get('email', 'N/A')}</p>
                        <p> <b>Skill Level:</b> {athlete.get('athleteSkillLevel', 'N/A')}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    except Exception as e:
        results_col.error(f"❗ Error fetching athletes: {e}")

# Streamlit UI Layout
st.set_page_config(page_title="Athlete Finder", layout="wide")

# Columns for Sidebar + Results
sidebar_col, results_col = st.columns([1, 3])

# Sidebar for Inputs
with sidebar_col:
    st.title("🔎 Athlete Search")
    sport = st.text_input('Enter Sport')
    sponsorship_type = st.selectbox(
        'Select Sponsorship Type',
        ['Financial', 'Equipment', 'Training']
    )
    sort_option = st.selectbox(
        'Sort By',
        ['None', 'Skill Level', 'Region']
    )
    
    if st.button('🔍 Search'):
        if sport:
            search_athletes(sport, sponsorship_type, sort_option, results_col)
        else:
            results_col.warning("⚠️ Please enter a sport to search.")

# Footer
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px;">
        <hr>
        <p style="color: grey;">Made with  using Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)
