import os
import shutil

source_directory = os.path.expanduser("~/Downloads/6.046j-spring-2015/static_resources")
target_directory = os.path.expanduser("~/Downloads/6.046")


def rename():
    # 确保目标目录存在
    os.makedirs(target_directory, exist_ok=True)

    # 遍历源目录中的文件
    for filename in os.listdir(source_directory):
        if "MIT6_046" in filename and filename.endswith(".pdf"):
            # 找到 "MIT6_046" 在文件名中的位置
            index = filename.index("MIT6_046")

            # 构建新的文件名
            new_filename = filename[index + len("MIT6_046"):]

            # 构建源文件和目标文件的路径
            source_path = os.path.join(source_directory, filename)
            target_path = os.path.join(target_directory, new_filename)

            # 复制文件到目标目录
            shutil.copy(source_path, target_path)

    print("Files copied to", target_directory)


def move_to_folder():
    types = ["recitation", "pset", "lec", "quiz"]
    for t in types:
        os.makedirs(os.path.join(target_directory, t), exist_ok=True)
        for filename in os.listdir(target_directory):
            if t in filename.lower():
                source_path = os.path.join(target_directory, filename)
                if os.path.isdir(source_path):
                    continue
                target_path = os.path.join(target_directory, t, filename)
                shutil.move(source_path, target_path)


if __name__ == '__main__':
    # rename()
    move_to_folder()
