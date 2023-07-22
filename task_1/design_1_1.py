# 实验内容一：波形产生
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon
import pyqtgraph as pg   
import numpy as np  

# 数字波形类
class MathWave(object):
    def __init__(self):
        self.result = []
        self.setPW()
        
        self.ui = QUiLoader().load('design_1.ui')
        self.ui.setWindowTitle('207班-09号-刘朴华')

        self.ui.button_1.clicked.connect(self.getData)
        self.ui.button_2.clicked.connect(self.resetData)
        # 绘图对象容器关联
        self.ui.fig_con.addWidget(self.pw1)
        self.ui.fig_con.addWidget(self.pw2)
        self.ui.fig_con.addWidget(self.pw3)
    # 绘图设置
    def setPW(self):
        # 绘图对象一
        self.pw1 = pg.PlotWidget()
        self.pw1.setTitle("波形绘制",color='008080',size='12pt')
        self.pw1.setBackground("w")
        # 绘图对象二
        self.pw2 = pg.PlotWidget()
        self.pw2.setBackground("w")
        # 绘图对象三
        self.pw3 = pg.PlotWidget()
        self.pw3.setBackground("w")
    # 数据获取方法
    def getData(self):
        self.a = self.ui.data_A.text().split(" ")
        self.b = self.ui.data_B.text().split(" ")
        self.F = self.ui.data_F.text().split(" ")
        if self.detectData() == False:
            QMessageBox.critical(self.ui,"错误提示","输入格式不规范，\n请重新输入。")
            self.ui.data_A.clear()
            self.ui.data_B.clear()
            self.ui.data_F.clear()
        else:
            self.ui.res_console.setPlainText("输入合法，即将运行！")
            self.run()      # 检测成功，直接运行
            self.display()
            self.draw()
    # 数据检测方法
    def detectData(self):
        # 逻辑数据A、B检测
        if len(self.a) != len(self.b):
            return False
        for i in range(len(self.a)):
            if self.a[i] != '0' and self.a[i] != '1':
                return False
            else:
                self.a[i] = int(self.a[i])
        for i in range(len(self.b)):
            if self.b[i] != '0' and self.b[i] != '1':
                return False
            else:
                self.b[i] = int(self.b[i])
        # 表达式F检测
        if len(self.F) == 2:
            if self.F[0] != '~':
                return False
            elif self.F[1] != 'A' and self.F[1] != 'B':
                return False
        elif len(self.F) == 3:
            if (self.F[0] != 'A' and self.F[0] != 'B') or (self.F[2] != 'A' and self.F[2] != 'B'):
                return False
            elif self.F[1] != '&' and self.F[1] != '|' and self.F[1] != '~' and self.F[1] != '^' and self.F[1] != '^-':
                return False
        elif len(self.F) != 2 and len(self.F) != 3:
            return False
        return True
    # 运行方法
    def run(self):       
        if len(self.F) == 3:
            if self.F[1] == '&':                    # 与运算
                for i in range(len(self.a)):
                    self.result.append(self.a[i] & self.b[i])
            elif self.F[1] == '|':                  # 或运算
                for i in range(len(self.a)):
                    self.result.append(self.a[i] | self.b[i])
            elif self.F[1] == '^': 
                for i in range(len(self.a)):        # 异或运算
                    self.result.append(self.a[i] ^ self.b[i])
            elif self.F[1] == '^-':
                for i in range(len(self.a)):        # 同或运算
                    self.result.append(1 if self.a[i] == self.b[i] else 0)
        elif len(self.F) == 2:
            if self.F[1] == 'A':
                for i in self.a:
                    self.result.append(1 if i == 0 else 0)
            if self.F[1] == 'B':
                for i in self.b:
                    self.result.append(1 if i == 0 else 0)
    # 结果显示方法
    def display(self):
        self.ui.res_console.append("\n>>> 运算结果："+"\n逻辑长度："+str(len(self.a))+"\n运算结果：F = "+str(self.result))
    # 数据重置方法
    def resetData(self):
        self.ui.data_A.clear()
        self.ui.data_B.clear()
        self.ui.data_F.clear()
        self.ui.res_console.clear()
        self.result = []
    # 波形绘制函数
    def draw(self):
        self.pw1.clear()
        self.pw2.clear()
        self.pw3.clear()
        x = np.array([]);y1 = np.array([])
        y2 = np.array([]);y3 = np.array([])
        for i in range(len(self.a)):
            x = np.append(x,i)
            x = np.append(x,i+1)
            y1 = np.append(y1,self.a[i])
            y1 = np.append(y1,self.a[i])
            y2 = np.append(y2,self.b[i])
            y2 = np.append(y2,self.b[i])
            y3 = np.append(y3,self.result[i])
            y3 = np.append(y3,self.result[i])
        self.pw1.plot(x,y1,pen=pg.mkPen('#000000')) 
        self.pw2.plot(x,y2,pen=pg.mkPen('#000000'))
        self.pw3.plot(x,y3,pen=pg.mkPen('#000000'))  
        
app = QApplication([])
app.setWindowIcon(QIcon('bupt.ico'))
math = MathWave()
math.ui.show()
app.exec_()