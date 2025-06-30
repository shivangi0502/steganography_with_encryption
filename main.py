import sys
from PyQt5.QtWidgets import QApplication
from src.gui import InstaStegGUI
def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = InstaStegGUI()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
