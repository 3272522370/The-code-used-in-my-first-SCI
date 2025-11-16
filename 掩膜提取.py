import rasterio
import geopandas as gpd
import numpy as np
import pandas as pd

def extract_values_from_tifs(grid_path, tif_paths):
    """
    提取渔网点的每个 TIF 文件对应值，返回一个二维数组。

    参数：
    - grid_path: 渔网文件的路径（shapefile）。
    - tif_paths: 包含 TIF 文件路径的列表（每个 TIF 文件应为单波段）。

    返回：
    - 一个二维 numpy 数组，每行表示一个渔网点，每列表示对应 TIF 文件的值。
    """
    # 读取渔网文件
    grid = gpd.read_file(grid_path)
    if grid.geometry.is_empty.any():
        raise ValueError("渔网文件中存在空几何对象！")
    if grid.crs is None:
        raise ValueError("渔网文件缺少 CRS 定义！")

    # 存储每个 TIF 文件提取的值
    all_values = []

    for tif_path in tif_paths:
        with rasterio.open(tif_path) as src:
            if src.count != 1:
                raise ValueError(f"TIF 文件 {tif_path} 不是单波段！")
            if src.crs != grid.crs:
                print(f"正在对齐 {tif_path} 的 CRS 到渔网文件 CRS...")
                grid = grid.to_crs(src.crs)

            # 将渔网点的几何转换为像素坐标
            point_coords = [(geom.x, geom.y) for geom in grid.geometry]
            pixel_coords = [src.index(x, y) for x, y in point_coords]

            # 提取像素值
            tif_data = src.read(1)  # 读取第一波段
            values = [
                tif_data[row, col] if 0 <= row < tif_data.shape[0] and 0 <= col < tif_data.shape[1] else np.nan
                for row, col in pixel_coords
            ]
            all_values.append(values)

    # 转换为 numpy 数组并返回
    return np.array(all_values).T

def save_df_to_excel(df, file_path, sheet_name='Sheet1', index=False, header=False):
    """
    将 DataFrame 存储到指定的 Excel 文件。

    参数:
    df (pandas.DataFrame): 要存储的 DataFrame。
    file_path (str): Excel 文件的路径。
    sheet_name (str): 工作表名称，默认为 'Sheet1'。
    index (bool): 是否包含索引，默认为 False。
    header (bool): 是否包含列标题，默认为 True。
    """
    try:
        df.to_excel(file_path, sheet_name=sheet_name, index=index, header=header)
        print(f"DataFrame 已成功存储到 {file_path} 的 {sheet_name} 工作表中。")
    except Exception as e:
        print(f"存储 DataFrame 时出错: {e}")

def process(year):
    '''玉米期与水稻期的NPP属于同一个时间段'''
    tif_files = [
        f"F:\\涝渍的频次和强度（二季晚稻）\\{year}\\持续天数(0.9).tif",
        f"F:\\涝渍的频次和强度（二季晚稻）\\{year}\\频次(0.9).tif",
        f"F:\\涝渍的频次和强度（二季晚稻）\\{year}\\平均相对含水量.tif",
        f"F:\\NPP（二季晚稻）\\{year}\\总NPP.tif",
        # f"G:\\NPP\\annual\\NPP_500m_Year_{year}_mask.tif",
        # f"G:\\玉米\\CCD_Maize_China_{year}_500m.tif",
        f"F:\\水稻\\CCD_Rice_China_{year}_500m.tif"
    ]
    net_file = 'F:\\区域与渔网\\华南的点2.shp'
    result_matrix = extract_values_from_tifs(net_file, tif_files)
    # 将结果矩阵转换为 DataFrame
    df = pd.DataFrame(result_matrix)
    save_df_to_excel(df,f"F:\\水稻和涝渍的关系\\华南（二季晚稻）\\涝渍数据\\{year}涝渍(0.9).xlsx",str(year))
def main():
    for year in range(2003,2024):
        process(year)
if __name__ == "__main__":
    main()