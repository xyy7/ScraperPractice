import concurrent.futures
import os
import os.path as osp
from multiprocessing import Pool

from openai import OpenAI
from tqdm import tqdm

client = OpenAI(api_key="sk-b5acb4b1065540e18551712bf77be24a", base_url="https://api.deepseek.com")

def process_one_file(filename):
    system = {
  "role": "system",
  "content": 
  """
【情感分类标准】  
需结合上下文语境、网络用语特征及弹幕特点，准确分析句子主导情感，并严格按以下层级分类：  

1. **乐（正面情绪）**  
- **快乐**：直接表达愉悦/满足（如“哈哈”“笑死”“绝了”）  
- **安心**：感到安全/放心（如“这样就好”“终于稳了”）  

2. **好（正向评价）**  
- **尊敬**：对地位/成就的敬重（如“致敬大师”）  
- **赞扬**：明确夸奖特质/表现（如“这演技太绝了”）  
- **相信**：表达信任感（如“交给你没问题”）  
- **喜爱**：直接表达喜欢（如“超爱这个角色”）  
- **祝愿**：对未来的美好期许（如“祝顺利”“越来越好”）  

3. **怒（愤怒/指责）**  
- **愤怒**：明显的负面情绪宣泄（如“太过分了！”“气死了”）  

4. **哀（负面情绪）**  
- **悲伤**：直接表露伤心（如“听哭了”“太难受了”）  
- **失望**：期待落空（如“原本以为会更好”）  
- **愧疚**：自我责备（如“都怪我”）  
- **怀念**：怀旧/感慨（如“想起当年”）  

5. **惧（紧张/害怕）**  
- **慌张**：紧张不安（如“怎么办啊”）  
- **恐惧**：真实的害怕感（如“吓死我了”）  
- **羞耻**：尴尬（如“好丢脸”）  

6. **恶（负面评价/厌恶）**  
- **烦躁**：不耐烦（如“能不能别说了”）  
- **憎恶**：强烈厌恶（如“恶心，吐了”）  
- **贬责**：负面评价（如“演技太烂了”）  
- **妒忌**：明显酸意（如“凭什么他就能？”）  
- **怀疑**：质疑真实性（如“假的吧？”）  

7. **惊（惊讶/意外）**  
- **惊奇**：超出预期的惊讶（如“居然还能这样？”）  

---  

【分析要求】  
1. **识别反讽/隐喻**（如“这操作真6”可能是**贬责**，需结合上下文判断）  
2. **注意转折词**（如“但”“却”可能改变情感指向，如“演技不错，但台词功底太差”→ **贬责**）  
3. **区分表面情感与真实意图**（如“好棒哦”可能是**反讽**，需看前后语境）  
4. **主导情感原则**：如一句话含多个情感，选最核心的主导情感（如“又感动又生气”→ **怒:愤怒**，因愤怒更强烈）  
5. **常见网络用语情感倾向**（可结合上下文微调）：
   - **正面**：绝了、牛、神仙操作、YYDS、猛男落泪  
   - **负面**：离谱、草、无语、裂开、搞笑（可能是反讽）  
   - **不确定**：有点意思（可能是惊奇或讽刺）  

示例输出：  
{
    "弹幕内容": "颜怡颜悦就是我的神",
    "情感分类": "好:尊敬",
    "分析依据": "神化比喻触发崇高化情感判定"
},
---  

【正误示例】  
✓ **“以前只有杨笠一人，被骂怕了，现在这么多陪着，她们一点不怕”** → **好:赞扬**（“这么多陪着”+“一点不怕”表支持与团结）  
✓ **“鸭绒这一段真的一下子就治好了我的肤色焦虑”** → **好:祝愿**（“治好焦虑”说明产生积极影响）  
✓ **“你可以赞扬她的灵魂，却偏偏更在乎她的外貌”** → **哀:失望**（“偏偏”表期待落空）  
✗ **“是我们，我们不怕”** → 误:惧:恐惧；正:乐:安心（“不怕”表放心）  
✓ **“个子好高腿好长真漂亮，这是你对她的夸奖？？？”** → **哀:失望**（“？？？”表反问，实际表达不满）  
✓ **“可以夸一个女生漂亮，但她现在是在自己工作领域，这样只关注外貌是不礼貌的”** → **怒:愤怒**（“不礼貌”带有负面情绪）  
✓ **“哈哈哈哈，这也太离谱了吧”** → **惊:惊奇**（“离谱”表示意外，但未必是负面）  
✓ **“牛得一批！简直神仙！”** → **好:赞扬**（正面夸张表达）  
✓ **“好家伙，真是人才”** → **恶:贬责**（常用于反讽）  
✓ **“这不比某些人强多了？”** → **恶:贬责**（“比某些人强”暗含贬低他人）  

---  

【新增优化】  
- **强化网络流行语的情感归类**（如“离谱”可正可负）  
- **调整反讽判断逻辑**（如“绝了”是否为讽刺需结合上下文）  
- **细化“情绪 vs. 评价”分类**（如“草”通常是惊讶，而“烂透了”是贬责）  
- **增加多情感共存的优先级规则**（如“又哭又笑”看哪种情绪更强）  

---
"""
}
    # if os.path.exists(filename.replace(".txt",'_result.txt')):
    #     return 

    write_file = filename.replace(".txt",'_result.txt')
    write_contents = []
    if os.path.exists(write_file):
        with open(write_file,'r+',encoding='utf8') as file:
            write_contents = file.readlines()
        
    with open(filename,'r',encoding='utf8') as file, open(write_file,'a+',encoding='utf8') as writeFile:
        contents = file.readlines()
        print(filename,filename.replace(".txt",'_result.txt'))
        print(f"have processed:{len(write_contents)//5}/{len(contents)}")

        contents = contents[len(write_contents)//5:]

        for i, c in enumerate(contents):
            user = {"role": "user", "content":c}
            messages = [system, user]
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                stream=False
            )
            res = response.choices[0].message.content
            print(response.usage)
            print(f'{i+1}/{len(contents)}',c,res,'\n')
            writeFile.write(res+"\n")
            # break

