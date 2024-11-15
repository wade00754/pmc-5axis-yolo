import re
from math import e

import cv2
from cv2.typing import MatLike
from playsound import playsound
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)
from ultralytics import YOLO

from .settings import DEFAULT_OFFSETS, OBJECT_MODEL, POSE_MODEL
from .tasks import OffsetSlider, adj_offsets, predict_multiple, predict_single
from .ui.ask_offset_ui import Ui_Dialog
from .ui.main_window_ui import Ui_MainWindow
from .utils import convert2QImage


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
        self.pose_model = YOLO(POSE_MODEL)
        self.object_model = YOLO(OBJECT_MODEL)
        self.offsets = DEFAULT_OFFSETS.copy()

        self.video_timer = QTimer()
        self.camera_timer = QTimer()
        self.timers = [self.video_timer, self.camera_timer]
        for timer in self.timers:
            timer.setInterval(1000)
        self.video = None
        # self.video2 = None
        self.camera_on = 0

        self.dialog = None
        self.aspect_ratio = 16 / 9
        self.bind_slots()
        self.ask_for_offsets()
        self.Label_HandStop_Status.setText("Hand on Stop: N/A")
        self.Label_HandFeed_Status.setText("Hand on Feed: N/A")
        self.Label_KnifeBaseCollid_status.setText("Knife Base Collided: N/A")

        self.now_step = 1
        self.steps_file = "SOP_step.txt"
        self.steps_totals = self.get_step_count()
        self.update_step_label()

        self.labels = [
            self.input_media,
            self.output_media,
            self.output_media2,
            self.output_media3,
            self.output_media4,
        ]

        self.camera_change_button = [
            self.camera_change1,
            self.camera_change2,
            self.camera_change3,
            self.camera_change4,
        ]

        self.change_mode()

    # ~~~~~~~~~~~~~~~~~~~~~~step labelr~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def update_step_label(self):

        step_descriptions = [
            (
                self.get_step_description(self.now_step - 1)
                if self.now_step > 1
                else "N/A"
            ),  # 上一步骤
            self.get_step_description(self.now_step),  # 当前步骤
            (
                self.get_step_description(self.now_step + 1)
                if self.now_step < self.steps_totals
                else "N/A"
            ),  # 下一步骤
        ]

        self.label_step_last.setText(f"last：{step_descriptions[0]}")
        self.label_step_now.setText(f"now：{step_descriptions[1]}")
        self.label_step_next.setText(f"next：{step_descriptions[2]}")

    def get_step_description(self, step_number):
        try:
            with open(self.steps_file, "r", encoding="utf-8") as file:
                steps = file.readlines()
                if 0 < step_number <= len(steps):
                    return steps[step_number - 1].strip()
                else:
                    return "N/A"
        except FileNotFoundError:
            return "FileOpenError"

    def step_ToNext(self):
        if self.now_step < self.steps_totals:
            self.now_step += 1
            self.update_step_label()

    def step_ToPrevious(self):
        if self.now_step > 1:
            self.now_step -= 1
            self.update_step_label()

    def get_step_count(self):
        with open(self.steps_file, "r") as file:
            steps = file.readlines()
        return len(steps)

    # ~~~~~~~~~~~~~~~~~~~~~~     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def ask_for_offsets(self):
        dialog = AskInitOffset(self.set_offsets)
        dialog.exec()

    def change_mode(self):
        self.output_media2.setVisible(self.camera_on)
        self.output_media3.setVisible(self.camera_on)
        self.output_media4.setVisible(self.camera_on)
        for button in self.camera_change_button:
            button.setVisible(self.camera_on)
        self.update_label_size()
        for timer in self.timers:
            timer.stop()

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
        for timer in self.timers:
            timer.stop()
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

    def test(
        self, file: str | MatLike | list[str | MatLike]
    ) -> MatLike | list[MatLike]:
        """
        Test an image or a single video frame and return the result.

        Args:
            file (str | MatLike | list[str | MatLike]): The file path or the image to test. It can also be a list of file paths or images.

        Returns:
            MatLike | list[MatLike]: The processed image or a list of processed images.
        """
        if isinstance(file, list):
            image, behavior = predict_multiple(
                file, self.pose_model, self.object_model, self.offsets
            )
        else:
            image, behavior = predict_single(
                file, self.pose_model, self.object_model, self.offsets
            )
        print(f"Is hand on stop button: {behavior.is_hand_on_stop.name}")
        print(f"Is hand on feed button: {behavior.is_hand_on_feed.name}")
        print(f"Does knife collide with base: {behavior.is_knife_base_collided.name}")
        self.Label_HandStop_Status.setText(
            f"Hand on Stop: {behavior.is_hand_on_stop.name}"
        )
        self.Label_HandFeed_Status.setText(
            f"Hand on Feed: {behavior.is_hand_on_feed.name}"
        )
        self.Label_KnifeBaseCollid_status.setText(
            f"Knife Base Collided: {behavior.is_knife_base_collided.name}"
        )
        if behavior.is_hand_on_stop.name == "NO":
            print("Hand not on stop button! Playing sound alert.")
            playsound("warning.mp3")
        if behavior.is_hand_on_feed.name == "NO":
            print("Hand not on stop button! Playing sound alert.")
            playsound("warning.mp3")

        return image

    # 圖片開啟
    def open_picture(self):
        self.camera_on = 0
        self.change_mode()

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
        image = self.test(file_path)
        self.output_media.setPixmap(QPixmap.fromImage(convert2QImage(image)))

    # 影片
    def open_video(self):
        self.camera_on = 0
        self.change_mode()

        print("Selecting a video...")
        file_path = QFileDialog.getOpenFileName(self, dir="images", filter="*.mp4")
        if file_path[0]:
            file_path = file_path[0]
            print(f"Opened video: {file_path}")
            self.video = cv2.VideoCapture(file_path)
            video_fps = self.video.get(cv2.CAP_PROP_FPS)
            self.video_timer.setInterval(1000 / video_fps)
            self.get_input_ratio()
            self.video_timer.start()
        else:
            print("No video selected.")

    def test_video(self):
        ret, frame = self.video.read()
        if not ret:
            self.video_timer.stop()
        else:
            image = self.test(frame)
            print("Testing video...")
            self.input_media.setPixmap(QPixmap.fromImage(convert2QImage(frame)))
            self.output_media.setPixmap(QPixmap.fromImage(convert2QImage(image)))

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~camera test~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def open_camera(self):
        self.camera_on = 1
        self.change_mode()

        # turn om camera from 0 to 4
        self.video = []
        for i in range(5):
            print(f"Turning on camera {i}...")
            self.video.append(cv2.VideoCapture(i))
            if not self.video[i].isOpened():
                print(f"Camera {i} did not turn on.")
        video_fps = self.video[0].get(cv2.CAP_PROP_FPS)
        if video_fps == 0:
            video_fps = 60
        self.camera_timer.setInterval(1000 / video_fps)
        self.get_input_ratio()
        self.camera_timer.start()

    def test_camera(self):
        frames = []
        for idx, video in enumerate(self.video):
            ret, frame = video.read()

            if not ret:
                if idx == 0:
                    self.camera_timer.stop()
                    return
            else:
                frames.append(frame)
                print(f"Appended camera {idx}...")

        images = self.test(frames)
        for idx, image in enumerate(images):
            if idx == 0:
                self.input_media.setPixmap(QPixmap.fromImage(convert2QImage(image)))
            elif idx == 1:
                self.output_media.setPixmap(QPixmap.fromImage(convert2QImage(image)))
            elif idx == 2:
                self.output_media2.setPixmap(QPixmap.fromImage(convert2QImage(image)))
            elif idx == 3:
                self.output_media3.setPixmap(QPixmap.fromImage(convert2QImage(image)))
            elif idx == 4:
                self.output_media4.setPixmap(QPixmap.fromImage(convert2QImage(image)))

    def stop_test(self):
        for timer in self.timers:
            timer.stop()
        print("STOP!")

    # 連結按鈕
    def bind_slots(self):
        self.button_picture.clicked.connect(self.open_picture)
        self.button_video.clicked.connect(self.open_video)
        self.button_camera.clicked.connect(self.open_camera)
        self.button_offset.clicked.connect(self.open_offset_slider)
        self.button_stop.clicked.connect(self.stop_test)

        self.camera_change1.clicked.connect(self.change_camera_1)
        self.camera_change2.clicked.connect(self.change_camera_2)
        self.camera_change3.clicked.connect(self.change_camera_3)
        self.camera_change4.clicked.connect(self.change_camera_4)

        self.button_step_last.clicked.connect(self.step_ToPrevious)
        self.button_step_next.clicked.connect(self.step_ToNext)

        self.video_timer.timeout.connect(self.test_video)
        self.camera_timer.timeout.connect(self.test_camera)

    # 獲得input長寬比
    def get_input_ratio(self):
        if isinstance(self.video, list):
            frame_width = int(self.video[0].get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(self.video[0].get(cv2.CAP_PROP_FRAME_HEIGHT))
        else:
            frame_width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.aspect_ratio = frame_width / frame_height
        self.update_label_size()

    # 當視窗大小改變時呼叫
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_label_size()

    def update_label_size(self):
        height = self.size().height()
        new_width = height * self.aspect_ratio * 0.6
        new_height = height * 0.6

        if self.camera_on == 0:
            self.input_media.setFixedSize(int(new_width), int(new_height))
            self.output_media.setFixedSize(int(new_width), int(new_height))
        elif self.camera_on == 1:
            output_width = int(new_width / 2)
            output_height = int(new_height / 2)

            # 为 output_media 和其他 QLabel 设置尺寸
            for label in self.labels:
                label.setFixedSize(output_width, output_height)

            # 检查各个标签是否在 gridLayout_2 中，并根据情况更新大小
            for label in self.labels:
                if self.gridLayout_2.indexOf(label) != -1:
                    label.setFixedSize(int(new_width), int(new_height))

    def change_mark_output(self):
        self.gridLayout_2.removeWidget(self.input_media)
        self.gridLayout.addWidget(self.input_media, 0, 0, 1, 1)
        self.gridLayout.removeWidget(self.output_media)
        self.gridLayout_2.addWidget(self.output_media, 2, 1, 1, 1)
        self.update_label_size()

    def change_camera_1(self):
        targetL = None
        targetR = None

        for Left in self.labels:
            if self.gridLayout_2.indexOf(Left) != -1:
                targetL = Left

        #  gridLayout 的 (0, 0, 1, 1) 位置上
        if self.gridLayout.itemAtPosition(0, 0) is not None:
            widget_at_0_0 = self.gridLayout.itemAtPosition(0, 0).widget()
            if widget_at_0_0 in self.labels:
                targetR = widget_at_0_0

        if targetL is not None and targetR is not None:
            self.gridLayout_2.removeWidget(targetL)
            self.gridLayout_2.addWidget(targetR, 2, 1, 1, 1)
            self.gridLayout.removeWidget(targetR)

            self.gridLayout.addWidget(targetL, 0, 0, 1, 1)
            self.update_label_size()

    def change_camera_2(self):
        targetL = None
        targetR = None

        for Left in self.labels:
            if self.gridLayout_2.indexOf(Left) != -1:
                targetL = Left

        #  gridLayout 的 (0, 0, 1, 1) 位置上
        if self.gridLayout.itemAtPosition(0, 0) is not None:
            widget_at_0_0 = self.gridLayout.itemAtPosition(0, 1).widget()
            if widget_at_0_0 in self.labels:
                targetR = widget_at_0_0

        if targetL is not None and targetR is not None:
            self.gridLayout_2.removeWidget(targetL)
            self.gridLayout_2.addWidget(targetR, 2, 1, 1, 1)
            self.gridLayout.removeWidget(targetR)

            self.gridLayout.addWidget(targetL, 0, 1, 1, 1)
            self.update_label_size()

    def change_camera_3(self):
        targetL = None
        targetR = None

        for Left in self.labels:
            if self.gridLayout_2.indexOf(Left) != -1:
                targetL = Left

        #  gridLayout 的 (0, 0, 1, 1) 位置上
        if self.gridLayout.itemAtPosition(0, 0) is not None:
            widget_at_0_0 = self.gridLayout.itemAtPosition(1, 0).widget()
            if widget_at_0_0 in self.labels:
                targetR = widget_at_0_0

        if targetL is not None and targetR is not None:
            self.gridLayout_2.removeWidget(targetL)
            self.gridLayout_2.addWidget(targetR, 2, 1, 1, 1)
            self.gridLayout.removeWidget(targetR)

            self.gridLayout.addWidget(targetL, 1, 0, 1, 1)
            self.update_label_size()

    def change_camera_4(self):
        targetL = None
        targetR = None

        for Left in self.labels:
            if self.gridLayout_2.indexOf(Left) != -1:
                targetL = Left

        #  gridLayout 的 (0, 0, 1, 1) 位置上
        if self.gridLayout.itemAtPosition(0, 0) is not None:
            widget_at_0_0 = self.gridLayout.itemAtPosition(1, 1).widget()
            if widget_at_0_0 in self.labels:
                targetR = widget_at_0_0

        if targetL is not None and targetR is not None:
            self.gridLayout_2.removeWidget(targetL)
            self.gridLayout_2.addWidget(targetR, 2, 1, 1, 1)
            self.gridLayout.removeWidget(targetR)

            self.gridLayout.addWidget(targetL, 1, 1, 1, 1)
            self.update_label_size()
