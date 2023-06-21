def Launch():
    from Modules.FileChooser import FilePick
    from ipyfilechooser import FileChooser
    from Modules import UI_parts
    import ipywidgets as widgets
    import os

    #Genereert dialoog boxen
    info1 = widgets.HTML(
        value = "<h3>Model keuze</h3> Selecteer je project. Voorspellingen worden opgeslagen onder ./{Project}/Voorspellingen:"
    )

    info2 = widgets.HTML(
        value = "selecteer het <b>model</b> (.pt of .onnx modelen):"
    )

    #Roept een widget aan die fungeert als interface om map locaties aan te vragen
    ModelFile = FileChooser()
    ModelFile.show_only_dirs = False

    submit = widgets.Button(
        value = False,
        description = "Submit",
        button_style = "success",
        layout = widgets.Layout(width = "80px")
    )

    @submit.on_click
    def SaveAndLaunch(PlaceHolder):
        if ModelFile.selected:
            if UI_parts.ProjectPicker.value:
                ProjectDir = os.path.join(os.getcwd(), UI_parts.ProjectPicker.value)
                if not os.path.exists(os.path.join(ProjectDir, "Voorspellingen")):
                    os.makedirs(os.path.join(ProjectDir, "Voorspellingen"))
                ModelPicker.close()
                FilePick(
                    Model = ModelFile.selected,
                    ProjectName = UI_parts.ProjectPicker.value            
                )    
            else:
                ErrorCode.value = """
                    <div style="text-align: right;">
                        <i><b><code style="color:red;">Er is een wel een model maar geen Project geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>Maak</b></font></kbd> drukt als je een nieuwe project wil maken/gebruiken.</code></b></i>
                    </div>
                    """
        else:
            ModelPicker.close()
            FilePick(
                Model = ModelFile.selected,
                ProjectName = UI_parts.ProjectPicker.value            
            )
    
    line = widgets.HTML(value = "<h3>____________________________________________________________________________________________________________________________________________</h3>")
    ErrorCode = widgets.HTML()

    ModelPicker = widgets.VBox([
        info1,
        UI_parts.ProjectInterface,
        info2,
        ModelFile,
        line,
        widgets.HBox([
            ErrorCode, 
            submit
        ], layout= widgets.Layout(justify_content="flex-end")),
        ], layout= widgets.Layout(width='888px'))

    display(ModelPicker)