def process_content_out(c):
    user = {"role": "user", "content": c}
    system = {
"role": "system",
"content": 
"""
【情感分类标准】  
需结合上下文语境、网络用语特征及弹幕特点，准确分析句子主导情感，并严格按以下层级分类：  

1. **乐（正面情绪）**  
- **快乐**：直接表达愉悦/满足（如“哈哈”“笑死”“绝了”）  
- **安心**：感到安全/放心（如“这样就好”“终于稳了”）  

2. **好（正向评价）**  
- **尊敬**：对地位/成就的敬重（如“致敬大师”）  
- **赞扬**：明确夸奖特质/表现（如“这演技太绝了”）  
- **相信**：表达信任感（如“交给你没问题”）  
- **喜爱**：直接表达喜欢（如“超爱这个角色”）  
- **祝愿**：对未来的美好期许（如“祝顺利”“越来越好”）  

3. **怒（愤怒/指责）**  
- **愤怒**：明显的负面情绪宣泄（如“太过分了！”“气死了”）  

4. **哀（负面情绪）**  
- **悲伤**：直接表露伤心（如“听哭了”“太难受了”）  
- **失望**：期待落空（如“原本以为会更好”）  
- **愧疚**：自我责备（如“都怪我”）  
- **怀念**：怀旧/感慨（如“想起当年”）  

5. **惧（紧张/害怕）**  
- **慌张**：紧张不安（如“怎么办啊”）  
- **恐惧**：真实的害怕感（如“吓死我了”）  
- **羞耻**：尴尬（如“好丢脸”）  

6. **恶（负面评价/厌恶）**  
- **烦躁**：不耐烦（如“能不能别说了”）  
- **憎恶**：强烈厌恶（如“恶心，吐了”）  
- **贬责**：负面评价（如“演技太烂了”）  
- **妒忌**：明显酸意（如“凭什么他就能？”）  
- **怀疑**：质疑真实性（如“假的吧？”）  

7. **惊（惊讶/意外）**  
- **惊奇**：超出预期的惊讶（如“居然还能这样？”）  

---  

【分析要求】  
1. **识别反讽/隐喻**（如“这操作真6”可能是**贬责**，需结合上下文判断）  
2. **注意转折词**（如“但”“却”可能改变情感指向，如“演技不错，但台词功底太差”→ **贬责**）  
3. **区分表面情感与真实意图**（如“好棒哦”可能是**反讽**，需看前后语境）  
4. **主导情感原则**：如一句话含多个情感，选最核心的主导情感（如“又感动又生气”→ **怒:愤怒**，因愤怒更强烈）  
5. **常见网络用语情感倾向**（可结合上下文微调）：
- **正面**：绝了、牛、神仙操作、YYDS、猛男落泪  
- **负面**：离谱、草、无语、裂开、搞笑（可能是反讽）  
- **不确定**：有点意思（可能是惊奇或讽刺）  

示例输出：  
{
"弹幕内容": "颜怡颜悦就是我的神",
"情感分类": "好:尊敬",
"分析依据": "神化比喻触发崇高化情感判定"
},
---  

【正误示例】  
✓ **“以前只有杨笠一人，被骂怕了，现在这么多陪着，她们一点不怕”** → **好:赞扬**（“这么多陪着”+“一点不怕”表支持与团结）  
✓ **“鸭绒这一段真的一下子就治好了我的肤色焦虑”** → **好:祝愿**（“治好焦虑”说明产生积极影响）  
✓ **“你可以赞扬她的灵魂，却偏偏更在乎她的外貌”** → **哀:失望**（“偏偏”表期待落空）  
✗ **“是我们，我们不怕”** → 误:惧:恐惧；正:乐:安心（“不怕”表放心）  
✓ **“个子好高腿好长真漂亮，这是你对她的夸奖？？？”** → **哀:失望**（“？？？”表反问，实际表达不满）  
✓ **“可以夸一个女生漂亮，但她现在是在自己工作领域，这样只关注外貌是不礼貌的”** → **怒:愤怒**（“不礼貌”带有负面情绪）  
✓ **“哈哈哈哈，这也太离谱了吧”** → **惊:惊奇**（“离谱”表示意外，但未必是负面）  
✓ **“牛得一批！简直神仙！”** → **好:赞扬**（正面夸张表达）  
✓ **“好家伙，真是人才”** → **恶:贬责**（常用于反讽）  
✓ **“这不比某些人强多了？”** → **恶:贬责**（“比某些人强”暗含贬低他人）  

---  

【新增优化】  
- **强化网络流行语的情感归类**（如“离谱”可正可负）  
- **调整反讽判断逻辑**（如“绝了”是否为讽刺需结合上下文）  
- **细化“情绪 vs. 评价”分类**（如“草”通常是惊讶，而“烂透了”是贬责）  
- **增加多情感共存的优先级规则**（如“又哭又笑”看哪种情绪更强）  

---
"""
}
    messages = [system, user]
    client_in_func = OpenAI(api_key="sk-b5acb4b1065540e18551712bf77be24a", base_url="https://api.deepseek.com")
    try:
        response = client_in_func.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=False
        )
        res = response.choices[0].message.content
    except:
        res = {}
    # print(response.usage)
    return res

