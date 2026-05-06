import sys
from PyQt6.QtWidgets import QApplication

from database import init_db
from ui import HealthApp


if __name__ == "__main__":
    init_db()

    app = QApplication(sys.argv)

    window = HealthApp()
    window.show()

    sys.exit(app.exec())
