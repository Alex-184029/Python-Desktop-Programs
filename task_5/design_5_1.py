# 实验内容五：扫雷游戏
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon
from PySide2.QtCore import QTimer
from functools import partial
import numpy as np

# 扫雷游戏类
class MineClear(object):
    def __init__(self):
        self.ui = QUiLoader().load('design_5.ui')
        self.ui.setWindowTitle('207班-09号-刘朴华') 
        self.policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.ui.btn_confirm.clicked.connect(self.confirm)
        self.ui.btn_clear.clicked.connect(self.clearAll)
        # 页面控件初始化
        self.ui.remain_num.setPlainText("0")
        self.ui.best_record.setPlainText("尚无")
        self.ui.success_pro.setPlainText("0 %")
    # 初始化数据
    def initData(self):
        self.sign = True          # 辅助实现长按功能 
        self.mine = []            # 雷的位置（1表示有雷）
        self.code = []            # 扫雷编码
        self.my_mine = []         # 玩家设定的雷（0初始，1设雷，-1点击）
        self.line = 0             # 方格边长
        self.num = 0              # 雷的个数
        self.step = 0             # 步数记录
        self.clean = 0            # 排雷记录
        self.value = 60           # 综合评测（后期记得实现）*******
        self.valueList = []       # 成绩记录列表
        self.pro = 0              # 成功概率，0~100
    # 确认选中
    def confirm(self):
        if self.ui.btn_contain.count() != 0:
            QMessageBox.information(self.ui,"游戏提示","为了确保游戏正常运行，\n请先点击清空按钮。")
            return
        self.initData()      # 数据初始化
        # 模式设置
        self.level = self.ui.level_option.currentText()
        if self.level == "简单模式":
            self.line = 5
            self.num = 5
            self.ui.success_pro.setPlainText("70 %")
            self.ui.res_console.setPlainText(">>> 模式选择成功！\n简单模式：5×5网格，共有5个雷。")
        elif self.level == "中等模式":
            self.line = 7
            self.num = 9
            self.pro = 60
            self.ui.success_pro.setPlainText("60 %")
            self.ui.res_console.setPlainText(">>> 模式选择成功！\n中等模式：7×7网格，共有9个雷。")
        elif self.level == "困难模式":
            self.line = 9
            self.num = 15
            self.pro = 50
            self.ui.success_pro.setPlainText("50 %")
            self.ui.res_console.setPlainText(">>> 模式选择成功！\n困难模式：9×9网格，共有15个雷。")
        self.createMine()
        self.createCode()
        self.createBtn()
    # 创建雷区
    def createMine(self):
        for i in range(self.line**2):
            self.mine.append(0)
            self.my_mine.append(0)
        cnt = 0
        while cnt < self.num:
            k = np.random.randint(self.line**2)
            if self.mine[k] == 0:
                self.mine[k] = 1
                cnt += 1
    # 生成代码（周围雷的个数，本身为雷-1表示）
    def createCode(self):
        for i in range(len(self.mine)):
            cnt = 0                                  # 中间变量，个数计量
            if self.mine[i] == 1:
                cnt = -1
            else:
                if i == 0:                           # 左上角
                    if self.mine[i+1] == 1:
                        cnt += 1
                    if self.mine[i+self.line] == 1:
                        cnt += 1
                    if self.mine[i+self.line+1] == 1:
                        cnt += 1
                elif i == self.line-1:               # 右上角
                    if self.mine[i-1] == 1:
                        cnt += 1
                    if self.mine[i+self.line] == 1:
                        cnt += 1
                    if self.mine[i+self.line-1] == 1:
                        cnt += 1
                elif i == self.line**2-self.line:    # 左下角
                    if self.mine[i+1] == 1:
                        cnt += 1
                    if self.mine[i-self.line] == 1:
                        cnt += 1
                    if self.mine[i-self.line+1] == 1:
                        cnt += 1
                elif i == self.line**2-1:            # 右下角
                    if self.mine[i-1] == 1:
                        cnt += 1
                    if self.mine[i-self.line] == 1:
                        cnt += 1
                    if self.mine[i-self.line-1] == 1:
                        cnt += 1
                elif i%self.line == 0:               # 左边界
                    if self.mine[i+1] == 1:
                        cnt += 1
                    if self.mine[i+self.line] == 1:
                        cnt += 1
                    if self.mine[i+self.line+1] == 1:
                        cnt += 1
                    if self.mine[i-self.line] == 1:
                        cnt += 1
                    if self.mine[i-self.line+1] == 1:
                        cnt += 1
                elif i%self.line == self.line-1:     # 右边界
                    if self.mine[i-1] == 1:
                        cnt += 1
                    if self.mine[i+self.line] == 1:
                        cnt += 1
                    if self.mine[i+self.line-1] == 1:
                        cnt += 1
                    if self.mine[i-self.line] == 1:
                        cnt += 1
                    if self.mine[i-self.line-1] == 1:
                        cnt += 1
                elif i < self.line:                  # 上边界                            
                    if self.mine[i-1] == 1:
                        cnt += 1
                    if self.mine[i+1] == 1:
                        cnt += 1
                    if self.mine[i+self.line] == 1:
                        cnt += 1
                    if self.mine[i+self.line-1] == 1:
                        cnt += 1
                    if self.mine[i+self.line+1] == 1:
                        cnt += 1
                elif i > self.line**2-self.line:     # 下边界                            
                    if self.mine[i-1] == 1:
                        cnt += 1
                    if self.mine[i+1] == 1:
                        cnt += 1
                    if self.mine[i-self.line] == 1:
                        cnt += 1
                    if self.mine[i-self.line-1] == 1:
                        cnt += 1
                    if self.mine[i-self.line+1] == 1:
                        cnt += 1
                else:                                # 中间部分
                    if self.mine[i-1] == 1:
                        cnt += 1
                    if self.mine[i+1] == 1:
                        cnt += 1
                    if self.mine[i+self.line] == 1:
                        cnt += 1
                    if self.mine[i+self.line-1] == 1:
                        cnt += 1
                    if self.mine[i+self.line+1] == 1:
                        cnt += 1
                    if self.mine[i-self.line] == 1:
                        cnt += 1
                    if self.mine[i-self.line-1] == 1:
                        cnt += 1
                    if self.mine[i-self.line+1] == 1:
                        cnt += 1
            self.code.append(cnt)
    # 生成按钮
    def createBtn(self):
        # 开始生成按钮
        for i in range(self.line):
            for j in range(self.line):
                button = QPushButton(" ",self.ui)
                button.setSizePolicy(self.policy)
                self.ui.btn_contain.addWidget(button,i,j)
        # 按钮点击方法关联
        for i in range(self.ui.btn_contain.count()):
            self.ui.btn_contain.itemAt(i).widget().released.connect(partial(self.handleRelease,i))
            self.ui.btn_contain.itemAt(i).widget().pressed.connect(partial(self.handlePress,i))
            self.ui.btn_contain.itemAt(i).widget().clicked.connect(self.handleClick)
        # 雷数初始化
        self.ui.remain_num.setPlainText(str(self.num-self.clean))
    # 一次点击事件
    def handleRelease(self,x):
        if self.sign:
            # 在这里写点击事件处理
            if self.code[x] == 0 and self.my_mine[x] == 0:      # 周围无雷，扩散算法
                self.expand(x)
                self.step += 1
            if self.code[x] == -1 and self.my_mine[x] == 0:     # 踩到雷
                self.ui.btn_contain.itemAt(x).widget().setFlat(True)
                self.ui.btn_contain.itemAt(x).widget().setIcon(QIcon('bomb.ico'))
                QMessageBox.critical(self.ui,"游戏结束","踩到雷咯\nGame Over")
                self.displayAll()         # 游戏结束，全局显示
                self.value = self.getValue()
                self.ui.res_console.append("\n>>> 挑战失败\n本次游戏中，您走了 %d 步，排出 %d 个雷。\n综合成绩：%.1f分"%(self.step,self.clean,self.value))
                self.displayBest()
                self.displayPro()
            if self.code[x] > 0 and self.my_mine[x] == 0:       # 周围有雷
                self.my_mine[x] = -1
                self.ui.btn_contain.itemAt(x).widget().setText(str(self.code[x]))
                self.ui.btn_contain.itemAt(x).widget().setFlat(True)
                self.step += 1
    # 按钮按下事件
    def handlePress(self,x):
        self.timer = QTimer()                                        # 定义、清空定时器
        self.timer.timeout.connect(partial(self.longClick,x))        # timer超时后执行longClick(x)
        self.timer.start(2000)                                       # 开启定时2000ms，超时视为长按
    # 超时事件
    def longClick(self,x):
        self.timer.stop()
        self.sign = False      # 取消点击事件
        # 在这里写长按事件处理（雷的图标）
        if self.my_mine[x] == 0:
            self.ui.btn_contain.itemAt(x).widget().setIcon(QIcon("flag.ico"))
            self.my_mine[x] = 1
            self.clean += 1
            self.ui.remain_num.setPlainText(str(self.num-self.clean))
            if self.isSucceed():
                self.setDisable()
                QMessageBox.information(self.ui,"游戏提示","成功清除所有的雷\n游戏通关！！！")
                self.value = self.getValue()+20
                self.ui.res_console.append("\n>>> 挑战成功\n本次游戏中，您走了 %d 步，排出 %d 个雷。\n综合成绩：%.1f分"%(self.step,self.clean,self.value))
                self.displayBest()
                self.displayPro()
        elif self.my_mine[x] == 1:
            self.ui.btn_contain.itemAt(x).widget().setIcon(QIcon())
            self.my_mine[x] = 0
            self.clean -= 1
            self.ui.remain_num.setPlainText(str(self.num-self.clean))
    # 按钮释放事件
    def handleClick(self):
        self.timer.stop()
        self.sign = True
    # 全局禁用（程序停止）
    def setDisable(self):
        for i in range(self.ui.btn_contain.count()):
            self.ui.btn_contain.itemAt(i).widget().setEnabled(False)      # 设置禁用状态
    # 判断游戏成功
    def isSucceed(self):
        for i in range(len(self.mine)):
            if self.mine[i] == 1 and self.my_mine[i] != 1:
                return False
        return True
    # 扩散方法（周围无雷，递归）
    def expand(self,i):
        self.ui.btn_contain.itemAt(i).widget().setText(" ")
        self.ui.btn_contain.itemAt(i).widget().setFlat(True)
        self.my_mine[i] = -1
        if i == 0:                                         # 左上角
            if self.my_mine[i+self.line] == 0:
                if self.code[i+self.line] == 0:
                    self.expand(i+self.line)
                else:
                    self.ui.btn_contain.itemAt(i+self.line).widget().setText(str(self.code[i+self.line]))
                    self.ui.btn_contain.itemAt(i+self.line).widget().setFlat(True)
                    self.my_mine[i+self.line] = -1
            if self.my_mine[i+1] == 0:
                if self.code[i+1] == 0:
                    self.expand(i+1)
                else:
                    self.ui.btn_contain.itemAt(i+1).widget().setText(str(self.code[i+self.line+1]))
                    self.ui.btn_contain.itemAt(i+1).widget().setFlat(True)
                    self.my_mine[i+1] = -1
            if self.my_mine[i+self.line+1] == 0:
                if self.code[i+self.line+1] == 0:
                    self.expand(i+self.line+1)
                else:
                    self.ui.btn_contain.itemAt(i+self.line+1).widget().setText(str(self.code[i+self.line+1]))
                    self.ui.btn_contain.itemAt(i+self.line+1).widget().setFlat(True)
                    self.my_mine[i+self.line+1] = -1
        elif i == self.line-1:                             # 右上角
            if self.my_mine[i-1] == 0:
                if self.code[i-1] == 0:
                    self.expand(i-1)
                else:
                    self.ui.btn_contain.itemAt(i-1).widget().setText(str(self.code[i-1]))
                    self.ui.btn_contain.itemAt(i-1).widget().setFlat(True)
                    self.my_mine[i-1] = -1
            if self.my_mine[i+self.line] == 0:
                if self.code[i+self.line] == 0:
                    self.expand(i+self.line)
                else:
                    self.ui.btn_contain.itemAt(i+self.line).widget().setText(str(self.code[i+self.line]))
                    self.ui.btn_contain.itemAt(i+self.line).widget().setFlat(True)
                    self.my_mine[i+self.line] = -1
            if self.my_mine[i+self.line-1] == 0:
                if self.code[i+self.line-1] == 0:
                    self.expand(i+self.line-1)
                else:
                    self.ui.btn_contain.itemAt(i+self.line-1).widget().setText(str(self.code[i+self.line-1]))
                    self.ui.btn_contain.itemAt(i+self.line-1).widget().setFlat(True)
                    self.my_mine[i+self.line-1] = -1
        elif i == self.line**2-self.line:                  # 左下角
            if self.my_mine[i-self.line] == 0:
                if self.code[i-self.line] == 0:
                    self.expand(i-self.line)
                else:
                    self.ui.btn_contain.itemAt(i-self.line).widget().setText(str(self.code[i-self.line]))
                    self.ui.btn_contain.itemAt(i-self.line).widget().setFlat(True)
                    self.my_mine[i-self.line] = -1
            if self.my_mine[i+1] == 0:
                if self.code[i+1] == 0:
                    self.expand(i+1)
                else:
                    self.ui.btn_contain.itemAt(i+1).widget().setText(str(self.code[i+1]))
                    self.ui.btn_contain.itemAt(i+1).widget().setFlat(True)
                    self.my_mine[i+1] = -1
            if self.my_mine[i-self.line+1] == 0:
                if self.code[i-self.line+1] == 0:
                    self.expand(i-self.line+1)
                else:
                    self.ui.btn_contain.itemAt(i-self.line+1).widget().setText(str(self.code[i-self.line+1]))
                    self.ui.btn_contain.itemAt(i-self.line+1).widget().setFlat(True)
                    self.my_mine[i-self.line+1] = -1
        elif i == self.line**2-1:                          # 右下角
            if self.my_mine[i-1] == 0:
                if self.code[i-1] == 0:
                    self.expand(i-1)
                else:
                    self.ui.btn_contain.itemAt(i-1).widget().setText(str(self.code[i-1]))
                    self.ui.btn_contain.itemAt(i-1).widget().setFlat(True)
                    self.my_mine[i-1] = -1
            if self.my_mine[i-self.line] == 0:
                if self.code[i-self.line] == 0:
                    self.expand(i-self.line)
                else:
                    self.ui.btn_contain.itemAt(i-self.line).widget().setText(str(self.code[i-self.line]))
                    self.ui.btn_contain.itemAt(i-self.line).widget().setFlat(True)
                    self.my_mine[i-self.line] = -1
            if self.my_mine[i-self.line-1] == 0:
                if self.code[i-self.line-1] == 0:
                    self.expand(i-self.line-1)
                else:
                    self.ui.btn_contain.itemAt(i-self.line-1).widget().setText(str(self.code[i-self.line-1]))
                    self.ui.btn_contain.itemAt(i-self.line-1).widget().setFlat(True)
                    self.my_mine[i-self.line-1] = -1
        elif i%self.line == 0:                             # 左边界
            if self.my_mine[i+1] == 0:
                if self.code[i+1] == 0:
                    self.expand(i+1)
                else:
                    self.ui.btn_contain.itemAt(i+1).widget().setText(str(self.code[i+1]))
                    self.ui.btn_contain.itemAt(i+1).widget().setFlat(True)
                    self.my_mine[i+1] = -1
            if self.my_mine[i-self.line] == 0:
                if self.code[i-self.line] == 0:
                    self.expand(i-self.line)
                else:
                    self.ui.btn_contain.itemAt(i-self.line).widget().setText(str(self.code[i-self.line]))
                    self.ui.btn_contain.itemAt(i-self.line).widget().setFlat(True)
                    self.my_mine[i-self.line] = -1
            if self.my_mine[i+self.line] == 0:
                if self.code[i+self.line] == 0:
                    self.expand(i+self.line)
                else:
                    self.ui.btn_contain.itemAt(i+self.line).widget().setText(str(self.code[i+self.line]))
                    self.ui.btn_contain.itemAt(i+self.line).widget().setFlat(True)
                    self.my_mine[i+self.line] = -1
            if self.my_mine[i-self.line+1] == 0:
                if self.code[i-self.line+1] == 0:
                    self.expand(i-self.line+1)
                else:
                    self.ui.btn_contain.itemAt(i-self.line+1).widget().setText(str(self.code[i-self.line+1]))
                    self.ui.btn_contain.itemAt(i-self.line+1).widget().setFlat(True)
                    self.my_mine[i-self.line+1] = -1
            if self.my_mine[i+self.line+1] == 0:
                if self.code[i+self.line+1] == 0:
                    self.expand(i+self.line+1)
                else:
                    self.ui.btn_contain.itemAt(i+self.line+1).widget().setText(str(self.code[i+self.line+1]))
                    self.ui.btn_contain.itemAt(i+self.line+1).widget().setFlat(True)
                    self.my_mine[i+self.line+1] = -1
        elif i%self.line == self.line-1:                   # 右边界
            if self.my_mine[i-1] == 0:
                if self.code[i-1] == 0:
                    self.expand(i-1)
                else:
                    self.ui.btn_contain.itemAt(i-1).widget().setText(str(self.code[i-1]))
                    self.ui.btn_contain.itemAt(i-1).widget().setFlat(True)
                    self.my_mine[i-1] = -1
            if self.my_mine[i-self.line] == 0:
                if self.code[i-self.line] == 0:
                    self.expand(i-self.line)
                else:
                    self.ui.btn_contain.itemAt(i-self.line).widget().setText(str(self.code[i-self.line]))
                    self.ui.btn_contain.itemAt(i-self.line).widget().setFlat(True)
                    self.my_mine[i-self.line] = -1
            if self.my_mine[i+self.line] == 0:
                if self.code[i+self.line] == 0:
                    self.expand(i+self.line)
                else:
                    self.ui.btn_contain.itemAt(i+self.line).widget().setText(str(self.code[i+self.line]))
                    self.ui.btn_contain.itemAt(i+self.line).widget().setFlat(True)
                    self.my_mine[i+self.line] = -1
            if self.my_mine[i-self.line-1] == 0:
                if self.code[i-self.line-1] == 0:
                    self.expand(i-self.line-1)
                else:
                    self.ui.btn_contain.itemAt(i-self.line-1).widget().setText(str(self.code[i-self.line-1]))
                    self.ui.btn_contain.itemAt(i-self.line-1).widget().setFlat(True)
                    self.my_mine[i-self.line-1] = -1
            if self.my_mine[i+self.line-1] == 0:
                if self.code[i+self.line-1] == 0:
                    self.expand(i+self.line-1)
                else:
                    self.ui.btn_contain.itemAt(i+self.line-1).widget().setText(str(self.code[i+self.line-1]))
                    self.ui.btn_contain.itemAt(i+self.line-1).widget().setFlat(True)
                    self.my_mine[i+self.line-1] = -1
        elif i < self.line:                                # 上边界
            if self.my_mine[i+self.line] == 0:
                if self.code[i+self.line] == 0:
                    self.expand(i+self.line)
                else:
                    self.ui.btn_contain.itemAt(i+self.line).widget().setText(str(self.code[i+self.line]))
                    self.ui.btn_contain.itemAt(i+self.line).widget().setFlat(True)
                    self.my_mine[i+self.line] = -1
            if self.my_mine[i-1] == 0:
                if self.code[i-1] == 0:
                    self.expand(i-1)
                else:
                    self.ui.btn_contain.itemAt(i-1).widget().setText(str(self.code[i-1]))
                    self.ui.btn_contain.itemAt(i-1).widget().setFlat(True)
                    self.my_mine[i-1] = -1
            if self.my_mine[i+1] == 0:
                if self.code[i+1] == 0:
                    self.expand(i+1)  
                else:
                    self.ui.btn_contain.itemAt(i+1).widget().setText(str(self.code[i+1])) 
                    self.ui.btn_contain.itemAt(i+1).widget().setFlat(True) 
                    self.my_mine[i+1] = -1         
            if self.my_mine[i+self.line+1] == 0:
                if self.code[i+self.line+1] == 0:
                    self.expand(i+self.line+1)
                else:
                    self.ui.btn_contain.itemAt(i+self.line+1).widget().setText(str(self.code[i+self.line+1]))
                    self.ui.btn_contain.itemAt(i+self.line+1).widget().setFlat(True)
                    self.my_mine[i+self.line+1] = -1
            if self.my_mine[i+self.line-1] == 0:
                if self.code[i+self.line-1] == 0:
                    self.expand(i+self.line-1)
                else:
                    self.ui.btn_contain.itemAt(i+self.line-1).widget().setText(str(self.code[i+self.line-1]))
                    self.ui.btn_contain.itemAt(i+self.line-1).widget().setFlat(True)
                    self.my_mine[i+self.line-1] = -1  
        elif i > self.line**2-self.line:                   # 下边界
            if self.my_mine[i-self.line] == 0:                            
                if self.code[i-self.line] == 0:
                    self.expand(i-self.line)
                else:
                    self.ui.btn_contain.itemAt(i-self.line).widget().setText(str(self.code[i-self.line]))
                    self.ui.btn_contain.itemAt(i-self.line).widget().setFlat(True)
                    self.my_mine[i-self.line] = -1
            if self.my_mine[i-1] == 0:
                if self.code[i-1] == 0:
                    self.expand(i-1)
                else:
                    self.ui.btn_contain.itemAt(i-1).widget().setText(str(self.code[i-1]))
                    self.ui.btn_contain.itemAt(i-1).widget().setFlat(True)
                    self.my_mine[i-1] = -1
            if self.my_mine[i+1] == 0:
                if self.code[i+1] == 0:
                    self.expand(i+1)  
                else:
                    self.ui.btn_contain.itemAt(i+1).widget().setText(str(self.code[i+1]))
                    self.ui.btn_contain.itemAt(i+1).widget().setFlat(True)
                    self.my_mine[i+1] = -1
            if self.my_mine[i-self.line+1] == 0:
                if self.code[i-self.line+1] == 0:
                    self.expand(i-self.line+1)
                else:
                    self.ui.btn_contain.itemAt(i-self.line+1).widget().setText(str(self.code[i-self.line+1]))
                    self.ui.btn_contain.itemAt(i-self.line+1).widget().setFlat(True)
                    self.my_mine[i-self.line+1] = -1
            if self.my_mine[i-self.line-1] == 0:
                if self.code[i-self.line-1] == 0:
                    self.expand(i-self.line-1)
                else:
                    self.ui.btn_contain.itemAt(i-self.line-1).widget().setText(str(self.code[i-self.line-1]))
                    self.ui.btn_contain.itemAt(i-self.line-1).widget().setFlat(True)
                    self.my_mine[i-self.line-1] = -1
        else:                                              # 中间部分
            if self.my_mine[i-1] == 0:
                if self.code[i-1] == 0:
                    self.expand(i-1)
                else:
                    self.ui.btn_contain.itemAt(i-1).widget().setText(str(self.code[i-1]))
                    self.ui.btn_contain.itemAt(i-1).widget().setFlat(True)
                    self.my_mine[i-1] = -1
            if self.my_mine[i+1] == 0:
                if self.code[i+1] == 0:
                    self.expand(i+1)
                else:
                    self.ui.btn_contain.itemAt(i+1).widget().setText(str(self.code[i+1]))
                    self.ui.btn_contain.itemAt(i+1).widget().setFlat(True)
                    self.my_mine[i+1] = -1
            if self.my_mine[i-self.line] == 0:
                if self.code[i-self.line] == 0:
                    self.expand(i-self.line)
                else:
                    self.ui.btn_contain.itemAt(i-self.line).widget().setText(str(self.code[i-self.line]))
                    self.ui.btn_contain.itemAt(i-self.line).widget().setFlat(True)
                    self.my_mine[i-self.line] = -1
            if self.my_mine[i+self.line] == 0:
                if self.code[i+self.line] == 0:
                    self.expand(i+self.line)
                else:
                    self.ui.btn_contain.itemAt(i+self.line).widget().setText(str(self.code[i+self.line]))
                    self.ui.btn_contain.itemAt(i+self.line).widget().setFlat(True)
                    self.my_mine[i+self.line] = -1
            if self.my_mine[i-self.line+1] == 0:
                if self.code[i-self.line+1] == 0:
                    self.expand(i-self.line+1)
                else:
                    self.ui.btn_contain.itemAt(i-self.line+1).widget().setText(str(self.code[i-self.line+1]))
                    self.ui.btn_contain.itemAt(i-self.line+1).widget().setFlat(True)
                    self.my_mine[i-self.line+1] = -1
            if self.my_mine[i-self.line-1] == 0:
                if self.code[i-self.line-1] == 0:
                    self.expand(i-self.line-1)
                else:
                    self.ui.btn_contain.itemAt(i-self.line-1).widget().setText(str(self.code[i-self.line-1]))
                    self.ui.btn_contain.itemAt(i-self.line-1).widget().setFlat(True)
                    self.my_mine[i-self.line-1] = -1
            if self.my_mine[i+self.line+1] == 0:
                if self.code[i+self.line+1] == 0:
                    self.expand(i+self.line+1)
                else:
                    self.ui.btn_contain.itemAt(i+self.line+1).widget().setText(str(self.code[i+self.line+1]))
                    self.ui.btn_contain.itemAt(i+self.line+1).widget().setFlat(True)
                    self.my_mine[i+self.line+1] = -1
            if self.my_mine[i+self.line-1] == 0:
                if self.code[i+self.line-1] == 0:
                    self.expand(i+self.line-1)
                else:
                    self.ui.btn_contain.itemAt(i+self.line-1).widget().setText(str(self.code[i+self.line-1]))
                    self.ui.btn_contain.itemAt(i+self.line-1).widget().setFlat(True)
                    self.my_mine[i+self.line-1] = -1
    # 组件清空
    def clearAll(self):
        for i in range(self.ui.btn_contain.count()):
            self.ui.btn_contain.itemAt(i).widget().deleteLater()
    # 获取评测成绩
    def getValue(self):
        cnt = 0
        for i in range(len(self.mine)):
            if self.mine[i] == 1 and self.my_mine[i] == 1:
                cnt += 1
        return cnt/self.num*80
    # 最佳成绩显示
    def displayBest(self):
        self.valueList.append(self.value)
        k = -1
        for i in self.valueList:
            if i > k:
                k = i
        self.ui.best_record.setPlainText("%.1f 分"%k)
    # 成功概率显示
    def displayPro(self):
        k = 0
        for i in self.valueList:
            k += i
        k /= len(self.valueList)             # 得到value平均值
        if self.line == 5:
            self.pro = k*0.6+70*0.4          # 设计权值，得出概率  
        elif self.line == 7:
            self.pro = k*0.6+60*0.4
        elif self.line == 9:
            self.pro = k*0.6+50*0.4
        else:
            print("程序出错，需要排除。")
        self.ui.success_pro.setPlainText("%.1f"%self.pro+" %")
    # 踩中雷，全局显示
    def displayAll(self):
        for i in range(len(self.code)):
            if self.code[i] == 0:
                self.ui.btn_contain.itemAt(i).widget().setFlat(True)
                self.ui.btn_contain.itemAt(i).widget().setEnabled(False)
            elif self.code[i] == -1:
                self.ui.btn_contain.itemAt(i).widget().setIcon(QIcon("bomb.ico"))
                self.ui.btn_contain.itemAt(i).widget().setFlat(True)
                self.ui.btn_contain.itemAt(i).widget().setEnabled(False)
            else:
                self.ui.btn_contain.itemAt(i).widget().setText(str(self.code[i]))
                self.ui.btn_contain.itemAt(i).widget().setFlat(True)
                self.ui.btn_contain.itemAt(i).widget().setEnabled(False)

app = QApplication([])
app.setWindowIcon(QIcon('bupt.ico'))
m = MineClear()
m.ui.show()
app.exec_()