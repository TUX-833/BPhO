import sys
from PyQt5.QtWidgets import QApplication
from gui import MyApp

app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

window = MyApp()
window.show()
sys.exit(app.exec_())