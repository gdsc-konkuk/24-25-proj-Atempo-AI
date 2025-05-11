from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from app.schemas import RequestModel
from app.hospital import (
    search_hospitals,
    enrich_hospital_info,
    summarize_condition,
    filter_hospitals_by_condition
)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Medicall API is running"}

@app.post("/medicall")
def medicall_endpoint(request_data: RequestModel):
    try:
        lat = request_data.location.latitude
        lng = request_data.location.longitude
        radius = request_data.search_radius
        condition = request_data.patient_condition

        hospitals, error = search_hospitals(lat, lng, radius)
        print("=== Raw hospital data ===")
        print(hospitals)
        print("Error:", error)
        if error or not hospitals: 
            return {
                "hospital_list": [],
                "ars_message": ""
            }

        hospital_list = enrich_hospital_info(hospitals, lat, lng)
        condition_summary = summarize_condition(condition)

        hospital_list = filter_hospitals_by_condition(hospital_list, condition_summary)

        ars_message = (
            f"This is Medicall, an AI-powered emergency room matching system. A patient with {condition_summary} "
            f"has been reported within {radius/1000:.0f} km. If your hospital can admit the patient, press 1. If not, press 2."
        )

        return {
            "hospital_list": hospital_list,
            "ars_message": ars_message
        }

    except Exception as e:
        return {
            "hospital_list": [],
            "ars_message": ""
        }