import pandas as pd
import json
import os
import re
from openpyxl import load_workbook
from openpyxl.styles import Alignment

def process_files(xlsx_path, txt_path, output_path=None):
    # 检查目标文件是否已存在
    output_path = output_path or xlsx_path.replace('.xlsx', '_with_emotion.xlsx')
    if os.path.exists(output_path):
        print(f"文件 {os.path.basename(output_path)} 已存在，跳过处理")
        return
        
    # 读取Excel文件
    df = pd.read_excel(xlsx_path)
    
    # 确保有弹幕内容和时间戳列
    if '弹幕' not in df.columns or '时间戳(秒)' not in df.columns:
        raise ValueError("Excel文件缺少'弹幕内容'或'时间戳'列")
    
    # 读取txt文件中的JSON数据
    emotions = []
    with open(txt_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # 使用正则表达式提取所有{}之间的内容
        json_matches = re.findall(r'\{.*?\}', content, re.DOTALL)
        for match in json_matches:
            try:
                # 清理可能的多余字符
                clean_match = match.strip()
                if clean_match.startswith('```json'):
                    clean_match = clean_match[7:].strip()
                if clean_match.endswith('```'):
                    clean_match = clean_match[:-3].strip()
                # 解析JSON
                data = json.loads(clean_match)
                emotions.append(data)
            except json.JSONDecodeError:
                continue
               
    
    # 调试输出：打印第一条情感分析记录
    if emotions:
        print(f"解析到的第一条情感分析记录: {emotions[0]}")
    else:
        print("错误：未解析到任何有效情感分析记录，请检查txt文件格式是否符合要求")
        return

    # 创建情感分类和分析依据的字典
    try:
        emotion_dict = {e['弹幕内容']: (e['情感分类'], e['分析依据']) for e in emotions
                      if all(key in e for key in ['弹幕内容', '情感分类', '分析依据'])}
    except KeyError as e:
        print(f"错误：缺少必要字段 '{e}'，请确保所有记录都包含'弹幕内容','情感分类'和'分析依据'字段")
        print(f"问题记录示例: {next((e for e in emotions if '弹幕内容' not in e), '无')}")
        return
    
    # 添加新列
    df['情感分类'] = ''
    df['分析依据'] = ''
    
    # 填充数据
    for idx, row in df.iterrows():
        content = row['弹幕']
        if content in emotion_dict:
            df.at[idx, '情感分类'], df.at[idx, '分析依据'] = emotion_dict[content]
    
    # 保存到新Excel文件
    output_path = output_path or xlsx_path.replace('.xlsx', '_with_emotion.xlsx')
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
        
        # 设置单元格自动换行
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        for row in worksheet.iter_rows():
            for cell in row:
                cell.alignment = Alignment(wrap_text=True)
    
    print(f"成功处理文件: {os.path.basename(xlsx_path)}")

def main():
    danmu_dir = os.path.join(os.path.dirname(__file__), 'danmu')
    
    # 获取所有xlsx文件
    for filename in os.listdir(danmu_dir):
        if filename.endswith('.xlsx'):
            base_name = filename[:-5]  # 去掉.xlsx后缀
            xlsx_path = os.path.join(danmu_dir, filename)
            txt_path = os.path.join(danmu_dir, f"{base_name}_result.txt")
            
            if os.path.exists(txt_path):
                try:
                    process_files(xlsx_path, txt_path)
                except Exception as e:
                    print(f"处理文件 {filename} 时出错: {str(e)}")

if __name__ == '__main__':
    main()