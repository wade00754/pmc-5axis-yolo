from dataclasses import dataclass, fields
from enum import Enum

import cv2
from cv2.typing import MatLike
from torch import Tensor
from ultralytics import YOLO
from ultralytics.engine.results import Results

from ..settings import (
    ARM_ANGLE_THRESHOLD,
    ARM_BEND_THRESHOLD,
    ARM_STRETCH_THRESHOLD,
    BUTTON_THRESHOLD,
    LIE_THRESHOLD,
    PREDICT_VERBOSE,
)
from ..utils import (
    calculate_angle,
    calculate_distance,
    extract_object_regions,
    generate_colors,
)


class SafeState(Enum):
    NO = 0
    YES = 1
    UNDETECTED = 2


class PoseState(Enum):
    STAND = "Standing"
    ARM_STRETCH = "Arm Stretching"
    ARM_BEND = "Arm Bending"
    LIE = "Lying"
    UNKNOWN = "Unknown"


@dataclass
class Behavior:
    is_hand_on_stop: SafeState = SafeState.UNDETECTED
    is_hand_on_feed: SafeState = SafeState.UNDETECTED
    is_knife_base_collided: SafeState = SafeState.UNDETECTED
    human_pose: PoseState = PoseState.UNKNOWN


def classify_pose(keypoints: Tensor) -> PoseState:
    left_shoulder = keypoints[5].tolist()
    right_shoulder = keypoints[6].tolist()
    left_elbow = keypoints[7].tolist()
    right_elbow = keypoints[8].tolist()
    left_wrist = keypoints[9].tolist()
    right_wrist = keypoints[10].tolist()
    left_hip = keypoints[11].tolist()
    right_hip = keypoints[12].tolist()
    left_knee = keypoints[13].tolist()
    right_knee = keypoints[14].tolist()

    # 計算平均肩膀、臀部、膝蓋的 y 座標
    avg_hip_y = (
        (left_hip[1] + right_hip[1]) / 2 if left_hip[1] != 0 and right_hip[1] != 0 else left_hip[1] or right_hip[1]
    )
    avg_knee_y = (
        (left_knee[1] + right_knee[1]) / 2
        if left_knee[1] != 0 and right_knee[1] != 0
        else left_knee[1] or right_knee[1]
    )
    avg_shoulder_y = (
        (left_shoulder[1] + right_shoulder[1]) / 2
        if left_shoulder[1] != 0 and right_shoulder[1] != 0
        else left_shoulder[1] or right_shoulder[1]
    )

    # 左右手伸直判斷
    left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
    # left_distance = calculate_distance(left_wrist, left_shoulder)
    right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
    # right_distance = calculate_distance(right_wrist, right_shoulder)

    # 判斷蹲下或躺下
    if (avg_hip_y != 0 and avg_shoulder_y != 0 and avg_hip_y - avg_shoulder_y < LIE_THRESHOLD) or (
        avg_knee_y != 0 and avg_hip_y != 0 and avg_knee_y - avg_hip_y < LIE_THRESHOLD
    ):
        return PoseState.LIE
    # 判斷手臂伸展或彎曲
    if (left_angle > ARM_ANGLE_THRESHOLD or right_angle > ARM_ANGLE_THRESHOLD) and (
        (left_wrist[1] != 0 and (avg_hip_y == 0 or avg_hip_y - left_wrist[1] > ARM_STRETCH_THRESHOLD))
        or (right_wrist[1] != 0 and (avg_hip_y == 0 or avg_hip_y - right_wrist[1] > ARM_STRETCH_THRESHOLD))
    ):
        return PoseState.ARM_STRETCH
    elif (left_wrist[1] != 0 and (avg_hip_y == 0 or avg_hip_y - left_wrist[1] > ARM_BEND_THRESHOLD)) or (
        right_wrist[1] != 0 and (avg_hip_y == 0 or avg_hip_y - right_wrist[1] > ARM_BEND_THRESHOLD)
    ):
        return PoseState.ARM_BEND
    # 判斷站立
    if (avg_hip_y != 0 and avg_shoulder_y != 0 and avg_hip_y > avg_shoulder_y) and (
        avg_knee_y != 0 and avg_hip_y != 0 and avg_knee_y > avg_hip_y
    ):
        return PoseState.STAND

    return PoseState.UNKNOWN


