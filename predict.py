from ultralytics import YOLO

# Load a model
model = YOLO(
    R"runs\detect\train2\weights\best.pt"
)  # load a pretrained model (recommended for training)
dataset = "..\datasets\project.v2i\data.yaml"

if __name__ == "__main__":
    model.predict(
        source=R"..\datasets\project.v2i\test\images", save=True
    )  # predict on an image
    # model.export(format="onnx")  # export a model to ONNX format
