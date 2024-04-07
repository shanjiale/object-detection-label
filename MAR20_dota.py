import os
import shutil


def move_files(source_dir, target_dir, file_names_file):
    # 检查源文件夹是否存在
    if not os.path.exists(source_dir):
        print(f"源文件夹 '{source_dir}' 不存在")
        return

    # 检查目标文件夹是否存在，若不存在则创建
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 打开文件名列表文件
    with open(file_names_file, 'r') as file:
        # 逐行读取文件名列表
        for filename in file:
            # 去除行末的换行符
            filename = filename.strip()+'.txt'
            source_file_path = os.path.join(source_dir, filename)
            # 检查源文件是否存在
            if os.path.exists(source_file_path):
                target_file_path = os.path.join(target_dir, filename)
                # 移动文件
                shutil.move(source_file_path, target_file_path)
                print(f"文件 '{filename}' 移动成功")
            else:
                print(f"文件 '{filename}' 不存在于源文件夹中")


# 指定源文件夹路径、目标文件夹路径和保存文件名的txt文件路径
source_directory = "H:\\飞机数据\\MAR20\\Annotations\\annfiles"
target_directory = "H:\\飞机数据\\MAR20\\Annotations\\1"
file_names_txt_file = "H:\\飞机数据\\MAR20\\ImageSets\\ImageSets\\Main\\test.txt"

# 调用函数移动文件
move_files(source_directory, target_directory, file_names_txt_file)
