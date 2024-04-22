import sys
from PyQt5.QtWidgets import QApplication,QSizePolicy, QLabel,QComboBox,QStyledItemDelegate, QPushButton,QGraphicsDropShadowEffect, QFontDialog, QWidget, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from model_processing import PrecessModel

            
def button_style(l_margin,r_margin):
    return f'''
            *{{border: 4px solid '#40A2E3';
            color: #40A2E3;
            font-family: 'shanti';
            font-size: 20px;
            border-radius: 25px;
            padding: 15px 0;
            margin-left:{l_margin}px;
            margin-right:{r_margin}px;
            margin-bottom: 30px;
            }}
            *:hover{{
                background: '#0D9276';
                color:#FFF6E9;
            }}
            '''

class ListAlgo(QWidget):

    def __init__(self,dataset):
        super().__init__()
        self.dataset = dataset
        self.algos = {"decision_tree":(2,0),"adaboost":(2,1),"Gradient_Boosting":(3,0),"Logistic_Regression":(3,1), "XGBoost":(4,0),"SVM":(4,1),"Random_Forest":(5,0)}
        self.buttons = []
        self.setWindowTitle("Intrusion Detection")
        self.setFixedWidth(600)
        self.setMinimumHeight(700)
        icon = QIcon('logo.png')
        self.setWindowIcon(icon)
        self.setStyleSheet("background:#FFF6E9;")
        # self.setFont(QFont('Times font', 10))
        grid = QGridLayout()
        # ***********************************go bakc button*************
        back = QPushButton("back ->")
        # self.back.setAlignment(QtCore.Qt.AlignRight)
        back.setStyleSheet(
        '''
        *{font-size: 15px;
        color: '#FFF6E9';
        padding: 5px;
        margin: 10px 200px;
        background: '#40A2E3';
        border: 1px solid '#40A2E3';
        border-radius: 35px;
        }
        *:hover{
                background: '#0D9276';
                color:#FFF6E9;
        }
        ''')
        back.setCursor(Qt.PointingHandCursor) 
        self.apply_shadow_effect(back)
        back.clicked.connect(self.back_to_main)

        # ************ logo ************************
        self.label = QLabel()
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        
        pixmap = QPixmap('logo.png')
        pixmap = pixmap.scaled(110, 110)

        
        self.label.setStyleSheet(" margin-top:20px; ")
        self.label.setPixmap(pixmap)
        grid.addWidget(self.label,0,0)
        

        grid.addWidget(back,0,1)

        # ********************** label********************
        label = QLabel("Select an algorithm!")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setStyleSheet("color:#0D9276; margin:5px 30px 25px 30px; Font-size:50px;")
        grid.addWidget(label,1,0,1,2)
        # **************button*******************
        for algo,position in self.algos.items():
            button = QPushButton(algo)
            button.setObjectName(algo)
            if position[1]==0:
                button.setStyleSheet(button_style(55,5))
            else:
                button.setStyleSheet(button_style(5,55))
            button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
            button.setFixedWidth(270)
            button.clicked.connect(self.show_algorithms)
            self.apply_shadow_effect(button)
            self.buttons.append(button)
            grid.addWidget(button,position[0],position[1])
            
        self.setLayout(grid)

    def apply_shadow_effect(self, widget):
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(15)  # Adjust the blur radius as needed
        shadow_effect.setColor(QtGui.QColor(0, 0, 0, 100))  # Adjust the shadow color and transparency
        widget.setGraphicsEffect(shadow_effect)
    def show_algorithms(self):
        self.w = PrecessModel(self.sender().objectName(),self.dataset)
        self.w.show()
        self.hide()  
    def back_to_main(self):
        from main_app import MainWindow
        self.w = MainWindow()
        self.w.show()
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)       
    window = ListAlgo()
    window.show()
    sys.exit(app.exec())     
      