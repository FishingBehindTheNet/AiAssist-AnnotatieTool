#lijst met ondersteunde bestandstype. Door functies die deze type nodig hebben te centreren zou toekomstig onderhoud versimpelt moeten worden.
ImageTypes = [".jpg", ".png", "jpeg"]

#Functie om Imagenamen om te zetten naar labelnamen.
def ImageToLabel(ImageName):
    LabelName = ImageName
    for Types in ImageTypes:
        LabelName = LabelName.replace(Types.lower(), ".txt")
        LabelName = LabelName.replace(Types.upper(), ".txt")
    return LabelName

#Checkt of een bestand een ondersteunt Imagetype is.
def ValidImageType(ImageName):
    valid = False
    for Types in ImageTypes:
        if ImageName.endswith(Types.lower()) or ImageName.endswith(Types.upper()):
            valid = True
    return valid