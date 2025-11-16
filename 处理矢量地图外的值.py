import rasterio
import geopandas as gpd
from rasterio.mask import mask
import numpy as np
import os

def mask_raster_with_vector(raster_path, vector_path, output_path, fill_value=None):
    # 读取矢量地图
    vector_data = gpd.read_file(vector_path)

    # 如果矢量数据没有 CRS，设置一个默认的 CRS（根据实际情况选择合适的 CRS）
    if vector_data.crs is None:
        vector_data.set_crs('EPSG:4326', allow_override=True, inplace=True)

    with rasterio.open(raster_path) as src:
        # 确保矢量数据与栅格数据在同一空间参考系
        # 获取栅格数据的 CRS
        raster_crs = src.crs
        # 将矢量数据转换为与栅格数据相同的 CRS
        vector_data = vector_data.to_crs(raster_crs)

        # 掩膜栅格数据
        out_image, out_transform = mask(src, vector_data.geometry, crop=False)

        # 对于单波段和多波段栅格数据进行处理
        if src.count == 1:
            out_image = out_image[0, :, :]
        else:
            out_image = np.array(out_image)

        # 输出掩膜后的图像最小值和最大值进行调试
        # print("掩膜后的图像最小值：", out_image.min())
        # print("掩膜后的图像最大值：", out_image.max())

        # 将掩膜范围外的值设置为指定的填充值
        if src.nodata is None:
            out_image[out_image == 0] = fill_value
        else:
            out_image[out_image == src.nodata] = fill_value

        # 更新元数据
        out_meta = src.meta.copy()
        out_meta.update({"nodata": fill_value})

    # 写入新的 tif 文件
    with rasterio.open(output_path, 'w', **out_meta) as dest:
        dest.write(out_image, 1)

    # print(f"处理后的栅格文件已保存到: {output_path}")
    #
    # print("矢量数据边界:", vector_data.total_bounds)
    # with rasterio.open(raster_path) as src:
    #     print("栅格数据边界:", src.bounds)
def create_geotiff_from_template(template_tif, matrix_data, output_tif):
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
            dtype='float32',
            crs=crs,
            transform=transform) as dst:
        dst.write(matrix_data, 1)

    print(f"\r成功生成 GeoTIFF 文件: {output_tif}", end='')
# 读取栅格数据
def change_tif(tif_name):
    with rasterio.open(tif_name) as src:
        # 读取矢量数据
        vector_data = gpd.read_file(r"vector\CN-sheng-A.shp")

        # 获取栅格数据的 CRS
        raster_crs = src.crs

        # 确保矢量数据与栅格数据的 CRS 一致
        if vector_data.crs != raster_crs:
            vector_data = vector_data.to_crs(raster_crs)

        # 获取矢量图的几何形状
        geometries = vector_data.geometry

        # 使用 mask 函数提取矢量图范围内的栅格数据，但不裁剪栅格图像
        out_image, out_transform = mask(src, geometries, crop=False, nodata=np.nan, filled=True)  # crop=False 表示不裁剪

    create_geotiff_from_template('Image_projection_example.tif', out_image[0], tif_name)
def process(tif_name):
    if tif_name[-8]=='_':
        return
    print('\r正在处理文件{}'.format(tif_name),end='')
    change_tif(tif_name)
    new_name = tif_name[:-7]+'new_'+tif_name[-7:]
    os.rename(tif_name,new_name)
    print('\r已经成功生成文件{}'.format(new_name),end='')
def main():
    for year in range(2003, 2024):
        StrName = 'G:\\新的土壤含水量2003-2023tif\\' + str(year)
        file_list = [os.path.join(StrName, filename) for filename in os.listdir(StrName) if filename.endswith('.tif')]
        for file_name in file_list:
            process(file_name)
main()