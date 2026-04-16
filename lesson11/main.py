from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
from database import connect_db
import sys
from PyQt6.QtCore import QDate


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("nhansu.ui", self)

        # Combobox
        self.cbGioiTinh.clear()
        self.cbGioiTinh.addItems(["Nam", "Nữ"])

        # Bảng
        self.tableNhanSu.setColumnCount(5)
        self.tableNhanSu.setHorizontalHeaderLabels(
            ["CCCD", "Họ tên", "Ngày sinh", "Giới tính", "Địa chỉ"]
        )

        self.load_data()

        # Sự kiện
        self.btnThem.clicked.connect(self.them)
        self.btnSua.clicked.connect(self.sua)
        self.btnXoa.clicked.connect(self.xoa)
        self.btnTim.clicked.connect(self.tim)
        self.tableNhanSu.cellClicked.connect(self.hien_len_form)

    # ========================= LOAD =========================
    def load_data(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM NhanSu")
            data = cursor.fetchall()

            self.tableNhanSu.setRowCount(0)

            for row_idx, row_data in enumerate(data):
                self.tableNhanSu.insertRow(row_idx)
                for col_idx, col_data in enumerate(row_data):
                    self.tableNhanSu.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

            conn.close()
        except Exception as e:
            QMessageBox.warning(self, "Lỗi load", str(e))

    # ========================= THÊM =========================
    def them(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()

            sql = "INSERT INTO NhanSu VALUES (%s, %s, %s, %s, %s)"
            values = (
                self.txtCCCD.toPlainText().strip(),
                self.txtHoTen.toPlainText().strip(),
                self.dateNgaySinh.date().toString("yyyy-MM-dd"),
                self.cbGioiTinh.currentText(),
                self.txtDiaChi.toPlainText().strip()
            )

            cursor.execute(sql, values)
            conn.commit()
            conn.close()

            QMessageBox.information(self, "OK", "Thêm thành công!")
            self.load_data()

        except Exception as e:
            QMessageBox.warning(self, "Lỗi", str(e))

    # ========================= SỬA =========================
    def sua(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()

            cccd = self.txtCCCD.toPlainText().strip()

            sql = """UPDATE NhanSu 
                     SET HoTen=%s, NgaySinh=%s, GioiTinh=%s, DiaChi=%s 
                     WHERE CCCD=%s"""

            values = (
                self.txtHoTen.toPlainText().strip(),
                self.dateNgaySinh.date().toString("yyyy-MM-dd"),
                self.cbGioiTinh.currentText(),
                self.txtDiaChi.toPlainText().strip(),
                cccd
            )

            cursor.execute(sql, values)

            if cursor.rowcount == 0:
                QMessageBox.warning(self, "Lỗi", "Không tìm thấy CCCD!")
            else:
                QMessageBox.information(self, "OK", "Sửa thành công!")

            conn.commit()
            conn.close()

            self.load_data()

        except Exception as e:
            QMessageBox.warning(self, "Lỗi", str(e))

    # ========================= XÓA =========================
    def xoa(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()

            cccd = self.txtCCCD.toPlainText().strip()

            sql = "DELETE FROM NhanSu WHERE CCCD=%s"
            cursor.execute(sql, (cccd,))

            if cursor.rowcount == 0:
                QMessageBox.warning(self, "Lỗi", "Không tìm thấy CCCD!")
            else:
                QMessageBox.information(self, "OK", "Xóa thành công!")

            conn.commit()
            conn.close()

            self.load_data()

        except Exception as e:
            QMessageBox.warning(self, "Lỗi", str(e))

    # ========================= TÌM =========================
    def tim(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()

            keyword = self.txtTim.toPlainText().strip()  # ✅ FIX crash

            sql = """SELECT * FROM NhanSu 
                     WHERE CCCD LIKE %s OR HoTen LIKE %s OR DiaChi LIKE %s"""

            cursor.execute(sql, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
            data = cursor.fetchall()

            self.tableNhanSu.setRowCount(0)

            for row_idx, row_data in enumerate(data):
                self.tableNhanSu.insertRow(row_idx)
                for col_idx, col_data in enumerate(row_data):
                    self.tableNhanSu.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

            conn.close()

        except Exception as e:
            QMessageBox.warning(self, "Lỗi tìm kiếm", str(e))

    # ========================= CLICK TABLE =========================
    def hien_len_form(self, row, column):
        self.txtCCCD.setPlainText(self.tableNhanSu.item(row, 0).text())
        self.txtHoTen.setPlainText(self.tableNhanSu.item(row, 1).text())

        date_str = self.tableNhanSu.item(row, 2).text()
        self.dateNgaySinh.setDate(QDate.fromString(date_str, "yyyy-MM-dd"))

        self.cbGioiTinh.setCurrentText(self.tableNhanSu.item(row, 3).text())
        self.txtDiaChi.setPlainText(self.tableNhanSu.item(row, 4).text())


# ========================= MAIN =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())