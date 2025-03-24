import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import Dict
import json
from prompt_utils import get_patient_status_prompt

# 환경 변수 로드
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini API 설정
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

def analyze_patient_status(patient_info: Dict) -> Dict:
    """
    환자 상태를 분석하는 함수입니다.
    
    Args:
        patient_info (Dict): 환자 정보 (나이, 성별, 증상, 지속시간)
    
    Returns:
        Dict: 분석 결과 (필요한 의료 서비스, 권장 조치사항)
    """
    prompt = get_patient_status_prompt(patient_info)
    
    try:
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        return {
            "error": f"환자 상태 분석 중 오류 발생: {str(e)}",
            "required_services": [],
            "recommendations": ["의료진의 직접적인 평가 필요"]
        } 