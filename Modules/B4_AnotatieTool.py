from Modules.Q_LabelConvert import YoloToWidget, WidgetToYolo, load_label_names
from Modules.Q_UniversalFunction import ImageToLabel, ValidImageType
from Modules.Q_UIparts import OutputScherm
from jupyter_bbox_widget import BBoxWidget
from ultralytics import YOLO
import ipywidgets as widgets
import logging
import random
import base64
import shutil
import gc
import os


# Onderdrukt de printstatements van yolo
logging.getLogger('ultralytics').setLevel(logging.WARNING)


def Annoteren(ImageMap, Annotaties, Labels, Model, ProjectName):
    #Maakt een map aan om foto's in op te slaan voor latere referentie
    if not os.path.exists(f"{ImageMap}/Check Later") and not ImageMap.endswith("/Check Later"):
        os.makedirs(f"{ImageMap}/Check Later")
    
    #laat de labels in zodat de Label.txt file niet onnodig geopend word.(Performance)
    label_names = load_label_names(Labels)

    # Work around om afbeeldingen zichtbaar te maken
    def encode_image(filepath):
        with open(filepath, "rb") as f:
            image_bytes = f.read()
        encoded = str(base64.b64encode(image_bytes), "utf-8")
        return "data:image/jpg;base64," + encoded

    #Functie voor het laden van BBox op de interface.
    def BoxPicker(Overwrite):
        #Schoont de BBoxen van de vorige foto op om vertraging minder opvallend te maken
        ImageView.bboxes = []
        #Update de ImageTitel
        PathLink()

        ImageLocation = os.path.join(
            ImageMap, 
            Files[HiddenProgress.value]
        )
        HumanLabelsLocation = os.path.join(
            Annotaties, 
            ImageToLabel(Files[HiddenProgress.value])
        )
        if Model:
            AiLabelsLocation = os.path.join(
                    os.getcwd(), 
                    ProjectName,
                    "Data/Voorspellingen/labels",
                    ImageToLabel(Files[HiddenProgress.value])
            )

        #Overwrite voor de "Genereer annotaties" knop zodat deze ook Ai Annotaties laat zien als AI uit staat
        if Overwrite == "reGen":
            #verwijderd ouwde voorspelling als deze bestaat.
            if os.path.exists(AiLabelsLocation):
                os.remove(AiLabelsLocation)
            
            # genereert de nieuwe annotaties
            model.predict(
                ImageLocation,
                save_txt=True,
                conf=0.2,
                exist_ok=True,
                project=ProjectName,
                name="Data/Voorspellingen",
                augment=True,
                verbose=False
            )

            #laadt de nieuwe annotaties in
            ImageView.bboxes = YoloToWidget(
                ImageMap=ImageMap,
                ImageName=Files[HiddenProgress.value],
                Annotaties=AiAnnotaties,
            )
        #Controleert of er een model geselecteerd is, ai aan staat en er nog geen handmatige annotaties zijn.
        elif Model and AiAssist.value and not os.path.exists(HumanLabelsLocation):
            #genereert de nieuwe annotaties als deze nog niet bestaan
            if not os.path.exists(AiLabelsLocation):
                model.predict(
                    ImageLocation,
                    save_txt=True,
                    conf=0.25,
                    exist_ok=True,
                    project=ProjectName,
                    name="Data/Voorspellingen",
                    augment=True,
                    verbose=False
                )
            #laadt de nieuwe annotaties in
            ImageView.bboxes = YoloToWidget(
                ImageMap=ImageMap,
                ImageName=Files[HiddenProgress.value],
                Annotaties=AiAnnotaties,
            )
        else:
            #laat de handmatige anotaties in die eerder opgeslagen zijn als deze bestaan.
            ImageView.bboxes = YoloToWidget(
                ImageMap=ImageMap,
                ImageName=Files[HiddenProgress.value],
                Annotaties=Annotaties,
            )

    LabeledImages = []
    UnlabeledImages = []

    # Loopt door de image folder heen en maakt twee lijsten:
    #   Een met images waar annotaties voor bestaan in de label folder
    #   Een met images zonder Label
    for filename in os.listdir(ImageMap):
        if ValidImageType(filename):
            if os.path.exists(os.path.join(Annotaties, ImageToLabel(filename))):
                LabeledImages.append(filename)
            else:
                UnlabeledImages.append(filename)

    # Shuffle de lijst met foto's zonder labels zodat wanneer je meerdere foto's van een object hebt je een kleinere kans hebt ze na elkaar te krijgen.
    # En dus minder gemakkelijk beïnvloed word door de herhaaldelijke weergaven van gelijke segmenten/afbeeldingen.
    random.shuffle(UnlabeledImages)

    # voegt de 2 lijsten samen zodat de gelabelde afbeeldingen voor in de lijst komen en overgeslagen kunnen worden.
    Files = LabeledImages + UnlabeledImages

    # laat zien hoeveel foto's geannoteerd zijn
    ProgressBar = widgets.IntProgress(
        value=len(LabeledImages),
        max=len(Files) - 1,
        description="Foto's geannoteerd:",
        style={"description_width": "initial"},
        tooltip=f"{len(LabeledImages)} van de {len(Files) - 1} foto's heeft een annotatie in de label folder",
        layout=widgets.Layout(width="100%"),
    )

    # een verborgen waarde die gebruikt word om de juiste foto te selecteren. Het gebruik van de widget ipv een standaard variable is om het aanpassen binnen andere functies te versimpelen
    HiddenProgress = widgets.BoundedIntText(
        value= ProgressBar.value,
        min=0,
        max=ProgressBar.max,
    )

    ImageTitle = widgets.HTML()

    # Genereert een klikbare link naar de imagelocatie zodat de foto gemakkelijk terug te vinden is buiten de widget
    def PathLink():
        Title = os.path.join(ImageMap, Files[HiddenProgress.value])
        Title.replace("\\", "/")
        ImageTitle.value = (
            f"<br><h2><a href='file:///{Title}'>{Files[HiddenProgress.value]}</a></h2>"
        )

    # Maakt knoppen aan(functionaliteit word hieronder besproken)
    Back = widgets.Button(
        description="Back",
        value=False,
        tooltip="Terug naar de vorige foto",
        button_style="warning",
    )

    AiAssist = widgets.ToggleButton(
        description="AI uit",
        value=False,
        tooltip="Ai annotaties aan/uit",
        button_style="",
    )

    reGen = widgets.Button(
        value=False,
        description="Genereer annotaties",
        tooltip="Verwijder Ai annotaties en genereer nieuwe annotaties",
        button_style="primary",
    )

    Later = widgets.Button(
        value=False,
        description="Check Later",
        tooltip=f"Kopier de image naar {ImageMap}/Check Later",
        button_style="info",
    )

    Delete = widgets.Button(
        value=False,
        description="Verwijder foto",
        tooltip=f"Verwijder image uit {ImageMap}",
        button_style="danger",
    )

    # Displays de foto en zorgt dat je kunt annoteren
    ImageView = BBoxWidget(
        image=encode_image(os.path.join(ImageMap, Files[HiddenProgress.value])),
        classes=label_names,
        layout=widgets.Layout(width="650px"),
    )
    
    # Laat de juiste BBoxen in
    BoxPicker("")

    # Variabelen met de opmaak voor een knop in html voor het versimpelen van de opmaak hieronder.
    ButtonF = '<kbd><font color="#424a48"><b>'
    ButtonB = "</b></font></kbd>"

    CheatSheet = widgets.HTML(
        value=f"""
        <style>
        td:first-child {{
            text-align: center;
        }}
        td:last-child {{
            text-align: left;
        }}
        </style>

        <h3>Key bindings</h3> 
        <table>
        <tr>
            <td>{ButtonF}1{ButtonB}-{ButtonF}9{ButtonB}</td>
            <td>Selecteert een label</td>
        </tr>
        <tr>
            <td>{ButtonF}Tab{ButtonB}</td>
            <td>Selecteert de volgende bounding box</td>
        </tr>
        <tr>
            <td>{ButtonF}Shift{ButtonB}-{ButtonF}Tab{ButtonB}</td>
            <td>Selecteert de vorige bounding box</td>
        </tr>
        <tr>
            <td>{ButtonF}c{ButtonB}</td>
            <td>Verander label van geselecteerde bounding box</td>
        </tr>
        <tr>
            <td>{ButtonF}Delete{ButtonB}</td>
            <td>verwijder geselecteerde bounding box</td>
        </tr>
        <tr>
            <td>{ButtonF}Enter{ButtonB}</td>
            <td>Submit: slaat het label op en laadt de volgende foto</td>
        </tr>
        <tr>
            <td>{ButtonF} Spatie {ButtonB}</td>
            <td>Skip: Laadt de volgende foto zonder de annotaties op te slaan</td>
        </tr>
        <tr>
            <td>{ButtonF}w{ButtonB} <br />
            {ButtonF}a{ButtonB}  {ButtonF}s{ButtonB}  {ButtonF}d{ButtonB}</td>
            <td>Verplaatst de bounding box <br />(gebruik {ButtonF}Shift{ButtonB} om de bounding box sneller te bewegen)</td>
        </tr>
        <tr>
            <td>{ButtonF}R{ButtonB}<br />{ButtonF}F{ButtonB}</td>
            <td>Past de lengte van de Bounding box aan <br />(gebruik {ButtonF}Shift{ButtonB} om de bounding box sneller aan te passen)</td>
        </tr>
        <tr>
            <td>{ButtonF}E{ButtonB}<br />{ButtonF}Q{ButtonB}</td>
            <td>Past de breedte van de Bounding box aan <br />(gebruik {ButtonF}Shift{ButtonB} om de bounding box sneller aan te passen)</td>
        </tr>
        """
    )
    
    #Voor het gebruik als spacing in de opmaak van de interface
    WiteLine = widgets.HTML(" ")

    # voegt alle widgets samen voor gemakkelijk aanroepen. De IF functie filtered eruit welke versie van de interface weergegeven gaat worden.
    #   Als er geen model geselecteerd word verdwijnen de "Genereer annotaties" en "AI aan/uit"
    #   Als je foto's uit de check later map aan het bekijken bent verdwijnt de "Check Later" knop om te voorkomen dat er een rabbit hole aan mappen gegenereerd word
    if Model and not ImageMap.endswith("/Check Later"):
        model = YOLO(Model, task="detect")
        AiAnnotaties = os.path.join(
            ProjectName,
            "Data/Voorspellingen/labels"
        )
        if not os.path.exists(AiAnnotaties):
            os.makedirs(AiAnnotaties)

        AnnoterenWidget = widgets.VBox([
            widgets.HBox([
                WiteLine, 
                Back, 
                AiAssist
            ]),
            widgets.HBox([
                ImageView,
                widgets.VBox([
                    ImageTitle,
                    widgets.HBox([
                        reGen, 
                        Later, 
                        Delete
                    ]),
                    ProgressBar,
                    CheatSheet,
                ])
            ])   
        ])
    elif Model and ImageMap.endswith("/Check Later"):
        model = YOLO(Model, task="detect")
        AiAnnotaties = os.path.join(
            ProjectName, "Data/Voorspellingen/labels")
        if not os.path.exists(AiAnnotaties):
            os.makedirs(AiAnnotaties)

        AnnoterenWidget = widgets.VBox([
            widgets.HBox([
                WiteLine, 
                Back, 
                AiAssist
            ]),
            widgets.HBox([
                ImageView,
                widgets.VBox([
                    ImageTitle,
                    widgets.HBox([
                        reGen,
                        Delete
                    ]),
                    ProgressBar,
                    CheatSheet,
                ])
            ])   
        ])
    elif ImageMap.endswith("/Check Later"):
        
        AnnoterenWidget = widgets.VBox([
            widgets.HBox([
                WiteLine, 
                Back,
            ]),
            widgets.HBox([
                ImageView,
                widgets.VBox([
                    ImageTitle,
                    widgets.HBox([
                        Delete
                    ]),
                    ProgressBar,
                    CheatSheet,
                ])
            ])   
        ])
    else:
        AnnoterenWidget = widgets.VBox([
            widgets.HBox([
                WiteLine, 
                Back,
            ]),
            widgets.HBox([
                ImageView,
                widgets.VBox([
                    ImageTitle,
                    widgets.HBox([
                        Later, 
                        Delete
                    ]),
                    ProgressBar,
                    CheatSheet,
                ])
            ])   
        ])

    #Update de status van de AI aan/uit knop kwa text en kleur. Status van deze knop word gebruikt in BoxPicker om te bepalen of er AI annotaties gegenereerd moeten worden.
    def on_button_clicked(PlaceHolder):
        if AiAssist.value:
            AiAssist.description = "AI aan"
            AiAssist.button_style = "primary"
            BoxPicker("")
        else:
            AiAssist.description = "AI uit"
            AiAssist.button_style = ""
            BoxPicker("")
    
    AiAssist.observe(on_button_clicked, names="value")

    #Functie verantwoordelijk voor het updaten van het imagenummer waarmee de rest van de functies de fotonaam kunnen vinden in de "Files" list
    def ProgressManager(Taak):
        # selecteer de volgende foto, Als je aan het einde van de lijst zit loopt deze functie je terug naar het begin van de lijst.
        if Taak == "+":
            if HiddenProgress.value >= ProgressBar.max:
                HiddenProgress.value = 0
            else:
                HiddenProgress.value += 1
        # selecteer de vorige foto, Als je aan het begin van de lijst zit loopt deze functie je terug naar het einde van de lijst.
        elif Taak == "-":
            if HiddenProgress.value == 0:
                HiddenProgress.value = HiddenProgress.max
            else:
                HiddenProgress.value -= 1
        #Checkt of de afbeelding waarvan de labels opgeslagen worden al labels had en zo niet dan voegt de file toe aan de lijst en update de Progressbar met +1
        elif Taak == "save":
            if not Files[HiddenProgress.value] in LabeledImages:
                LabeledImages.append(Files[HiddenProgress.value])
                ProgressBar.value = len(LabeledImages)
                ProgressBar.tooltip=f"{ProgressBar.value} van de {ProgressBar.max} foto's heeft een annotatie in de label folder"
        #checkt of de verwijderde foto in "LabeledImages" staat en update de Progressbar met -1. Daarnaast verwijdert hij het bestand altijd uit de "Files" lijst en verlaagt hij de max van ProgressBar en HiddenProgress
        elif Taak == "del":
            if Files[HiddenProgress.value] in LabeledImages:
                del LabeledImages[Files[HiddenProgress.value]]
                ProgressBar.value = len(LabeledImages)
            del Files[HiddenProgress.value]
            ProgressBar.max = len(Files)-1
            HiddenProgress.max = ProgressBar.max
            
            ProgressBar.tooltip=f"{ProgressBar.value} van de {ProgressBar.max} foto's heeft een annotatie in de label folder"
    
    # gaat naar de volgende foto zonder de vooruitgang op te slaan
    @ImageView.on_skip
    def skip():
        ProgressManager(Taak="+")
        image_file = Files[HiddenProgress.value]
        ImageView.image = encode_image(os.path.join(ImageMap, image_file))
        BoxPicker("")
        if HiddenProgress.value % 20 == 0:
            gc.collect()

    # slaat vooruitgang op en roept nieuwe foto aan en gebruikt dan de skip() functie
    @ImageView.on_submit
    def save():
        image_file = Files[HiddenProgress.value]
        WidgetToYolo(
            ImageMap=ImageMap,
            ImageName=image_file,
            Annotaties=Annotaties,
            BBox=ImageView.bboxes,
        )
        ProgressManager(Taak="save")
        skip()

    # Gaat een foto terug zonder op te slaan
    @Back.on_click
    def Back(PlaceHolder):
        ProgressManager(Taak="-")
        image_file = Files[HiddenProgress.value]
        ImageView.image = encode_image(os.path.join(ImageMap, image_file))
        BoxPicker("")

    #roept de BoxPiker aan die de oude AI annotaties zal verwijderen en een nieuwe genereert. Negeert status AI aan/uit
    @reGen.on_click
    def DelVoorspelling(PlaceHolder):
        BoxPicker(Overwrite="reGen")

    #verwijderd de image en label uit de image en label folder en roept de ProgressManager aan om de bestandsnaam uit alle relevante lijsten te verwijderen en benodigde waarden te updaten.
    @Delete.on_click
    def DelImage(PlaceHolder):
        image_file = Files[HiddenProgress.value]
        ProgressManager(Taak="del")
        os.remove(os.path.join(ImageMap, image_file))
        if os.path.exists(os.path.join(Annotaties, ImageToLabel(image_file))) and not ImageMap.endswith("/Check Later"):
            os.remove(os.path.join(Annotaties, ImageToLabel(image_file)))
        ImageView.image = encode_image(os.path.join(ImageMap, Files[HiddenProgress.value]))
        BoxPicker("")
    
    #Kopieert de geselecteerde foto naar de CheckLater map en laadt de volgende foto in de lijst in. 
    @Later.on_click
    def move(PlaceHolder):
        image_file = Files[HiddenProgress.value]
        ProgressManager(Taak="+")
        ImageView.image = encode_image(os.path.join(ImageMap, Files[HiddenProgress.value]))
        BoxPicker("")
        shutil.copy2(os.path.join(ImageMap, image_file),
                     f"{ImageMap}/Check Later")

    OutputScherm.clear_output(wait=True)
    with OutputScherm:
        display(AnnoterenWidget)
