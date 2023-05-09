def ModelPick(ImageMap, Annotaties):
    from Modules.LabelCheck import LabelCheck
    from ipyfilechooser import FileChooser
    import ipywidgets as widgets
    import os

    #Genereert dialoog boxen
    info1 = widgets.HTML(
        value = "<h3>Model keuze</h3> selecteer het <b>model</b> (getest met .pt en .onnx modelen):"
    )

    info2 = widgets.HTML(
        value = "Input de naam van de dataset. Voorspellingen worden opgeslagen onder ./Model/{naam}/labels:"
    )

    #Roept een widget aan die fungeert als interface om map locaties aan te vragen
    ModelFile = FileChooser()
    ModelFile.show_only_dirs = False

    ProjectInput = widgets.Text(
    placeholder='dataset',
    description='naam:',
    disabled=False
    )
    ProjectInput.continuous_update = False

        #Knop om de annotatietool te starten
    submit = widgets.Button(
        value = False,
        description = "Submit",
        button_style = "success"
    )

    #geeft benodigde gegevens door aan de annotatietool
    @submit.on_click
    def SaveAndLaunch(PlaceHolder):
        LabelCheck(
            ImageMap = ImageMap,
            Annotaties = Annotaties,
            Model = ModelFile.selected,
            DataName = ProjectInput.value            
        )
        ModelPicker.close()
    
    WiteLine = widgets.HTML("<b></b>")

    #voegt alle losse widgets samen in een interface
    ModelPicker = widgets.VBox([
        info1,
        ModelFile,
        info2,
        ProjectInput,
        WiteLine,
        submit
    ])
    
    display(ModelPicker)