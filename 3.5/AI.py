import re
import subprocess
from openai import OpenAI

# ===== API Groq =====
client = OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

# ===== Đề bài =====
text = """
Bài 4: Viết chương trình nhập một số nguyên dương và kiểm tra xem số đó có chia hết cho 2 hoặc cho 3 hoặc cả hai hay không?
Bài 5: Viết chương trình giải phương trình bậc 2: a*x*x + b*x + c = 0. Trong đó 3 tham số a,b,c được nhập từ bàn phím. Sử dụng thư viện math và hàm sqrt().
"""

# ===== Tách bài =====
bai_list = re.findall(r"Bài\s*(\d+):(.*?)(?=Bài\s*\d+:|$)", text, re.S)

for num, problem in bai_list:

    prompt = f"""
Viết chương trình Python giải bài sau:

{problem}

Chỉ trả về code Python.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    code = response.choices[0].message.content

    # xoá markdown
    code = re.sub(r"```python|```", "", code).strip()

    filename = f"Bai{num}.py"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)

    print("Đã tạo file:", filename)

# ===== PUSH GITHUB =====

print("Đang push lên GitHub...")

subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "AI auto generate exercises"])
subprocess.run(["git", "push"])

print("Push GitHub thành công 🚀")