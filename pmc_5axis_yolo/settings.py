OBJECT_MODEL = "pmc5axis11n.pt"
POSE_MODEL = "yolo11n-pose.pt"
PREDICT_VERBOSE = False
DEFAULT_OFFSETS = {
    "stop_x": 52,
    "stop_y": 1,
    "feed_x": 44,
    "feed_y": -10,
}
CAMERA_COUNT = 5  # MAX 5
LIE_THRESHOLD = 0.14  # normalized
ARM_ANGLE_THRESHOLD = 150  # degrees
ARM_STRETCH_THRESHOLD = 0.1  # normalized
ARM_BEND_THRESHOLD = 0.05  # normalized
