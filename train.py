from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

if __name__ == "__main__":
    # Use the model
    model.train(data="..\datasets\project.v1i\data.yaml", epochs=5)  # train the model
    model.val()  # evaluate model performance on the validation set
    # model.predict(source="images", save=True)  # predict on an image
    # model.export(format="onnx")  # export a model to ONNX format
