from ultralytics import YOLO

model = YOLO("yolov10n.pt")
model.train(data='dataset.yaml', epochs=500, batch=32, imgsz=374)
