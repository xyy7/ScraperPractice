import os
import re

FILE = 'total.bib'

def log(info, level=1):
    if level == 0:
        print("\033[31m" + info + "\033[0m")
    elif level == 1:
        print("\033[34m" + info + "\033[0m")


def split(file):
    # 寻找到两个@之间，或者@然后结束
    with open(file, 'r',encoding='utf8') as file:
        contents = file.read()
    pattern = r'@.*?\n\n'
    res = re.findall(pattern, contents, re.S)  # re.S可以忽略\n

    # for c in res:
    #     print(c)

    return res


# 中文、英文和其他国姓氏如何区分统一？暂时不能。
# 全都当成英文处理，姓氏默认后边。但是中文在前面，所以中文需要自己根据全名缩写。
def convert_author(author):
    names = author.split(' and ')
    new_names = []
    # print(names)
    for name in names:
        print(name)
        if name.find(',') != -1:  # 姓名切分
            first_name, second_name = name.split(',')
            first_name = first_name.strip()
            second_name = second_name.strip()
            # print(first_name)
            # print(second_name)
            if second_name.find(' ') != -1:  # 名字缩写，空格隔开
                secs = second_name.split(' ')
                second_name = ''
                for i, sec in enumerate(secs):
                    if sec != '':
                        second_name += sec[0].upper()
                        second_name += ' '
            elif second_name.find('-') != -1:  # 名字缩写,'-'隔开
                secs = second_name.split('-')
                second_name = ''
                for i, sec in enumerate(secs):
                    if sec != '':
                        second_name += sec[0].upper()
                        second_name += ' '
            else:  # 单字
                second_name = second_name[0].upper()

            name = first_name + ' ' + second_name
            new_names.append(name)
        else:  # 姓名没有切分
            new_names.append(name)

    # 排序
    # new_names.sort()
    names = ''
    length = len(new_names)
    for i, name in enumerate(new_names):
        name = name.strip()
        names += name
        if i == length - 2:
            names += ' and '
        elif i == length - 1:
            names += '.'
            break
        else:
            names += ', '

    # log(names)
    return names


def convert_DOI(DOI):
    # http://dx.doi.org/10.48550/arXiv.2202.06028
    return f' [DOI: {re.search("doi.org/(.*)", DOI).group(1)}]'


def parse_meta(content):
    meta = {}
    p0 = '@(.*?){'
    type = re.search(p0,content).group(1)
    meta['type'] = type

    p1 = '.*?=.*?\n'  # 不能首尾都是\n,匹配完一个之后，中间掉线了
    res = re.findall(p1, content)

    p2 = '{(.*)}'
    p3 = '(.*?)='
    for r in res:
        # print(r)
        # cont = re.search(p2, r).group()  # 只匹配一个，match从头开始，search匹配到第一个
        value = re.search(p2, r).group(1)  # 部分匹配，小括号+group可以是第几个匹配的
        key = re.search(p3, r).group(1).strip(' ')
        # print(key, value)
        meta[key] = value
    # print()
    return meta


def main():
    """
    @unpublished{20220031030 ,
    language = {English},
    copyright = {Compilation and indexing terms, Copyright 2023 Elsevier Inc.},
    copyright = {Compendex},
    title = {OctAttention: Octree-Based Large-Scale Contexts Model for Point Cloud Compression},
    journal = {arXiv},
    author = {Fu, Chunyang and Li, Ge and Song, Rui and Gao, Wei and Liu, Shan},
    year = {2022},
    issn = {23318422},
    abstract = {<div data-language="eng" data-ev-field="abstract">In point cloud compression, sufficient contexts are significant for modeling the point cloud distribution. However, the contexts gathered by the previous voxel-based methods decrease when handling sparse point clouds. To address this problem, we propose a multiple-contexts deep learning framework called OctAttention employing the octree structure, a memory-efficient representation for point clouds. Our approach encodes octree symbol sequences in a lossless way by gathering the information of sibling and ancestor nodes. Expressly, we first represent point clouds with octree to reduce spatial redundancy, which is robust for point clouds with different resolutions. We then design a conditional entropy model with a large receptive field that models the sibling and ancestor contexts to exploit the strong dependency among the neighboring nodes and employ an attention mechanism to emphasize the correlated nodes in the context. Furthermore, we introduce a mask operation during training and testing to make a trade-off between encoding time and performance. Compared to the previous state-of-the-art works, our approach obtains a 10%-35% BD-Rate gain on the LiDAR benchmark (e.g. SemanticKITTI) and object point cloud dataset (e.g. MPEG 8i, MVUB), and saves 95% coding time compared to the voxel-based baseline. The code is available at https://github.com/zb12138/OctAttention.<br/></div> Copyright &copy; 2022, The Authors. All rights reserved.},
    key = {Encoding (symbols)},
    keywords = {Deep learning;Economic and social effects;},
    note = {Cloud distributions;Context models;Large-scales;Learning frameworks;Memory efficient;Multiple contexts;Octrees;Point-clouds;Sparse point cloud;Symbol sequences;},
    URL = {http://dx.doi.org/10.48550/arXiv.2202.06028},
    }
    :return:
    """

    contents = split(FILE)
    for content in contents:
        meta = parse_meta(content)

        author = convert_author(meta["author"]) + '\n'
        author += meta["author"] + '. \n'  # 双重保障
        year = meta["year"] + '. '
        title = meta["title"]
        log(meta["type"],0)
        if meta['type'] == "article":
            journal = '. '+meta["journal"] + ', ' if "journal" in meta.keys() else ". "
        else:
            journal = '// Proceedings of \n' + meta["journal"].replace("Proceedings - ", "") + ', ' if "journal" in meta.keys() else ". "
        # print(title)

        # print("journal", journal)

        # 期刊
        volume = meta["volume"] if 'volume' in meta.keys() else ""
        number = f'({meta["number"]}): ' if 'number' in meta.keys() else ""
        volume = meta["volume"]+': ' if 'volume' in meta.keys() and number == "" else volume

        # print("volume", volume)

        # 会议
        address = "Piscataway, NJ: "
        publisher = meta["publisher"] + ": " if 'publisher' in meta.keys() else ""
        publisher = "IEEE: " if publisher == "" else publisher

        if meta["type"] == "article":
            address = ""
            publisher = ""

        volume = "" if address != "" else volume

        pages = meta["pages"] if 'pages' in meta.keys() else ""
        pages = pages.replace('--', '-')
        pages = pages.replace(" ", '')

        # print("pages", pages)
        doi = convert_DOI(meta['URL']) if 'URL' in meta.keys() else ""
        # print("doi", doi)

        # 期刊文章：全体作者. 出版年. 文献题名. 刊名, 卷（期）: 起止页码[DOI:]
        # 当没有key 卷时：全体作者. 出版年. 文献题名. 刊名， 地址，出版: 起止页码[DOI:]
        citation = author + year + title + journal + volume+number + address + publisher + pages + doi
        with open('convert_2.txt', 'a') as file:
            file.write(citation+'\n\n\n')
        log(citation)


if __name__ == '__main__':
    main()
