# TravelBuddy Pro ✈️
An interactive, AI-powered travel planner for crafting personalized Indian holidays. Built with Streamlit and powered by the Google Gemini API, this app transforms simple user inputs into detailed, actionable, and multi-lingual travel itineraries.

## ✨ Features
AI-Powered Itineraries: Leverages the Google Gemini API to generate creative and practical travel plans from scratch.

Deep Personalization: Tailors every itinerary based on destination, duration, number of travelers, budget, and specific interests.

Interactive Mapping: Visualizes the entire trip on an interactive map using Pydeck, pinpointing suggested sights, restaurants, and hotels.

Dynamic Map Filtering: Focus the map on a specific day's activities with the click of a button for a more "pinpointed" view.

Multi-Language Support: Supports itinerary generation in multiple languages, including English, Hindi (हिन्दी), Bengali (বাংলা), and Telugu (తెలుగు), with a focus on vernacular usability.

Actionable Suggestions: Integrates "Ride with Uber" and "Book on EaseMyTrip" buttons for locations and accommodations, making the plan instantly usable.

PDF Export: Allows users to download their complete itinerary as a PDF, with full support for vernacular language characters.



## 🛠️ Tech Stack
This project is built with a modern, open-source stack:

Frontend: Streamlit

AI Model: Google Gemini

Mapping: Pydeck & Mapbox

Data Handling: Pandas

PDF Generation: FPDF2

Deployment: Streamlit Community Cloud

## 🚀 Getting Started
To run this project on your local machine, follow these steps.

Prerequisites
Python 3.8+

A GitHub account to clone the repository.

### 1. Clone the Repository
Bash

git clone https://github.com/Abhinaba925/TravelBuddyPro.git
cd TravelBuddyPro
### 2. Create a Virtual Environment
It's highly recommended to use a virtual environment to keep dependencies isolated.

Bash

### For macOS/Linux
'''python3 -m venv venv
source venv/bin/activate'''

### For Windows
python -m venv venv
.\venv\Scripts\activate
### 3. Install Dependencies
Install all the required Python libraries from the requirements.txt file.

Bash

pip install -r requirements.txt
### 4. Set Up API Keys (Secrets)
The application requires API keys for Google Gemini and Mapbox. For local development, you'll use a .env file.

Create a new file in the root of your project folder named .env.

Copy the content below into the file and replace the placeholder text with your actual API keys.

Code snippet

### .env file
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"
MAPBOX_API_TOKEN="pk.eyJ1...YOUR_MAPBOX_PUBLIC_TOKEN_HERE"
Get your Google Gemini key from Google AI Studio.

Get your Mapbox token from your Mapbox Account Dashboard.

### 5. Download the Font for PDF Export
The PDF generation for vernacular languages requires a specific font.

Download the font: Noto Sans Devanagari

Place the file: Make sure the downloaded NotoSansDevanagari-Regular.ttf file is inside the fonts folder in your project.

### 6. Run the App
You're all set! Run the following command in your terminal:

Bash

'''streamlit run app.py'''
☁️ Deployment
This application is deployed and live on Streamlit Community Cloud.


(Note: You will need to replace the link above with the actual URL of your deployed app)

Deployment is handled automatically by Streamlit Cloud whenever a new commit is pushed to the main branch of the GitHub repository. Secrets (GOOGLE_API_KEY and MAPBOX_API_TOKEN) are configured directly in the Streamlit Cloud dashboard for security.
