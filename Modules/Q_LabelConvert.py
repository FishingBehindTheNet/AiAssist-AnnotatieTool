import os
import cv2
from Modules.Q_UniversalFunction import ImageToLabel

#Laat de lijst met labels in zodat deze hergebruikt kan worden.
def load_label_names(Labels):
    global label_names
    with open(Labels, 'r') as f:
        label_names = [line.strip() for line in f.readlines()]
    return label_names

#Functie voor het opslaan van an annotaties in YOLO format. (De widget werkt met de COCO format, mogelijk kun je deze functie dus vaker gebruiken.)
def WidgetToYolo(ImageMap, ImageName, Annotaties, BBox):
    #formuleert de locatie van de annotatie en zorcht dat het .txt bestand leeg is
    AnnoLocation = os.path.join(Annotaties, ImageToLabel(ImageName))
    with open(AnnoLocation, "w+") as a:
        a.write("")

    #Berekend het formaat van de image voor gebruik in de formule
    img = cv2.imread(os.path.join(ImageMap, ImageName))
    img_y, img_x = img.shape[:2]
    cv2.destroyAllWindows()
    
    #loopt over alle annotaties van de foto
    for Box in BBox:
        #zoekt naar de positie van het de label in de lijst en geeft deze terug. Dit is nodig voor YOLO om de labels in te kunnen lezen.
        for i, lines in enumerate(label_names):
            if Box["label"] in lines:
                yoloL = i
        
        BoxX = Box["x"]
        BoxY = Box["y"]
        BoxW = Box["width"]
        BoxH = Box["height"]
        
        #Controleert de coördinaten van de BBox en corrigeert deze als ze buiten de foto vallen.
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

                #Rekent de coördinaten om van COCO 
                #   (X en Y pixelwaarde van de hoek rechts boven. Breedte en Hoogte van bow in pixels)
                # naar YOLO format
                #   (Alle waarden genormaliseerd tussen 0 en 1. X en Y van het centrum van de box, Breedte en Hoogte zijn ook genormaliseerd)
                yoloX = (BoxX + (BoxW/2))/img_x
                yoloY = (BoxY + (BoxH/2))/img_y
                yoloW = BoxW / img_x
                yoloH = BoxH / img_y

                #slaat de nieuwe waarden op in een text bestand met de zelfde naam als de image
                with open(AnnoLocation, "a") as c:
                    c.write(f"{yoloL} {yoloX} {yoloY} {yoloW} {yoloH}\n")

# leest YOLO annotaties in en rekent ze om naar COCO zodat de widgets ze kan gebruiken.
def YoloToWidget(ImageMap, ImageName, Annotaties):
    #formuleert de locatie van de annotatie.
    AnnoLocation = os.path.join(Annotaties, ImageToLabel(ImageName))
    if os.path.exists(AnnoLocation):
        #Berekend het formaat van de image voor gebruik in de formule
        img = cv2.imread(os.path.join(ImageMap, ImageName))
        img_y, img_x = img.shape[:2]
        cv2.destroyAllWindows()

        #Maakt een lege lijst aan zodat als de annotaties leeg zijn er toch een output is.
        annotations = []
        
        with open(AnnoLocation, 'r') as e:
            #loopt over alle lijnen en berekend coco waarden voor iedere lijn.
            lines = e.readlines()
            for line in lines:
                yoloL, yoloX, yoloY, yoloW, yoloH = map(float, line.split())
                
                x = (yoloX * img_x) - (yoloW * img_x / 2)
                y = (yoloY * img_y) - (yoloH * img_y / 2)
                width = yoloW * img_x
                height = yoloH * img_y
                #Selecteert het label op basis van de positie in de lijst. 
                label = label_names[int(yoloL)].strip()
                
                #voegt de annotaties toe aan de lijst van annotaties
                annotations.append({'x': x, 'y': y, 'width': width, 'height': height, 'label': label})
        
        return annotations
    else:
        return []
