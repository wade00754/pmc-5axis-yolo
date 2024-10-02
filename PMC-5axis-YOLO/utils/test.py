from ultralytics import YOLO

model = YOLO(R"best.pt")  # load a pretrained model (recommended for training)
result = model.predict(
    source=[
        R"images/2.jpg",
        R"images/3.jpg",
        R"images/4.jpg",
        R"images/5.jpg",
        R"images/6.jpg",
    ],
)  # predict on an image
