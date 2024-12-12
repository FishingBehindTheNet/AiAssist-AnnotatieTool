from Modules.B2_FileChooser import FilePick
from Modules.Q_UIparts import OutputScherm
from ipyfilechooser import FileChooser
from Modules import Q_UIparts
import ipywidgets as widgets
import os


def Launch():
    OutputScherm.clear_output(wait=False)
    Titel = widgets.HTML("<h1>Model keuze (Niet verplicht!)")

    # Roept een widget aan die fungeert als interface om Folder locaties aan te vragen
    ModelFile = FileChooser(
        filter_pattern=["*.pt", "*.onnx"],
        title="<b>Selecteer hier een model voor de AI assist (alleen .pt of .onnx modellen):",
    )
    ModelFile.show_only_dirs = False

    # Maakt een knop en bijbehorende functie om de selectie te bevestigen
    submit = widgets.Button(
        value=False,
        description="Submit",
        button_style="success",
        layout=widgets.Layout(width="80px"),
    )

    @submit.on_click
    def SaveAndLaunch(PlaceHolder):
        # If functie om te checken of een model geselecteerd is en zo ja of er ook een project geselecteerd is en update de interface naar het volgende scherm
        if ModelFile.selected:
            if Q_UIparts.ProjectPicker.value:
                OutputScherm.clear_output(wait=True)
                FilePick(
                    Model=ModelFile.selected, ProjectName=Q_UIparts.ProjectPicker.value
                )
            else:
                ErrorCode.value = """
                    <div style="text-align: right;">
                        <i><b><code style="color:red;">Er is een wel een model maar geen Project geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>Maak</b></font></kbd> drukt als je een nieuwe project wil maken/gebruiken.</code></b></i>
                    </div>
                    """
        else:
            OutputScherm.clear_output(wait=True)
            FilePick(
                Model=ModelFile.selected, ProjectName=Q_UIparts.ProjectPicker.value
            )

    line = widgets.HTML(value="<hr>")
    ErrorCode = widgets.HTML()

    ModelPicker = widgets.VBox([
        Titel,
        Q_UIparts.ProjectInterface,
        ModelFile,
        line,
        widgets.HBox([
            ErrorCode, 
            submit
        ], layout=widgets.Layout(justify_content="flex-end")
        )], layout=widgets.Layout(width="888px"),
    )
    
    OutputScherm.close()
    with OutputScherm:
        display(ModelPicker)
