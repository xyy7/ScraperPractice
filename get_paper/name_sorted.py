import os
import re

FILE = 'convert.txt'


def log(info, level=1):
    if level == 0:
        print("\033[31m" + info + "\033[0m")
    elif level == 1:
        print("\033[34m" + info + "\033[0m")


def split(file):
    # 寻找到两个@之间，或者@然后结束
    with open(file, 'r', encoding='utf8') as file:
        contents = file.read()
    pattern = r'(.*?)\n'
    res = re.findall(pattern, contents)  # re.S可以忽略\n

    # for c in res:
    #     print(c)

    return res


# 中文、英文和其他国姓氏如何区分统一？暂时不能。
# 全都当成英文处理，姓氏默认后边。但是中文在前面，所以中文需要自己根据全名缩写。
def convert_author(author):
    names = author.split(',')
    if names[-1].find('and') != -1:
        nn = names[-1].split(' and ')
        names[-1] = nn[0]
        names.append(nn[1])

    # 排序
    new_names = []
    for name in names:
        new_names.append(name.strip())

    new_names.sort()
    names = ''
    length = len(new_names)
    for i, name in enumerate(new_names):
        name = name.strip()
        names += name
        if i == length - 2:
            names += ' and '
        elif i == length - 1:
            names += ''
            break
        else:
            names += ', '

    # log(names)
    return names


def main():
    contents = split(FILE)
    for content in contents:
        if re.search('\n?(.*?)\. [0-9]{4}', content) is None:
            log("none match \n", 0)
            continue
        name = re.search('\n?(.*?)\. [0-9]{4}', content).group(1).strip()
        log(name)
        author = convert_author(name)
        # print(name)
        # print(author)
        # exit()
        citation = content.replace(name, author)
        with open('convert_name_sorted.txt', 'a') as file:
            file.write(citation + '\n\n\n')


if __name__ == '__main__':
    main()
