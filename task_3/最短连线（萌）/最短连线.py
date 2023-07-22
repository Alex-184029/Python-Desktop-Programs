# 开发者：赤色漫步
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
import random
import math
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams["font.family"]="SimHei"  #全局修改使得标题可以用中文

# 初始化坐标数组
X = []
Y = []

# 存放距离的数组
L = []

# 存放坐标角标的数组
m = []
n = []

# 设置一个数组，存放最关键的东西，就是连线的坐标的顺序！！！！！！！！！
ShunXu = []

# 暂时存放一段坐标序列，一会要记得导入ShunXu这个给列表
K = []

# 最小值mini
mini = 0

# 存放最终的顺序！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
ZuiZhongShunXu= []

# 存放长度和的列表
changduheliebiao = []

# 先产生两个坐标的数组
XShunXu = []
YShunXu = []

class chuangkou:

    def __init__(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load("最短连线.ui")               # ui为变量名

        # 以下两个函数可以加入一定数量的点
        self.ui.button1.clicked.connect(self.handle1)         # 逐个加入
        self.ui.button2.clicked.connect(self.handle2)         # 一键加入

        # 清除已有坐标
        self.ui.button3.clicked.connect(self.clearXY)         # 清除已有坐标

        # 显示已有坐标
        self.ui.button4.clicked.connect(self.look)         # 显示已有坐标

        # 生成连线函数
        self.ui.button.clicked.connect(self.handle)

    # 逐个加入
    def handle1(self):
        # 从用户界面读取生成的图形的长宽值
        self.a = self.ui.Box1.value()
        self.b = self.ui.Box2.value()

        # 从用户界面读取生成的坐标的个数
        self.sum = self.ui.Box3.value()

        # 从用户界面读取坐标的数值
        self.x = self.ui.Box4.value()
        self.y = self.ui.Box5.value()

        # 以下为检验程序：
        # 先检验满了没有
        if (len(X) == self.sum):
            self.ui.Edit1.setPlainText("坐标已满，请勿再添加！！！")
            return
        # 再检验是否横坐标在[0，a],纵坐标在[0，b]
        if (self.x > self.a or self.x < 0 or self.y > self.b or self.y < 0):
            self.ui.Edit1.setPlainText("该坐标未在规定方格内，请重新选择坐标！！！")
        # 若该数未存在则加入，反之报错
        i = 0
        while (i < len(X)):
            if (self.x == X[i] and self.y == Y[i]):
                self.ui.Edit1.setPlainText("该坐标已有，请重新选择坐标！！！")
                return
            i = i + 1
        X.append(self.x)
        Y.append(self.y)

        # 显示已有坐标：
        # 先检验坐标是否对等
        if (len(X) != len(Y)):
            self.ui.Edit1.setPlainText("横坐标和纵坐标数量不一样，请立即清楚所有坐标！！！")
            return

        # 然后显示已有坐标
        self.look()

    # 一键加入
    def handle2(self):
        # 从用户界面读取生成的图形的长宽值
        self.a = self.ui.Box1.value()
        self.b = self.ui.Box2.value()

        # 从用户界面读取生成的坐标的个数
        self.sum = self.ui.Box3.value()

        # 先加入：
        # 不满足数量时循环
        while(len(X) < self.sum):
            # 调用加入坐标的函数
            self.handleJiaRu()

        # 再显示已有坐标:
        # 先检验坐标是否对等
        if (len(X) != len(Y)):
            self.ui.Edit1.setPlainText("横坐标和纵坐标数量不一样，请立即清楚所有坐标！！！")

        # 然后显示已有坐标
        self.look()

    # 清除X，Y坐标的函数
    def clearXY(self):
        X.clear()
        Y.clear()
        self.look()

    # 显示X，Y坐标的函数
    def look(self):
        # 然后显示已有坐标
        i = 0
        self.ui.Edit1.setPlainText("已有坐标为：")
        while (i < len(X)):
            self.ui.Edit1.appendPlainText("（{0}，{1}）".format(X[i], Y[i]))
            i = i + 1

    # 一个将生成的数检验是否存在然后再加入到X，Y中去的函数
    def handleJiaRu(self):
        # 将随机生成的数检验是否存在然后再加入到X，Y中去
        x = random.randrange(self.a + 1)
        y = random.randrange(self.b + 1)
        # 以下为检验程序
        # 检验是否重复
        i = 0
        while (i < len(X)):
            if (x == X[i] and y == Y[i]):
                self.handleJiaRu()
                return
            i = i + 1
        X.append(x)
        Y.append(y)

    # 实现计算距离的功能，将距离保存在L列表，距离对应的两个点，一个点在m列表，一个点在n列表
    def suanjuli(self):
        L.clear()
        m.clear()
        n.clear()
        xuanze = self.ui.comboBox.currentText()
        if (xuanze == "直线"):
            i = 0
            while (i < len(X)):
                j = 0
                while (j < len(X)):
                    if (i != j):
                        r = math.sqrt((X[i] - X[j]) ** 2 + (Y[i] - Y[j]) ** 2)
                        L.append(r)
                        m.append(i)
                        n.append(j)
                        j = j + 1
                    else:
                        j = j + 1
                i = i + 1
            print("M为：{0}".format(m))
            print("N为：{0}".format(n))
        elif (xuanze == "折线"):
            i = 0
            while (i < len(X)):
                j = 0
                while (j < len(Y)):
                    if (i != j):
                        r = math.fabs(X[i] - X[j]) + math.fabs(Y[i] - Y[j])
                        L.append(r)
                        m.append(i)
                        n.append(j)
                        j = j + 1
                    else:
                        j = j + 1
                i = i + 1

    # 判断并删去长度较大的坐标顺序
    def judge(self):
        changduheliebiao.clear()
        ZuiZhongShunXu.clear()
        # 循环，每len（X）一组，然后加上距离，求和
        i = 0
        while (i < (len(ShunXu) / len(X))):
            he = 0
            # 现在对角标为j的ShunXu列表进行求距离和
            j = i * len(X)
            while (j < ((i + 1) * len(X) - 1)):
                # 循环，找出m，n中与ShunXu这个列表匹配的k，然后在L列表里面得到距离，加到he上
                k = 0
                while (k < len(m)):
                    if (m[k] == ShunXu[j] and n[k] == ShunXu[j + 1]):
                        he = he + L[k]
                    k = k + 1
                j = j + 1
            changduheliebiao.append(he)
            i = i + 1
        print("长度和的列表为：{0}".format(changduheliebiao))
        # 找最小值
        mini = min(changduheliebiao)
        print("MINI为：{0}".format(mini))
        # 循环，当不是最小值的时候不要，其余的加入新的列表，我叫他最终的顺序！！！！！！
        i = 0
        while (i < len(changduheliebiao)):
            if (changduheliebiao[i] == mini):
                # 开始赋值
                j = i * len(X)
                while (j < (i + 1) * len(X)):
                    ZuiZhongShunXu.append(ShunXu[j])
                    j = j + 1
            i = i + 1
        print("最终顺序为：{0}".format(ZuiZhongShunXu))

    # 算出最短路径的主函数
    def Calculate(self):
        print("开始计算最短路径")
        # 首先搞一个循环，从0到sum-2,sum为坐标点的个数
        i = 0
        while (i < len(X)):
            print("计算以{0}开头的连线".format(i))
            # 清空状态
            S = []
            K.clear()
            K.append(i)
            # 先把为i的坐标和其他坐标的距离找出来，存放到S里面
            j = 0
            print("M为：{0}".format(m))
            while (j < len(m)):
                if (m[j] == i):
                    S.append(L[j])
                j = j + 1
            print("S为：{0}".format(S))
            # 找出S里面的最小值，记作mini
            mini = min(S)
            print("MINI为：{0}".format(mini))
            # 再循环，先找出为i的坐标，然后再看是不是最小距离
            j = 0
            while (j < len(m)):
                # 先找到为i的坐标
                if (m[j] == i):
                    # 再看是不是最小距离
                    if (L[j] == mini):
                        K.append(n[j])
                        print("K为：{0}".format(K))
                        self.Cal(n[j])
                        K.remove(n[j])
                j = j + 1
            i = i + 1

    # 算出最短路径的副函数
    def Cal(self,x):
        print("开始副函数")
        # 先判断暂存的一个序列是否够数了，不够就继续算
        if (len(K) < len(X)):
            print("不够数，可以开始算了")
            # 清空状态
            S = []
            # 先把为x的坐标和其他坐标的距离找出来，存放到S里面。注意，要去掉已有的坐标的距离！！！！！
            j = 0
            while (j < len(m)):
                # 先找到为i的坐标
                if (m[j] == x):
                    # 再看和以前的点重复了没有
                    if (n[j] not in K):
                        S.append(L[j])
                j = j + 1
            print("S为：{0}".format(S))
            # 找出S里面的最小值，记作mini
            mini = min(S)
            print("MINI为：{0}".format(mini))
            # 再循环，先找出为i的坐标，然后
            j = 0
            while (j < len(m)):
                # 先找到为x的坐标
                if (m[j] == x):
                    # 再看和以前的点重复了没有
                    if (n[j] not in K):
                        # 再看是不是最小距离
                        if (L[j] == mini):
                            K.append(n[j])
                            print("K为：{0}".format(K))
                            self.Cal(n[j])
                            K.remove(n[j])
                j = j + 1
        # 给ShunXu赋值
        else:
            print("开始赋值")
            print("ShunXu为：{0}".format(ShunXu))
            print("K为：{0}".format(K))
            # K1为K的倒置
            K1 = []
            i = 0
            while (i < len(K)):
                K1.append(K[len(K) - i - 1])
                i = i + 1
            print("K1为：{0}".format(K1))
            # 先判断长度，为0直接赋值，否则判断
            if (len(ShunXu) == 0):
                # 赋值
                i = 0
                while (i < len(K)):
                    ShunXu.append(K[i])
                    i = i + 1
            else:
                # 判断是否有重复
                # 先循环，分组看
                i = 0
                while (i < (len(ShunXu) / len(X))):
                    j = i * len(X)
                    # geshu1记录重复个数
                    geshu1 = 0
                    while (j < (i + 1) * len(X)):
                        if (K[j % len(X)] == ShunXu[j]):
                            geshu1 = geshu1 + 1
                        j = j + 1
                    if (geshu1 == len(K)):
                        print("不进行赋值，ShunXu为：{0}".format(ShunXu))
                        return

                    j = i * len(X)
                    # geshu2记录重复个数
                    geshu2 = 0
                    while (j < (i + 1) * len(X)):
                        if (K1[j % len(X)] == ShunXu[j]):
                            geshu2 = geshu2 + 1
                        j = j + 1
                    if (geshu2 == len(K)):
                        print("不进行赋值，ShunXu为：{0}".format(ShunXu))
                        return
                    i = i + 1
                # 赋值
                i = 0
                while (i < len(K)):
                    ShunXu.append(K[i])
                    i = i + 1
            print("ShunXu为：{0}".format(ShunXu))

    # 找出最小值的函数
    def min(self, X):
        mini = X[0]
        # 找出最小的叫做mini
        for item in X:
            if (item < mini):
                mini = item
        return mini

    # 生成最短连线的函数
    def handle(self):
        self.suanjuli()
        self.Calculate()
        self.judge()
        ShunXu.clear()
        print(ZuiZhongShunXu)
        xuanze = self.ui.comboBox.currentText()
        if (xuanze == "直线"):


            # 定义坐标格的长a，宽b
            self.a = self.ui.Box1.value()
            self.b = self.ui.Box2.value()
            x1, x2 = 0, self.a
            y1, y2 = 0, self.b

            # 以下语句可以绘图
            i = 0
            a = len(ZuiZhongShunXu) / len(X)
            print("a为：{0}".format(a))
            while (i < a):
                # 绘制第i+1个图
                plt.subplot(1, int(a), i + 1)
                # 先产生两个坐标的数组
                XShunXu = []
                YShunXu = []
                j = i * len(X)
                while (j < ((i + 1) * len(X)) ):
                    XShunXu.append(X[ZuiZhongShunXu[j]])
                    YShunXu.append(Y[ZuiZhongShunXu[j]])
                    j =j + 1
                # 再绘图
                plt.plot(XShunXu, YShunXu)
                plt.title("第{0}个线路的图".format(i+1))
                # x轴标题
                plt.xlabel('X')
                # y轴标题
                plt.ylabel('Y')
                # 绘制表格以及图形所在的位置
                plt.axis([x1, x2, y1, y2])
                plt.grid(True)
                plt.show()
                i = i + 1

        elif(xuanze == "折线"):
            # 定义坐标格的长a，宽b
            self.a = self.ui.Box1.value()
            self.b = self.ui.Box2.value()
            x1, x2 = 0, self.a
            y1, y2 = 0, self.b

            # 以下语句可以绘图
            i = 0
            a = len(ZuiZhongShunXu) / len(X)
            print("a为：{0}".format(a))
            while (i < a):
                # 绘制第i+1个图
                plt.subplot(1, int(a), i + 1)
                # 先产生两个坐标的数组
                XShunXu = []
                YShunXu = []
                j = i * len(X)
                while (j < ((i + 1) * len(X))):
                    if (j % len(X) == 0):
                        XShunXu.append(X[ZuiZhongShunXu[j]])
                        YShunXu.append(Y[ZuiZhongShunXu[j]])
                    else:
                        XShunXu.append(X[ZuiZhongShunXu[j]])
                        YShunXu.append(Y[ZuiZhongShunXu[j-1]])
                        XShunXu.append(X[ZuiZhongShunXu[j]])
                        YShunXu.append(Y[ZuiZhongShunXu[j]])
                    j = j + 1
                # 再绘图
                plt.plot(XShunXu, YShunXu)
                plt.title("第{0}个线路的图".format(i + 1))
                # x轴标题
                plt.xlabel('X')
                # y轴标题
                plt.ylabel('Y')
                # 绘制表格以及图形所在的位置
                plt.axis([x1, x2, y1, y2])
                plt.grid(True)
                plt.show()
                i = i + 1


# 以下四句为固定语句
app = QApplication([])      #创建窗口
state = chuangkou()
state.ui.show()
app.exec_()                 #死循环