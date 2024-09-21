def adj_offsets(
    to_adj, offsets, image, pose_model, object_model
):  # similar to test_hand_on_button
    if to_adj:
        print("Adjusting offsets...")
        pose_results = pose_model(image)
        object_results = object_model(image)

        # 獲取關鍵點 索引為: 9 是右手腕，10 是左手腕（根據 COCO 的姿態標註）
        keypoints = pose_results[0].keypoints.xy[0]

        # 取得右手與左手的座標 (x, y)
        left_hand = keypoints[9]  # (x, y) of left hand
        right_hand = keypoints[10]  # (x, y) of right hand

        # 初始化 Stop 和 Feed 按鈕的範圍變數
        stop_region = None
        feed_region = None

        # 遍歷每一個偵測結果來找到 stop 和 feed 的範圍
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

        # 判斷左手和 Stop 按鈕的相對位置
        if stop_region:
            x = (stop_region["x_min"] + stop_region["x_max"]) / 2
            y = (stop_region["y_min"] + stop_region["y_max"]) / 2
            offsets["stop_x"] = x - left_hand.cpu().numpy()[0]
            offsets["stop_y"] = y - left_hand.cpu().numpy()[1]

        # 判斷右手和 Feed 按鈕的相對位置
        if feed_region:
            x = (feed_region["x_min"] + feed_region["x_max"]) / 2
            y = (feed_region["y_min"] + feed_region["y_max"]) / 2
            offsets["feed_x"] = x - right_hand.cpu().numpy()[0]
            offsets["feed_y"] = y - right_hand.cpu().numpy()[1]

    if offsets == {
        "stop_x": 52,
        "stop_y": 0,
        "feed_x": 45,
        "feed_y": -20,
    }:
        print("No changes adjusted. Using default offsets.")
    else:
        print(
            f"Adjusted offsets:",
            " ".join(f"[{value}: {offsets[value]:.3f}]" for value in offsets),
        )

    return offsets


# # test codes
# import cv2
# from ultralytics import YOLO

# if __name__ == "__main__":
#     image = cv2.imread("images/1.jpg")
#     pose_model = YOLO("yolov8n-pose.pt")
#     object_model = YOLO("best.pt")
#     adj_offsets(True, image, pose_model, object_model)
