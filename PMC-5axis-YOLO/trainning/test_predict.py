from ultralytics import YOLO

# Load a model
model = YOLO(R"best.pt")  # load a pretrained model (recommended for training)
dataset = "..\datasets\project.v6i\data.yaml"

if __name__ == "__main__":
    model.predict(source=R"images/5.jpg", save=True)  # predict on an image
    # model.export(format="onnx")  # export a model to ONNX format
