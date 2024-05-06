from ipyfilechooser import FileChooser
import ipywidgets as widgets
from Modules import Q_UIparts, Q_UniversalFunction
from ultralytics import YOLO
import shutil
import os

#vaste variabelen
ModellenMap = "Modellen"
ResultatenMap = "Model Resultaten"



def train():
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #general code
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    RunningInfo = widgets.HTML(
        value = "Running:"
    )

    #text vak voor het opgeven van de naam van het nieuwe model
    ModelNaam = widgets.Text(
    placeholder='Model naam (Geen speciale tekens!)',
    description='Model:',
    disabled=False
    )
    ModelNaam.continuous_update = False

    # Maakt een selectie vak voor cofig file aan. Wanneer een Config file geselecteerd word word de naam van het data eruit gefilterd en al value voor de modelnaam gebruikt.
    # Dit word aanbevolen om een goed beeld te behouden van welk model op welke data getraind is.
    Config = FileChooser(filter_pattern="*.yaml", title="<b>Selecteer hier je configuration.yaml file:")
    @Config.register_callback
    def ModelInputUpdate(Placeholder):
        ModelNaam.value = str(Config.selected_filename).replace("_Config.yaml", "")

    # widget voor maken van horizontale lijn
    line = widgets.HTML(value = "<hr>")
    #Text blok voor het weergeven van errorcodes wanneer nodig
    ErrorCode = widgets.HTML()

    Epochs = widgets.BoundedIntText(
        value=50,
        min=10,
        max=10000000,
        step=1,
        description='Num epochs:',
        disabled=False
    )

    Batch = widgets.BoundedIntText(
        value=16,
        min=0,
        max=50,
        step=1,
        description='image/batch:',
        disabled=False
    )

    Size = widgets.BoundedIntText(
        value=640,
        min=0,
        max=2000,
        step=1,
        description="Foto Size:",
        disabled=False
    )

    # Laatste stap van de code. kopieert het nieuw getrainde model naar de Modellen map van 
    # het geselecteerde project, hernoemt het model en maakt een .ONNX versie naast de .pt versie. Dit word voor zowel het laatste als het beste model gedaan.
    def LastSteps(Project, ModelNaam):
        Modellen = f"{Project}/{ModellenMap}"
        Resultaten = f"{Project}/{ResultatenMap}/{ModelNaam}/training"
            
        if not os.path.exists(Modellen):
            os.mkdir(Modellen)

        Best= os.path.join(
            os.getcwd(), 
            Resultaten,
            "weights/best.pt"
        )
        BestNew= os.path.join(
            os.getcwd(), 
            Modellen,
            f"{ModelNaam}_best.pt"
        )
        shutil.copy(Best, BestNew)
        BestModel = YOLO(BestNew)
        BestModel.export(format='onnx')

        Last= os.path.join(
            os.getcwd(), 
            Resultaten, 
            "weights/last.pt"
        )
        LastNew= os.path.join(
            os.getcwd(), 
            Modellen,
            f"{ModelNaam}_last.pt"
        )
        shutil.copy(Last, LastNew)
        LastModel = YOLO(LastNew)
        LastModel.export(format='onnx')

        # Maakt een scherm die de locatie van de gegenereerde bestanden weergeeft. dit word weergeven wanneer de training klaar is.
        RunningInfo.value = f"""
            <style>
            td:first-child {{
                text-align: right;
            }}
            td:last-child {{
                text-align: left;
            }}
            </style>

            <h3>Succes!</h3> 
            <table>
            <tr>
                <td><b>Modellen:</b></td>
                <td>{Modellen}</td>
            </tr>
            <tr>
                <td><b>Resultaten:</b></td>
                <td>{Resultaten}</td>
            </tr>
            """

    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Resume training specific code
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    ResumeModel = FileChooser(filter_pattern="*.pt", title="<b>Selecteer hier het last.pt van het model waarvan je de training wil afmaken<br> uit je \"Model Resultaten/{model naam}/Training/weights\" map:")

    ResumeSubmit = widgets.Button(
        value = False,
        description = "Submit",
        button_style = "success",
        layout = widgets.Layout(width = "80px")
        
    )

    @ResumeSubmit.on_click
    def ResumeSubmitRun(PlaceHolder):
        if not ResumeModel.selected:
            ErrorCode.value = """
            <div style="text-align: right;">
                <i><b><code style="color:red;">Er is geen model geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>select</b></font></kbd> drukt na het kiezen van model.pt om je selectie te bevestigen.</code></b></i>
            </div>
            """
        else:
            project = str(ResumeModel.selected).split("/")[-6]
            name = str(ResumeModel.selected).split("/")[-4]

            TrainView.close()
            display(RunningInfo)
            model = YOLO(ResumeModel.selected)
            model.train(resume=True)

            LastSteps(Project=project, ModelNaam=name)

    #voegt alle losse widgets samen in een interface
    Resume = widgets.VBox([
        ResumeModel,
        line,
        widgets.HBox([
            ErrorCode, 
            ResumeSubmit
        ], layout= widgets.Layout(justify_content="flex-end"))
    ])

    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #training vanaf model specific code
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    OudModel = FileChooser(filter_pattern="*.pt", title= "<b>Selecteer hier het model.pt wat als startpunt gaat dienen voor de training van het nieuwe model.")

    NewSubmit = widgets.Button(
        value = False,
        description = "Submit",
        button_style = "success"
    )

    @NewSubmit.on_click
    def NewSubmitRun(PlaceHolder):
        if not OudModel.selected:
            ErrorCode.value = """
            <div style="text-align: right;">
                <i><b><code style="color:red;">Er is geen model.pt geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>select</b></font></kbd> drukt na het kiezen van model.pt om je selectie te bevestigen.</code></b></i>
            </div>
            """
        elif not Config.selected:
            ErrorCode.value = """
            <div style="text-align: right;">
                <i><b><code style="color:red;">Er is geen config.yaml geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>select</b></font></kbd> drukt na het kiezen van het bestand om je selectie te bevestigen.</code></b></i>
            </div>
            """
        elif not ModelNaam.value:
            ErrorCode.value = """
            <div style="text-align: right;">
                <i><b><code style="color:red;">Er is geen model naam opgegeven</code></b></i>
            </div>
            """
        elif not Q_UIparts.ProjectPicker.value:
            ErrorCode.value = """
            <div style="text-align: right;">
                <i><b><code style="color:red;">Er is geen Project geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>Maak</b></font></kbd> drukt als je een nieuwe project wil maken/gebruiken.</code></b></i>
            </div>
            """

        elif os.path.splitext(OudModel.selected)[-1] == ".pt":
            TrainView.close()
            display(RunningInfo)
            from ultralytics import YOLO
            model = YOLO(OudModel.selected)
            model.train(
                data = Config.selected,
                epochs = Epochs.value,
                batch = Batch.value,
                imgsz = Size.value,
                project = Q_UIparts.ProjectPicker.value,
                name = f"{ResultatenMap}/{ModelNaam.value}/training",
                exist_ok = False,           
            )
            LastSteps(Project=Q_UIparts.ProjectPicker.value, ModelNaam=ModelNaam.value)

    WiteLine = widgets.HTML("<b>")

    #voegt alle losse widgets samen in een interface
    NewModelView = widgets.VBox([
        OudModel,
        Config,
        Q_UIparts.ProjectInterface,
        ModelNaam,
        Epochs,
        Batch,
        Size,
        line,
        widgets.HBox([
            ErrorCode, 
            NewSubmit
        ], layout= widgets.Layout(justify_content="flex-end"))
    ])

    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #training vanaf grond specific code
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    ScratchModel=widgets.Dropdown(
        options = [("nano", "yolov8n.pt"), ("Small", "yolov8s.pt"), ("medium", "yolov8m.pt"), ("Large", "yolov8l.pt"), ("Xtra large", "yolov8x.pt")],
        value = "yolov8n.pt",
        description = 'Yolo model:',
    )

    ScratchSubmit = widgets.Button(
        value = False,
        description = "Submit",
        button_style = "success"
    )

    @ScratchSubmit.on_click
    def ScratchSubmitRun(PlaceHolder):
        if not Config.selected:
            ErrorCode.value = """
            <div style="text-align: right;">
                <i><b><code style="color:red;">Er is geen config.yaml geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>select</b></font></kbd> drukt na het kiezen van het bestand om je selectie te bevestigen.</code></b></i>
            </div>
            """
        elif not ModelNaam.value:
            ErrorCode.value = """
            <div style="text-align: right;">
                <i><b><code style="color:red;">Er is geen model naam opgegeven</code></b></i>
            </div>
            """
        elif not Q_UIparts.ProjectPicker.value:
            ErrorCode.value = """
            <div style="text-align: right;">
                <i><b><code style="color:red;">Er is geen Project geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>Maak</b></font></kbd> drukt als je een nieuwe project wil maken/gebruiken.</code></b></i>
            </div>
            """
        else:
            TrainView.close()
            display(RunningInfo)
            from ultralytics import YOLO
            model = YOLO(ScratchModel.value)
            model.train(
                data = Config.selected,
                epochs = Epochs.value,
                batch = Batch.value,
                imgsz = Size.value,
                project = Q_UIparts.ProjectPicker.value,
                name = f"{ResultatenMap}/{ModelNaam.value}/training",
                exist_ok = False
            )
            LastSteps(Project=Q_UIparts.ProjectPicker.value, ModelNaam=ModelNaam.value)
            

    ScratchModelView = widgets.VBox([
        ScratchModel,
        Config,
        Q_UIparts.ProjectInterface,
        ModelNaam,
        Epochs,
        Batch,
        Size,
        line,
        widgets.HBox([
            ErrorCode, 
            ScratchSubmit,
        ], layout= widgets.Layout(justify_content="flex-end"))
    ])

    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #general interface
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    TrainView = widgets.Tab(layout= widgets.Layout(width='900px'))
    TrainView.children = [NewModelView, ScratchModelView, Resume]
    TrainView.titles = ('Train vanaf model', 'Train van grond op', 'Resume training')
    display(TrainView)