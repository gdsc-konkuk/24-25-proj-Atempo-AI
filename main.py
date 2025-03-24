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

@app.get("/analyze-patient")
async def analyze_patient_get(age: int, gender: str, symptoms: str, duration: str):
    try:
        # symptoms 문자열을 리스트로 변환
        symptoms_list = [s.strip() for s in symptoms.split(",")]
        
        # PatientInfo 모델 사용
        patient = PatientInfo(
            age=age,
            gender=gender,
            symptoms=symptoms_list,
            duration=duration
        )
        
        result = analyze_patient_status(patient.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-patient")
async def analyze_patient(patient: PatientInfo):
    try:
        result = analyze_patient_status(patient.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 테스트용 코드
if __name__ == "__main__":
    # 테스트 데이터
    test_patient = {
        "age": 58,
        "gender": "남성",
        "symptoms": ["가슴 통증", "호흡 곤란"],
        "duration": "30분"
    }
    
    # 테스트 실행
    print(json.dumps(analyze_patient_status(test_patient), ensure_ascii=False, indent=4))