import cv2

if __name__ == "__main__":

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
