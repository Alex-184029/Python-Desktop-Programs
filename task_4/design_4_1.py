# 实验内容四：四则运算
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon
import threading

# 四则运算类
class Calc(object):
    def __init__(self):
        self.ui = QUiLoader().load('design_4.ui')
        self.ui.setWindowTitle('207班-09号-刘朴华') 

        self.ui.radio_odd.setCheckable(False)
        self.ui.radio_even.setCheckable(False)
        self.ui.radio_zero.setCheckable(False)
        self.ui.to_operate.clicked.connect(self.operate)
    # 运算方法
    def operate(self):
        # 定义线程
        self.t = threading.Thread(target=self.thread)
        # 原始数据清空
        self.ui.radio_odd.setDown(False)
        self.ui.radio_even.setDown(False)
        self.ui.radio_zero.setDown(False)
        self.ui.res_console.clear()
        # 数据检测与获取
        self.A = self.ui.data_A.value()
        self.B = self.ui.data_B.value()
        self.F = self.ui.data_F.currentText()
        if not self.detect():
            QMessageBox.critical(self.ui,"错误提示","数据或运算符有误，\n请重新输入。")
            self.ui.data_A.setValue(0.0)
            self.ui.data_B.setValue(0.0)
        else:
            self.ui.res_console.append("数据符合规范，程序即将运行。\n")
            #开始运算
            if self.F == '+':
                self.result = self.A+self.B
            elif self.F == '-':
                self.result = self.A-self.B
            elif self.F == '*':
                self.result = self.A*self.B
            elif self.F == '/':
                self.result = self.A/self.B
            else:
                QMessageBox.info(self.ui,"信息提示","程序运行出错，\n请重新运行。")
            # 多线程控制
            self.t.start()
            self.t.join()
            # 控制台结果显示
            self.ui.res_console.append("计算结果：%.2f + %.2f = %.3f"%(self.A,self.B,self.result))
    # 数据检测
    def detect(self):
        if self.F != '+' and self.F != '-' and self.F != '*' and self.F != '/':
            return False
        elif self.F == '/' and self.B == 0.:
            return False
        return True
    # 线程函数
    def thread(self):
        self.ui.res_console.append(">>> 线程%s运行中。。。"%(threading.current_thread().name))
        x = int(self.result)
        if x == 0:
            self.ui.radio_zero.setDown(True)
        elif x%2 == 0:
            self.ui.radio_even.setDown(True)
        elif x%2 == 1:
            self.ui.radio_odd.setDown(True)

app = QApplication([])
app.setWindowIcon(QIcon('bupt.ico'))
c = Calc()
c.ui.show()
app.exec_()