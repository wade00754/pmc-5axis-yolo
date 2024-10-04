import sys

import cv2
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QMainWindow,
    QWidget,
)
from ultralytics import YOLO

from .offset_slider import OffsetSlider
from .ui.ask_offset_ui import Ui_Dialog
from .ui.main_window_ui import Ui_MainWindow
from .utils import *


def convert2QImage(img):
    height, width, channel = img.shape
    bytes_per_line = width * channel
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return QImage(img.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)


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
    NowOffset = Signal(float, float, float, float)

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
        self.timer2 = QTimer()
        self.timer.setInterval(1000)
        self.video = None
        self.video2 = None
        self.camera_on = 0
        self.dialog = None
        self.aspect_ratio = 16 / 9
        self.bind_slots()
        self.ask_for_offsets()
        self.Label_HandStop_Status.setText("Hand on Stop: N/A")
        self.Label_HandFeed_Status.setText("Hand on Feed: N/A")
        self.Label_KnifeBaseCollid_status.setText("Knife Base Collided: N/A")

    def ask_for_offsets(self):
        dialog = AskInitOffset(self.set_offsets)
        dialog.exec()

    # ~~~~~~~~~~~~~~~~~~~~~~offset_slider~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def open_offset_slider(self):
        self.dialog = OffsetSlider(
            self.offsets["stop_x"],
            self.offsets["stop_y"],
            self.offsets["feed_x"],
            self.offsets["feed_y"],
        )
        self.dialog.offset_changed.connect(self.update_offsets)
        self.dialog.cancel_signal.connect(self.reset_offsets)
        self.dialog.PictureSetCalled.connect(self.closedialog)
        self.dialog.exec()

    def update_offsets(self, stop_x, stop_y, feed_x, feed_y):
        self.offsets = {
            "stop_x": stop_x,
            "stop_y": stop_y,
            "feed_x": feed_x,
            "feed_y": feed_y,
        }
        print(
            "Offsets updated:",
            " ".join(f"[{key}: {self.offsets[key]:.3f}]" for key in self.offsets),
        )

    def reset_offsets(self, stop_x, stop_y, feed_x, feed_y):
        self.offsets = {
            "stop_x": stop_x,
            "stop_y": stop_y,
            "feed_x": feed_x,
            "feed_y": feed_y,
        }
        print(
            "Offsets reset to initial values:",
            " ".join(f"[{key}: {self.offsets[key]:.3f}]" for key in self.offsets),
        )

    def closedialog(self):
        self.dialog.close()
        self.set_offsets()
        self.open_offset_slider()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
        self.offsets = adj_offsets(
            to_adj, self.offsets, file_path, self.pose_model, self.object_model
        )

    def test_single(self, file):
        image, is_hand_on_stop, is_hand_on_feed, is_knife_base_collided = (
            predict_single(file, self.pose_model, self.object_model, self.offsets)
        )
        print(f"Is hand on stop button: {is_hand_on_stop.name}")
        print(f"Is hand on feed button: {is_hand_on_feed.name}")
        print(f"Does knife collide with base: {is_knife_base_collided.name}")
        self.Label_HandStop_Status.setText(f"Hand on Stop: {is_hand_on_stop.name}")
        self.Label_HandFeed_Status.setText(f"Hand on Feed: {is_hand_on_feed.name}")
        self.Label_KnifeBaseCollid_status.setText(
            f"Knife Base Collided: {is_knife_base_collided.name}"
        )

        return image

    # 圖片開啟
    def open_picture(self):
        self.camera_on = 0
        self.timer.stop()
        self.timer2.stop()
        print("Selecting a picture...")
        file_path = QFileDialog.getOpenFileName(
            self, dir="images", filter="*.jpg;*.png;*.jpeg"
        )
        if file_path[0]:
            file_path = file_path[0]
            print(f"Opened picture: {file_path}")

            img = cv2.imread(file_path)
            frame_height, frame_width, _ = img.shape
            self.aspect_ratio = frame_width / frame_height
            self.update_label_size()

            self.test_picture(file_path)
        else:
            print("No picture selected.")

    def test_picture(self, file_path):
        self.input_media.setPixmap(QPixmap(file_path))
        print("Testing picture...")
        image = self.test_single(file_path)
        self.output_media.setPixmap(QPixmap.fromImage(convert2QImage(image)))

    # 影片
    def open_video(self):
        self.camera_on = 0
        self.timer.stop()
        self.timer2.stop()
        print("Selecting a video...")
        file_path = QFileDialog.getOpenFileName(self, dir="images", filter="*.mp4")
        if file_path[0]:
            file_path = file_path[0]
            print(f"Opened video: {file_path}")
            self.video = cv2.VideoCapture(file_path)
            video_fps = self.video.get(cv2.CAP_PROP_FPS)
            self.timer.setInterval(1000 / video_fps)
            self.get_input_ratio()
            self.timer.start()
        else:
            print("No video selected.")

    def test_video(self):
        ret, frame = self.video.read()
        if not ret:
            self.timer.stop()
        else:
            if self.camera_on == 0:
                self.input_media.setPixmap(QPixmap.fromImage(convert2QImage(frame)))
            print("Testing video...")
            image = self.test_single(frame)
            self.output_media.setPixmap(QPixmap.fromImage(convert2QImage(image)))

    def test_camera2(self):
        ret, frame = self.video2.read()
        if not ret:
            self.timer2.stop()
        else:
            print("Testing video2...")
            image = self.test_single(frame)
            self.input_media.setPixmap(QPixmap.fromImage(convert2QImage(image)))

    # 相機
    def open_camera(self):
        self.camera_on = 1
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
        self.get_input_ratio()
        self.timer.start()

    def open_camera2(self):
        print("Opening second camera...")
        camera_num = 1  # 第二个摄像头
        self.video2 = cv2.VideoCapture(camera_num)
        self.timer2.start()
        if not self.video2.isOpened():
            print("No second camera opening.")
            return

    def stop_test(self):
        self.timer.stop()
        print("STOP!")

    # 連結按鈕
    def bind_slots(self):
        self.button_picture.clicked.connect(self.open_picture)
        self.button_video.clicked.connect(self.open_video)
        self.button_camera.clicked.connect(self.open_camera)
        self.button_camera.clicked.connect(self.open_camera2)
        self.button_offset.clicked.connect(self.open_offset_slider)
        self.button_stop.clicked.connect(self.stop_test)
        self.timer.timeout.connect(self.test_video)
        self.timer2.timeout.connect(self.test_camera2)

    # 獲得input長寬比
    def get_input_ratio(self):
        frame_width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.aspect_ratio = frame_width / frame_height
        self.update_label_size()

    # 當視窗大小改變時呼叫
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_label_size()

    # 左右圖的新大小
    def update_label_size(self):
        height = self.size().height()
        new_width = height * self.aspect_ratio * 0.6
        new_height = height * 0.6
        self.input_media.setFixedSize(int(new_width), int(new_height))
        self.output_media.setFixedSize(int(new_width), int(new_height))
