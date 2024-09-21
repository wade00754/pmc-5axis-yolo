import sys
import cv2
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QTimer
from ui.main_window_ui import Ui_MainWindow
from ultralytics import YOLO
from utils.predict import predict_single


def convert2QImage(img):
    height, width, channel = img.shape
    bytes_per_line = width * channel
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)


class MainWindow(QMainWindow, Ui_MainWindow):
    # 啟動
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.pose_model = YOLO("yolov8n-pose.pt")
        self.object_model = YOLO("best.pt")
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.video = None
        self.bind_slots()

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
        # TODO: implement adj_value function & Objects範圍寬限值
        adj_value = [52, 0, 45, -20]  # adj_value=[stop_x, stop_y, feed_x, feed_y]
        image, is_hand_on_stop, is_hand_on_feed = predict_single(
            file_path, self.pose_model, self.object_model, adj_value
        )
        print(f"Is hand on stop button: {is_hand_on_stop}")
        print(f"Is hand on feed button: {is_hand_on_feed}")
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
            adj_value = [52, 0, 45, -20]  # adj_value=[stop_x, stop_y, feed_x, feed_y]
            image, is_hand_on_stop, is_hand_on_feed = predict_single(
                frame, self.pose_model, self.object_model, adj_value
            )
            print(f"Is hand on stop button: {is_hand_on_stop}")
            print(f"Is hand on feed button: {is_hand_on_feed}")
            self.output_media.setPixmap(QPixmap.fromImage(convert2QImage(image)))

    # 連結按鈕
    def bind_slots(self):
        self.button_picture.clicked.connect(self.open_picture)
        self.button_video.clicked.connect(self.open_video)
        self.timer.timeout.connect(self.test_video)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
