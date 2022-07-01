import re

with open('text.txt', 'r', encoding='utf-8') as f:
    content = f.read()

alls = re.findall(r'\[(\d+)\]', content)

print(alls)

for a in list(reversed(alls)):
    print(a)
    new_a = str(int(a) + 10)
    print(new_a)

    content = content.replace(f'[{a}]', f'[{new_a}]')

with open('text.txt', 'w', encoding='utf-8') as f:
    f.write(content)

f.close()

