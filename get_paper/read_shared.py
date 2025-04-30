import re

metas1 = []
metas2 = []
with open('shared.txt', 'r',encoding='utf8') as file:
    contents = file.readlines()

    for line in contents:
        p = '[0-9]{4}\. (.*?)[./]'
        meta = {}
        meta['content'] = line
        if re.search(p, line) is None:
            metas1.append(meta)
            continue

        print(line[:6], end='')
        title = re.search(p, line).group(1).strip()
        meta["title"] = title
        metas1.append(meta)
        print(title)
print()
with open('convert_2.txt', 'r', encoding='gbk') as file:
    contents = file.readlines()

    for line in contents:
        if line == '\n':
            continue
        p = '[0-9]{4}\. (.*?)[./]'
        meta = {}
        if re.search(p, line) is None:
            continue
        meta['content'] = line
        title = re.search(p, line).group(1)
        meta["title"] = title.strip()
        metas2.append(meta)
        print(title)

print(len(metas1),len(metas2))
for m2 in metas2:
    for m1 in metas1:
        if "title" in m1.keys():
            if m1['title'].upper() == m2['title'].upper():
                print(m1['title'])
                m1['content'] = m1['content'][0:6]+m2['content']
                break

# merge
with open('merge_publisher_city.txt', 'a') as file:
    for m in metas1:
        file.write(m["content"])

