import json
import os
import re

import pandas as pd

from getDanmu import *


def parse_one_file(filename, emotion_dict):
    with open(filename,'r',encoding='utf8') as file:
        contents = file.read()
        emotion_pattern = re.compile(r'"情感分类":\s*"([^"]+)"')
        emotion = re.findall(emotion_pattern,contents)
        # print(emotion)
        for e in emotion:
            if e in emotion_dict:
                emotion_dict[e]+=1
            else:
                emotion_dict[e]=1

def process_one_dir(root):
    all_emotion_dicts = []
    files = os.listdir(root)
    files = [f for f in files if f.endswith('result.txt')]
    print(files)
    for i,f in enumerate(files):
        print(f)
        bv_id = re.findall(r'(BV.*?)_',f)[0]
        print(bv_id)
        title, url = get_title_from_bv(bv_id) 
        title = title[0]
        print(title)

        f = os.path.join(root,f)
        emotion_dict = {"title":title,"url":url}
        parse_one_file(f,emotion_dict)
        print(emotion_dict)
        all_emotion_dicts.append(emotion_dict)
        

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(all_emotion_dicts)
    
    # Write the accumulated data to a single Excel file
    df.to_excel(f'{root}.xlsx', index=False)
    

if __name__ == '__main__':
    # process_one_dir("danmu-strict")
    # process_one_dir("danmu-humor")
    process_one_dir("danmu")
   



