import sys
import cv2
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QTimer
from main_window_ui import Ui_MainWindow
from ultralytics import YOLO


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
        self.model = YOLO("best.pt")
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
            qimage = self.test_picture(file_path)
            self.input_media.setPixmap(QPixmap(file_path))
            self.output_media.setPixmap(QPixmap.fromImage(qimage))
        else:
            print("No picture selected.")

    def test_picture(self, file_path):
        print("Predicting picture...")
        results = self.model(file_path)
        image = results[0].plot()
        return convert2QImage(image)

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
            print("Predicting video...")
            results = self.model(frame)
            image = results[0].plot()
            self.output_media.setPixmap(QPixmap.fromImage(convert2QImage(image)))

    #相機
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
        self.timer.setInterval(1000/video_fps)
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




    # 連結按鈕
    def bind_slots(self):
        self.button_picture.clicked.connect(self.open_picture)
        self.button_video.clicked.connect(self.open_video)
        self.button_camera.clicked.connect(self.open_camera)
        self.timer.timeout.connect(self.test_video)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()