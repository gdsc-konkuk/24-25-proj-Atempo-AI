import os
import json
import requests
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Load environment variables
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite", temperature=0.4)

def search_hospitals(latitude, longitude, radius=5000):
    url = "https://places.googleapis.com/v1/places:searchNearby"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_PLACES_API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.nationalPhoneNumber,places.location,places.formattedAddress",
        "Accept-Language": "en"
    }
    payload = {
        "includedTypes": ["hospital"],
        "locationRestriction": {
            "circle": {
                "center": {"latitude": float(latitude), "longitude": float(longitude)},
                "radius": float(radius)
            }
        }
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        data = res.json()
    except:
        return [], "API request failed"

    if "places" not in data:
        msg = data.get("error", {}).get("message", "Unknown error")
        return [], f"Error: {msg}"

    results = []
    seen_numbers = set()

    for item in data["places"]:
        name = item.get("displayName", {}).get("text", "Unknown")
        phone = item.get("nationalPhoneNumber")
        if phone:
            phone = "+82" + phone
        address = item.get("formattedAddress", "Unknown")
        location = item.get("location", {})
        lat, lng = location.get("latitude"), location.get("longitude")

        if not phone or phone in seen_numbers or lat is None or lng is None:
            continue

        seen_numbers.add(phone)

        results.append({
            "name": name,
            "phone_number": phone,
            "address": address,
            "lat": lat,
            "lng": lng
        })

    return results, None

def summarize_condition(condition_text):
    prompt = PromptTemplate(
        input_variables=["condition"],
        template="""
The following is a description of a patient's emergency condition.
Please summarize it into one concise and informative sentence for hospital staff.

Condition:
{condition}
"""
    )
    try:
        result = (prompt | llm).invoke({"condition": condition_text})
        return result.content.strip().replace("**", "")
    except:
        return "Failed to summarize condition."

def get_distance_and_time(hospital_name, user_lat, user_lng, hospital_lat, hospital_lng):
    prompt = f"""
You are acting as a navigation assistant for paramedics.

You are assisting paramedics by estimating the realistic driving distance and travel time between a patient and a hospital in Seoul, South Korea.

This estimation must be based on actual roads, not straight-line (air) distance.

Patient location:
- Latitude: {user_lat}
- Longitude: {user_lng}

Hospital:
- Name: \"{hospital_name}\"
- Latitude: {hospital_lat}
- Longitude: {hospital_lng}

Assumptions:
- Use average daytime traffic in Seoul.
- Assume a standard car route using public roads and highways.
- Avoid estimating based on straight-line distance or walking paths.

Return only a JSON object like:
{{
  "distance": "X.X km",
  "travel_time": "X minutes"
}}

Do not include explanations, markdown, or extra text.
"""
    try:
        response = llm.invoke(prompt)
        content = response.content.strip()
        if "```" in content:
            content = content.split("```", 1)[-1].strip()
        start, end = content.find("{"), content.rfind("}") + 1
        data = json.loads(content[start:end])
        return data.get("distance", "Unknown"), data.get("travel_time", "Unknown")
    except:
        return "Unknown", "Unknown"

def get_hospital_details(hospital_name):
    prompt = f"""
You are an assistant helping paramedics understand the key medical specialties of the hospital below.

Hospital name: \"{hospital_name}\"
Location: Seoul, South Korea

Based on this hospital's name and typical structure of major Korean hospitals, provide exactly 3 English department names that best represent this hospital’s primary specialties.
Avoid repeating the same set of departments for different hospitals unless clearly appropriate.

Return only a JSON object like:
{{
  "departments": ["Cardiology", "Emergency Medicine", "Neurology"]
}}
"""
    try:
        response = llm.invoke(prompt)
        content = response.content.strip()

        if "```" in content:
            content = content.split("```", 1)[-1].strip()

        start, end = content.find("{"), content.rfind("}") + 1
        data = json.loads(content[start:end])

        return {
            "departments": data.get("departments", [])
        }
    except:
        return {
            "departments": []
        }

def enrich_hospital_info(hospitals, user_lat, user_lng):
    result = []

    for hospital in hospitals[:20]:
        name = hospital["name"]
        h_lat, h_lng = hospital["lat"], hospital["lng"]

        distance, travel_time = get_distance_and_time(name, user_lat, user_lng, h_lat, h_lng)
        extra = get_hospital_details(name)

        result.append({
            "name": name,
            "phone_number": hospital["phone_number"],
            "address": hospital["address"],
            "distance": distance,
            "travel_time": travel_time,
            "departments": extra["departments"]
        })

    return result