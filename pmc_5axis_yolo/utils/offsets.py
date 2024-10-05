from matplotlib.pylab import f
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog

from ..ui.offset_slider_ui import Ui_Dialog


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
    to_adj, offsets, image, pose_model, object_model
):  # similar to test_hand_on_button
    old_offsets = offsets.copy()  # save old offsets

    if to_adj:
        print("Adjusting offsets...")
        pose_results = pose_model(image)
        object_results = object_model(image)

        # 獲取關鍵點 索引為: 9 是右手腕，10 是左手腕（根據 COCO 的姿態標註）
        keypoints = pose_results[0].keypoints.xy[0]

        # 取得右手與左手的座標 (x, y)
        left_hand = keypoints[9]  # (x, y) of left hand
        right_hand = keypoints[10]  # (x, y) of right hand

        # 初始化 Stop 和 Feed 按鈕的範圍變數
        stop_region = None
        feed_region = None

        # 遍歷每一個偵測結果來找到 stop 和 feed 的範圍
        for object in object_results[0].boxes:
            # 獲取偵測框的座標
            x1, y1, x2, y2 = map(int, object.xyxy[0].tolist())

            # 獲取物件的類別編號
            class_id = int(object.cls[0])

            # 獲取物件的類別名稱
            class_name = object_results[0].names[class_id]

            # 如果是 Stop 按鈕，記錄其範圍
            if class_name == "stop":
                stop_region = {"x_min": x1, "x_max": x2, "y_min": y1, "y_max": y2}

            # 如果是 Feed 按鈕，記錄其範圍
            if class_name == "feed":
                feed_region = {"x_min": x1, "x_max": x2, "y_min": y1, "y_max": y2}

        # 判斷左手和 Stop 按鈕的相對位置
        if stop_region:
            x = (stop_region["x_min"] + stop_region["x_max"]) / 2
            y = (stop_region["y_min"] + stop_region["y_max"]) / 2
            offsets["stop_x"] = x - left_hand.cpu().numpy()[0]
            offsets["stop_y"] = y - left_hand.cpu().numpy()[1]

        # 判斷右手和 Feed 按鈕的相對位置
        if feed_region:
            x = (feed_region["x_min"] + feed_region["x_max"]) / 2
            y = (feed_region["y_min"] + feed_region["y_max"]) / 2
            offsets["feed_x"] = x - right_hand.cpu().numpy()[0]
            offsets["feed_y"] = y - right_hand.cpu().numpy()[1]

    if offsets == {
        "stop_x": 52,
        "stop_y": 0,
        "feed_x": 45,
        "feed_y": -20,
    }:
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
