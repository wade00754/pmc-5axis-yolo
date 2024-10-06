import os

from roboflow import Roboflow

if __name__ == "__main__":
    rf = Roboflow(api_key=os.environ["ROBOFLOW_API_KEY"])
    project = rf.workspace("pmc-5axis-yolo").project("pmc-detection")
    project.version(8).deploy("yolov11", "runs/detect/train5")