def write_to_file(results, writeFile):
    for res in results:
        print(res)
        writeFile.write(res + "\n")
    writeFile.flush()

def process_one_file_process_pool(filename, num_process=48):
    write_file = filename.replace(".txt",'_result.txt')
    write_contents = []
    if os.path.exists(write_file):
        with open(write_file,'r+',encoding='utf8') as file:
            write_contents = file.readlines()
        
    with open(filename,'r',encoding='utf8') as file, open(write_file,'a+',encoding='utf8') as writeFile:
        contents = file.readlines()
        print(filename,filename.replace(".txt",'_result.txt'))
        print(f"have processed:{len(write_contents)//5}/{len(contents)}")

        contents = contents[len(write_contents)//5:]

        for i in range(0, len(contents), num_process*5):
            print("process:",i,len(contents))
            cons = contents[i:i+num_process*5] # BV1wL411i7St BV1xipFeZEvy
            with Pool(processes=num_process) as pool: 
                # ret = pool.map(process_content_out, contents)
                ret = list(tqdm(pool.imap_unordered(process_content_out, cons), total=len(cons)))
                write_to_file(ret, writeFile)

def process_files_in_pool(root):
    files = os.listdir(root)
    files = sorted(files)
    
    # 过滤出文件路径
    file_paths = [osp.join(root, f) for f in files if os.path.isfile(osp.join(root, f)) and not f.endswith('result.txt')]
    print(file_paths,len(file_paths))
    # # 使用进程池并行处理文件，最多使用4个进程
    with Pool(processes=16) as pool:
        pool.map(process_one_file, file_paths)


# if __name__ == "__main__single_process":
if __name__ == "__main__":
    root = r'F:\szu18-onedrive\OneDrive - email.szu.edu.cn\CodeRep\Work-06_scrapper\get_danmuku\danmu'
    files = os.listdir(root)
    files = sorted(files)
    for f in files:
        if os.path.isfile(osp.join(root,f)) and not f.endswith('result.txt'):
            process_one_file_process_pool(osp.join(root,f))
        # break

if __name__ == "__main__process_pool":
# if __name__ == "__main__":
    root = r'F:\szu18-onedrive\OneDrive - email.szu.edu.cn\CodeRep\Work-06_scrapper\get_danmuku\danmu'
    process_files_in_pool(root) 
