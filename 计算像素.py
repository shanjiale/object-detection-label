import os


def calculate_rectangle_area(x1, y1, x2, y2, x3, y3, x4, y4):
    # 计算矩形的边长
    width1 = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    width2 = ((x4 - x3) ** 2 + (y4 - y3) ** 2) ** 0.5
    height1 = ((x1 - x3) ** 2 + (y1 - y3) ** 2) ** 0.5
    height2 = ((x2 - x4) ** 2 + (y2 - y4) ** 2) ** 0.5

    # 取长和宽的最大值作为矩形的边长
    width = max(width1, width2)
    height = max(height1, height2)

    # 计算面积
    area = width * height
    return width


# def process_txt_file(file_path):
#     total_rectangles = 0
#     rectangles_less_than_50 = 0
#     rectangles_mid=0
#     rectangles_large=0
#     with open(file_path, 'r') as file:
#         for line in file:
#             # 解析每行数据，假设每行数据以空格分隔
#             values = line.strip().split()
#             if len(values) >= 8:
#                 x1, y1 = map(float, values[:2])
#                 x2, y2 = map(float, values[2:4])
#                 x3, y3 = map(float, values[4:6])
#                 x4, y4 = map(float, values[6:8])
#
#                 # 计算矩形面积
#                 rectangle_area, bi = calculate_rectangle_area(x1, y1, x2, y2, x3, y3, x4, y4)
#                 total_rectangles += 1
#
#                 # 统计面积小于50的矩形个数
#                 if 100<rectangle_area < 2500:
#                     rectangles_less_than_50 += 1
#                 if 2500<rectangle_area<90000:
#                     rectangles_mid+=1
#                 else:
#                     rectangles_large=+1
#
#     return total_rectangles, rectangles_less_than_50,rectangles_large,rectangles_mid

def process_txt_file(file_path):
    small = 0
    mid = 0
    large = 0
    total_rectangles=0
    with open(file_path, 'r') as file:
        for line in file:
            # 解析每行数据，假设每行数据以空格分隔
            values = line.strip().split()
            if len(values) >= 8:
                x1, y1 = map(float, values[:2])
                x2, y2 = map(float, values[2:4])
                x3, y3 = map(float, values[4:6])
                x4, y4 = map(float, values[6:8])

                # 计算矩形面积
                width = calculate_rectangle_area(x1, y1, x2, y2, x3, y3, x4, y4)
                total_rectangles += 1

                # 统计面积小于50的矩形个数
                if 10<width < 50:
                    small += 1
                if 50<width<300:
                   mid+=1
                else:
                    large=+1

    return total_rectangles, small,mid,large

def process_folder(folder_path):
    total_rectangles_files=0
    small_files=0
    mid_files=0
    large_files=0

    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            print("处理文件:", file_path)
            total_rectangles, small,mid,large = process_txt_file(file_path)
            total_rectangles_files += total_rectangles
            small_files+=small
            mid_files+=mid
            large_files+=large
    print("总共的矩形个数:", total_rectangles_files)
    print("面积小的矩形个数:", small_files)
    print("面积中间的矩形个数:", mid_files)
    print("面积大的矩形个数:", large_files)


# 文件夹路径
folder_path = r'H:\myself_data\成对数据\船舶\label\txt_label'

# 处理文件夹中的所有txt文件
process_folder(folder_path)