# 測試安全行為 (假設畫面中只有一個人)
def predict_safe(pose_results: list[Results], object_results: list[Results], offsets: dict) -> Behavior:
    # 初始化行為
    behavior = Behavior()
    single = len(pose_results) == 1 or len(object_results) == 1
    # 0號機處理人體姿態，1號機處理人體上半身及控制器，2號機處理底座及刀具
    for idx, (pose_result, object_result) in enumerate(zip(pose_results, object_results)):
        # 獲取關鍵點 索引為: 9 是右手腕，10 是左手腕（根據 COCO 的姿態標註）
        keypoints = pose_result.keypoints

        # 取得右手與左手的座標 (x, y)
        if keypoints.xy[0].numel() == 0:  # 沒有偵測到人
            person = False
        else:
            person = True
            left_hand = keypoints.xy[0][9].tolist()  # (x, y) of left hand
            right_hand = keypoints.xy[0][10].tolist()  # (x, y) of right hand

        # 提取 stop、feed、knife 和 base 的範圍
        regions = extract_object_regions(object_result, ["stop", "feed", "knife", "base"])

        if idx == 1 or single:
            # 判斷人的姿態
            if person:
                behavior.human_pose = classify_pose(keypoints.xyn[0])
        if idx == 0 or single:
            # 判斷左手是否在 Stop 按鈕上
            if regions["stop"] and person:
                if sum(left_hand) != 0:  # 有偵測到左手
                    left_hand_x = left_hand[0] + offsets.get("stop_x", 0)
                    left_hand_y = left_hand[1] + offsets.get("stop_y", 0)
                    behavior.is_hand_on_stop = (
                        SafeState.YES
                        if regions["stop"].x_min - BUTTON_THRESHOLD
                        <= left_hand_x
                        <= regions["stop"].x_max + BUTTON_THRESHOLD
                        and regions["stop"].y_min - BUTTON_THRESHOLD
                        <= left_hand_y
                        <= regions["stop"].y_max + BUTTON_THRESHOLD
                        else SafeState.NO
                    )

            # 判斷右手是否在 Feed 按鈕上
            if regions["feed"] and person:
                if sum(right_hand) != 0:  # 有偵測到右手
                    right_hand_x = right_hand[0] + offsets.get("feed_x", 0)
                    right_hand_y = right_hand[1] + offsets.get("feed_y", 0)
                    behavior.is_hand_on_feed = (
                        SafeState.YES
                        if regions["feed"].x_min - BUTTON_THRESHOLD
                        <= right_hand_x
                        <= regions["feed"].x_max + BUTTON_THRESHOLD
                        and regions["feed"].y_min - BUTTON_THRESHOLD
                        <= right_hand_y
                        <= regions["feed"].y_max + BUTTON_THRESHOLD
                        else SafeState.NO
                    )
        if idx == 2 or single:
            # 判斷 Knife 是否碰到 Base
            if regions["knife"] and regions["base"]:
                behavior.is_knife_base_collided = (
                    SafeState.YES
                    if regions["knife"].y_max >= regions["base"].y_min  # -5 # 5 pixels tolerance
                    and (
                        regions["base"].x_min <= regions["knife"].x_min <= regions["base"].x_max
                        or regions["base"].x_min <= regions["knife"].x_max <= regions["base"].x_max
                    )
                    else SafeState.NO
                )

    return behavior


