# 实验内容二：电子钢琴
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon
from winsound import Beep
import time

# 音阶相关参数
tone = [131,147,165,175,196,220,247,262,296,330,349,392,440,494,523,587,659,698,784,880,988,1047,1175,1319,1568,1760,1976]
scale1 = [600,600,600,800,600,600,600,800]                         # “两只老虎”时间间隔
scale2 = [600,500,950,600,500,950]                                 # “乖宝宝”时间间隔

# 电子钢琴类
class Piano(object):
    def __init__(self):
        self.ui = QUiLoader().load('design_2.ui')
        self.ui.setWindowTitle('207班-09号-刘朴华')

        self.ui.btn_1.clicked.connect(self.autoPlay)
        self.ui.btn_2.clicked.connect(self.strPlay)
        self.ui.beatOption.addItems(['两只老虎','乖宝宝'])
        self.ui.stringLine.setPlaceholderText("小写字母a~u")
    # 自动播放方法
    def autoPlay(self):
        self.ini = self.ui.digital.value()
        if self.ini > 2000 or self.ini<40:
            QMessageBox.critical(self.ui,"错误提示","输入数据超出范围，\n请重新输入。")
        else:
            self.ui.res_console.setPlainText(">>> 功能一运行："+"\n    初始频率："+str(self.ini)+"Hz\n    频率间隔：100Hz"+"\n\n---------开始播放---------")
            x = self.ini
            while x <= 2000:
                Beep(x,500)
                x += 100   
        self.ui.digital.setValue(0)
    # 字串播放方法
    def strPlay(self):
        self.string = self.ui.stringLine.text()
        if self.detectStr() == False:
            QMessageBox.critical(self.ui,"错误提示","字串不合规范，\n请重新输入。")
            self.ui.stringLine.clear()
        else:
            self.ui.stringLine.clear()
            self.beat = self.ui.beatOption.currentText()
            self.ui.res_console.setPlainText(">>> 功能二运行："+"\n    选中节拍："+self.beat+"\n    输入字串："+self.string+"\n\n---------开始播放---------")
            if self.beat == "两只老虎":
                self.play_1()
            elif self.beat == "乖宝宝":
                self.play_2()
    # 字串检测方法
    def detectStr(self):
        for i in self.string:
            if ord(i) < 97 or ord(i) > 117:
                return False
        return True
    # 播放节拍：两只老虎*
    def play_1(self):
        for i in range(len(self.string)):
            Beep(tone[ord(self.string[i])-97],scale1[i%8])
            if i%8 == 0:
                time.sleep(1)
    # 播放节拍：乖宝宝       
    def play_2(self):
        for i in range(len(self.string)):
            Beep(tone[ord(self.string[i])-97],scale2[i%6])
            if i%11 == 0:
                time.sleep(1)

app = QApplication([])
app.setWindowIcon(QIcon('bupt.ico'))
p = Piano()
p.ui.show()
app.exec_()