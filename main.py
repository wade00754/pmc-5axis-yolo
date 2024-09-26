import sys
import cv2
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QDialog,
    QWidget,
    QDialogButtonBox,
)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QTimer, Qt
from ultralytics import YOLO
from ui.main_window_ui import Ui_MainWindow
from ui.ask_offset_ui import Ui_Dialog
import utils


def convert2QImage(img):
    height, width, channel = img.shape
    bytes_per_line = width * channel
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)


class AskInitOffset(QDialog):
    def __init__(self, set_offsets_callback):
        super(AskInitOffset, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.set_offsets_callback = set_offsets_callback

        self.ui.AskOffsetButton.accepted.connect(self.on_accept)
        self.ui.AskOffsetButton.rejected.connect(self.on_reject)

    def on_accept(self):
        if self.set_offsets_callback:
            self.set_offsets_callback()
        self.accept()

    def on_reject(self):
        self.reject()


class MainWindow(QMainWindow, Ui_MainWindow):
    # 啟動
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.pose_model = YOLO("yolov8n-pose.pt")
        self.object_model = YOLO("best.pt")
        self.offsets = {
            "stop_x": 52,
            "stop_y": 0,
            "feed_x": 45,
            "feed_y": -20,
        }
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.video = None
        self.bind_slots()
        self.ask_for_offsets()
        self.Label_HandStop_Status.setText("Hand on Stop: N/A")
        self.Label_HandFeed_Status.setText("Hand on Feed: N/A")

    def ask_for_offsets(self):
        dialog = AskInitOffset(self.set_offsets)
        dialog.exec()

    # 設定手腕調整值
    def set_offsets(self):
        self.timer.stop()
        # TODO: implement adj_offsets UI
        # TODO: objects範圍寬限值
        to_adj = True
        file_path = None
        if to_adj:
            print("Selecting a picture...")
            file_path = QFileDialog.getOpenFileName(
                self, dir="images", filter="*.jpg;*.png;*.jpeg"
            )
            if file_path[0]:
                file_path = file_path[0]
                print(f"Opened picture: {file_path}")
            else:
                to_adj = False
                print("No picture selected.")
        self.offsets = utils.adj_offsets(
            to_adj, self.offsets, file_path, self.pose_model, self.object_model
        )

    # 圖片開啟
    def open_picture(self):
        self.timer.stop()
        print("Selecting a picture...")
        file_path = QFileDialog.getOpenFileName(
            self, dir="images", filter="*.jpg;*.png;*.jpeg"
        )
        if file_path[0]:
            file_path = file_path[0]
            print(f"Opened picture: {file_path}")
            self.test_picture(file_path)
        else:
            print("No picture selected.")

    def test_picture(self, file_path):
        self.input_media.setPixmap(QPixmap(file_path))
        print("Testing picture...")
        image, is_hand_on_stop, is_hand_on_feed = utils.predict_single(
            file_path, self.pose_model, self.object_model, self.offsets
        )
        print(f"Is hand on stop button: {is_hand_on_stop}")
        print(f"Is hand on feed button: {is_hand_on_feed}")
        self.Label_HandStop_Status.setText(
            f"Hand on Stop: {'Yes' if is_hand_on_stop else 'No'}"
        )
        self.Label_HandFeed_Status.setText(
            f"Hand on Feed: {'Yes' if is_hand_on_feed else 'No'}"
        )
        self.output_media.setPixmap(QPixmap.fromImage(convert2QImage(image)))

    # 影片
    def open_video(self):
        self.timer.stop()
        print("Selecting a video...")
        file_path = QFileDialog.getOpenFileName(self, dir="images", filter="*.mp4")
        if file_path[0]:
            file_path = file_path[0]
            print(f"Opened video: {file_path}")
            self.video = cv2.VideoCapture(file_path)
            video_fps = self.video.get(cv2.CAP_PROP_FPS)
            self.timer.setInterval(1000 / video_fps)
            self.timer.start()
        else:
            print("No video selected.")

    def test_video(self):
        ret, frame = self.video.read()
        if not ret:
            self.timer.stop()
        else:
            self.input_media.setPixmap(QPixmap.fromImage(convert2QImage(frame)))
            print("Testing video...")
            image, is_hand_on_stop, is_hand_on_feed = utils.predict_single(
                frame, self.pose_model, self.object_model, self.offsets
            )
            print(f"Is hand on stop button: {is_hand_on_stop}")
            print(f"Is hand on feed button: {is_hand_on_feed}")
            self.Label_HandStop_Status.setText(
                f"Hand on Stop: {'Yes' if is_hand_on_stop else 'No'}"
            )
            self.Label_HandFeed_Status.setText(
                f"Hand on Feed: {'Yes' if is_hand_on_feed else 'No'}"
            )
            self.output_media.setPixmap(QPixmap.fromImage(convert2QImage(image)))

    # 相機
    def open_camera(self):
        self.timer.stop()
        print("camera open")
        camera_num = 0
        self.video = cv2.VideoCapture(camera_num)
        if not self.video.isOpened():
            print("No camera opening.")
            return
        video_fps = self.video.get(cv2.CAP_PROP_FPS)
        if video_fps == 0:
            video_fps = 60
        self.timer.setInterval(1000 / video_fps)
        self.timer.start()

    def test_camera(self):
        ret, frame = self.video.read()
        if not ret:
            self.timer.stop()
        else:
            self.input_media.setPixmap(QPixmap.fromImage(convert2QImage(frame)))
            print("Predecting camera...")
            results = self.model(frame)
            image = results[0].plot()
            self.output_media.setPixmap(QPixmap.fromImage(convert2QImage(image)))

    def stop_test(self):
        self.timer.stop()
        print("STOP!")

    # 連結按鈕
    def bind_slots(self):
        self.button_picture.clicked.connect(self.open_picture)
        self.button_video.clicked.connect(self.open_video)
        self.button_camera.clicked.connect(self.open_camera)
        self.button_offset.clicked.connect(self.set_offsets)
        self.button_stop.clicked.connect(self.stop_test)
        self.timer.timeout.connect(self.test_video)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
