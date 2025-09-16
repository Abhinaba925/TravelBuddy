# TravelBuddy 🌍
TravelBuddy is an AI-powered travel planner that creates personalized holiday itineraries for travel within India. Using Google's Gemini model and a Streamlit web interface, it generates detailed day-by-day plans, complete with budget allocations, based on user preferences.

## Features
Personalized Itineraries: Generates travel plans based on origin, destination, trip duration, number of travelers, and specific interests.

Dynamic Budget Allocation: Provides a clear, table-based budget for flights, accommodation, food, and activities.

Vernacular Language Support: Creates itineraries in multiple languages, including English, Hindi, Bengali, and Tamil.

Simple Web UI: An intuitive and easy-to-use interface built with Streamlit.

## How to Run Locally
Follow these steps to set up and run the project on your machine.

### 1. Prerequisites
Python 3.8+

A Google Gemini API Key

### 2. Clone the Repository
If you've uploaded the project to GitHub, clone it. Otherwise, just navigate to your project folder.

Bash

git clone https://github.com/your-username/TravelBuddy.git
cd TravelBuddy
### 3. Set Up Your Environment
Create a file named .env in the project's root directory and add your Gemini API key:

GOOGLE_API_KEY="YOUR_API_KEY_HERE"
### 4. Install Dependencies
Install the required Python libraries from the requirements.txt file.

Bash

pip install -r requirements.txt
### 5. Run the Streamlit App
Launch the application by running the following command in your terminal:

Bash

streamlit run app.py
Your web browser should automatically open with the TravelBuddy application running.
