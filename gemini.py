import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import Dict
import json

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
    prompt = f"""
    다음 환자 정보를 보고 필요한 의료 서비스와 조치사항을 판단해주세요.
    환자 정보: {json.dumps(patient_info, ensure_ascii=False)}
    
    다음 형식으로 JSON 응답을 제공해주세요:
    {{
        "required_services": ["필요한 의료 서비스 목록"],
        "recommendations": ["권장 조치사항 목록"]
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        print("API 응답:", response.text)  # 디버깅용
        
        if not response.text:
            raise ValueError("API 응답이 비어있습니다.")
            
        try:
            result = json.loads(response.text)
            if not isinstance(result, dict) or "required_services" not in result or "recommendations" not in result:
                raise ValueError("응답 형식이 올바르지 않습니다.")
            return result
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 에러: {response.text}")  # 디버깅용
            raise ValueError(f"응답을 JSON으로 변환할 수 없습니다: {str(e)}")
            
    except ValueError as e:
        print(f"값 검증 에러: {str(e)}")  # 디버깅용
        return {
            "error": f"환자 상태 분석 중 오류 발생: {str(e)}",
            "required_services": [],
            "recommendations": ["의료진의 직접적인 평가 필요"]
        }
    except genai.types.generation_types.BlockedPromptException as e:
        print(f"프롬프트 차단 에러: {str(e)}")  # 디버깅용
        return {
            "error": "부적절한 프롬프트가 감지되었습니다.",
            "required_services": [],
            "recommendations": ["의료진의 직접적인 평가 필요"]
        }
    except genai.types.generation_types.GenerationException as e:
        print(f"생성 에러: {str(e)}")  # 디버깅용
        return {
            "error": "응답 생성 중 오류가 발생했습니다.",
            "required_services": [],
            "recommendations": ["의료진의 직접적인 평가 필요"]
        } 