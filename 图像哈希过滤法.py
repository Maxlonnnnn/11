import os
import imagehash
from PIL import Image
from collections import defaultdict
from tqdm import tqdm  # 进度条库

# 忽略 PIL 的解压炸弹警告
Image.MAX_IMAGE_PIXELS = None


def find_similar_images(directory, threshold=10, max_image_size=100 * 1024 * 1024):
    """
    查找并删除相似的图片（包括子目录）。
    :param directory: 包含图片的根目录路径
    :param threshold: 相似度阈值，值越小，要求越严格
    :param max_image_size: 最大允许处理的图片文件大小（字节），默认为100MB
    """
    # 存储图像哈希值和文件路径的字典
    hashes = defaultdict(list)

    # 收集所有待处理的图像文件路径
    image_files = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                image_files.append(os.path.join(root, filename))

    # 使用进度条显示处理进度
    for path in tqdm(image_files, desc="Processing images"):
        try:
            # 检查文件大小
            if os.path.getsize(path) > max_image_size:
                print(f"Skipping large image: {path}")
                continue

            with Image.open(path) as img:
                # 计算图像的感知哈希值
                hash_value = imagehash.phash(img)
                hashes[hash_value].append(path)
        except (OSError, ValueError) as e:
            print(f"Error processing file {path}: {e}")

    # 删除相似的图片
    for hash_value, files in hashes.items():
        if len(files) > 1:
            for i in range(1, len(files)):
                os.remove(files[i])  # 删除除了第一个文件之外的所有文件
                print(f"Deleted similar image: {files[i]}")


# 请求用户输入目录地址
directory_path = input("请输入包含图片的目录路径：")
find_similar_images(directory_path)
