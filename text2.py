import rasterio
import numpy as np
# 打开.tif文件
with rasterio.open(r'G:\洪涝的频次和强度（全年）\2003\平均相对含水量.tif') as src:
    # 获取文件的元数据
    print(src.meta)

    # 读取整个影像数据
    data = src.read()
    print(type(data[0][0][0]))
    print(data.shape)
    # 查询影像的尺寸
    print(src.width)
    print(src.height)

    # 查询影像的坐标系统
    print(src.crs)

def check_size():
    """
    此函数用于检查 numpy.float32 的大小
    """
    size_in_bytes = np.dtype(np.float32).itemsize
    print(f"numpy.float32 的大小为: {size_in_bytes} 字节")

