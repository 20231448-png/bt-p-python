from PyQt6.QtWidgets import (
    QWidget, QMessageBox, QTableWidgetItem
)
from PyQt6 import uic
from ai_service import ask_groq_health_ai

from database import (
    insert_record,
    get_all_records,
    get_stats,
    get_latest_record
)


class HealthApp(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("health_app.ui", self)

        self.save_btn.clicked.connect(self.save_record)
        self.chat_btn.clicked.connect(self.chat_ai)

        self.load_data()
        self.load_stats()

    def save_record(self):
        try:
            height = float(self.height_input.text())
            weight = float(self.weight_input.text())
            heart_rate = int(self.heart_input.text())
            co2 = int(self.co2_input.text())

            if height <= 0 or weight <= 0:
                raise ValueError

            status = insert_record(height, weight, heart_rate, co2)

            QMessageBox.information(
                self,
                "Thành công",
                f"Đã lưu dữ liệu.\n{status}"
            )

            self.warning_label.setText("Trạng thái: " + status)

            self.height_input.clear()
            self.weight_input.clear()
            self.heart_input.clear()
            self.co2_input.clear()

            self.load_data()
            self.load_stats()

        except ValueError:
            QMessageBox.warning(
                self,
                "Lỗi",
                "Vui lòng nhập dữ liệu hợp lệ."
            )

    def load_data(self):
        rows = get_all_records()
        self.table.setRowCount(len(rows))

        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                if isinstance(value, float):
                    value = round(value, 2)

                self.table.setItem(
                    row_idx,
                    col_idx,
                    QTableWidgetItem(str(value))
                )

        self.table.resizeColumnsToContents()

    def load_stats(self):
        total, avg_bmi, avg_heart, avg_co2, warning_count = get_stats()

        self.total_label.setText(f"Tổng số bản ghi: {total}")

        if total == 0:
            self.avg_bmi_label.setText("BMI trung bình: chưa có dữ liệu")
            self.avg_heart_label.setText("Nhịp tim trung bình: chưa có dữ liệu")
            self.avg_co2_label.setText("CO2 trung bình: chưa có dữ liệu")
            self.warning_count_label.setText("Số lần cảnh báo: 0")
        else:
            self.avg_bmi_label.setText(f"BMI trung bình: {avg_bmi:.2f}")
            self.avg_heart_label.setText(
                f"Nhịp tim trung bình: {avg_heart:.2f} bpm"
            )
            self.avg_co2_label.setText(f"CO2 trung bình: {avg_co2:.2f} ppm")
            self.warning_count_label.setText(
                f"Số lần phát hiện bất thường: {warning_count}"
            )

    def chat_ai(self):
        question_original = self.chat_input.text().strip()

        if question_original == "":
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập câu hỏi.")
            return

        latest = get_latest_record()

        try:
            answer = ask_groq_health_ai(question_original, latest)
        except Exception as e:
            answer = (
                "Không thể kết nối Groq AI.\n"
                "Hãy kiểm tra GROQ_API_KEY hoặc kết nối Internet.\n"
                f"Lỗi: {e}"
            )

        self.chat_display.append("Bạn: " + question_original)
        self.chat_display.append("AI: " + answer)
        self.chat_display.append("--------------------------------")
        self.chat_input.clear()