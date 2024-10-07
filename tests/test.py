from ultralytics import YOLO
from ultralytics.engine.model import Model
from ultralytics.engine.results import Results

if __name__ == "__main__":
    model = YOLO(R"best.pt")  # load a pretrained model (recommended for training)
    result = model.predict(source=R"images/5.jpg")  # predict on an image
    print(type(model))
    print(type(result))