# 測試單張影像
def predict_result(
    image: str | MatLike | list, pose_model: YOLO, object_model: YOLO, offsets: dict
) -> tuple[list[MatLike], Behavior]:
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
    pose_results = pose_model.predict(image, conf=0.5, verbose=PREDICT_VERBOSE)

    # 繪製姿態估計結果
    pose_annotated_frames = []
    for pose_result in pose_results:
        pose_annotated_frames.append(pose_result.plot())

    # ------------------------------
    # 步驟 2: 進行物件偵測
    # ------------------------------
    # 使用你自訓練的物件偵測模型進行偵測
    print("Predicting objects...")
    object_results = object_model.predict(image, conf=0.3, verbose=PREDICT_VERBOSE)

    # 獲取類別數量（假設類別編號從 0 開始連續編號）
    num_classes = len(object_model.names)
    colors = generate_colors(num_classes)

    # 獲取類別名稱
    class_names = object_model.names

    # 複製姿態估計的結果框架以進行繪製
    ret_combined_frames = []
    # behaviors = []

    for object_result, pose_annotated_frame in zip(object_results, pose_annotated_frames):
        combined_frame = pose_annotated_frame.copy()

        # 遍歷每一個偵測結果
        for object in object_result.boxes:
            # 獲取偵測框的座標
            x1, y1, x2, y2 = map(int, object.xyxy[0].tolist())

            # 獲取物件的置信度
            confidence = object.conf[0]

            # 獲取物件的類別編號
            class_id = int(object.cls[0])

            # 獲取物件的類別名稱
            class_name = class_names[class_id] if class_id < len(class_names) else f"class_{class_id}"

            # 獲取對應的顏色
            color = colors[class_id]

            # 繪製偵測框
            cv2.rectangle(combined_frame, (x1, y1), (x2, y2), color, 2)

            # 準備顯示的文字（類別名稱和置信度）
            label = f"{class_name} {confidence:.2f}"

            # 計算文字的寬高以確保文字不會超出框架
            (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

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

        ret_combined_frames.append(combined_frame)

    ret_behavior = predict_safe(pose_results, object_results, offsets)

    # # TODO: behavior判斷不準確 11/29改成不同攝影機處理不同行為
    # ret_behavior = Behavior()
    # for b in behaviors:
    #     for field in fields(b):
    #         behavior_value = getattr(b, field.name)
    #         ret_behavior_value = getattr(ret_behavior, field.name)
    #         if isinstance(behavior_value, SafeState):
    #             if behavior_value != SafeState.UNDETECTED:
    #                 if ret_behavior_value == SafeState.UNDETECTED:
    #                     setattr(ret_behavior, field.name, behavior_value)
    #                 else:
    #                     if field.name == "is_knife_base_collided":
    #                         setattr(
    #                             ret_behavior,
    #                             field.name,
    #                             behavior_value or ret_behavior_value,
    #                         )
    #                     else:
    #                         setattr(
    #                             ret_behavior,
    #                             field.name,
    #                             behavior_value and ret_behavior_value,
    #                         )
    #         else:
    #             if behavior_value != PoseState.UNKNOWN:
    #                 setattr(ret_behavior, field.name, behavior_value)

    return ret_combined_frames, ret_behavior


# def predict_multiple(
#     images: list[str | MatLike], pose_model: YOLO, object_model: YOLO, offsets: dict
# ) -> tuple[list[MatLike], Behavior]:
#     combined_frames = []
#     behaviors = Behavior()

#     for image in images:
#         combined_frame, behavior = result(image, pose_model, object_model, offsets)
#         combined_frames.append(combined_frame)

#         for field in fields(behavior):
#             behavior_value = getattr(behavior, field.name)
#             behaviors_value = getattr(behaviors, field.name)
#             if behavior_value != SafeState.UNDETECTED:
#                 if behaviors_value == SafeState.UNDETECTED:
#                     setattr(behaviors, field, behavior_value)
#                 else:
#                     if field == "is_knife_base_collided":
#                         setattr(behaviors, field, behaviors_value or behavior_value)
#                     else:
#                         setattr(behaviors, field, behaviors_value and behavior_value)

#     return combined_frames, behaviors


# # ------------------------------
# # 步驟 3: 顯示最終結果
# # ------------------------------
# # 調整視窗大小以適應顯示
# cv2.namedWindow("Pose Estimation and Object Detection Combined", cv2.WINDOW_NORMAL)
# cv2.imshow("Pose Estimation and Object Detection Combined", combined_frame)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.imwrite("output.jpg", combined_frame)
