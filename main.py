from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from gemini import analyze_patient_status

app = FastAPI(
    title="Atempo Gemini API",
    description="환자 상태 분석을 위한 Gemini API 서버",
    version="1.0.0"
)

class PatientInfo(BaseModel):
    age: int
    gender: str
    symptoms: List[str]
    duration: str

@app.get("/")
async def root():
    return {"message": "Atempo Gemini API 서버에 오신 것을 환영합니다."}

@app.post("/analyze-patient")
async def analyze_patient(patient: PatientInfo):
    try:
        result = analyze_patient_status(patient.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 