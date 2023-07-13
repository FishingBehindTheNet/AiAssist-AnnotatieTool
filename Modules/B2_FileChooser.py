from Modules.B3_LabelCheck import LabelCheck
from Modules import Q_UIparts
import ipywidgets as widgets
import os


def FilePick(Model, ProjectName):
    Titel = widgets.HTML("<h1>Folder selectie")

    # Checkt of het eerder geselecteerde project (niet verplicht) een folder met annotaties heeft en zet deze als startpunten van ImagePick en LabelPick zodat data sneller geselecteerd kan worden
    if os.path.exists(os.path.join(os.getcwd(), f"{ProjectName}//Data//Annoteren")):
        Q_UIparts.ImagePick.default_path = os.path.join(
            os.getcwd(), f"{ProjectName}//Data//Annoteren"
        )
        Q_UIparts.LabelPick.default_path = os.path.join(
            os.getcwd(), f"{ProjectName}//Data//Annoteren"
        )

    # creëert een knop om verder te gaan met aangegeven folders
    submit = widgets.Button(
        value=False,
        description="Submit",
        button_style="success",
    )

    line = widgets.HTML(value="<h3>")
    ErrorCode = widgets.HTML()

    # Checkt of er een folder voor zowel
    @submit.on_click
    def SaveAndLaunch(PlaceHolder):
        if Q_UIparts.ImagePick.selected_path and Q_UIparts.LabelPick.selected_path:
            LabelCheck(
                ImageMap=Q_UIparts.ImagePick.selected_path,
                Annotaties=Q_UIparts.LabelPick.selected_path,
                Model=Model,
                ProjectName=ProjectName,
            )
            DirsPicker.close()
        elif not Q_UIparts.ImagePick.selected_path:
            ErrorCode.value = """
                <div style="text-align: right;">
                    <i><b><code style="color:red;">Folder met foto's niet geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>select</b></font></kbd> drukt na het kiezen van een folder om je selectie te bevestigen.</code></b></i>
                </div>
                """
        else:
            ErrorCode.value = """
                <div style="text-align: right;">
                    <i><b><code style="color:red;">Folder met labels niet geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>select</b></font></kbd> drukt na het kiezen van een folder om je selectie te bevestigen.</code></b></i>
                </div>
                """

    # voegt alle losse widgets samen in een interface
    DirsPicker = widgets.VBox([
        Titel,        
        Q_UIparts.FilePickInterface,
        line,
        widgets.HBox([
            ErrorCode, 
            submit
        ], layout=widgets.Layout(justify_content="flex-end")
        )], layout=widgets.Layout(width="888px"),
    )

    display(DirsPicker)
