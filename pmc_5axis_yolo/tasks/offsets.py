from cv2.typing import MatLike
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog
from ultralytics import YOLO

from ..settings import DEFAULT_OFFSETS, PREDICT_VERBOSE
from ..ui.offset_slider_ui import Ui_Dialog
from ..utils import extract_object_regions


class OffsetSlider(QDialog, Ui_Dialog):
    offset_changed = Signal(float, float, float, float)
    cancel_signal = Signal(float, float, float, float)
    PictureSetCalled = Signal()

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
        self.Button_Offset_Picture.clicked.connect(self.PictureSetCall)

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

    def PictureSetCall(self):
        self.PictureSetCalled.emit()

    def cancel(self):
        self.cancel_signal.emit(
            self.initial_stop_x,
            self.initial_stop_y,
            self.initial_feed_x,
            self.initial_feed_y,
        )
        self.reject()


def adj_offsets(
    to_adj: bool,
    offsets: dict,
    image: str | MatLike,
    pose_model: YOLO,
    object_model: YOLO,
) -> dict:  # similar to test_hand_on_button
    old_offsets = offsets.copy()  # save old offsets

    if to_adj:
        print("Adjusting offsets...")
        pose_results = pose_model.predict(image, conf=0.4, verbose=PREDICT_VERBOSE)
        object_results = object_model.predict(image, conf=0.3, verbose=PREDICT_VERBOSE)

        # 獲取關鍵點 索引為: 9 是右手腕，10 是左手腕（根據 COCO 的姿態標註）
        keypoints = pose_results[0].keypoints.xy[0]

        # 取得右手與左手的座標 (x, y)
        left_hand = keypoints[9].tolist()  # (x, y) of left hand
        right_hand = keypoints[10].tolist()  # (x, y) of right hand

        # 提取 stop 和 feed 按鈕的範圍
        regions = extract_object_regions(object_results[0], ["stop", "feed"])

        # 判斷左手和 Stop 按鈕的相對位置
        if regions["stop"]:
            x = (regions["stop"].x_min + regions["stop"].x_max) / 2
            y = (regions["stop"].y_min + regions["stop"].y_max) / 2
            offsets["stop_x"] = x - left_hand[0]
            offsets["stop_y"] = y - left_hand[1]

        # 判斷右手和 Feed 按鈕的相對位置
        if regions["feed"]:
            x = (regions["feed"].x_min + regions["feed"].x_max) / 2
            y = (regions["feed"].y_min + regions["feed"].y_max) / 2
            offsets["feed_x"] = x - right_hand[0]
            offsets["feed_y"] = y - right_hand[1]

    if offsets == DEFAULT_OFFSETS:
        print("No changes adjusted. Using default offsets.")
    elif offsets == old_offsets:
        print("No changes adjusted. Using previous offsets.")
    else:
        print(
            f"Adjusted offsets:",
            " ".join(f"[{key}: {offsets[key]:.3f}]" for key in offsets),
        )

    return offsets


if __name__ == "__main__":
    import sys

    import cv2
    from PySide6.QtWidgets import QApplication
    from ultralytics import YOLO

    app = QApplication(sys.argv)
    window = OffsetSlider()
    window.show()
    sys.exit(app.exec())
#     image = cv2.imread("images/1.jpg")
#     pose_model = YOLO("yolov8n-pose.pt")
#     object_model = YOLO("best.pt")
#     adj_offsets(True, image, pose_model, object_model)
