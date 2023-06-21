import os
import cv2

def load_label_names(Labels):
    global label_names
    with open(Labels, 'r') as f:
        label_names = [line.strip() for line in f.readlines()]

def WidgetToYolo(ImageMap, ImageName, Annotaties, BBox):
    AnnoName = ImageName.replace(".jpg", ".txt").replace(".JPG", ".txt")
    AnnoLocation = os.path.join(Annotaties, AnnoName)
    with open(AnnoLocation, "w+") as a:
        a.write("")

    img = cv2.imread(os.path.join(ImageMap, ImageName))
    img_y, img_x = img.shape[:2]
    cv2.destroyAllWindows()

    for Box in BBox:
        for i, lines in enumerate(label_names):
            if Box["label"] in lines:
                yoloL = i
        BoxX = Box["x"]
        BoxY = Box["y"]
        BoxW = Box["width"]
        BoxH = Box["height"]
        
        if BoxX < img_x and BoxY < img_y:
            if BoxX < 0:
                BoxW = BoxW + BoxX
                BoxX = 0
            if BoxY < 0:
                BoxH = BoxH + BoxY
                BoxY = 0
            if BoxW > 0 and BoxH > 0:
                if BoxW + BoxX > img_x:
                    BoxW = img_x - BoxX
                if BoxH + BoxY > img_y:
                    BoxH = img_y - BoxY
            
                yoloX = (BoxX + (BoxW/2))/img_x
                yoloY = (BoxY + (BoxH/2))/img_y
                yoloW = BoxW / img_x
                yoloH = BoxH / img_y

                with open(AnnoLocation, "a") as c:
                    c.write(f"{yoloL} {yoloX} {yoloY} {yoloW} {yoloH}\n")

def YoloToWidget(ImageMap, ImageName, Annotaties):
    AnnoName = ImageName.replace(".jpg", ".txt").replace(".JPG", ".txt")
    AnnoLocation = os.path.join(Annotaties, AnnoName)
    if os.path.exists(AnnoLocation):
        img = cv2.imread(os.path.join(ImageMap, ImageName))
        img_y, img_x = img.shape[:2]
        cv2.destroyAllWindows()

        annotations = []
        with open(AnnoLocation, 'r') as e:
            lines = e.readlines()
            for line in lines:
                yoloL, yoloX, yoloY, yoloW, yoloH = map(float, line.split())
                
                x = (yoloX * img_x) - (yoloW * img_x / 2)
                y = (yoloY * img_y) - (yoloH * img_y / 2)
                width = yoloW * img_x
                height = yoloH * img_y
                label = label_names[int(yoloL)].strip()
                
                annotations.append({'x': x, 'y': y, 'width': width, 'height': height, 'label': label})
        
        return annotations
    else:
        return []
