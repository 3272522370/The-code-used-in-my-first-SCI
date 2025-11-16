import os
import dbfread
import pandas as pd


def merge_dbf_files_to_excel(dbf_file_paths, output_excel_path):
    """
    将多个DBF文件的数据合并到一个Excel文件中。

    :param dbf_file_paths: DBF文件的路径列表。
    :param output_excel_path: 输出Excel文件的路径名。
    """
    all_data_frames = []

    # 定义一个函数来读取dbf文件并返回DataFrame
    def read_dbf_file(dbf_file_path):
        try:
            print(f'正在读取文件{dbf_file_path}')
            table = dbfread.DBF(dbf_file_path,encoding='utf-8')
            df = pd.DataFrame(iter(table))
            return df
        except Exception as e:
            print(f"读取文件 {dbf_file_path} 出错: {e}")
            return None

    year = 2000
    for dbf_file_path in dbf_file_paths:
        df = read_dbf_file(dbf_file_path)
        df['year'] = year
        year+=1
        if df is not None:
            all_data_frames.append(df)

    # 将所有DataFrame合并为一个
    merged_df = pd.concat(all_data_frames, ignore_index=True)

    # 将合并后的数据写入Excel文件
    try:
        merged_df.to_csv(output_excel_path, index=False)
        print(f"数据已成功写入 {output_excel_path}")
    except Exception as e:
        print(f"写入Excel文件出错: {e}")
def main():
    file_list = []
    file_name = 'G:\\绘图\\频次(0.9)\\表格数据\\'
    for name in os.listdir(file_name):
        if name.endswith('dbf'):
            detail_name = file_name+name
            file_list.append(detail_name)
    out_name = r'G:\绘图\频次(0.9)\表格.csv'
    merge_dbf_files_to_excel(file_list,out_name)
main()