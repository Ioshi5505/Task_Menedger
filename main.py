import sys
from PySide6.QtWidgets import QApplication
from task_manager import TaskManager
from utils import load_stylesheet

def main():
    app = QApplication(sys.argv)
    stylesheet = load_stylesheet()
    if stylesheet is not None:
        app.setStyleSheet(stylesheet)

    window = TaskManager()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
