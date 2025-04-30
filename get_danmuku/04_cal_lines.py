import os

def count_lines_in_file(file_path):
    """统计单个文件的行数"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return sum(1 for line in file)

def count_lines_in_directory(directory):
    """统计目录下所有txt文件的行数"""
    total_lines = 0
    file_counts = {}
    
    # 确保目录存在
    if not os.path.exists(directory):
        print(f"目录 {directory} 不存在")
        return None
    
    # 遍历目录下的所有文件
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            try:
                lines = count_lines_in_file(file_path)
                file_counts[filename] = lines
                total_lines += lines
            except Exception as e:
                print(f"读取文件 {filename} 时出错: {e}")
    
    return file_counts, total_lines

def main():
    directory = 'danmu'
    results = count_lines_in_directory(directory)
    
    if results is not None:
        file_counts, total_lines = results
        
        # 打印每个文件的行数
        print("各文件行数统计:")
        for filename, lines in file_counts.items():
            print(f"{filename}: {lines} 行")
        
        # 打印总计行数
        print(f"\n总计行数: {total_lines} 行")

if __name__ == "__main__":
    main()