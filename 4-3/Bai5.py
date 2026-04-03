with open("demo_file1.txt", "r", encoding="utf-8") as f:
    text = f.read()

words = text.split()

count = {}

for word in words:
    if word in count:
        count[word] += 1
    else:
        count[word] = 1

print(count)