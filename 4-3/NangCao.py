import os
import difflib
import re
import ast

# ===== Đọc toàn bộ file .py =====
def read_code(folder):
    code = ""
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        code += f.read() + "\n"
                except:
                    pass
    return code


# ===== Chuẩn hóa code =====
def normalize(code):
    # Xóa comment
    code = re.sub(r"#.*", "", code)

    # Xóa khoảng trắng
    code = re.sub(r"\s+", "", code)

    return code


# ===== So sánh text =====
def similarity(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio() * 100


# ===== So sánh AST (logic) =====
def ast_similarity(code1, code2):
    try:
        tree1 = ast.dump(ast.parse(code1))
        tree2 = ast.dump(ast.parse(code2))
        return similarity(tree1, tree2)
    except:
        return 0


# ===== MAIN =====
folder1 = input("Nhập thư mục 1: ")
folder2 = input("Nhập thư mục 2: ")

code1 = read_code(folder1)
code2 = read_code(folder2)

# 1. So sánh cơ bản
basic = similarity(code1, code2)

# 2. So sánh chuẩn hóa
norm1 = normalize(code1)
norm2 = normalize(code2)
advanced = similarity(norm1, norm2)

# 3. So sánh logic
logic = ast_similarity(code1, code2)

# ===== KẾT QUẢ =====
print("\n===== KẾT QUẢ =====")
print(f"📄 Trùng lặp code (text): {basic:.2f}%")
print(f"🧹 Trùng lặp sau khi chuẩn hóa: {advanced:.2f}%")
print(f"🧠 Trùng lặp logic (AST): {logic:.2f}%")

# ===== Đánh giá =====
print("\n===== ĐÁNH GIÁ =====")

if logic > 80:
    print("⚠️ RẤT GIỐNG NHAU (có thể copy hoặc cùng cách giải)")
elif logic > 50:
    print("⚠️ KHÁ GIỐNG (có thể cùng ý tưởng)")
else:
    print("✅ KHÁC NHAU (logic khác)")