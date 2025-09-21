import streamlit as st
import google.generativeai as genai
import os
import pandas as pd
import pydeck as pdk
import re
from dotenv import load_dotenv
from fpdf import FPDF
from urllib.parse import quote

# --- Load Environment Variables ---
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Page Configuration ---
st.set_page_config(
    page_title="TravelBuddy Pro",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data Loading & Icon ---
ICON_URL = "https://img.icons8.com/plasticine/100/000000/marker.png"
ICON_DATA = {
    "url": ICON_URL,
    "width": 128,
    "height": 128,
    "anchorY": 128,
}

def get_city_data():
    """Returns a DataFrame of Indian cities with coordinates."""
    data = {
        'city': ['Mumbai', 'Delhi', 'Bengaluru', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Goa', 'Kochi', 'Varanasi', 'Agra', 'Rishikesh', 'Shimla', 'Darjeeling', 'Udaipur', 'Amritsar'],
        'lat': [19.0760, 28.6139, 12.9716, 13.0827, 22.5726, 17.3850, 18.5204, 23.0225, 26.9124, 15.2993, 9.9312, 25.3176, 27.1767, 30.0869, 31.1048, 27.0360, 24.5854, 31.6340],
        'lon': [72.8777, 77.2090, 77.5946, 80.2707, 88.3639, 78.4867, 73.8567, 72.5714, 75.7873, 74.1240, 76.2673, 82.9739, 78.0081, 78.2676, 77.1734, 88.2627, 73.6826, 74.8723]
    }
    return pd.DataFrame(data)

CITIES_DF = get_city_data()

# --- Helper Functions ---
def extract_locations(text):
    """Extracts place names, days, and coordinates from the itinerary text."""
    pattern = r"\*\*([\w\s,'-]+\w)\*\*\s*\(day:\s*(\d+),\s*lat:\s*([\d.-]+),\s*lon:\s*([\d.-]+)\)"
    locations = re.findall(pattern, text)
    
    if not locations:
        return pd.DataFrame(columns=['name', 'day', 'lat', 'lon'])
        
    df = pd.DataFrame(locations, columns=['name', 'day', 'lat', 'lon'])
    df['day'] = pd.to_numeric(df['day'])
    df['lat'] = pd.to_numeric(df['lat'])
    df['lon'] = pd.to_numeric(df['lon'])
    df['icon_data'] = [ICON_DATA] * len(df)
    return df

def generate_travel_plan(origin, destination, duration, travelers, budget, interests, language):
    """Generates a personalized travel plan using the Gemini API."""
    if not API_KEY:
        st.error("🚨 Google API Key not found. Please set it in your .env file.")
        return None
    try:
        genai.configure(api_key=API_KEY)
        
        full_prompt = f"""
        You are an expert travel planner named TravelBuddy. Your response must be in {language}.
        Create a complete travel plan for a trip from {origin} to {destination} for {duration} days for {travelers} people with a {budget} budget, focusing on {', '.join(interests)}.

        Your response MUST use the following specific tags and format:

        [TRIP_SUMMARY]
        A brief, engaging summary.

        [BUDGET_ALLOCATION]
        A Markdown table for the budget.

        [DAY_BY_DAY_ITINERARY]
        A detailed day-by-day plan. For each specific point of interest (like a monument, restaurant, or park), YOU MUST format it as: **Name of Place** (day: X, lat: XX.XXXX, lon: YY.YYYY).
        Example: The plan is to visit **Baga Beach** (day: 1, lat: 15.5560, lon: 73.7517).

        [ACCOMMODATION_SUGGESTIONS]
        List 2-3 accommodation options. For each, use the same format as above, using the arrival day (day: 1).
        Example: Stay at **Taj Fort Aguada Resort & Spa** (day: 1, lat: 15.4957, lon: 73.7667).

        [TRANSPORTATION_TIPS]
        Provide brief advice.
        """
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(full_prompt)
        return response.text

    except Exception as e:
        return f"An error occurred: {e}. Please check your API key and network connection."

def parse_plan(plan_text):
    """Parses the generated plan text using unique identifiers."""
    try:
        sections = {
            "summary": plan_text.split("[TRIP_SUMMARY]")[1].split("[BUDGET_ALLOCATION]")[0],
            "budget": plan_text.split("[BUDGET_ALLOCATION]")[1].split("[DAY_BY_DAY_ITINERARY]")[0],
            "itinerary": plan_text.split("[DAY_BY_DAY_ITINERARY]")[1].split("[ACCOMMODATION_SUGGESTIONS]")[0],
            "accommodation": plan_text.split("[ACCOMMODATION_SUGGESTIONS]")[1].split("[TRANSPORTATION_TIPS]")[0],
            "transport": plan_text.split("[TRANSPORTATION_TIPS]")[1]
        }
        return sections
    except IndexError:
        st.error("⚠️ Failed to parse the AI's response. The structure might be incorrect. Please try generating again.")
        return None

class PDF(FPDF):
    def header(self):
        self.add_font('NotoSans', '', 'fonts/NotoSansDevanagari-Regular.ttf')
        self.set_font('NotoSans', size=12)
        self.cell(0, 10, 'Your TravelBuddy Itinerary', 0, 1, 'C')
        self.ln(10)
    def footer(self):
        self.set_y(-15)
        self.add_font('NotoSans', '', 'fonts/NotoSansDevanagari-Regular.ttf')
        self.set_font('NotoSans', size=8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    def chapter_title(self, title):
        self.set_font('NotoSans', size=14)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)
    def chapter_body(self, body):
        self.set_font('NotoSans', size=11)
        self.multi_cell(0, 7, body)
        self.ln()

def create_pdf(plan_data, destination):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf_plan_data = {
        f"Trip to {destination}": plan_data['summary'],
        "Budget Allocation": plan_data['budget'],
        "Day-by-Day Itinerary": plan_data['itinerary'],
        "Accommodation Suggestions": plan_data['accommodation'],
        "Transportation Tips": plan_data['transport']
    }
    for title, body in pdf_plan_data.items():
        pdf.chapter_title(title.replace("_", " ").title())
        pdf.chapter_body(body.strip())
    return bytes(pdf.output())

def display_day_plan(day_content, all_locations):
    """Displays the itinerary for a single day and adds Uber link buttons."""
    day_title = day_content.strip().split('\n')[0]
    
    with st.expander(day_title, expanded=True):
        st.markdown(day_content.strip())
        
        day_num_match = re.search(r'Day (\d+)', day_title)
        if day_num_match:
            day_num = int(day_num_match.group(1))
            day_locations = all_locations[all_locations['day'] == day_num]
            
            if not day_locations.empty:
                st.markdown("**Actionable Locations for this Day:**")
                for index, loc in day_locations.iterrows():
                    uber_url = (
                        f"https://m.uber.com/ul/?action=setPickup&pickup=my_location"
                        f"&dropoff[latitude]={loc['lat']}&dropoff[longitude]={loc['lon']}"
                        f"&dropoff[nickname]={quote(loc['name'])}"
                    )
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"📍 {loc['name']}")
                    with col2:
                        st.link_button("Ride with Uber 🚕", uber_url, use_container_width=True)

# --- Initialize Session State ---
if 'plan' not in st.session_state:
    st.session_state.plan = None
if 'selected_day' not in st.session_state:
    st.session_state.selected_day = "All"

# --- App Header ---
st.title("TravelBuddy Pro ✈️")
st.markdown("Your interactive AI trip planner for unforgettable Indian holidays.")
st.markdown("---")

# --- Sidebar ---
with st.sidebar:
    st.header("Build Your Trip 📝")
    st.subheader("📍 Locations")
    origin = st.selectbox("From:", CITIES_DF['city'].unique(), index=1)
    destination = st.selectbox("To:", CITIES_DF['city'].unique(), index=9)
    st.subheader("🗓️ Duration & Guests")
    col1, col2 = st.columns(2)
    with col1:
        duration = st.number_input("Days", min_value=1, max_value=20, value=5)
    with col2:
        travelers = st.number_input("Travelers", min_value=1, max_value=10, value=2)
    st.subheader("⚙️ Personalization")
    budget = st.select_slider("Select Your Budget:", options=["💰 Budget", "💰💰 Mid-Range", "💰💰💰 Luxury"], value="💰💰 Mid-Range")
    interests = st.multiselect("Select Your Interests:", ["🏞️ Adventure", "🏛️ History & Culture", "🍽️ Food", "🧘‍♀️ Wellness", "🎉 Nightlife", "🛍️ Shopping"], default=["🧘‍♀️ Wellness", "🍽️ Food"])
    language = st.selectbox("Select Language:", ["English", "Hindi (हिन्दी)", "Bengali (বাংলা)", "Telugu (తెలుగు)"])
    st.markdown("---")
    if st.button("Generate My Travel Plan", use_container_width=True, type="primary"):
        st.session_state.selected_day = "All"
        with st.spinner("TravelBuddy is crafting your personalized journey... 🧘"):
            plan_output = generate_travel_plan(origin, destination, duration, travelers, budget, interests, language)
            if plan_output and "An error occurred" not in plan_output:
                st.session_state.plan = plan_output
            else:
                st.session_state.plan = None
                st.error(plan_output or "Failed to generate a plan. Please try again.")

# --- Main Content Area ---
if st.session_state.plan:
    dest_coords = CITIES_DF[CITIES_DF['city'] == destination].iloc[0]
    parsed_plan = parse_plan(st.session_state.plan)

    if parsed_plan:
        st.header(f"Your Custom Itinerary: {origin} to {destination}")
        st.write(parsed_plan['summary'])
        st.markdown("---")

        all_locations = extract_locations(parsed_plan['itinerary'] + parsed_plan['accommodation'])
        
        if st.session_state.selected_day == "All":
            map_locations = all_locations
            view_lat, view_lon, view_zoom = dest_coords['lat'], dest_coords['lon'], 11
        else:
            map_locations = all_locations[all_locations['day'] == st.session_state.selected_day]
            if not map_locations.empty:
                view_lat, view_lon, view_zoom = map_locations['lat'].mean(), map_locations['lon'].mean(), 13
            else:
                view_lat, view_lon, view_zoom = dest_coords['lat'], dest_coords['lon'], 11

        st.subheader("📍 Interactive Trip Map")
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(latitude=view_lat, longitude=view_lon, zoom=view_zoom, pitch=50),
            layers=[
                pdk.Layer('IconLayer', data=map_locations, get_icon='icon_data', get_position='[lon, lat]',
                          get_size=4, size_scale=15, pickable=True)
            ],
            tooltip={"html": "<b>{name}</b>", "style": {"color": "white"}}
        ))

        # --- THIS IS THE CORRECTED LINE ---
        itinerary_days = re.split(r'(?=\*\*\s*Day\s*\d+\s*[:-])', parsed_plan['itinerary'])
        
        day_numbers = sorted(all_locations['day'].unique())
        
        if day_numbers:
            cols = st.columns(len(day_numbers) + 1)
            if cols[0].button("Show All Days", use_container_width=True):
                st.session_state.selected_day = "All"
            
            for i, day_num in enumerate(day_numbers):
                if cols[i+1].button(f"Day {day_num}", use_container_width=True):
                    st.session_state.selected_day = day_num
        
        st.markdown("#### Day-by-Day Plan")
        for day_content in itinerary_days:
            if day_content.strip():
                display_day_plan(day_content, all_locations)

        st.markdown("---")
        
        with st.expander("🏨 Accommodation Suggestions", expanded=True):
            accommodation_locations = extract_locations(parsed_plan['accommodation'])
            
            if accommodation_locations.empty:
                st.markdown(parsed_plan['accommodation'])
            else:
                st.markdown("Here are some AI-powered suggestions. Click to search on EaseMyTrip.")
                for index, loc in accommodation_locations.iterrows():
                    search_term = f"{loc['name']}, {destination}"
                    emt_url = f"https://www.easemytrip.com/hotels/search-hotels/?search={quote(search_term)}"
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"🏨 **{loc['name']}**")
                    with col2:
                        st.link_button("Book on EaseMyTrip", emt_url, use_container_width=True)

        with st.expander("💰 Budget Breakdown"):
            st.markdown(parsed_plan['budget'])
        
        pdf_bytes = create_pdf(parsed_plan, destination)
        st.download_button(label="📥 Download Itinerary as PDF", data=pdf_bytes, file_name=f"TravelBuddy_Itinerary_{destination}.pdf", mime="application/octet-stream")

# Disclaimer
st.markdown("---")
st.warning("Disclaimer: TravelBuddy is a prototype. All recommendations should be independently verified.", icon="⚠️")
