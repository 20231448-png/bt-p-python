_list = ['python', 'java', 'c', 'javascript', 'go', 'ruby']

n = int(input("Nhập n: "))

result = []

for word in _list:
    if len(word) > n:
        result.append(word)

print("Các từ có độ dài lớn hơn", n, ":", result)