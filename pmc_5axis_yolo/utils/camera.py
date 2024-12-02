import os
from calendar import c
from datetime import datetime

import cv2
import numpy as np


def test_camera_num():
    cap = cv2.VideoCapture(0)
    print(f"Switch to camera 0")

    while True:
        if not cap.isOpened():
            break
        # 從攝影機擷取一張影像
        ret, frame = cap.read()

        # 顯示圖片
        cv2.imshow("frame", frame)

        key = cv2.waitKey(1) & 0xFF
        # 若按下 q 鍵則離開迴圈
        if key == ord("q"):
            break
        elif ord("0") <= key <= ord("9"):
            new_index = key - ord("0")
            new_cap = cv2.VideoCapture(new_index)
            if new_cap.isOpened():
                cap.release()
                cap = new_cap
                print(f"Switch to camera {new_index}")
            else:
                new_cap.release()
                print(f"Failed to switch to camera {new_index}")

    # 釋放攝影機
    cap.release()

    # 關閉所有 OpenCV 視窗
    cv2.destroyAllWindows()


def record_with_multiple_camera():
    nums = int(input("Enter the number of cameras: "))
    # 取得目前時間作為檔案名稱的一部分
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    parent = os.path.join("captured_images", "videos")
    os.makedirs(parent, exist_ok=True)

    # 設定每個鏡頭的輸出檔名
    filenames = [os.path.join(parent, f"cam_{i}_{current_time}.mp4") for i in range(nums)]

    caps = []
    outs = []

    for index, filename in enumerate(filenames):
        # 打開攝影機
        cap = cv2.VideoCapture(index)

        # 設定攝影機的解析度
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # 定義編碼方式和輸出檔案格式
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(filename, fourcc, 30.0, (1280, 720))
        caps.append(cap)
        outs.append(out)

    while True:
        frames = []
        for index, (cap, out) in enumerate(zip(caps, outs)):
            ret, frame = cap.read()
            if not ret:
                print(f"無法從攝影機 {index} 讀取影像")
                break

            # 寫入影像到檔案
            out.write(frame)

            frames.append(frame)

        combined_frame = cv2.resize(np.hstack(frames), (0, 0), fx=0.5, fy=0.5)
        # 顯示影像
        cv2.imshow(f"Recording...", combined_frame)

        # 按 'q' 鍵退出錄影
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # 釋放資源
    for cap, out in zip(caps, outs):
        cap.release()
        out.release()
    cv2.destroyAllWindows()

    print("錄影結束")


if __name__ == "__main__":

    mode = input("Choose mode (1: test_camera_num, 2: record with multiple camera): ")

    if mode == "1":
        test_camera_num()
    elif mode == "2":
        record_with_multiple_camera()
