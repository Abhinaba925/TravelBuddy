import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- Load Environment Variables ---
# This will load the GOOGLE_API_KEY from your .env file
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Page Configuration ---
st.set_page_config(
    page_title="TravelBuddy - Your AI Trip Planner",
    page_icon="🌍",
    layout="wide"
)

# --- App Header ---
st.title("TravelBuddy 🌍 - Your AI Trip Planner")
st.markdown("Craft your perfect Indian holiday with the power of AI. Get a personalized, day-by-day itinerary complete with budget allocation and travel tips.")
st.markdown("---")


# --- Helper Function for Gemini API call ---
def generate_travel_plan(origin, destination, duration, travelers, budget, interests, language):
    """
    Generates a personalized travel plan using the Gemini API.
    """
    if not API_KEY:
        st.error("🚨 Google API Key not found. Please set it in your .env file.")
        return None

    try:
        genai.configure(api_key=API_KEY)
        
        # This is the simplified prompt without the JSON request
        full_prompt = f"""
        You are an expert travel planner named TravelBuddy, specializing in creating personalized, detailed, and practical itineraries for travel within India. Your response must be in {language}.

        Please create a complete travel plan based on the following details:
        - **Origin:** {origin}
        - **Destination:** {destination}
        - **Trip Duration:** {duration} days
        - **Number of Travelers:** {travelers}
        - **Budget:** {budget}
        - **Primary Interests:** {', '.join(interests)}
        - **Response Language:** {language}

        Your response MUST be structured in Markdown format as follows:

        ---

        ### ✈️ Trip to {destination}: Your Personalized Itinerary

        **Trip Summary:** A brief, engaging 2-3 sentence summary of the trip you've planned.

        ---

        ### **💰 Budget Allocation**
        Provide a table with an estimated budget breakdown. The total should align with the user's selected budget level.

        | Category              | Estimated Cost (INR) | Notes                                           |
        |-----------------------|----------------------|-------------------------------------------------|
        | ✈️ Flights/Transport   | *Your Estimate* | Round trip from {origin} and local transport.   |
        | 🏨 Accommodation       | *Your Estimate* | Based on a {budget} budget for {travelers} people. |
        | 🍽️ Food & Dining      | *Your Estimate* | A mix of local cuisine and cafes.               |
        | 🎟️ Activities & Sights | *Your Estimate* | Entry fees and activity costs.                  |
        | 🛍️ Miscellaneous       | *Your Estimate* | Souvenirs, shopping, and unforeseen expenses.   |
        | **Total Estimated** | **₹ *Your Total*** |                                                 |

        ---

        ### **🗺️ Day-by-Day Itinerary**

        **Day 1: Arrival and Local Flavors**
        - **Morning:** Describe the morning activity (e.g., Arrive at {destination} airport, transfer to hotel, and check-in).
        - **Afternoon:** Suggest an activity that aligns with the interests ({', '.join(interests)}).
        - **Evening:** Suggest a relaxing evening activity or dining experience.
        - **Meal Suggestions:** Recommend types of restaurants or specific dishes to try that fit the budget.

        **Day 2: [Give this day a theme, e.g., Historical Exploration or Adventure Awaits]**
        - **Morning:** Describe the main activity for the morning.
        - **Afternoon:** Describe the afternoon activity.
        - **Evening:** Describe the evening activity.
        - **Meal Suggestions:** Recommend relevant dining options.

        [... continue this format for all {duration} days ...]

        ---

        ### **🏨 Accommodation Suggestions**
        List 2-3 accommodation options that fit the {budget} category (e.g., Luxury Hotel, Boutique Homestay, Budget-friendly Hostel).

        ---

        ### **🚗 Transportation Tips**
        Provide brief advice on getting around {destination} (e.g., "Use app-based services like Ola/Uber for convenience. Auto-rickshaws are great for short distances but be sure to negotiate the fare.").

        ---
        """

        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(full_prompt)
        return response.text

    except Exception as e:
        return f"An error occurred: {e}. Please check your API key and network connection."

# --- Sidebar for User Inputs ---
with st.sidebar:
    st.header("Build Your Trip 📝")
    
    st.subheader("Trip Details")
    origin = st.text_input("From (City):", "Delhi")
    destination = st.text_input("To (City):", "Goa")
    duration = st.number_input("How many days?", min_value=1, max_value=15, value=4)
    travelers = st.number_input("Number of Travelers:", min_value=1, max_value=10, value=2)

    st.markdown("---")

    st.subheader("Personalization")
    budget = st.selectbox("Select Your Budget:", ["💰 Budget-Friendly", "💰💰 Mid-Range", "💰💰💰 Luxury"])
    
    interests = st.multiselect("Select Your Interests:",
                               ["🏞️ Adventure & Outdoors", "🏛️ History & Culture", "🍽️ Food & Culinary",
                                "🧘‍♀️ Relaxation & Wellness", "🎉 Nightlife & Entertainment", "🛍️ Shopping"],
                               default=["🧘‍♀️ Relaxation & Wellness", "🍽️ Food & Culinary"])

    language = st.selectbox("Select Language:", ["English", "Hindi (हिन्दी)", "Bengali (বাংলা)", "Tamil (தமிழ்)"])
    
    st.markdown("---")

    generate_button = st.button("Generate My Travel Plan", use_container_width=True)


# --- Main Content Area ---
if generate_button:
    if not origin or not destination:
        st.error("🚨 Please enter both 'From' and 'To' locations.")
    else:
        with st.spinner("TravelBuddy is crafting your personalized journey... 🧘"):
            plan_output = generate_travel_plan(origin, destination, duration, travelers, budget, interests, language)
            if plan_output:
                st.markdown(plan_output)


st.markdown("---")
st.warning("Disclaimer: TravelBuddy is a prototype. All recommendations, including costs and timings, should be independently verified before making any bookings.", icon="⚠️")