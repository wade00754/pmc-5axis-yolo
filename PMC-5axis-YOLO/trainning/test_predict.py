from ultralytics import YOLO

# Load a model
model = YOLO(R"best.pt")  # load a pretrained model (recommended for training)
dataset = "..\datasets\project.v6i\data.yaml"

if __name__ == "__main__":
    result = model.predict(
        source=[
            R"images/2.jpg",
            R"images/3.jpg",
            R"images/4.jpg",
            R"images/5.jpg",
            R"images/6.jpg",
        ],
    )  # predict on an image
    # model.export(format="onnx")  # export a model to ONNX format
