def Launch(PlaceHolder):
    from ipyfilechooser import FileChooser
    from Modules.ModelPicker import ModelPick
    import ipywidgets as widgets

    #Genereert dialoog boxen
    info1 = widgets.HTML(
        value = "<h3>Map locaties</h3> Deze map bevat alle <b>Foto's</b>:"
    )

    info2 = widgets.HTML(
        value = "Deze map bevat alle <b>Labels</b>:"
    )

    #Roept een widget aan die fungeert als interface om map locaties aan te vragen
    ImagePick = FileChooser()
    ImagePick.show_only_dirs = True

    LabelPick = FileChooser()
    LabelPick.show_only_dirs = True

    #creert een knop om verder te gaan met aangegeven mappen
    submit = widgets.Button(
        value = False,
        description = "Submit",
        button_style = "success"
    )

    @submit.on_click
    def SaveAndLaunch(PlaceHolder):
        if ImagePick.selected_path and LabelPick.selected_path:
            ModelPick(
                ImageMap = ImagePick.selected_path,
                Annotaties = LabelPick.selected_path
            )
            DirsPicker.close()

    WiteLine = widgets.HTML("<b>")

    #voegt alle losse widgets samen in een interface
    DirsPicker = widgets.VBox([
        info1,
        ImagePick,
        info2,
        LabelPick,
        WiteLine,
        submit
    ])
    
    display(DirsPicker)