
import json
from datetime import datetime
import requests, os

# Assuming these environment variables are set up in your environment:
# APP_ID, API_KEY, EXERCISE_ENDPOINT, SHEETY_AUTH_TOKEN

gender = "male"
weight_in_kg = "75.8"
height_in_cm = "179"
age = 40

# Retrieving sensitive data from environment variables
APP_ID = os.environ.get('APP_ID')
API_KEY = os.environ.get('API_KEY')
exercise_endpoint = os.environ.get('EXERCISE_ENDPOINT')
sheety_auth_token = os.environ.get('SHEETY_AUTH_TOKEN')  # Your Sheety authorization token

exercise_text = input("Please tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": gender,
    "weight_kg": weight_in_kg,
    "height_cm": height_in_cm,
    "age": age,
}

exercise_response = requests.post(url=exercise_endpoint, json=parameters, headers=headers)
exercise_result = exercise_response.json()
print(exercise_result)

date_and_time_now = datetime.now()
now_formatted_date = date_and_time_now.strftime("%d/%m/%Y")
now_formatted_time = date_and_time_now.strftime("%H:%M:%S")

sheety_endpoint_url = "https://api.sheety.co/61ebfea22e49232bb280d6a22d698d26/sirisWorkouts/workouts"
sheety_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {sheety_auth_token}"  # Adding authorization header for Sheety API
}

for each_exercise in exercise_result['exercises']:
    json_payload_sheet_inputs = {
        'workout': {
            "date": now_formatted_date,
            "time": now_formatted_time,
            "exercise": each_exercise['name'].title(),
            "duration": each_exercise['duration_min'],
            "calories": each_exercise['nf_calories'],
        }
    }
    sheety_post_request_response = requests.post(url=sheety_endpoint_url, json=json_payload_sheet_inputs, headers=sheety_headers)
    print(sheety_post_request_response.text)
