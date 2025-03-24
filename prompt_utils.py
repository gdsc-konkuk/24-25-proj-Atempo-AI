from typing import Dict
import json

def get_patient_status_prompt(patient_info: Dict) -> str:
    """
    환자 상태를 분석하는 프롬프트를 생성하는 함수입니다.
    
    Args:
        patient_info (Dict): 환자 정보
    
    Returns:
        str: 생성된 프롬프트
    """
    return f"""
    다음 환자 정보를 보고 필요한 의료 서비스와 조치사항을 판단해주세요:
    {json.dumps(patient_info, ensure_ascii=False)}
    
    다음 형식으로 JSON 응답을 제공해주세요:
    {{
        "required_services": ["응급실", "심장내과", "외과" 등],
        "recommendations": ["즉시 응급실 방문", "혈압 측정 필요" 등]
    }}
    """ 