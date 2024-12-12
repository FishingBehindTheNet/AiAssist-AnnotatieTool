import sys
import importlib

#lijst met ondersteunde bestandstype. Door functies die deze type nodig hebben te centreren zou toekomstig onderhoud versimpelt moeten worden.
ImageTypes = [".jpg", ".png", "jpeg"]
LocalModuleFolder = 'Modules'

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

# Reloads local modules so widget.observe and widget.on_click wil work on rerun of cell
def SoftReset(PlaceHolder = None):

    # Step 1: Identify all modules that start with 'LocalModuleFolder' in sys.modules
    modules_to_reload = [module for module in sys.modules if module.startswith(LocalModuleFolder)]

    # Step 2: Reload all modules in reverse order (from deepest dependency to top)
    for module_name in reversed(modules_to_reload):
        module = sys.modules[module_name]
        importlib.reload(module)