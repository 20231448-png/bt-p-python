from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox,
    QTableWidget, QTableWidgetItem, QGroupBox,
    QGridLayout, QTextEdit
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from database import (
    insert_record,
    get_all_records,
    get_stats,
    get_latest_record
)


class HealthApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ứng dụng theo dõi sức khỏe")
        self.setGeometry(200, 100, 1150, 700)

        self.setStyleSheet("""
            QWidget {
                background-color: #f4f6f9;
                font-size: 16px;
                color: #111111;
                font-family: Arial;
            }

            QLabel {
                color: #111111;
                font-size: 16px;
                font-weight: bold;
            }

            QLineEdit {
                background-color: #ffffff;
                color: #000000;
                padding: 10px;
                border: 2px solid #888888;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }

            QLineEdit:focus {
                border: 2px solid #1976D2;
                background-color: #ffffff;
                color: #000000;
            }

            QTextEdit {
                background-color: #ffffff;
                color: #000000;
                font-size: 15px;
                border: 2px solid #cccccc;
                border-radius: 8px;
                padding: 8px;
            }

            QPushButton {
                background-color: #1976D2;
                color: white;
                padding: 12px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #0D47A1;
            }

            QGroupBox {
                background-color: #ffffff;
                color: #000000;
                border: 2px solid #cccccc;
                border-radius: 12px;
                margin-top: 14px;
                padding: 14px;
                font-size: 17px;
                font-weight: bold;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
                color: #000000;
                font-size: 17px;
                font-weight: bold;
            }

            QTableWidget {
                background-color: #ffffff;
                color: #000000;
                gridline-color: #cccccc;
                font-size: 15px;
                border: 1px solid #cccccc;
            }

            QHeaderView::section {
                background-color: #1976D2;
                color: white;
                font-size: 15px;
                font-weight: bold;
                padding: 6px;
                border: 1px solid #cccccc;
            }
        """)

        self.build_ui()
        self.load_data()
        self.load_stats()

    def build_ui(self):
        main_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        title = QLabel("THEO DÕI SỨC KHỎE")
        title.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        left_layout.addWidget(title)

        input_box = QGroupBox("Nhập chỉ số")
        input_layout = QGridLayout()

        self.height_input = QLineEdit()
        self.weight_input = QLineEdit()
        self.heart_input = QLineEdit()
        self.co2_input = QLineEdit()

        self.height_input.setPlaceholderText("Ví dụ: 170")
        self.weight_input.setPlaceholderText("Ví dụ: 60")
        self.heart_input.setPlaceholderText("Ví dụ: 80")
        self.co2_input.setPlaceholderText("Ví dụ: 500")

        input_layout.addWidget(QLabel("Chiều cao cm:"), 0, 0)
        input_layout.addWidget(self.height_input, 0, 1)

        input_layout.addWidget(QLabel("Cân nặng kg:"), 1, 0)
        input_layout.addWidget(self.weight_input, 1, 1)

        input_layout.addWidget(QLabel("Nhịp tim bpm:"), 2, 0)
        input_layout.addWidget(self.heart_input, 2, 1)

        input_layout.addWidget(QLabel("CO2 ppm:"), 3, 0)
        input_layout.addWidget(self.co2_input, 3, 1)

        save_btn = QPushButton("Lưu dữ liệu")
        save_btn.clicked.connect(self.save_record)

        input_layout.addWidget(save_btn, 4, 0, 1, 2)

        input_box.setLayout(input_layout)
        left_layout.addWidget(input_box)

        warning_box = QGroupBox("Cảnh báo")
        warning_layout = QVBoxLayout()

        self.warning_label = QLabel("Trạng thái: Chưa có dữ liệu")
        self.warning_label.setStyleSheet("""
            color: #d00000;
            font-size: 18px;
            font-weight: bold;
        """)

        warning_layout.addWidget(self.warning_label)
        warning_box.setLayout(warning_layout)

        left_layout.addWidget(warning_box)

        stats_box = QGroupBox("Thống kê sức khỏe")
        stats_layout = QVBoxLayout()

        self.total_label = QLabel()
        self.avg_bmi_label = QLabel()
        self.avg_heart_label = QLabel()
        self.avg_co2_label = QLabel()
        self.warning_count_label = QLabel()

        stats_layout.addWidget(self.total_label)
        stats_layout.addWidget(self.avg_bmi_label)
        stats_layout.addWidget(self.avg_heart_label)
        stats_layout.addWidget(self.avg_co2_label)
        stats_layout.addWidget(self.warning_count_label)

        stats_box.setLayout(stats_layout)
        left_layout.addWidget(stats_box)

        chat_box = QGroupBox("Chat AI tư vấn sức khỏe")
        chat_layout = QVBoxLayout()

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setPlaceholderText(
            "AI sẽ tư vấn dựa trên chỉ số sức khỏe mới nhất..."
        )

        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText(
            "Ví dụ: Tôi nên tăng cân hay giảm cân?"
        )

        chat_btn = QPushButton("Gửi câu hỏi")
        chat_btn.clicked.connect(self.chat_ai)

        chat_layout.addWidget(self.chat_display)
        chat_layout.addWidget(self.chat_input)
        chat_layout.addWidget(chat_btn)

        chat_box.setLayout(chat_layout)
        left_layout.addWidget(chat_box)

        table_box = QGroupBox("Lịch sử dữ liệu")
        table_layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Thời gian",
            "Chiều cao",
            "Cân nặng",
            "BMI",
            "Nhịp tim",
            "CO2",
            "Trạng thái"
        ])

        table_layout.addWidget(self.table)
        table_box.setLayout(table_layout)

        right_layout.addWidget(table_box)

        main_layout.addLayout(left_layout, 4)
        main_layout.addLayout(right_layout, 6)

        self.setLayout(main_layout)

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
            self.avg_co2_label.setText(
                f"CO2 trung bình: {avg_co2:.2f} ppm"
            )
            self.warning_count_label.setText(
                f"Số lần phát hiện bất thường: {warning_count}"
            )

    def chat_ai(self):
        question = self.chat_input.text().lower().strip()

        if question == "":
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập câu hỏi.")
            return

        latest = get_latest_record()

        if latest is None:
            answer = (
                "Bạn chưa có dữ liệu sức khỏe.\n"
                "Hãy nhập chiều cao, cân nặng, nhịp tim và CO2 trước."
            )
        else:
            time, height, weight, bmi, heart_rate, co2, status = latest

            answer = f"Dữ liệu mới nhất lúc {time}:\n"
            answer += f"- Chiều cao: {height} cm\n"
            answer += f"- Cân nặng: {weight} kg\n"
            answer += f"- BMI: {bmi:.2f}\n"
            answer += f"- Nhịp tim: {heart_rate} bpm\n"
            answer += f"- CO2: {co2} ppm\n"
            answer += f"- Trạng thái: {status}\n\n"

            if "tăng cân" in question or "gầy" in question:
                if bmi < 18.5:
                    answer += (
                        "Bạn đang có BMI thấp, nên tăng cân.\n"
                        "Gợi ý: ăn đủ bữa, tăng protein như trứng, sữa, thịt, cá, "
                        "đậu, bổ sung tinh bột tốt và tập luyện nhẹ."
                    )
                elif bmi < 25:
                    answer += (
                        "BMI của bạn đang bình thường.\n"
                        "Nếu muốn tăng cân, nên tăng từ từ bằng chế độ ăn lành mạnh, "
                        "không nên ăn quá nhiều đồ ngọt hoặc dầu mỡ."
                    )
                else:
                    answer += (
                        "BMI của bạn đang cao.\n"
                        "Bạn không nên tăng cân thêm, nên duy trì hoặc giảm cân nhẹ."
                    )

            elif "giảm cân" in question or "béo" in question or "mập" in question:
                if bmi >= 25:
                    answer += (
                        "Bạn đang có BMI cao, nên giảm cân.\n"
                        "Gợi ý: giảm nước ngọt, đồ chiên rán, ăn nhiều rau xanh, "
                        "uống đủ nước và vận động đều đặn."
                    )
                elif bmi >= 18.5:
                    answer += (
                        "BMI của bạn đang bình thường.\n"
                        "Nếu muốn giảm cân, chỉ nên giảm nhẹ và vẫn phải ăn đủ chất."
                    )
                else:
                    answer += (
                        "BMI của bạn đang thấp.\n"
                        "Bạn không nên giảm cân thêm."
                    )

            elif "bmi" in question:
                if bmi < 18.5:
                    answer += "BMI của bạn thấp, có thể đang thiếu cân."
                elif bmi < 25:
                    answer += "BMI của bạn nằm trong mức bình thường."
                else:
                    answer += "BMI của bạn cao, có thể đang thừa cân."

            elif "nhịp tim" in question or "tim" in question:
                if heart_rate < 60:
                    answer += (
                        "Nhịp tim của bạn hơi thấp.\n"
                        "Nếu có chóng mặt, mệt hoặc khó thở thì nên đi khám."
                    )
                elif heart_rate > 100:
                    answer += (
                        "Nhịp tim của bạn hơi cao.\n"
                        "Bạn nên nghỉ ngơi, tránh căng thẳng và theo dõi thêm."
                    )
                else:
                    answer += "Nhịp tim của bạn đang trong khoảng bình thường."

            elif "co2" in question or "không khí" in question:
                if co2 > 1000:
                    answer += (
                        "Chỉ số CO2 cao.\n"
                        "Bạn nên mở cửa, bật quạt thông gió hoặc ra nơi thoáng khí hơn."
                    )
                else:
                    answer += "Chỉ số CO2 đang ở mức ổn."

            elif "tư vấn" in question or "sức khỏe" in question:
                answer += (
                    "Gợi ý chung:\n"
                    "- Ăn uống cân bằng\n"
                    "- Ngủ đủ giấc\n"
                    "- Uống đủ nước\n"
                    "- Vận động thường xuyên\n"
                    "- Theo dõi chỉ số sức khỏe mỗi ngày"
                )

            else:
                answer += (
                    "Bạn có thể hỏi AI các câu như:\n"
                    "- Tôi nên tăng cân hay giảm cân?\n"
                    "- BMI của tôi có bình thường không?\n"
                    "- Nhịp tim của tôi thế nào?\n"
                    "- CO2 cao có nguy hiểm không?"
                )

            answer += "\n\nLưu ý: Đây chỉ là tư vấn tham khảo, không thay thế cho bác sĩ."

        self.chat_display.append("Bạn: " + self.chat_input.text())
        self.chat_display.append("AI: " + answer)
        self.chat_display.append("--------------------------------")
        self.chat_input.clear()