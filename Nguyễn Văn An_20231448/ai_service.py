import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

HEALTH_KEYWORDS = [
    "sức khỏe", "bmi", "cân nặng", "chiều cao", "tăng cân", "giảm cân",
    "nhịp tim", "tim", "co2", "không khí", "huyết áp", "calo",
    "ăn uống", "dinh dưỡng", "vận động", "tập luyện", "ngủ",
    "béo", "gầy", "thừa cân", "thiếu cân"
]


def is_health_question(question):
    q = question.lower()
    return any(keyword in q for keyword in HEALTH_KEYWORDS)


def ask_groq_health_ai(question, latest_record):
    if not is_health_question(question):
        return "Mình chỉ trả lời các câu hỏi liên quan đến sức khỏe."

    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    if not api_key:
        return "Chưa có GROQ_API_KEY. Hãy kiểm tra file .env."

    if latest_record is None:
        health_data = "Người dùng chưa nhập dữ liệu sức khỏe."
    else:
        time, height, weight, bmi, heart_rate, co2, status = latest_record
        health_data = f"""
Dữ liệu mới nhất:
- Thời gian: {time}
- Chiều cao: {height} cm
- Cân nặng: {weight} kg
- BMI: {bmi:.2f}
- Nhịp tim: {heart_rate} bpm
- CO2: {co2} ppm
- Trạng thái: {status}
"""

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": """
Bạn là AI tư vấn sức khỏe.
Chỉ trả lời về sức khỏe, BMI, tăng cân, giảm cân, nhịp tim, CO2,
dinh dưỡng, vận động và giấc ngủ.
Không trả lời chủ đề ngoài sức khỏe.
Không chẩn đoán bệnh, không kê đơn thuốc.
Luôn nhắc đây chỉ là tư vấn tham khảo, không thay thế bác sĩ.
Trả lời bằng tiếng Việt, ngắn gọn, dễ hiểu.
"""
            },
            {
                "role": "user",
                "content": f"{health_data}\n\nCâu hỏi: {question}"
            }
        ],
        temperature=0.3,
        max_tokens=500
    )

    return response.choices[0].message.content