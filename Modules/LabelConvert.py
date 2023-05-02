import os
import cv2

def WidgetToYolo(ImageMap, ImageName, Annotaties, Labels, BBox):
    AnnoName = ImageName.replace(".jpg", ".txt").replace(".JPG", ".txt")
    AnnoLocation = os.path.join(Annotaties, AnnoName)
    with open(AnnoLocation, "w+") as a:
        a.write("")

    img = cv2.imread(os.path.join(ImageMap, ImageName))
    img_y, img_x = img.shape[:2]

    for Box in BBox:
        with open(Labels, 'r') as b:
            lines = b.readlines()
            for i, lines in enumerate(lines):
                if Box["label"] in lines:
                    yoloL = i
        
        yoloX = (Box["x"] + (Box["width"]/2))/img_x
        yoloY = (Box["y"] + (Box["height"]/2))/img_y
        yoloW = Box["width"] / img_y
        yoloH = Box["height"] / img_x
        with open(AnnoLocation, "a") as c:
            c.write(f"{yoloL} {yoloX} {yoloY} {yoloW} {yoloH}\n")

def YoloToWidget(ImageMap, ImageName, Annotaties, Labels):
    AnnoName = ImageName.replace(".jpg", ".txt").replace(".JPG", ".txt")
    AnnoLocation = os.path.join(Annotaties, AnnoName)
    if os.path.exists(AnnoLocation):
        img = cv2.imread(os.path.join(ImageMap, ImageName))
        img_y, img_x = img.shape[:2]

        with open(Labels, 'r') as a:
            label_names = a.readlines()

        annotations = []
        with open(AnnoLocation, 'r') as b:
            lines = b.readlines()
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
