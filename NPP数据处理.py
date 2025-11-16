import os
import rasterio
import numpy as np

def create_folder(folder_path):
    """
    此函数用于创建一个文件夹
    :param folder_path: 要创建的文件夹的路径
    """
    try:
        os.makedirs(folder_path)
        print(f"文件夹 {folder_path} 已成功创建")
    except FileExistsError:
        print(f"文件夹 {folder_path} 已经存在")
    except Exception as e:
        print(f"创建文件夹 {folder_path} 时出错: {e}")

def list_tif_files_in_folder(folder_path):
    """
    此函数用于打开一个文件夹，并将其中后缀为.tif 的文件的绝对路径存储在列表中
    :param folder_path: 要打开的文件夹的路径
    :return: 存储后缀为.tif 文件的绝对路径的列表，如果文件夹不存在或者无法访问则返回空列表
    """
    file_paths = []
    try:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.tif'):
                    file_paths.append(os.path.abspath(os.path.join(root, file)))
    except Exception as e:
        print(f"访问文件夹 {folder_path} 时出现错误: {e}")
    return file_paths

def split_year_list():
    List = list_tif_files_in_folder("F:\\NPP\\8d")
    Dict={}
    index=0
    for year in range(2000,2024):
        Dict[year]=[]
        while index<len(List) and str(year)==List[index][-14:-10]:
            Dict[year].append(List[index])
            index+=1
    return Dict

def create_geotiff_from_template(template_tif, matrix_data, output_tif,data_type):
    with rasterio.open(template_tif) as src:
        transform = src.transform
        crs = src.crs
        height = src.height
        width = src.width

    # 检查矩阵大小是否和模板匹配
    if matrix_data.shape != (height, width):
        raise ValueError(f"矩阵尺寸 {matrix_data.shape} 与模板 TIFF 尺寸 {(height, width)} 不匹配")

    # 创建新的 GeoTIFF 文件
    with rasterio.open(
            output_tif, 'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,
            dtype=data_type,
            crs=crs,
            transform=transform) as dst:
        dst.write(matrix_data, 1)

    print(f"\n成功生成 GeoTIFF 文件: {output_tif}",end='')

def calculate(List,address):
    shape=(10510,9666)
    mean_NPP=np.full(shape,0,dtype=np.float32)
    for file in List:
        with rasterio.open(file) as fl:
            data = fl.read(1)
        print(f"正在计算{file}文件")
        mean_NPP = mean_NPP + data
    create_geotiff_from_template("NPP_example.tif",mean_NPP,f"{address}\\总NPP.tif","float32")
def exclude_other_days(List):#去除玉米期以外的天
    start = 0
    end = 0
    for i in range(len(List)):
        month = int(List[i][-9:-7])
        day = int(List[i][-6:-4])
        if start == 0:
            if 7<=month<=11:#############决定时间段
                start = i
        else:
            if month>11 and end==0:#############决定时间段
                end = i
                break
    return List[start:end]
def main():
    Dict = split_year_list()
    for year in Dict:
        Dict[year]=exclude_other_days(Dict[year])
        print(Dict[year])
    for year in range(2003,2024):
        address=f'F:\\NPP（二季晚稻）\\{year}'
        calculate(Dict[year],address)
main()