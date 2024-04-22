import sys
from PyQt5.QtWidgets import QApplication,QFileDialog, QLabel,QComboBox,QStyledItemDelegate, QPushButton,QGraphicsDropShadowEffect, QFontDialog, QWidget, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap,QFont,QIcon
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from  list_algos import ListAlgo
from PyQt5.QtGui import QPixmap


combo_style = '''
            QComboBox {
                border: 4px solid '#40A2E3';
                color: #40A2E3;
                font-family: 'shanti';
                font-size: 20px;
                border-radius: 15px;
                padding: 15px 125px 15px 125px;
                margin: 20px 90px 0px 90px;
                text-align: center;
            }
             QComboBox::drop-down {
                width: 0px; /* Set the width of the drop-down button to 0 */
            }

            QComboBox::down-arrow {
                width: 0px; /* Set the width of the down-arrow icon to 0 */
                height: 0px; /* Set the height of the down-arrow icon to 0 */
            }
            *:hover{
                background: '#0D9276';
                color:#FFF6E9;
            }

            '''

button2Style = '''
            *{border: 4px solid '#40A2E3';
            color: #40A2E3;
            font-family: 'shanti';
            font-size: 20px;
            border-radius: 25px;
            padding: 15px 0;
            margin: 40px 90px 20px 90px;
            margin-bottom: 50px;
            }
            *:hover{
                background: '#0D9276';
                color:#FFF6E9;
            }
            '''

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Intrusion Detection")
        self.setFixedWidth(600)
        icon = QIcon('logo.png')
        self.setWindowIcon(icon)
        self.setStyleSheet("background:#FFF6E9;")
        self.grid = QGridLayout()
        self.dataset = "dataset1"
        # ********************** self.label********************
        self.logo = QLabel()
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        
        pixmap = QPixmap('logo.png')
        
        self.logo.setStyleSheet(" margin-top:50px;")
        self.logo.setPixmap(pixmap)
        self.grid.addWidget(self.logo,0,0)
        # **************button*******************
        self.combo_box = QComboBox()
        self.combo_box.setItemDelegate(CenteredTextDelegate())
        self.combo_box.setStyleSheet(combo_style)
        self.apply_shadow_effect(self.combo_box)
        self.combo_box.addItems(["Pick a dataset","dataset1: 5.3KB ","dataset2: 2.6KB","dataset3: 270KB"])
        self.combo_box.currentIndexChanged.connect(self.pick_data_set)

        button2= QPushButton("List the algorithms")
        button2.setStyleSheet(button2Style)
        button2.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button2.clicked.connect(self.show_algorithms)
        self.apply_shadow_effect(button2)
        self.grid.addWidget(self.combo_box,1,0)
        self.grid.addWidget(button2,2,0)
        self.setLayout(self.grid)
    def pick_data_set(self):
        self.dataset = self.combo_box.currentText()[:8]
    def apply_shadow_effect(self, widget):
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(15)  
        shadow_effect.setColor(QtGui.QColor(0, 0, 0, 100))  
        widget.setGraphicsEffect(shadow_effect)
    def show_algorithms(self):
        if not (self.dataset == "dataset1" or self.dataset == "dataset2" or self.dataset == "dataset3"):
            self.dataset = "dataset1"
        self.w = ListAlgo(self.dataset)
        self.w.show()
        self.hide()

class CenteredTextDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.displayAlignment = Qt.AlignCenter
        super().paint(painter, option, index)


if __name__ == '__main__':
    app = QApplication(sys.argv)       
    window = MainWindow()
    window.show()
    sys.exit(app.exec())