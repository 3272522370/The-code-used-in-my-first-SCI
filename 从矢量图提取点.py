import geopandas as gpd
import pandas as pd
import rasterio
import numpy as np


def extract_points_and_values(vector_path, tif_path):
    pass

def count_ones_in_shp(shp_path, tif_path):
    """
    计算 shp 文件范围内 tif 文件中值为 1 的点的数量。

    参数:
    shp_path (str): shp 文件的路径。
    tif_path (str): tif 文件的路径。

    返回:
    int: shp 文件范围内 tif 文件中值为 1 的点的数量。
    """
    try:
        # 读取 shp 文件
        shp_df = gpd.read_file(shp_path)
        # 读取 tif 文件
        with rasterio.open(tif_path) as src:
            tif_crs = src.crs
        # 将 shp 文件的几何对象转换为 tif 文件的 CRS
        shp_df = shp_df.to_crs(tif_crs)
        # 假设 shp 文件只有一个几何对象，取第一个
        geometry = shp_df.geometry[0]
        with rasterio.open(tif_path) as src:
            # 获取 tif 文件的 transform 和形状
            transform = src.transform
            rows, cols = src.shape
            # 生成网格点
            minx, miny, maxx, maxy = geometry.bounds
            window = src.window(minx, miny, maxx, maxy)
            window_transform = src.window_transform(window)
            window_shape = (int(window.height), int(window.width))
            # 读取窗口内的数据
            data = src.read(1, window=window)
            # 将数据转换为 numpy 数组
            data_array = np.array(data)
            # 计算窗口内值为 1 的点的数量
            count = np.sum(data_array == 1)
            return count
    except Exception as e:
        print(f"出现错误: {e}")
        return 0


def main():
    # 示例调用
    vector_path = r'G:\华北.shp'  # 范围图文件路径，使用原始字符串
    tif_paths = [
        r'G:\干旱的频次与强度\2000\频次(0.6).tif',
        r'G:\频次和强度\2000\2000(0.9).tif',
        r'G:\NPP\NPP_500m_Year_2000_mask.tif',
        r'G:\玉米\CCD_Maize_China_2000_500m.tif'
    ]
    xlsx_path = '2000旱涝和玉米数据.xlsx'  # 输出文件路径
    # extract_points_and_values(vector_path, tif_paths, xlsx_path)

    print(count_ones_in_shp(vector_path,r'G:\玉米\CCD_Maize_China_2000_500m.tif'))

if __name__ == "__main__":
    main()