from Modules.B4_AnotatieTool import Annoteren
from Modules.Q_LabelConvert import load_label_names
from ultralytics import YOLO
import ipywidgets as widgets
from onnx import load
import os


def LabelCheck(ImageMap, Annotaties, Model, ProjectName):
    Titel = widgets.HTML(
        "<h1>Labels aanmaken</h1> <b>De volgende Labels zijn al in gebruik:</b><br>"
    )
    # checkt of er al een LabelDoc bestaat en maakt deze anders aan
    LabelDoc = os.path.join(Annotaties, "Labels.txt")
    if not os.path.exists(LabelDoc):
        with open(LabelDoc, "w+") as a:
            a.write("")

    # functie om de weergegeven lijst van labels te updaten
    def LaadLabelLijst():
        with open(LabelDoc, "r") as b:
            labels = b.read()
            labels = labels.replace("\n", "<br>")
            if not labels:
                labels = ("*Labels.txt is nog leeg*")
            return labels

    # weergeeft labels
    LabelLijst = widgets.HTML(value=LaadLabelLijst())

    # weergeeft een text box die de input van nieuwe labels faciliteert
    LabelInputTitel= widgets.HTML("<b>Nieuw label:")
    LabelInput = widgets.Text(
        placeholder="Naam label (Geen speciale tekens!)",
        disabled=False,
    )

    LabelInput.continuous_update = False

    # Knop voor het toevoegen van Labels
    LabelSubmit = widgets.Button(
        value=False, 
        description="Permanent toevoegen", 
        button_style="",
    )

    # Functie om nieuwe labels toe te voegen en de weergave te updaten
    def AddToList(PlaceHolder):
        with open(LabelDoc, "r") as c:
            if LabelInput.value not in c.read():
                with open(LabelDoc, "a") as d:
                    d.write(LabelInput.value + "\n")
            LabelInput.value = ""
            LabelLijst.value = LaadLabelLijst()

    LabelSubmit.on_click(AddToList)
    LabelInput.observe(AddToList)

    # Knop om de annotatietool te starten
    submit = widgets.Button(
        value=False, 
        description="Start met annoteren", 
        button_style="success",
    )

    # geeft benodigde gegevens door aan de annotatietool maar geeft een error als er 0 labels in totaal zijn
    @submit.on_click
    def SaveAndLaunch(PlaceHolder):
        load_label_names(LabelDoc)
        if load_label_names(LabelDoc):
            Annoteren(
                ImageMap=ImageMap,
                Annotaties=Annotaties,
                Labels=LabelDoc,
                Model=Model,
                ProjectName=ProjectName,
            )
            LabelCheck.close()
        else:
            ErrorCode.value = """
                <div style="text-align: right;">
                    <i><b><code style="color:red;">Er staan geen labels in labels.txt<br>Een minimum van 1 label moet toegevoegd worden.</code></b></i>
                </div>
                """

    line = widgets.HTML(value="<hr>")
    ErrorCode = widgets.HTML()

    # Clustert de widgets in een interface
    LabelCheck = widgets.VBox([
        Titel,
        LabelLijst,
        widgets.HBox([
            LabelInputTitel,
            LabelInput,
            LabelSubmit,
        ]),
        line,
        widgets.HBox([
            ErrorCode, 
            submit
        ], layout=widgets.Layout(justify_content="flex-end")
        )], layout=widgets.Layout(width="888px"),
    )

    # Checkt voordat de interface ingeladen word of de labels van het geselecteerde model (Niet verplicht!) gelijk zijn aan die van
    if Model:
        # laat het geselecteerde model in en filtert de labelnamen eruit.
        if Model.endswith(".pt"):

            model = YOLO(Model, task="detect")
            MLabels = model.model.names
            ModelLabels = ""
            for labels in MLabels:
                ModelLabels += f"{MLabels[labels]}<br>"
        elif Model.endswith(".onnx"):
            model = load(Model)
            MLabels = (
                str(model)
                .split('\nmetadata_props {\n  key: "names"\n  value: "')[-1]
                .replace("{", "")
                .replace("}", "")
                .replace("\\'", "")
                .replace("\n", "")
                .replace('"', "")
                .split(", ")
            )
            ModelLabels = ""
            for labels in MLabels:
                ModelLabels += f"{labels.split(': ')[-1]}<br>"

        if LabelLijst.value != ModelLabels:
            # Als de lijsten niet overeenkomen word een extra "Label Check" scherm weergegeven om om de verschillen weer te geven en de gebruiker tussen de 2 opties te laten kiezen
            LLijst = widgets.HTML(
                f"<div style='text-align: right;'><code style='color:red;'><b>Labels.txt</b><br>{LaadLabelLijst()}"
            )
            MLijst = widgets.HTML(
                f"<div style='text-align: left;'><code style='color:green;'><b>Model labels</b><br>{ModelLabels}"
            )

            # PickL of Pick label.txt is de knop voor het negeren van het conflict.
            PickL = widgets.Button(
                value=False, 
                description="Gebruik Labels.txt"
            )
            PickL.style.button_color = "red"

            @PickL.on_click
            def PL(PlaceHolder):
                Conflict.close()
                display(LabelCheck)

            # PickM of Pick Model is de knop om de modellabels te gebruiken. 
            # De functie overschrijft Label.txt met de labels van het model. 
            # Oude labels worden niet bewaard!
            PickM = widgets.Button(
                value=False, 
                description="Vervang Labels.txt"
            )
            PickM.style.button_color = "green"

            @PickM.on_click
            def PM(PlaceHolder):
                with open(LabelDoc, "w+") as e:
                    e.write("")
                    with open(LabelDoc, "a") as f:
                        MLabels = ModelLabels.split("<br>")
                        for labels in MLabels:
                            if labels:
                                f.write(f"{labels}\n")
                LabelLijst.value = LaadLabelLijst()
                Conflict.close()
                display(LabelCheck)

            ConflictTitel = widgets.HTML(
                "<h1>Label check</h1><b>Er is een Conflict gevonden tussen Labels.txt in de label folder en de label van het gekozen model. Dit kan mogelijk gegenereerde annotaties verkeert labelen als de volgorde en/of betekenis van de labels verandert is. Negeer dit conflict (rode knop) of overschrijf de labels in Labels.txt en voorkom dit probleem in de toekomst (groene knop)</b>"
            )

            # Clustert de widgets in een interface
            Conflict = widgets.VBox([
                ConflictTitel,
                widgets.HBox([
                    LLijst, 
                    MLijst
                ], layout=widgets.Layout(justify_content="center", width="400px"),
                ),
                widgets.HBox([
                    PickL, 
                    PickM
                ], layout=widgets.Layout(justify_content="center", width="400px"),
                )], layout=widgets.Layout(width="888px"),
            )
            display(Conflict)
        else:
            display(LabelCheck)
    else:
        display(LabelCheck)
