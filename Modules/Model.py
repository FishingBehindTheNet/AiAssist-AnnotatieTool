from ultralytics import YOLO
def voorspel(Images, model): 
    Model = YOLO(model)
    Model.predict(Images, save_txt=True, conf=0.5, save=True, exist_ok=True, project="Model", name="Voorspellingen")