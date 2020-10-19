import copy


class node1:  # 定义的节点信息其中包括父亲节点信息，当前节点信息，步数
    def __init__(self, father, now, step):
        self.father = father
        self.now = now
        self.step = step


xx = [1, 0, -1, 0]  # 可以移动的四个方向
yy = [0, 1, 0, -1]
start = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # 初始化初始状态
end = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # 初始化目标状态
open = []  # 初始化open、close
close = []


def Isdangerous(x, y):  # 危险位置判断
    if x >= 0 and x <= 2 and y >= 0 and y <= 2:
        return 1
    return 0


def fin(temp):  # 最终状态判断
    for i in range(3):
        for j in range(3):
            if temp[i][j] != end[i][j]:
                return 0
    return 1


def pd(temp1, temp2):  # temp1和temp2状态是否相同
    for i in range(3):
        for j in range(3):
            if temp1[i][j] != temp2[i][j]:
                return 0
    return 1


def cf(temp):  # 重复状态判断
    for item in open:
        if pd(item.now, temp) == 1:
            return 1
    for item in close:
        if pd(item.now, temp) == 1:
            return 1
    return 0


def gjhs(chess1, chess2):  # 估计函数进行判断这个状态与目标状态错位数字数量
    sum = 0
    for i in range(3):
        for j in range(3):
            if chess1[i][j] != chess2[i][j]:
                sum += 1
    return sum


def BFS():  # 进行BFS遍历
    x = 0
    y = 0
    zt = []
    while (len(open) != 0):
        zt = open[0].now
        bs = open[0].step
        if fin(zt) == 1:
            return
        for i in range(3):
            for j in range(3):
                if zt[i][j] == '0':
                    x, y = i, j

        for i in range(4):
            nx = x + xx[i]
            ny = y + yy[i]
            if Isdangerous(nx, ny) == 1:
                temp = copy.deepcopy(zt)  # 这里是深拷贝！！！
                arr = temp[x][y]
                temp[x][y] = temp[nx][ny]
                temp[nx][ny] = arr
                if cf(temp) == 0:
                    temp2 = node1(zt, temp, bs + 1)
                    open.append(temp2)

        open.remove(open[0])  # 移除open表里面的第一个元素
        for i in range(len(open)):  # 按照估计函数值大小进行排序
            f1 = gjhs(open[i].now, end)
            for j in range(i, len(open)):
                f2 = gjhs(open[j].now, end)
                if f1 > f2:
                    arr = open[i]
                    open[i] = open[j]
                    open[j] = arr
        close.append(open[0])  # 添加到close列表里面


def printf(chess):  # 用来输出测试
    for i in range(3):
        for j in range(3):
            print(chess[i][j], end=' ')
        print()


def nixushu(chess):  # 逆序数计算
    list = []
    sum = 0
    for i in range(3):
        for j in range(3):
            list.append(chess[i][j])
    for i in range(1, len(list)):
        if list[i] != '0':
            for j in range(0, i):
                if list[j] > list[i]:
                    sum += 1
    return sum


def jo(num):  # 奇数偶数判断
    if num % 2 == 0:
        return 1
    return 0


if __name__ == "__main__":  # 主函数

    print("请输入初始状态:")
    for i in range(3):
        line = input().split(' ')
        for j in range(3):
            start[i][j] = line[j]
    open.append(node1([], start, 0))
    print("请输入目标状态:")
    for i in range(3):
        line1 = input().split(' ')
        for j in range(3):
            end[i][j] = line1[j]
    if jo(nixushu(start)) == jo(nixushu(end)):
        BFS()
        lj = []
        lj.append(close[-1].now)
        father = close[-1].father
        while True:
            if pd(father, start) == 1:
                lj.append(father)
                break
            else:
                for item in close:
                    if pd(father, item.now) == 1:
                        lj.append(father)
                        father = item.father
        sum = 0
        print("找到的解路径")
        for i in range(-1, -len(lj) - 1, -1):
            printf(lj[i])
            print()
            sum += 1
    else:
        print("找不到一个路径！")
