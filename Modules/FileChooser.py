def FilePick(Model, ProjectName):
    from Modules.LabelCheck import LabelCheck
    from Modules import UI_parts
    import ipywidgets as widgets
    import os

    if os.path.exists(os.path.join(os.getcwd(), f"{ProjectName}//Data")):
        UI_parts.ImagePick.default_path = os.path.join(os.getcwd(), f"{ProjectName}//Data")
        UI_parts.LabelPick.default_path = os.path.join(os.getcwd(), f"{ProjectName}//Data")

    #creert een knop om verder te gaan met aangegeven mappen
    submit = widgets.Button(
        value = False,
        description = "Submit",
        button_style = "success"
    )
    
    line = widgets.HTML(value = "<h3>____________________________________________________________________________________________________________________________________________</h3>")
    ErrorCode = widgets.HTML()

    @submit.on_click
    def SaveAndLaunch(PlaceHolder):
        if UI_parts.ImagePick.selected_path and UI_parts.LabelPick.selected_path:
            if UI_parts.ImagePick.selected_path != UI_parts.LabelPick.selected_path:
                LabelCheck(
                    ImageMap = UI_parts.ImagePick.selected_path,
                    Annotaties = UI_parts.LabelPick.selected_path,
                    Model = Model,
                    ProjectName = ProjectName,
                )
                DirsPicker.close()
            else:
                ErrorCode.value = """
                    <div style="text-align: right;">
                        <i><b><code style="color:red;">Map met labels en map met foto's zijn gelijk.<br>Zorg ervoor dat je foto map en label map 2 losse mappen zijn.</code></b></i>
                    </div>

                    """
        elif not UI_parts.ImagePick.selected_path:
            ErrorCode.value = """
                <div style="text-align: right;">
                    <i><b><code style="color:red;">Map met foto's niet geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>select</b></font></kbd> drukt na het kiezen van een map om je selectie te bevestigen.</code></b></i>
                </div>
                """
        else:
            ErrorCode.value = """
                <div style="text-align: right;">
                    <i><b><code style="color:red;">Map met labels niet geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>select</b></font></kbd> drukt na het kiezen van een map om je selectie te bevestigen.</code></b></i>
                </div>

                """

    #voegt alle losse widgets samen in een interface
    DirsPicker = widgets.VBox([
        UI_parts.FilePickInterface,
        line,
        widgets.HBox([
            ErrorCode, 
            submit
        ], layout= widgets.Layout(justify_content="flex-end")),
        ], layout= widgets.Layout(width='888px'))
    
    display(DirsPicker)