def train():
    from ipyfilechooser import FileChooser
    import ipywidgets as widgets
    from Modules import UI_parts
    from ultralytics import YOLO
    import shutil
    import os

    RunningInfo = widgets.HTML(
        value = "Running:"
    )

    ResumeInfo = widgets.HTML(
        value = "selecteer het <b>model.pt (NIET .ONNX)</b> waarvan je de training wil afmaken.:"
    )

    Model = FileChooser()

    ResumeSubmit = widgets.Button(
        value = False,
        description = "Submit",
        button_style = "success",
        layout = widgets.Layout(width = "80px")
        
    )

    @ResumeSubmit.on_click
    def ResumeSubmitRun(PlaceHolder):
        if not Model.selected:
            ErrorCode.value = """
            <div style="text-align: right;">
                <i><b><code style="color:red;">Er is geen model geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>select</b></font></kbd> drukt na het kiezen van model.pt om je selectie te bevestigen.</code></b></i>
            </div>
            """
        elif os.path.splitext(Model.selected)[-1] == ".pt":
            TrainView.close()
            display(RunningInfo)
            from ultralytics import YOLO
            model = YOLO(Model.selected)
            model.train(resume=True)

            project = os.path.splitext(Model.selected)[-4]
            name = os.path.splitext(Model.selected)[-3]

            if not os.path.exists(rf"{os.getcwd()}\{project}\Modellen"):
                os.mkdir(rf"{os.getcwd()}\{project}\Modellen")

            Best= rf"{os.getcwd()}\{project}\{name}\weights\best.pt"
            BestNew= rf"{os.getcwd()}\{project}\Modellen\{name}_best.pt"
            shutil.copy(Best, BestNew)
            BestModel = YOLO(BestNew)
            BestModel.export(format='onnx')

            Last= rf"{os.getcwd()}\{project}\{name}\weights\last.pt"
            LastNew= rf"{os.getcwd()}\{project}\Modellen\{name}_last.pt"
            shutil.copy(Last, LastNew)
            LastModel = YOLO(LastNew)
            LastModel.export(format='onnx')
            
        else:
            ErrorCode.value = """
            <div style="text-align: right;">
                <i><b><code style="color:red;">Het gekozen model is geen .pt file en kan dus niet gebruikt worden<br>Selecteer een ander bestand</code></b></i>
            </div>
            """
            

    line = widgets.HTML(value = "<h3>_________________________________________________________________________________________________________________________________________</h3>")
    ErrorCode = widgets.HTML()

    #voegt alle losse widgets samen in een interface
    Resume = widgets.VBox([
        ResumeInfo,
        Model,
        line,
        widgets.HBox([
            ErrorCode, 
            ResumeSubmit
        ], layout= widgets.Layout(justify_content="flex-end"))
    ])

    #Genereert dialoog boxen
    Info1 = widgets.HTML(
        value = "selecteer het <b>model.pt (NIET .ONNX)</b> waarvan het nieuwe model kan beginnen met leren:"
    )

    Info2 = widgets.HTML(
        value = "Selecteer je <b>Configuration file</b>:"
    )

    Config = FileChooser()

    ModelInput = widgets.Text(
    placeholder='Model naam (Geen speciale tekens!)',
    description='Model:',
    disabled=False
    )
    ModelInput.continuous_update = False

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

    NewSubmit = widgets.Button(
        value = False,
        description = "Submit",
        button_style = "success"
    )

    @NewSubmit.on_click
    def NewSubmitRun(PlaceHolder):
        if not Model.selected:
            ErrorCode.value = """
            <div style="text-align: right;">
                <i><b><code style="color:red;">Er is geen model.pt geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>select</b></font></kbd> drukt na het kiezen van model.pt om je selectie te bevestigen.</code></b></i>
            </div>
            """
        elif not os.path.splitext(Model.selected)[-1] == ".pt":
            ErrorCode.value = """
            <div style="text-align: right;">
                <i><b><code style="color:red;">Het gekozen model is geen .pt file en kan dus niet gebruikt worden<br>Selecteer een ander bestand</code></b></i>
            </div>
            """
        elif not Config.selected:
            ErrorCode.value = """
            <div style="text-align: right;">
                <i><b><code style="color:red;">Er is geen config.yaml geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>select</b></font></kbd> drukt na het kiezen van het bestand om je selectie te bevestigen.</code></b></i>
            </div>
            """
        elif not os.path.splitext(Config.selected)[-1] == ".yaml":
            ErrorCode.value = """
            <div style="text-align: right;">
                <i><b><code style="color:red;">Het gekozen config bestand is geen .yaml file en kan dus niet gebruikt worden<br>Selecteer een ander bestand</code></b></i>
            </div>
            """
        elif not ModelInput.value:
            ErrorCode.value = """
            <div style="text-align: right;">
                <i><b><code style="color:red;">Er is geen model naam opgegeven</code></b></i>
            </div>
            """
        elif not UI_parts.ProjectPicker.value:
            ErrorCode.value = """
            <div style="text-align: right;">
                <i><b><code style="color:red;">Er is geen Project geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>Maak</b></font></kbd> drukt als je een nieuwe project wil maken/gebruiken.</code></b></i>
            </div>
            """

        elif os.path.splitext(Model.selected)[-1] == ".pt":
            TrainView.close()
            display(RunningInfo)
            from ultralytics import YOLO
            model = YOLO(Model.selected)
            model.train(
                data = Config.selected,
                epochs = Epochs.value,
                batch = Batch.value,
                imgsz = Size.value,
                project = UI_parts.ProjectPicker.value,
                name = ModelInput.value,
                exist_ok = True,           
            )

            Modellen = os.path.join(os.getcwd(), f"{UI_parts.ProjectPicker.value}\\Modellen")
            Resultaten = os.path.join(os.getcwd(), f"{UI_parts.ProjectPicker.value}\\{ModelInput.value}")
            SuccesScherm = widgets.HTML(
                value = f"""
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
            )
                
            if not os.path.exists(Modellen):
                os.mkdir(Modellen)

            Best= rf"{os.getcwd()}\{UI_parts.ProjectPicker.value}\{ModelInput.value}\weights\best.pt"
            BestNew= rf"{os.getcwd()}\{UI_parts.ProjectPicker.value}\Modellen\{ModelInput.value}_best.pt"
            shutil.copy(Best, BestNew)
            BestModel = YOLO(BestNew)
            BestModel.export(format='onnx')

            Last= rf"{os.getcwd()}\{UI_parts.ProjectPicker.value}\{ModelInput.value}\weights\last.pt"
            LastNew= rf"{os.getcwd()}\{UI_parts.ProjectPicker.value}\Modellen\{ModelInput.value}_last.pt"
            shutil.copy(Last, LastNew)
            LastModel = YOLO(LastNew)
            LastModel.export(format='onnx')
            RunningInfo.close()
            display(SuccesScherm)

    WiteLine = widgets.HTML("<b>")

    #voegt alle losse widgets samen in een interface
    NewModelView = widgets.VBox([
        Info1,
        Model,
        Info2,
        Config,
        UI_parts.ProjectInterface,
        ModelInput,
        Epochs,
        Batch,
        Size,
        line,
        widgets.HBox([
            ErrorCode, 
            NewSubmit
        ], layout= widgets.Layout(justify_content="flex-end"))
    ])

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
        elif not os.path.splitext(Config.selected)[-1] == ".yaml":
            ErrorCode.value = """
            <div style="text-align: right;">
                <i><b><code style="color:red;">Het gekozen config bestand is geen .yaml file en kan dus niet gebruikt worden<br>Selecteer een ander bestand</code></b></i>
            </div>
            """
        elif not ModelInput.value:
            ErrorCode.value = """
            <div style="text-align: right;">
                <i><b><code style="color:red;">Er is geen model naam opgegeven</code></b></i>
            </div>
            """
        elif not UI_parts.ProjectPicker.value:
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
                project = UI_parts.ProjectPicker.value,
                name = ModelInput.value,
                exist_ok = True
            )
                
            if not os.path.exists(rf"{os.getcwd()}\{UI_parts.ProjectPicker.value}\Modellen"):
                os.mkdir(rf"{os.getcwd()}\{UI_parts.ProjectPicker.value}\Modellen")

            Best= rf"{os.getcwd()}\{UI_parts.ProjectPicker.value}\{ModelInput.value}\weights\best.pt"
            BestNew= rf"{os.getcwd()}\{UI_parts.ProjectPicker.value}\Modellen\{ModelInput.value}_best.pt"
            shutil.copy(Best, BestNew)
            BestModel = YOLO(BestNew)
            BestModel.export(format='onnx')

            Last= rf"{os.getcwd()}\{UI_parts.ProjectPicker.value}\{ModelInput.value}\weights\last.pt"
            LastNew= rf"{os.getcwd()}\{UI_parts.ProjectPicker.value}\Modellen\{ModelInput.value}_last.pt"
            shutil.copy(Last, LastNew)
            LastModel = YOLO(LastNew)
            LastModel.export(format='onnx')

    ScratchModelView = widgets.VBox([
        ScratchModel,
        Info2,
        Config,
        UI_parts.ProjectInterface,
        ModelInput,
        Epochs,
        Batch,
        Size,
        line,
        widgets.HBox([
            ErrorCode, 
            ScratchSubmit,
        ], layout= widgets.Layout(justify_content="flex-end"))
    ])

    TrainView = widgets.Tab(layout= widgets.Layout(width='900px'))
    TrainView.children = [NewModelView, ScratchModelView, Resume]
    TrainView.titles = ('Train vanaf model', 'Train van grond op', 'Resume training')
    display(TrainView)