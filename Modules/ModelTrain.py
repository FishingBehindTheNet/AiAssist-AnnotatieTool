def train():
    import os
    import ipywidgets as widgets
    from ipyfilechooser import FileChooser


    RunningInfo = widgets.HTML(
        value = "Running:"
    )

    ResumeInfo = widgets.HTML(
        value = "selecteer het <b>model</b> waarvan je de training wil afmaken.:"
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
        if Model.selected:
            TrainView.close()
            display(RunningInfo)
            from ultralytics import YOLO
            model = YOLO(Model.selected)
            model.train(resume=True)
            

    WiteLine = widgets.HTML("<b>")

    #voegt alle losse widgets samen in een interface
    Resume = widgets.VBox([
        ResumeInfo,
        Model,
        WiteLine,
        ResumeSubmit,
    ])

    #Genereert dialoog boxen
    Info1 = widgets.HTML(
        value = "selecteer het <b>model</b> waarvan het nieuwe model kan beginnen met leren:"
    )

    Info2 = widgets.HTML(
        value = "Selecteer je <b>Configuration file</b>:"
    )

    Config = FileChooser()

    ModelInput = widgets.Text(
    placeholder='Model naam',
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
        description='Grote batch:',
        disabled=False
    )

    Size = widgets.BoundedIntText(
        value=640,
        min=0,
        max=2000,
        step=1,
        description="Grote foto's:",
        disabled=False
    )

    ProjectPicker = widgets.Select(
        options=[Dir for Dir in os.listdir(os.getcwd()) if os.path.isdir(Dir) and Dir != 'Modules'],
        description='Project:',
        disabled=False
    )

    ProjectInput = widgets.Text(
    placeholder='Project naam',
    description='Nieuw:',
    disabled=False
    )
    ProjectInput.continuous_update = False

    Add = widgets.Button(
        value = False,
        description = "Maak",
        button_style = "info",
        layout = widgets.Layout(width = '80px')
    )

    NewSubmit = widgets.Button(
        value = False,
        description = "Submit",
        button_style = "success"
    )

    @NewSubmit.on_click
    def NewSubmitRun(PlaceHolder):
        if Model.selected and Config.selected and ModelInput.value:
            TrainView.close()
            display(RunningInfo)
            from ultralytics import YOLO
            model = YOLO(Model.selected)
            model.train(
                data = Config.selected,
                epochs = Epochs.value,
                batch = Batch.value,
                imgsz = Size.value,
                project = ProjectPicker.value,
                name = ModelInput.value,
                exist_ok = True,
                save_period = 5            
            )

    WiteLine = widgets.HTML("<b>")

    #voegt alle losse widgets samen in een interface
    NewModelView = widgets.VBox([
        Info1,
        Model,
        Info2,
        Config,
        widgets.HBox([ProjectInput, Add]),
        ProjectPicker,
        ModelInput,
        Epochs,
        Batch,
        Size,
        WiteLine,
        NewSubmit
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
        if Config.selected and ModelInput.value:
            TrainView.close()
            display(RunningInfo)
            from ultralytics import YOLO
            model = YOLO(ScratchModel.value)
            model.train(
                data = Config.selected,
                epochs = Epochs.value,
                batch = Batch.value,
                imgsz = Size.value,
                project = ProjectPicker.value,
                name = ModelInput.value,
                exist_ok = True,
                save_period = 5  
            )

    ScratchModelView = widgets.VBox([
        ScratchModel,
        Info2,
        Config,
        widgets.HBox([ProjectInput, Add]),
        ProjectPicker,
        ModelInput,
        Epochs,
        Batch,
        Size,
        WiteLine,
        ScratchSubmit
    ])

    TrainView = widgets.Tab()
    TrainView.children = [NewModelView, ScratchModelView, Resume]
    TrainView.titles = ('Train vanaf model', 'Train van grond op', 'Resume training')
    display(TrainView)