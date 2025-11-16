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
def get_name(year,day):
    name = f'G:\\新的土壤含水量2003-2023tif\\{str(year)}\\'+'new_{:0>3}.tif'.format(day)
    return name
def get_list(year):
    ls = []
    start = 244
    end = 334 #334
    if year%4==0:
        start+=1
        end+=1
    for day in range(start,end):
        ls.append(get_name(year,day))
    return ls
def process_year(year,threshold):
    with rasterio.open('FC.tif') as FC_tif:
        FC_data = FC_tif.read(1)
    shape = (3903, 6417)
    days = np.zeros(shape)
    days_real = np.zeros(shape)
    days_simu = np.zeros(shape)
    days_ave = np.zeros(shape=shape ,dtype=np.float32)
    day_bool = np.full(shape,False,dtype=bool)
    for file_name in get_list(year):
        try:
            with rasterio.open(file_name) as file:
                data = file.read(1)
            print(f'正在计算文件{file_name}')
            day_bool = np.where( (data / (FC_data * 10) > threshold), True, False)
            days_simu = np.where(day_bool,days_simu+1,0)
            days_real = np.where(days_simu>days_real,days_simu,days_real)
            days = np.where(day_bool,days+1,days)
            days_ave += data
        except:
            days_real = np.where(days_real>days_simu , days_real , days_simu)
    days_ave = np.where(days>0,days_ave/(len(get_list(year))*FC_data*10),0)
    create_geotiff_from_template("Image_projection_example.tif",days,
                                 f"F:\\涝渍的频次和强度（二季晚稻）\\{year}\\频次({threshold}).tif",
                                 'uint8')
    create_geotiff_from_template("Image_projection_example.tif", days_real,
                                 f"F:\\涝渍的频次和强度（二季晚稻）\\{year}\\持续天数({threshold}).tif",
                                 'uint8')
    create_geotiff_from_template("Image_projection_example.tif", days_ave,
                                 f"F:\\涝渍的频次和强度（二季晚稻）\\{year}\\平均相对含水量.tif",
                                 'float32')
def main():
    for year in range(2003,2024):
        process_year(year,0.9)
if __name__ == '__main__':
    main()