from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(title="Gemini Data Analysis API")

# هيكلية البيانات التي يتوقعها التطبيق عند إرسال سؤال
class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"status": "running", "message": "Welcome to the Software API Server!"}

@app.post("/analyze")
def analyze_data(request: PromptRequest):
    # وضع المفتاح المؤقت للتجربة الحالية
    api_key = "AQ.Ab8RN6KzG8iwOUsycp1X_7hT1-5C-aYkeVI6PzcCUmAkloJ6fw"
    
    # رابط استدعاء نموذج فلاش المستقر لعام 2026
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [{"text": request.prompt}]
            }
        ]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            result_data = response.json()
            # استخراج النص الراجع من سيرفرات جوجل
            ai_text = result_data['candidates'][0]['content']['parts'][0]['text']
            return {"response": ai_text}
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
