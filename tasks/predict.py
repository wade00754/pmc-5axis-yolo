import cv2
from ultralytics import YOLO
import random


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
def test_hand_on_button(pose_results, detection_results, adj_value):
    # 獲取關鍵點 (關注左手或右手的位置)
    # 假設關鍵點索引為: 9 是右手腕，10 是左手腕（根據 COCO 的姿態標註）
    keypoints = pose_results[0].keypoints.xy[0]

    # 取得右手與左手的座標 (x, y)
    left_hand = keypoints[9]  # (x, y) of left hand
    right_hand = keypoints[10]  # (x, y) of right hand

    # 初始化 Stop 和 Feed 按鈕的範圍變數及手是否在按鈕上的變數
    stop_region = None
    feed_region = None
    is_hand_on_stop = False
    is_hand_on_feed = False

    # 遍歷每一個偵測結果來找到 stop 和 feed 的範圍
    for detection in detection_results[0].boxes:
        # 獲取偵測框的座標
        x1, y1, x2, y2 = map(int, detection.xyxy[0].tolist())

        # 獲取物件的類別編號
        class_id = int(detection.cls[0])

        # 獲取物件的類別名稱
        class_name = detection_results[0].names[class_id]

        # 如果是 Stop 按鈕，記錄其範圍
        if class_name == "stop":
            stop_region = {"x_min": x1, "x_max": x2, "y_min": y1, "y_max": y2}

        # 如果是 Feed 按鈕，記錄其範圍
        if class_name == "feed":
            feed_region = {"x_min": x1, "x_max": x2, "y_min": y1, "y_max": y2}

    # 判斷手是否在 Stop 按鈕上
    if stop_region:
        right_hand_x = right_hand[0] + adj_value[0]
        right_hand_y = right_hand[1] + adj_value[1]
        left_hand_x = left_hand[0] + adj_value[0]
        left_hand_y = left_hand[1] + adj_value[1]
        x_min = stop_region["x_min"]
        x_max = stop_region["x_max"]
        y_min = stop_region["y_min"]
        y_max = stop_region["y_max"]
        is_hand_on_stop = (
            x_min <= right_hand_x <= x_max and y_min <= right_hand_y <= y_max
        ) or (x_min <= left_hand_x <= x_max and y_min <= left_hand_y <= y_max)

    # 判斷手是否在 Feed 按鈕上
    if feed_region:
        right_hand_x = right_hand[0] + adj_value[2]
        right_hand_y = right_hand[1] + adj_value[3]
        left_hand_x = left_hand[0] + adj_value[2]
        left_hand_y = left_hand[1] + adj_value[3]
        x_min = feed_region["x_min"]
        x_max = feed_region["x_max"]
        y_min = feed_region["y_min"]
        y_max = feed_region["y_max"]
        is_hand_on_feed = (
            x_min <= right_hand_x <= x_max and y_min <= right_hand_y <= y_max
        ) or (x_min <= left_hand_x <= x_max and y_min <= left_hand_y <= y_max)

    return is_hand_on_stop, is_hand_on_feed


# 測試單張影像
def predict_single(image, pose_model, object_model, adj_value):
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
    pose_results = pose_model(image)

    # 繪製姿態估計結果
    pose_annotated_frame = pose_results[0].plot()

    # ------------------------------
    # 步驟 2: 進行物件偵測
    # ------------------------------
    # 使用你自訓練的物件偵測模型進行偵測
    print("Predicting objects...")
    object_results = object_model(image)

    # 獲取類別數量（假設類別編號從 0 開始連續編號）
    num_classes = len(object_model.model.names)
    colors = generate_colors(num_classes)

    # 獲取類別名稱
    class_names = object_model.model.names

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

        # 繪製文字背景
        cv2.rectangle(
            combined_frame, (x1, y1 - text_height - 4), (x1 + text_width, y1), color, -1
        )

        # 在框架上繪製文字
        cv2.putText(
            combined_frame,
            label,
            (x1, y1 - 2),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )

    is_hand_on_stop, is_hand_on_feed = test_hand_on_button(
        pose_results, object_results, adj_value
    )

    return combined_frame, is_hand_on_stop, is_hand_on_feed


# # ------------------------------
# # 步驟 3: 顯示最終結果
# # ------------------------------
# # 調整視窗大小以適應顯示
# cv2.namedWindow("Pose Estimation and Object Detection Combined", cv2.WINDOW_NORMAL)
# cv2.imshow("Pose Estimation and Object Detection Combined", combined_frame)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.imwrite("output.jpg", combined_frame)
