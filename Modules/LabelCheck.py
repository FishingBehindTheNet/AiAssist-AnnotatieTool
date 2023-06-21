def LabelCheck(ImageMap, Annotaties, Model, ProjectName):
    from Modules.AnotatieTool import Annoteren
    import ipywidgets as widgets
    import os

    #ceckt of er al een LabelDoc bestaat en maakt deze anders aan
    LabelDoc = os.path.join(Annotaties, "Labels.txt")
    if not os.path.exists(LabelDoc):
        with open(LabelDoc, "w+") as a:
            a.write("")

    #functie om de weergegeven lijst van labels te updaten
    def LaadLabelLijst():
        with open(LabelDoc, "r") as b:
            labels = b.read()
            labels = labels.replace("\n", "<br>")
            return "<b>De volgende Labels zijn al geregistreerd:</b><br>" + labels
    if Model:
        if Model.endswith(".pt"):
            from ultralytics import YOLO
            model = YOLO(Model, task='detect')
            MLabels = model.model.names
            ModelLabels = "<b>De volgende Labels zijn al geregistreerd:</b><br>"
            for labels in MLabels:
                ModelLabels += f"{MLabels[labels]}<br>"
        elif Model.endswith(".onnx"):
            from onnx import load
            model = load(Model)
            MLabels = str(model).split('\nmetadata_props {\n  key: \"names\"\n  value: \"')[-1].replace("{", "").replace("}", "").replace("\\'", "").replace("\n", "").replace('"', "").split(", ")
            ModelLabels = "<b>De volgende Labels zijn al geregistreerd:</b><br>"
            for labels in MLabels:
                ModelLabels += f"{labels.split(': ')[-1]}<br>"    

    #weergeeft labels
    LabelLijst = widgets.HTML(
        value = LaadLabelLijst()
    )

    #weergeeft een text box die de input van nieuwe labels faciliteert
    LabelInput = widgets.Text(
        placeholder='Naam label (Geen speciale tekens!)',
        description='Add:',
        disabled=False   
    )

    LabelInput.continuous_update = False

    #Knop voor het toevoegen van Labels
    LabelSubmit = widgets.Button(
        value = False,
        description = "Permanent toevoegen",
        button_style = ""
    )

    #Functie om nieuwe labels toe te voegen en de weergave te updaten
    def AddToList(PlaceHolder):
        with open(LabelDoc, "r") as c:
            if LabelInput.value not in c.read():
                with open(LabelDoc, "a") as d:
                    d.write(LabelInput.value + "\n")
                LabelInput.value = ""
                LabelLijst.value = LaadLabelLijst()

    LabelSubmit.on_click(AddToList)
    LabelInput.observe(AddToList)

    #Knop om de annotatietool te starten
    submit = widgets.Button(
        value = False,
        description = "Start met annoteren",
        button_style = "success"
    )

    Wachtscherm = widgets.HTML(value = "<h3>Laden...</h3>")

    #geeft benodigde gegevens door aan de annotatietool
    @submit.on_click
    def SaveAndLaunch(PlaceHolder):
        LabelCheck.close()
        display(Wachtscherm)
        Annoteren(
            ImageMap = ImageMap,
            Annotaties = Annotaties,
            Labels = LabelDoc,
            Model = Model,
            ProjectName = ProjectName
            )
        Wachtscherm.close()
    
    line = widgets.HTML(value = "<h3>____________________________________________________________________________________________________________________________________________</h3>")

    LabelCheck = widgets.VBox([
        LabelLijst,
        widgets.HBox([
        LabelInput,
        LabelSubmit,
        ]),
        line,
        widgets.HBox([
            submit
        ], layout= widgets.Layout(justify_content="flex-end")),
        ], layout= widgets.Layout(width='888px'))

    #Clustert de widgets in een interface
    if Model:
        if (Model.endswith(".pt") or Model.endswith(".onnx")) and LabelLijst.value != ModelLabels:
            LL = LabelLijst.value
            LLijst= widgets.HTML(LL.replace("<b>De volgende Labels zijn al geregistreerd:</b><br>", "<div style='text-align: right;'><code style='color:red;'><b>Labels.txt</b><br>"))
            ML = ModelLabels
            MLijst = widgets.HTML(ML.replace("<b>De volgende Labels zijn al geregistreerd:</b><br>", "<div style='text-align: left;'><code style='color:green;'><b>Model labels</b><br>"))
            
            PickL = widgets.Button(
            value = False,
            description = "Gebruik Labels.txt"
            )
            PickL.style.button_color = 'red'
            @PickL.on_click
            def PL(PlaceHolder):
                Conflict.close()
                display(LabelCheck)

            PickM = widgets.Button(
            value = False,
            description = "Vervang Labels.txt"
            )
            PickM.style.button_color = 'green'
            @PickM.on_click
            def PM(PlaceHolder):
                with open(LabelDoc, "w+") as e:
                    e.write("")
                    with open(LabelDoc, "a") as f:
                        MLabels = ML.replace("<b>De volgende Labels zijn al geregistreerd:</b><br>", "").split("<br>")
                        for labels in MLabels:
                            if labels:
                                f.write(f"{labels}\n")
                LabelLijst.value = LaadLabelLijst()
                Conflict.close()
                display(LabelCheck)

            ConflictTitel = widgets.HTML("<b>Er is een Conflict gevonden tussen labels.txt in de labelmap en de labellijst van het gekozen model</b>")

            Conflict = widgets.VBox([
                widgets.HBox([
                    ConflictTitel,
                    ],
                    layout= widgets.Layout(justify_content="center", width='800px')),
                widgets.HBox([
                    LLijst,
                    MLijst
                    ],
                    layout= widgets.Layout(justify_content="center", width='800px')),
                widgets.HBox([
                    PickL,
                    PickM
                    ],
                    layout= widgets.Layout(justify_content="center", width='800px')),
                ], layout= widgets.Layout(justify_content="center", width='888px'))
            display(Conflict)

        else:
            display(LabelCheck)
    else:
        display(LabelCheck)