import numpy as np
import h5py, os
import rasterio

def create_geotiff_from_template(template_tif, matrix_data, output_tif,data_type="float32"):
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
def merge(year):
    with rasterio.open(f'F:\\涝渍的频次和强度（二季早稻）\\{year}\\频次(0.9).tif') as WF1_tif:
        WF1 = WF1_tif.read(1)
    with rasterio.open(f'F:\\涝渍的频次和强度（二季晚稻）\\{year}\\频次(0.9).tif') as WF2_tif:
        WF2 = WF2_tif.read(1)
    with rasterio.open(f'F:\\涝渍的频次和强度（二季早稻）\\{year}\\持续天数(0.9).tif') as WD1_tif:
        WD1 = WD1_tif.read(1)
    with rasterio.open(f'F:\\涝渍的频次和强度（二季晚稻）\\{year}\\持续天数(0.9).tif') as WD2_tif:
        WD2 = WD2_tif.read(1)
    with rasterio.open(f'F:\\涝渍的频次和强度（二季早稻）\\{year}\\平均相对含水量.tif') as AWC1_tif:
        AWC1 = AWC1_tif.read(1)
    with rasterio.open(f'F:\\涝渍的频次和强度（二季晚稻）\\{year}\\平均相对含水量.tif') as AWC2_tif:
        AWC2 = AWC2_tif.read(1)
    WF=WF1+WF2
    WD=WD1+WD2
    AWC=(AWC1+AWC2)/2
    create_geotiff_from_template("Image_projection_example.tif",WF,
                                 f"F:\\涝渍的频次和强度（二季稻）\\{year}\\频次(0.9).tif",
                                 'uint8')
    create_geotiff_from_template("Image_projection_example.tif",WD,
                                 f"F:\\涝渍的频次和强度（二季稻）\\{year}\\持续天数(0.9).tif",
                                 'uint8')
    create_geotiff_from_template("Image_projection_example.tif",AWC,
                                 f"F:\\涝渍的频次和强度（二季稻）\\{year}\\平均相对含水量.tif",
                                 'float32')
def main():
    for year in range(2003,2024):
        merge(year)
main()