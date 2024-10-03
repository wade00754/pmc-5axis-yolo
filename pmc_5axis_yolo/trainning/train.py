from ultralytics import YOLO

# Load a model
model = YOLO(R"runs\detect\train2\weights\best.pt")
# model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
dataset = "..\datasets\project.v6i\data.yaml"

if __name__ == "__main__":
    # Use the model
    model.train(data=dataset, epochs=150)  # train the model
    model.val(data=dataset, split="test")  # evaluate model performance on the test set
    # model.predict(source="images", save=True)  # predict on an image
    # model.export(format="onnx")  # export a model to ONNX format
