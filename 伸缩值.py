import json
import os
import pandas as pd

def modify_and_save_csv(file_directory, json_file_path):
    # 读取json文件
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    # 处理过程
    for filename, json_value in json_data.items():
        file_path = os.path.join(file_directory, f'{filename}')

        # 读取文件
        csv_file = pd.read_csv(file_path)

        # 对指定年份数据进行乘法运算，并保存
        csv_file.loc[(csv_file['year'] >= 2000) & (csv_file['year'] <= 2002), ['MEAN', 'STD']] = csv_file.loc[(
            csv_file['year'] >= 2000) & (csv_file['year'] <= 2002), ['MEAN', 'STD']].apply(lambda x: x * json_value)
        csv_file.to_csv(file_path, index=False, encoding='utf-8')
modify_and_save_csv('G:\\绘图\\频次(0.9)\\9个区域','G:\\绘图\\频次(0.9)\\伸缩.json')