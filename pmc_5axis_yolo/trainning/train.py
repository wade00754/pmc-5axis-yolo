from ultralytics import YOLO

# Load a model
model = YOLO(R"yolo11n-pose.pt")  # load a pretrained model (recommended for training)
dataset = "..\datasets\project-pose.v1i\data.yaml"

if __name__ == "__main__":
    # Use the model
    model.train(data=dataset, epochs=100, imgsz=640)  # train the model
    # model.val(data=dataset, split="test")  # evaluate model performance on the test set
    # model.predict(source="images", save=True)  # predict on an image
    # model.export(format="onnx")  # export a model to ONNX format
