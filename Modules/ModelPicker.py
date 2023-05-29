def ModelPick(ImageMap, Annotaties):
    from Modules.LabelCheck import LabelCheck
    from ipyfilechooser import FileChooser
    import ipywidgets as widgets
    import os

    #Genereert dialoog boxen
    info1 = widgets.HTML(
        value = "<h3>Model keuze</h3> Selecteer je project. Voorspellingen worden opgeslagen onder ./{Project}/Voorspellingen:"
    )

    info2 = widgets.HTML(
        value = "selecteer het <b>model</b> (getest met .pt en .onnx modelen):"
    )

    #Roept een widget aan die fungeert als interface om map locaties aan te vragen
    ModelFile = FileChooser()
    ModelFile.show_only_dirs = False


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

    submit = widgets.Button(
        value = False,
        description = "Submit",
        button_style = "success",
        layout = widgets.Layout(width = "80px")
    )

    def add(PlaceHolder):
        if ProjectInput.value:
            NewLocation = os.path.join(os.getcwd(), ProjectInput.value)
            if not os.path.exists(NewLocation):
                os.makedirs(NewLocation)
                ProjectPicker.options= [Dir for Dir in os.listdir(os.getcwd()) if os.path.isdir(Dir) and Dir != 'Modules']
                ProjectPicker.value = ProjectInput.value
        ProjectInput.value = ""

    Add.on_click(add)
    ProjectInput.observe(add)

    @submit.on_click
    def SaveAndLaunch(PlaceHolder):
        if ModelFile.selected:
            ProjectDir = os.path.join(os.getcwd(), ProjectPicker.value)
            if not os.path.exists(os.path.join(ProjectDir, "Voorspellingen")):
                os.makedirs(os.path.join(ProjectDir, "Voorspellingen"))
        ModelPicker.close()
        LabelCheck(
            ImageMap = ImageMap,
            Annotaties = Annotaties,
            Model = ModelFile.selected,
            ProjectName = ProjectPicker.value            
        )

    ModelPicker = widgets.VBox([
        info1,
        widgets.HBox([
            ProjectInput,
            Add,
        ]),
        ProjectPicker,
        info2,
        ModelFile,
        submit
        ])

    display(ModelPicker)