import random
from calendar import c
from enum import Enum
from typing import Any

import cv2
from cv2.typing import MatLike
from ultralytics import YOLO
from ultralytics.engine.results import Results


class SafeState(Enum):
    NO = 0
    YES = 1
    UNDETECTED = 2


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


# 測試手部是否在按鈕上
def predict_safe(
    pose_results: list[Results], object_results: list[Results], offsets: dict
) -> tuple[SafeState, SafeState, SafeState]:
    # 獲取關鍵點 索引為: 9 是右手腕，10 是左手腕（根據 COCO 的姿態標註）
    keypoints = pose_results[0].keypoints.xy[0]

    # 取得右手與左手的座標 (x, y)
    if keypoints.numel() == 0:  # 沒有偵測到人
        person = False
    else:
        person = True
        left_hand = keypoints[9]  # (x, y) of left hand
        right_hand = keypoints[10]  # (x, y) of right hand

    # 初始化 Stop 和 Feed 按鈕的範圍變數及手是否在按鈕上的變數
    stop_region = None
    feed_region = None
    knife_region = None
    base_region = None
    is_hand_on_stop = SafeState.UNDETECTED
    is_hand_on_feed = SafeState.UNDETECTED
    is_knife_base_collided = SafeState.UNDETECTED

    # 遍歷每一個偵測結果來找到 stop、feed、knife 和 base 的範圍
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

        # 如果是 Knife，記錄其範圍
        if class_name == "knife":
            knife_region = {"x_min": x1, "x_max": x2, "y_min": y1, "y_max": y2}

        # 如果是 Base，記錄其範圍
        if class_name == "base":
            base_region = {"x_min": x1, "x_max": x2, "y_min": y1, "y_max": y2}

    # 判斷左手是否在 Stop 按鈕上
    if stop_region and person:
        if sum(left_hand.cpu().numpy()) == 0:  # 沒有偵測到左手
            is_hand_on_stop = SafeState.UNDETECTED
        else:
            left_hand_x = left_hand.cpu().numpy()[0] + offsets.get("stop_x", 0)
            left_hand_y = left_hand.cpu().numpy()[1] + offsets.get("stop_y", 0)
            is_hand_on_stop = (
                SafeState.YES
                if stop_region["x_min"] <= left_hand_x <= stop_region["x_max"]
                and stop_region["y_min"] <= left_hand_y <= stop_region["y_max"]
                else SafeState.NO
            )

    # 判斷右手是否在 Feed 按鈕上
    if feed_region and person:
        if sum(right_hand.cpu().numpy()) == 0:  # 沒有偵測到右手
            is_hand_on_feed = SafeState.UNDETECTED
        else:
            right_hand_x = right_hand.cpu().numpy()[0] + offsets.get("feed_x", 0)
            right_hand_y = right_hand.cpu().numpy()[1] + offsets.get("feed_y", 0)
            is_hand_on_feed = (
                SafeState.YES
                if feed_region["x_min"] <= right_hand_x <= feed_region["x_max"]
                and feed_region["y_min"] <= right_hand_y <= feed_region["y_max"]
                else SafeState.NO
            )

    # 判斷 Knife 是否碰到 Base
    if knife_region and base_region:
        is_knife_base_collided = (
            SafeState.YES
            if knife_region["y_max"] >= base_region["y_min"]  # -5 # 5 pixels tolerance
            and (
                base_region["x_min"] <= knife_region["x_min"] <= base_region["x_max"]
                or base_region["x_min"] <= knife_region["x_max"] <= base_region["x_max"]
            )
            else SafeState.NO
        )

    return is_hand_on_stop, is_hand_on_feed, is_knife_base_collided


