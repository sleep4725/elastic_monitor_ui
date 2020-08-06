import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from esProj.esControl import EsControl

class Window(QWidget, EsControl):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("elasticsearch handler by KimJunHyeon")
        self.setGeometry(300, 300, 300, 200)

        ## Elasticsearch Button setting___________
        esStartButton = QPushButton("elastic_all_start_button", self)
        esStartButton.setToolTip("this is test button")
        esStartButton.move(0, 0)
        esStartButton.clicked.connect(self.es_all_service_start)
        ## _______________________________________

        ## Elasticsearch Button setting___________
        esStopButton = QPushButton("elastic_all_stop_button", self)
        esStopButton.setToolTip("this is test button")
        esStopButton.move(0, 50)
        esStopButton.clicked.connect(self.es_all_service_close)
        ## _______________________________________

        ## kibana all start Button setting___________
        esStartButton = QPushButton("kibana_all_start_button", self)
        esStartButton.setToolTip("this is test button")
        esStartButton.move(10, 100)
        esStartButton.clicked.connect(self.kibana_all_service_start)
        ## _______________________________________

        ## kibana all stop Button setting___________
        esStopButton = QPushButton("kibana_all_stop_button", self)
        esStopButton.setToolTip("this is test button")
        esStopButton.move(10, 150)
        esStopButton.clicked.connect(self.kibana_all_service_close)
        ## _______________________________________

        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() == Qt.Key_F:
            self.showFullScreen()
        elif e.key() == Qt.Key_N:
            self.showNormal()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())