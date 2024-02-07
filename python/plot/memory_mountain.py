import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

# memory mountain 数据结果生成脚本 https://csapp.cs.cmu.edu/3e/students.html
if __name__ == '__main__':

    # 读取结果文件
    df = pd.read_csv('result.txt', sep=' ', index_col=0, skiprows=2)

    # 设置 x y z 轴的值
    X = df.columns.astype(str)  # stride
    Y = df.index.astype(str)  # size
    x, y = np.meshgrid(np.arange(len(X)), np.arange(len(Y)))
    z = df.values.astype(float)

    # 绘制平面图
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z, cmap='rainbow')

    # 设置坐标轴的标签
    ax.set_xlabel('stride(x8 bytes)')
    ax.set_ylabel('size(bytes)')
    ax.set_zlabel('read throughout(MB/s)')

    # 设置图片标题
    cpu = 'Intel i7-13700'
    ax.set_title(f'memory mountain\n {cpu}')

    # 设置坐标轴刻度的标签
    plt.xticks(range(len(X)), X)
    plt.yticks(range(len(Y)), Y)

    # # 缩放坐标轴刻度
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(4))
    # ax.yaxis.set_major_locator(ticker.MultipleLocator(2))

    # # 保存图片
    # plt.savefig('my_mountain.jpg')

    # 显示图片
    plt.show()
