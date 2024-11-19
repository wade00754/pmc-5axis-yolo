import random
from dataclasses import dataclass

import cv2
import numpy as np
from cv2.typing import MatLike
from PySide6.QtGui import QImage
from ultralytics.engine.results import Results


def convert2QImage(img: MatLike) -> QImage:
    height, width, channel = img.shape
    bytes_per_line = width * channel
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return QImage(img.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)


# 定義一個函數來生成隨機顏色
def generate_colors(num_classes):
    random.seed(42)  # 設定隨機種子以確保顏色一致
    colors = {}
    for i in range(num_classes):
        colors[i] = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
    return colors


# 計算兩點間的歐幾里得距離
def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


# 計算三個點之間的夾角
def calculate_angle(A, B, C):
    ba = np.array([A[0] - B[0], A[1] - B[1]])
    bc = np.array([C[0] - B[0], C[1] - B[1]])
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)


@dataclass(frozen=True)
class Region:
    x_min: int
    x_max: int
    y_min: int
    y_max: int


def extract_object_regions(
    object_result: Results, target_classes: list[str]
) -> dict[str, Region]:
    """從物件偵測結果中提取指定類別的範圍（bounding boxes）."""
    regions = {class_name: None for class_name in target_classes}

    for detection in object_result.boxes:
        # 獲取偵測框的座標
        x1, y1, x2, y2 = map(int, detection.xyxy[0].tolist())

        # 獲取物件的類別編號
        class_id = int(detection.cls[0])

        # 獲取物件的類別名稱
        class_name = object_result.names[class_id]

        # 如果類別名稱符合目標類別，記錄其範圍
        if class_name in target_classes:
            regions[class_name] = Region(x1, x2, y1, y2)

    return regions
