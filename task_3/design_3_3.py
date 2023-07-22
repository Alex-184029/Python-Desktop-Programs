# 实验三：最短连线
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon
import pyqtgraph as pg
import numpy as np

# 结点类
class Node(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
    # 边距方法一：可斜线
    def getLen1(self,ano):
        return np.sqrt((self.x-ano.x)**2+(self.y-ano.y)**2)
    # 边距方法二：仅直线
    def getLen2(self,ano):
        return np.abs(self.x-ano.x)+np.abs(self.y-ano.y)
    # 判断相等
    def isEqual(self,ano):
        if self.x == ano.x and self.y == ano.y:
            return True
        return False
    # 显示方法
    def display(self):
        print("(%d,%d)"%(self.x,self.y),end=" ")
    # 字串返回方法
    def toString(self):
        return "(%d,%d) "%(self.x,self.y)
        
# 最短连线类
class Shortest(object):
    def __init__(self):
        self.ui = QUiLoader().load('design_3.ui')
        self.ui.setWindowTitle('207班-09号-刘朴华')

        self.initData()
        self.setPW()
        self.ui.fig_con.addWidget(self.pw,0,0)          # 加入画布

        self.ui.btn_1.clicked.connect(self.setSize)
        self.ui.btn_2.clicked.connect(self.addLocation)
        self.ui.btn_3.clicked.connect(self.run)
        self.ui.line_option.buttonClicked.connect(self.lineChange)
    # 数据初始化
    def initData(self):
        self.a = 0;self.b = 0       # 画布大小
        self.num = 0                # 生成点数
        self.line = ""              # 连线类型
        self.nodeList = []          # 结点存放序列
        self.shortList = []         # 最短连线序列（二维）
        self.color = ["#0000FF","#FF0000","#66DD00","#FF0088","#9900FF"]        # 用于生成随机颜色 
    # 画布初始化
    def setPW(self):
        self.pw = pg.PlotWidget()
        self.pw.setBackground("w")
        self.pw.showGrid(x=True, y=True)
        self.pw.setXRange(min=0,max=10)
        self.pw.setYRange(min=0,max=10)
    # 连线方式
    def lineChange(self):
        self.line = self.ui.line_option.checkedButton().text()
    # 方格设置大小
    def setSize(self):
        self.a = self.ui.data_a.value()
        self.b = self.ui.data_b.value()
        if self.a > 30 or self.a <= 4 or self.b > 30 or self.b <= 4:
            QMessageBox.critical(self.ui,"错误提示","方格无效，\n请重新输入。")
        else:
            self.ui.res_console.append("设置画布大小：(%d × %d)"%(self.a,self.b))
            self.pw.setXRange(min=0,max=self.a)
            self.pw.setYRange(min=0,max=self.b)
    # 加入坐标
    def addLocation(self):
        self.num = self.ui.data_num.value()
        x = self.ui.data_x.value()
        y = self.ui.data_y.value()
        if len(self.nodeList) >= self.num:
            QMessageBox.critical(self.ui,"错误提示","数据超出范围，\n请修改“设置点数”。")
        elif self.isRepeat(x,y):
            QMessageBox.critical(self.ui,"错误提示","加入坐标重复，\n请重新输入。")
        elif x > self.a or x < 0 or y > self.b or y < 0:
            QMessageBox.critical(self.ui,"错误提示","坐标超出画布范围，\n请重新输入。")
        else:
            self.nodeList.append(Node(x,y))
            self.ui.res_console.append(">>> 加入坐标：(%d, %d)"%(x,y)) 
    # 判断坐标是否重复（辅助）
    def isRepeat(self,x,y):
        for i in self.nodeList:
            if x == i.x and y == i.y:
                return True
        return False
    # 获取所有结点（不够的随机生成）
    def getAllNode(self):
        self.num = self.ui.data_num.value()
        while len(self.nodeList) < self.num:
            n = Node(np.random.randint(self.a),np.random.randint(self.b))
            sign = True
            for i in self.nodeList:
                if n.isEqual(i):
                    sign = False
            if sign:
                self.nodeList.append(n)      
    # 最短连线生成
    def run(self):
        if self.a == 0:
            QMessageBox.warning(self.ui,"错误警告","请先确定方格大小。")
            return
        elif self.line != "可斜线" and self.line != "仅直线":
            QMessageBox.warning(self.ui,"错误警告","请先选择连线方式。")
            return
        # 相关数据初始化        
        self.shortList = []    
        self.pw.clear()     
        # 最短连线生成开始
        self.getAllNode()          # 获取所有结点（默认随机生成）
        self.toStringNode()        # 所有点的显示
        for i in range(self.num):  # 获取从所有点开始的最短连线，存放二维序列中
            self.getList(i)
        self.getLength()           # 获取连线距离，序列末尾存放
        self.selectList()          # 连线筛选，生成最终连线
        self.toStringShort()       # 最短连线控制台显示
        self.draw()                # 图形绘制
    # 获取一个最短连线
    def getList(self,x):
        self.l = []
        short = []
        for i in range(self.num):
            self.l.append(0)
        short.append(x)
        self.l[x] = 1
        while self.remain():
            l = []
            for i in range(self.num):
                if self.l[i] == 0:
                    l.append(i)
            k = l[0]
            if self.line == "可斜线":
                for i in l:
                    if self.nodeList[x].getLen1(self.nodeList[i]) < self.nodeList[x].getLen1(self.nodeList[k]):
                        k = i
            elif self.line == "仅直线":
                for i in l:
                    if self.nodeList[x].getLen1(self.nodeList[i]) < self.nodeList[x].getLen1(self.nodeList[k]):
                        k = i
            else:
                print("Program Error getList.")
            self.l[k] = 1
            short.append(k)
        self.shortList.append(short)
    # 判断是否有点未计入
    def remain(self):
        for i in self.l:
            if i == 0:
                return True
        return False
    # 全部点的控制台显示
    def toStringNode(self):
        string = "\n>>> 点的坐标：\n"
        for i in self.nodeList:
            string += i.toString()
        self.ui.res_console.append(string)
    # 最短连线控制台显示
    def toStringShort(self):
        string = ">>> 最短连线：\n"
        for i in self.shortList:
            for j in range(len(i)-1):
                string += self.nodeList[i[j]].toString()
            string += "，连线长度 %.2f\n"%(i[-1])
        self.ui.res_console.append(string)
    # 获取每一组连线的长度，存放末尾
    def getLength(self):
        if self.line == "可斜线":
            for i in self.shortList:
                length = 0
                for j in range(len(i)-1):
                    length += self.nodeList[i[j]].getLen1(self.nodeList[i[j+1]])
                i.append(length)
        elif self.line == "仅直线":
            for i in self.shortList:
                length = 0
                for j in range(len(i)-1):
                    length += self.nodeList[i[j]].getLen2(self.nodeList[i[j+1]])
                i.append(length)
        else:
            print("program error getLength.")
    # 删除重复连线组
    def selectList(self):
        # 删除非最短连线
        l = []
        k = self.shortList[0][-1]
        for i in self.shortList:              # 此循环找出最短长度
            if i[-1] < k:
                k = i[-1]
        for i in range(len(self.shortList)):  # 记下长度非最短索引
            if self.shortList[i][-1] > k:
                l.append(i)
        self.myPop(l)                         # 非最短连线删除
        # 删除重复连线
        l = []
        for i in range(len(self.shortList)):  # 此循环找到重复，索引存入序列l中
            for j in range(i+1,len(self.shortList)):
                if self.isEqualList(self.shortList[i],self.shortList[j]):
                    l.append(j)
        self.myPop(l)                         # 删除重复连线
    # 判断连线序列是否相同
    def isEqualList(self,l1,l2):
        l = []
        for i in range(len(l2)-1):
            l.append(l2[i])
        l = l[::-1]
        for i in range(len(l)):
            if l[i] != l1[i]:
                return False
        return True
    # 删除序列元素
    def myPop(self,l):
        lAno = []
        for i in range(len(self.shortList)):
            if not (i in l):
                lAno.append(self.shortList[i])
        self.shortList = lAno
    # 图形绘制方法
    def draw(self):
        if len(self.shortList) == 0:
            QMessageBox.critical(self.ui,"错误提示","最短连线生成失败，\n请重新运行。")
            return
        self.pw.setXRange(min=0,max=self.a)
        self.pw.setYRange(min=0,max=self.b)
        if self.line == "可斜线":
            l = self.shortList[0]
            x = np.array([])
            y = np.array([])
            for i in range(len(l)-1):       # 末尾元素表示长度，不可计入
                x = np.append(x,self.nodeList[l[i]].x)
                y = np.append(y,self.nodeList[l[i]].y)
            self.pw.plot(x,y,pen=pg.mkPen(self.color[np.random.randint(len(self.color))]))   # 随机颜色绘制
            if len(self.shortList) > 1:
                for i in range(1,len(self.shortList)):
                    self.helpDraw(i)     # 辅助绘制，弹窗显示
        elif self.line == "仅直线":
            l = self.shortList[0]
            x = np.array([self.nodeList[l[0]].x])
            y = np.array([self.nodeList[l[0]].y])
            for i in range(1,len(l)-1):      # 末尾元素表示长度，不可计入
                x = np.append(x,self.nodeList[l[i]].x)
                y = np.append(y,self.nodeList[l[i-1]].y)
                x = np.append(x,self.nodeList[l[i]].x)
                y = np.append(y,self.nodeList[l[i]].y)
            self.pw.plot(x,y,pen=pg.mkPen(self.color[np.random.randint(len(self.color))]))   # 随机颜色绘制
            if len(self.shortList) > 1:
                for i in range(1,len(self.shortList)):
                    self.helpDraw(i)     # 辅助绘制，弹窗显示
        else:
            print("program error draw.")
    # 辅助绘图方法（连线不唯一，则另外弹窗显示）
    def helpDraw(self,x):
        # 创建实例化绘图对象
        pw = pg.plot()
        pw.setTitle("最短连线 "+str(x+1),size='12pt')   
        pw.setBackground('w')          
        pw.showGrid(x=True, y=True)    
        pw.setYRange(min=0,max=self.a)
        pw.setXRange(min=0,max=self.b)
        # 开始图形绘制
        if self.line == "可斜线":
            l = self.shortList[x]
            x = np.array([])
            y = np.array([])
            for i in range(len(l)-1):       # 末尾元素表示长度，不可计入
                x = np.append(x,self.nodeList[l[i]].x)
                y = np.append(y,self.nodeList[l[i]].y)
            pw.plot(x,y,pen=pg.mkPen(self.color[np.random.randint(len(self.color))]))   # 随机颜色绘制
        elif self.line == "仅直线":
            l = self.shortList[x]
            x = np.array([self.nodeList[l[0]].x])
            y = np.array([self.nodeList[l[0]].y])
            for i in range(1,len(l)-1):      # 末尾元素表示长度，不可计入
                x = np.append(x,self.nodeList[l[i]].x)
                y = np.append(y,self.nodeList[l[i-1]].y)
                x = np.append(x,self.nodeList[l[i]].x)
                y = np.append(y,self.nodeList[l[i]].y)
            pw.plot(x,y,pen=pg.mkPen(self.color[np.random.randint(len(self.color))]))   # 随机颜色绘制
        # 生成弹窗
        pg.Qt.QtGui.QApplication.instance().exec_()       
        
app = QApplication([])
app.setWindowIcon(QIcon('bupt.ico'))
s = Shortest()
s.ui.show()
app.exec_()