# 測試單張影像
def predict_single(
    image: str | MatLike, pose_model: YOLO, object_model: YOLO, offsets: dict
) -> tuple[MatLike, SafeState, SafeState, SafeState]:
    # # 讀取影像
    # image_path = cv2.imread(image_path)

    # # 確認影像讀取成功
    # if image_path is None:
    #     raise ValueError(f"無法讀取影像：{image_path}")

    # ------------------------------
    # 步驟 1: 進行姿態估計
    # ------------------------------
    # 使用 YOLOv8n-pose 進行姿態估計
    print("Predicting pose...")
    pose_results = pose_model.predict(image, conf=0.4)

    # 繪製姿態估計結果
    pose_annotated_frame = pose_results[0].plot()

    # ------------------------------
    # 步驟 2: 進行物件偵測
    # ------------------------------
    # 使用你自訓練的物件偵測模型進行偵測
    print("Predicting objects...")
    object_results = object_model.predict(image, conf=0.3)

    # 獲取類別數量（假設類別編號從 0 開始連續編號）
    num_classes = len(object_model.names)
    colors = generate_colors(num_classes)

    # 獲取類別名稱
    class_names = object_model.names

    # 複製姿態估計的結果框架以進行繪製
    combined_frame = pose_annotated_frame.copy()

    # 遍歷每一個偵測結果
    for detection in object_results[0].boxes:
        # 獲取偵測框的座標
        x1, y1, x2, y2 = map(int, detection.xyxy[0].tolist())

        # 獲取物件的置信度
        confidence = detection.conf[0]

        # 獲取物件的類別編號
        class_id = int(detection.cls[0])

        # 獲取物件的類別名稱
        class_name = (
            class_names[class_id]
            if class_id < len(class_names)
            else f"class_{class_id}"
        )

        # 獲取對應的顏色
        color = colors[class_id]

        # 繪製偵測框
        cv2.rectangle(combined_frame, (x1, y1), (x2, y2), color, 2)

        # 準備顯示的文字（類別名稱和置信度）
        label = f"{class_name} {confidence:.2f}"

        # 計算文字的寬高以確保文字不會超出框架
        (text_width, text_height), _ = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
        )

        # 調整文字背景的位置以避免超出影像範圍
        text_y1 = y1 - text_height - 4 if y1 - text_height - 4 > 0 else y1

        # 繪製文字背景
        cv2.rectangle(
            combined_frame,
            (x1, text_y1),
            (x1 + text_width, text_y1 + text_height + 4),
            color,
            -1,
        )

        # 在框架上繪製文字
        cv2.putText(
            combined_frame,
            label,
            (x1, text_y1 + text_height + 2),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )

    is_hand_on_stop, is_hand_on_feed, is_knife_base_collided = predict_safe(
        pose_results, object_results, offsets
    )

    return combined_frame, is_hand_on_stop, is_hand_on_feed, is_knife_base_collided


def predict_multiple(
    images: list[str | MatLike], pose_model: YOLO, object_model: YOLO, offsets: dict
) -> tuple[list[MatLike], SafeState, SafeState, SafeState]:
    combined_frames = []
    is_hand_on_stop = SafeState.UNDETECTED
    is_hand_on_feed = SafeState.UNDETECTED
    is_knife_base_collided = SafeState.UNDETECTED

    for image in images:
        combined_frame, hand_on_stop, hand_on_feed, knife_base_collided = (
            predict_single(image, pose_model, object_model, offsets)
        )
        combined_frames.append(combined_frame)

        if hand_on_stop != SafeState.UNDETECTED:
            if is_hand_on_stop == SafeState.UNDETECTED:
                is_hand_on_stop = hand_on_stop
            else:
                is_hand_on_stop = is_hand_on_stop and hand_on_stop

        if hand_on_feed != SafeState.UNDETECTED:
            if is_hand_on_feed == SafeState.UNDETECTED:
                is_hand_on_feed = hand_on_feed
            else:
                is_hand_on_feed = is_hand_on_feed and hand_on_feed

        if knife_base_collided != SafeState.UNDETECTED:
            if is_knife_base_collided == SafeState.UNDETECTED:
                is_knife_base_collided = knife_base_collided
            else:
                is_knife_base_collided = is_knife_base_collided or knife_base_collided

    return combined_frames, is_hand_on_stop, is_hand_on_feed, is_knife_base_collided


# # ------------------------------
# # 步驟 3: 顯示最終結果
# # ------------------------------
# # 調整視窗大小以適應顯示
# cv2.namedWindow("Pose Estimation and Object Detection Combined", cv2.WINDOW_NORMAL)
# cv2.imshow("Pose Estimation and Object Detection Combined", combined_frame)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.imwrite("output.jpg", combined_frame)
