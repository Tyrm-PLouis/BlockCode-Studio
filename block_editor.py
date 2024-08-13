import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Chemin vers le fichier HTML
        self.browser = QWebEngineView()
        html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')
        self.browser.setUrl(QUrl.fromLocalFile(html_path))

        # Ajuster la taille de la fenêtre
        self.setCentralWidget(self.browser)
        self.setWindowTitle("Blockly avec PyQt5")
        self.resize(1200, 800)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
