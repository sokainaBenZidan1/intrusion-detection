import sys
from PyQt5.QtWidgets import QApplication,QSizePolicy, QLabel,QComboBox,QStyledItemDelegate, QPushButton, QWidget, QGraphicsDropShadowEffect, QGridLayout,QHBoxLayout
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor


import time
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from sklearn.preprocessing import LabelEncoder #,Imputer 
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score,precision_recall_fscore_support
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score, recall_score, precision_score, f1_score 
import joblib


combo_style = '''
            QComboBox {
                border: 2px solid #BBE2EC; /* Green border */
                border-radius: 10px; /* Rounded corners */
                padding: 8px  180px 8px 180px; /* Add some padding */
                margin:0px 5px;
                background-color: #FFF6E9; /* Light gray background color */
                font-size: 20px; /* Font size */
                color:#40A2E3;
            }
            QComboBox::down-arrow {
                width: 0; /* Hide the default down arrow */
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right; /* Position the custom down arrow */
                width: 20px; /* Width of the custom down arrow */
                border-left: 2px solid #4CAF50; /* Match the combo box border */
                height: 100%;
            }
            QComboBox::down-arrow:on {
                top: 0; /* Adjust position for centering text */
            }
            '''


        

class PrecessModel(QWidget):

    def __init__(self,algo,dataset):
        super().__init__()
        self.dataset = dataset
        self.algo = algo
        self.X_test,self.y_test,self.y_predict,self.score_test,self.predict_time,self.precision,self.recall,self.fscore= self.load_model()
        self.exactitude_DT = accuracy_score(self.y_test,self.y_predict)

        self.setWindowTitle("Intrusion Detection")
        self.setFixedWidth(600)
        self.setMinimumHeight(800)
        icon = QIcon('logo.png')
        self.setWindowIcon(icon)
        self.setStyleSheet("background:#FFF6E9;")

        self.combo_box = QComboBox()
        self.combo_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.combo_box.setItemDelegate(CenteredTextDelegate())
        self.combo_box.setStyleSheet(combo_style)
        self.apply_shadow_effect(self.combo_box)
        self.combo_box.addItems(["decision_tree","adaboost","Gradient_Boosting","Logistic_Regression", "XGBoost","SVM","Random_Forest"])
        self.combo_box.setCurrentText(self.algo)
        self.combo_box.currentIndexChanged.connect(self.pick_different_algo)
        # ********************** self.label********************
        self.logo = QLabel()
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        
        pixmap = QPixmap('logo.png')
        pixmap =  pixmap.scaled(90,90)
        self.logo.setStyleSheet(" margin-top:5px 0px 5px 100px;")
        self.logo.setPixmap(pixmap)
        
        # ************************** back button***********************
        self.backButton = QPushButton("back to main ->")
        self.backButton.clicked.connect(self.back_to_main)
        self.backButton.setCursor(Qt.PointingHandCursor) 
        
        self.backButton.setStyleSheet(
        '''
        *{font-size: 13px;
        color: '#FFF6E9';
        padding: 5px;
        margin: 5px 10px 0px 300px;
        background: '#40A2E3';
        border: 1px solid '#40A2E3';
        border-radius: 35px;
        }
        *:hover{
                background: '#0D9276';
                color:#FFF6E9;
        }
        ''')

        # Create a horizontal layout
        self.apply_shadow_effect(self.backButton)
        self.label = InfoLabels(self.algo,self.score_test,self.predict_time,self.exactitude_DT,self.precision,self.recall,self.fscore,1-self.exactitude_DT)
        
        self.layout = QGridLayout()
        
        
        # ***************** adding widgets*******************************
        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.logo)
        self.h_layout.addWidget(self.backButton)
        self.layout.addLayout(self.h_layout,0,0)
        self.layout.addWidget(self.combo_box,1,0)
        self.fill_data()

    def fill_data(self):

        self.paint_matrice(self.y_test,self.y_predict)
        self.layout.addWidget(self.label, 2, 0)
        self.layout.addWidget(self.canvas,3,0)
        self.setLayout(self.layout)
    def pick_different_algo(self):
        self.algo = self.combo_box.currentText()
        self.X_test,self.y_test,self.y_predict,self.score_test,self.predict_time,self.precision,self.recall,self.fscore= self.load_model()
        self.exactitude_DT = accuracy_score(self.y_test,self.y_predict)
        
        self.label.update_values(self.algo,self.score_test,self.predict_time,self.exactitude_DT,self.precision,self.recall,self.fscore,1-self.exactitude_DT)
        self.fill_data()

    def paint_matrice(self,y_test,y_predict):
        self.figure, self.ax = plt.subplots(figsize=(5, 5))
        self.figure.patch.set_facecolor('#FFF6E9')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        cm = confusion_matrix(y_test, y_predict)
        self.ax.clear()
        sns.heatmap(cm, annot=True, linewidth=0.5, linecolor="red", fmt=".0f", ax=self.ax)

        self.ax.set_xlabel("y_pred")
        self.ax.set_ylabel("y_test")
        self.canvas.draw()
    def back_to_main(self):
        from main_app import MainWindow
        self.w = MainWindow()
        self.w.show()
        self.hide()
    def load_model(self):
        X_test,y_test = joblib.load(f'{self.dataset}.joblib')
        model = joblib.load(f"{self.algo}_model.joblib")

        # Make predictions
        start = time.time()
        y_predict = model.predict(X_test)
        score_test=model.score(X_test, y_test)
        print (" Score test: "+str (score_test) )
        end = time.time()
        predict_time = end  - start
        
        precision,recall,fscore,none= precision_recall_fscore_support(y_test, y_predict, average='weighted') 

        return  X_test,y_test,y_predict,score_test,predict_time,precision,recall,fscore
    def apply_shadow_effect(self, widget):
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(20)  
        shadow_effect.setColor(QtGui.QColor(0, 0, 0, 100))  
        widget.setGraphicsEffect(shadow_effect)
    
class CenteredTextDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.displayAlignment = Qt.AlignCenter
        super().paint(painter, option, index)

class InfoLabels(QWidget):
    def __init__(self,algorithm,test_score,predict_time,exactitude_DT,precision,recall,fscore,error_score):
        super().__init__()
        self.test_score = str(test_score)
        self.algorithm = algorithm
        self.exactitude_DT=str(exactitude_DT)
        self.predict_time=str(predict_time)
        self.precision=str(precision)
        self.recall=str(recall)
        self.fscore=str(fscore)
        self.error = str(error_score)

        self.create()

    def create(self):
        layout = QGridLayout(self)
        self.metric_labels = []
        self.value_labels = []

        data = [
            ("Score test:",self.test_score),
            ('temps prediction:', self.predict_time),
            ('Exactitude de '+self.algorithm+':', self.exactitude_DT),
            ('Précision de '+self.algorithm+':', self.precision),
            ('Taux de détection de '+self.algorithm+':', self.recall),
            ('F1-score de '+self.algorithm+':', self.fscore),
            ('ERROR SCORE :', self.error)
        ]

        for row, (metric, value) in enumerate(data):
            label_metric = QLabel(metric)
            label_value = QLabel(value)
            label_metric.setStyleSheet("font-size: 15px; color: #0D9276; font-weight: bold; padding: 5px;margin-left:20px; margin-bottom: 5px; text-align: center;")
            label_value.setStyleSheet("font-size: 15px; color: #333; padding: 5px;margin-left:20px; margin-bottom: 5px; text-align: center;")
            self.metric_labels.append(label_metric)
            self.value_labels.append(label_value)
            layout.addWidget(label_metric, row, 0)
            layout.addWidget(label_value, row, 1)

        self.setLayout(layout)
    
    def update_values(self,algorithm,test_score,predict_time,exactitude_DT,precision,recall,fscore,error_score):
        self.test_score = str(test_score)
        self.algorithm = algorithm
        self.predict_time = str(predict_time)
        self.exactitude_DT = str(exactitude_DT)
        self.precision = str(precision)
        self.recall = str(recall)
        self.fscore = str(fscore)
        self.error = str(error_score)

        data = [
            ("Score test:",self.test_score),
            ('temps prediction:', self.predict_time),
            ('Exactitude de ' + self.algorithm + ':', self.exactitude_DT),
            ('Précision de ' + self.algorithm + ':', self.precision),
            ('Taux de détection de ' + self.algorithm + ':', self.recall),
            ('F1-score de ' + self.algorithm + ':', self.fscore),
            ('ERROR SCORE :', self.error)
        ]

        for idx, (metric, value) in enumerate(data):
            self.metric_labels[idx].setText(metric)
            self.value_labels[idx].setText(value)


if __name__ == '__main__':
    app = QApplication(sys.argv)       
    window = PrecessModel("decision_tree","dataset1")
    window.show()
    sys.exit(app.exec())