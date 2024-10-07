from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QFileDialog

from .tasks import *


class SetOffset:
    def __init__(self, offsets, pose_model, object_model, parent=None, timer=None):
        self.offsets = offsets
        self.pose_model = pose_model
        self.object_model = object_model
        self.parent = parent
        self.timer = timer

    def set_offsets(self):

        self.timer.stop()

        to_adj = True
        file_path = None

        if to_adj:
            print("Selecting a picture...")
            file_path = QFileDialog.getOpenFileName(
                self.parent, dir="images", filter="*.jpg;*.png;*.jpeg"
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
        return self.offsets
