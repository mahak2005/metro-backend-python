import pandas as pd
import nltk
import os
from nltk.chat.util import Chat, reflections
from flask import Flask, request, jsonify
import re

# Step 1: Load CSV Data
routes_df = pd.read_csv("data/route.csv")
stations_df = pd.read_csv("data/stop.csv")  
stoptimes_df = pd.read_csv("data/stop_time.csv")  

# Function to get route information
def get_route_info(route_name):
    route = routes_df[routes_df['route_short_name'].str.contains(route_name, case=False) | 
                      routes_df['route_long_name'].str.contains(route_name, case=False)]
    if not route.empty:
        return f"Route: {route['route_long_name'].values[0]} ({route['route_short_name'].values[0]})\nColor: {route['route_color'].values[0]}"
    else:
        return "Sorry, no such route found."

# Function to get station details
def get_station_info(station_name):
    station = stations_df[stations_df['stop_name'].str.contains(station_name, case=False)]
    if not station.empty:
        return f"Station: {station['stop_name'].values[0]}\nLocation: ({station['stop_lat'].values[0]}, {station['stop_lon'].values[0]})"
    else:
        return "Sorry, no such station found."

# Function to get schedule information for a station
def get_schedule_info(station_name):
    station = stations_df[stations_df['stop_name'].str.contains(station_name, case=False)]
    if not station.empty:
        stop_id = station['stop_id'].values[0]
        stop_times = stoptimes_df[stoptimes_df['stop_id'] == stop_id]
        if not stop_times.empty:
            schedules = stop_times[['trip_id', 'arrival_time', 'departure_time']].to_dict(orient='records')
            schedule_info = "Schedules:\n"
            for schedule in schedules:
                schedule_info += f"Trip ID: {schedule['trip_id']}, Arrival: {schedule['arrival_time']}, Departure: {schedule['departure_time']}\n"
            return schedule_info
        else:
            return "No schedule available for this station."
    else:
        return "No such station found."

# Step 3: Define chatbot patterns
patterns = [
    (r'hi|hello|hey', ['Hello! How can I assist you today with the Delhi Metro?']),
    (r'help', ['I can assist with station details, route information, and schedules. What would you like to know?']),
    (r'(?i)(route|line) (.*)', [get_route_info]),  
    (r'(?i)(station|stop) (.*)', [get_station_info]),  
    (r'(?i)(schedule|timing) (.*)', [get_schedule_info]),  
    (r'(bye|exit)', ['Goodbye! Have a nice day!'])
]

# Step 4: Initialize the chatbot
def chatbot_response(user_input):
    for pattern, responses in patterns:
        match = re.search(pattern, user_input)
        if match:
            matched_input = match.group(2).strip()
            if responses[0] == get_route_info:
                return get_route_info(matched_input)
            elif responses[0] == get_station_info:
                return get_station_info(matched_input)
            elif responses[0] == get_schedule_info:
                return get_schedule_info(matched_input)
    return "Sorry, I didn't understand that. Please try asking something else."

# Step 5: Flask app for the chatbot
app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input')
    if not user_input:
        return jsonify({"error": "No input provided"}), 400
    
    bot_response = chatbot_response(user_input)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render dynamically assigns the port
    app.run(host='0.0.0.0', port=port, debug=False)  
