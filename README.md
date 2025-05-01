# Medicall API

**Medicall** is an AI-powered emergency room matching system.  
It finds nearby hospitals based on the patient's location and condition, summarizes the emergency context using Gemini, and prepares a response message for ARS systems.

## How to Run

```bash
# 1. Activate virtual environment
.venv\Scripts\activate   # For Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the FastAPI server
uvicorn app.main:app --reload
