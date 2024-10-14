import cv2
from cv2.typing import MatLike
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
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
        self.pose_model = YOLO(OBJECT_MODEL)
        self.object_model = YOLO(POSE_MODEL)
        self.offsets = DEFAULT_OFFSETS.copy()
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
        self.timer2.stop()
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
        self.offsets = adj_offsets(to_adj, self.offsets, file_path)

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
            image, behavior = predict_multiple(file, self.offsets)
        else:
            image, behavior = predict_single(file, self.offsets)
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

        return image

    # 圖片開啟
    def open_picture(self):
        self.camera_on = 0
        self.change_mode()

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
        image = self.test(file_path)
        self.output_media.setPixmap(QPixmap.fromImage(convert2QImage(image)))

    # 影片
    def open_video(self):
        self.camera_on = 0
        self.change_mode()

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
            image = self.test(frame)
            self.output_media.setPixmap(QPixmap.fromImage(convert2QImage(image)))

    def test_camera2(self):
        ret, frame = self.video2.read()
        if not ret:
            self.timer2.stop()
        else:
            print("Testing video2...")
            image = self.test(frame)
            self.input_media.setPixmap(QPixmap.fromImage(convert2QImage(image)))

    # 相機
    def open_camera(self):
        self.camera_on = 1
        self.change_mode()

        self.timer.stop()
        print("Turning on the camera...")
        camera_num = 0
        self.video = cv2.VideoCapture(camera_num)
        if not self.video.isOpened():
            print("No camera turned on.")
            return
        video_fps = self.video.get(cv2.CAP_PROP_FPS)
        if video_fps == 0:
            video_fps = 60
        self.timer.setInterval(1000 / video_fps)
        self.get_input_ratio()
        self.timer.start()

    def open_camera2(self):
        self.timer2.stop()
        print("Turning on second camera...")
        camera_num = 1  # 第二个摄像头
        self.video2 = cv2.VideoCapture(camera_num)
        self.timer2.start()
        if not self.video2.isOpened():
            print("No second camera turned on.")
            return

    def stop_test(self):
        self.timer.stop()
        self.timer2.stop()
        print("STOP!")

    def camera_button_function(self):
        if self.camera_on == 1:
            self.change_mark_output()
        else:
            self.open_camera()
            # self.open_camera2()

    # 連結按鈕
    def bind_slots(self):
        self.button_picture.clicked.connect(self.open_picture)
        self.button_video.clicked.connect(self.open_video)
        self.button_camera.clicked.connect(self.camera_button_function)
        self.button_offset.clicked.connect(self.open_offset_slider)
        self.button_stop.clicked.connect(self.stop_test)

        self.camera_change1.clicked.connect(self.change_camera_1)
        self.camera_change2.clicked.connect(self.change_camera_2)
        self.camera_change3.clicked.connect(self.change_camera_3)
        self.camera_change4.clicked.connect(self.change_camera_4)

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
