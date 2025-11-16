import pandas as pd
import os

def split_to_9(path):
    # 读取 CSV 文件
    df = pd.read_csv(path)

    # 根据SNAME_1进行分组
    grouped = df.groupby('ZONE_CODE')

    # 输出文件夹路径
    output_folder = f'{os.path.dirname(path)}/9个区域'

    # 创建输出文件夹，如果存在则不创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历每个分组
    for name, group in grouped:
        # 输出文件的路径
        file_path = os.path.join(output_folder, f'{name}.csv')

        # 将分组数据保存为 csv 文件
        group.to_csv(file_path, index=False)
split_to_9('G:\绘图\频次(0.9)\表格.csv')