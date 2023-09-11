import os

if __name__ == '__main__':
    dir_path = '/Users/shur/Downloads/mit/'
    for file_name in os.listdir(dir_path):
        new_file_name = file_name.split('_', 1)[1]
        os.rename(dir_path + file_name, dir_path + new_file_name)
