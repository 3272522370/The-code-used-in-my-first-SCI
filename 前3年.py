import os
import rasterio
import numpy as np

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

    print(f"\n成功生成 GeoTIFF 文件: {output_tif}",end='')

def process(file_list):
    with rasterio.open('FC.tif') as file:
        FC = file.read(1)
    shape = (3903, 6417)
    days1,days2,lon_days1,lon_days2= np.zeros(shape),np.zeros(shape),np.zeros(shape),np.zeros(shape)
    #生成缓存矩阵
    day_bool1 = np.full(shape=shape,fill_value=False,dtype=bool)
    day_bool2 = np.full(shape=shape,fill_value=False,dtype=bool)
    lon1,lon2 = np.zeros(shape),np.zeros(shape)
    for file_name in file_list:
        print(f'\r正在处理文件{file_name}',end='')
        with rasterio.open(file_name) as file:
            data = file.read(1)
        #两个阈值
        day_bool1 = np.where(data/(FC*10)>0.9,True,False)
        day_bool2 = np.where(data/(FC*10)>=1,True,False)
        #处理频次
        days1 = np.where(day_bool1,days1+1,days1)
        days2 = np.where(day_bool2,days2+1,days2)
        #处理最长天数
        lon1 = np.where(day_bool1,lon1+1,0)
        lon2 = np.where(day_bool2,lon2+1,0)
        lon_days1 = np.where(lon_days1>lon1,lon_days1,lon1)
        lon_days2 = np.where(lon_days2>lon2,lon_days2,lon2)
    return days1,days2,lon_days1,lon_days2

def main():
    for year in range(2000,2003):
        StrName = f'G:\\新的土壤含水量2003-2023tif\\{str(year)}'
        file_list = [os.path.join(StrName, filename) for filename in os.listdir(StrName) if filename.endswith('.tif')]
        days1,days2,lon_days1,lon_days2 = process(file_list[0:5])
        OutName = f'G:\\相对含水量频次\\{str(year)}\\{str(year)}'
        create_geotiff_from_template('Image_projection_example.tif',days1,OutName+'(0.9).tif')
        create_geotiff_from_template('Image_projection_example.tif',days2,OutName+'(1).tif')
        create_geotiff_from_template('Image_projection_example.tif',lon_days1,OutName+'最长天数(0.9).tif')
        create_geotiff_from_template('Image_projection_example.tif',lon_days2,OutName+'最长天数(1).tif')
if __name__ == '__main__':
    main()