from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Signal
from ui.offset_slider_ui import Ui_Dialog


class OffsetSlider(QDialog, Ui_Dialog):
    offset_changed = Signal(float, float, float, float)
    cancel_signal = Signal(float, float, float, float)

    def __init__(self, initial_stop_x, initial_stop_y, initial_feed_x, initial_feed_y):
        super().__init__()
        self.setupUi(self)

        # 存預設值
        self.initial_stop_x = initial_stop_x
        self.initial_stop_y = initial_stop_y
        self.initial_feed_x = initial_feed_x
        self.initial_feed_y = initial_feed_y

        # 滑桿預設
        self.Stop_X_Slider.setRange(-100, 100)
        self.Stop_X_Slider.setValue(initial_stop_x)
        self.Stop_Y_Slider.setRange(-100, 100)
        self.Stop_Y_Slider.setValue(initial_stop_y)
        self.Feed_X_Slider.setRange(-100, 100)
        self.Feed_X_Slider.setValue(initial_feed_x)
        self.Feed_Y_Slider.setRange(-100, 100)
        self.Feed_Y_Slider.setValue(initial_feed_y)
        self.update_offsets()

        # 改變滑桿訊號(待降低重複性)
        self.Stop_X_Slider.valueChanged.connect(self.update_offsets)
        self.Stop_Y_Slider.valueChanged.connect(self.update_offsets)
        self.Feed_X_Slider.valueChanged.connect(self.update_offsets)
        self.Feed_Y_Slider.valueChanged.connect(self.update_offsets)

        # 按鈕改變滑桿
        self.Stop_X_Plusbutton.clicked.connect(
            lambda: self.adjust_slider(self.Stop_X_Slider, 1)
        )
        self.Stop_X_MinusButton.clicked.connect(
            lambda: self.adjust_slider(self.Stop_X_Slider, -1)
        )
        self.Stop_Y_PlusButton.clicked.connect(
            lambda: self.adjust_slider(self.Stop_Y_Slider, 1)
        )
        self.Stop_Y_MinusButton.clicked.connect(
            lambda: self.adjust_slider(self.Stop_Y_Slider, -1)
        )
        self.Feed_X_PlusButton.clicked.connect(
            lambda: self.adjust_slider(self.Feed_X_Slider, 1)
        )
        self.Feed_X_MinusButton.clicked.connect(
            lambda: self.adjust_slider(self.Feed_X_Slider, -1)
        )
        self.Feed_Y_PlusButton.clicked.connect(
            lambda: self.adjust_slider(self.Feed_Y_Slider, 1)
        )
        self.Feed_Y_MinusButton.clicked.connect(
            lambda: self.adjust_slider(self.Feed_Y_Slider, -1)
        )

        self.Offset_Slider_Button.accepted.connect(self.accept)
        self.Offset_Slider_Button.rejected.connect(self.cancel)

    # 透過按鈕改變過程
    def adjust_slider(self, slider, increment):
        current_value = slider.value()
        new_value = current_value + increment
        slider.setValue(new_value)

    def update_offsets(self):
        stop_x = self.Stop_X_Slider.value()
        stop_y = self.Stop_Y_Slider.value()
        feed_x = self.Feed_X_Slider.value()
        feed_y = self.Feed_Y_Slider.value()
        self.Stop_X_Label.setText(f"Stop_X: {stop_x}")
        self.Stop_Y_Label.setText(f"Stop_Y: {stop_y}")
        self.Feed_X_Label.setText(f"Feed_X: {feed_x}")
        self.Feed_Y_Label.setText(f"Feed_Y: {feed_y}")
        self.offset_changed.emit(stop_x, stop_y, feed_x, feed_y)

    def cancel(self):
        self.cancel_signal.emit(
            self.initial_stop_x,
            self.initial_stop_y,
            self.initial_feed_x,
            self.initial_feed_y,
        )
        self.reject()


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = OffsetSlider()
    window.show()
    sys.exit(app.exec())
