from ipyfilechooser import FileChooser
import ipywidgets as widgets
import os

# --------------------------------------------------------------------------------------------------------------------------------------------------------
# Project picker
# --------------------------------------------------------------------------------------------------------------------------------------------------------

ProjectName = widgets.HTML("<b>Selecteer een project folder voor opslag:")

#Maakt een lijst van de mappen in de folder waar de code gedraaid word, bij juist gebruik zijn dit alleen projecten (Module map word eruit gefilterd)
opties = [
    Dir for Dir in os.listdir(os.getcwd()) if os.path.isdir(Dir) and Dir != "Modules"
]

#Voegt een lege optie toe zodat het niet selecteren van een project herkend kan worden.
opties.append("")

#Maakt delen van de interface aan
ProjectPicker = widgets.Select(
    options=opties,
    value="",
    tooltip="Selecteer een project",
    disabled=False,
)

ProjectInput = widgets.Text(
    placeholder="Nieuw (Geen speciale tekens!)",
    description="",
    disabled=False,
    tooltip="Selecteer een project hierboven of geef de naam ven het nieuwe project(GEEN SPECIALE TEKENS) en druk op maak",
    layout=widgets.Layout(width="216px"),
)
ProjectInput.continuous_update = False

#linkt de 2 widgets zodat, wanneer een project geselecteerd word, deze ook in de 
def ProjectLink(Placeholder):
    ProjectInput.value = ProjectPicker.value


ProjectPicker.observe(ProjectLink)

Add = widgets.Button(
    value=False,
    description="Maak",
    button_style="info",
    tooltip="Selecteer een project hierboven of geef de naam ven het nieuwe project(GEEN SPECIALE TEKENS) en druk op maak",
    layout=widgets.Layout(width="80px"),
)


def add(PlaceHolder):
    if ProjectInput.value:
        Project = ProjectInput.value
        NewLocation = os.path.join(os.getcwd(), Project)
        if not os.path.exists(NewLocation):
            os.makedirs(NewLocation)
            ProjectPicker.options = [
                Dir
                for Dir in os.listdir(os.getcwd())
                if os.path.isdir(Dir) and Dir != "Modules"
            ]
            ProjectPicker.value = Project


Add.on_click(add)
ProjectInput.observe(add)

ProjectInterface = widgets.VBox(
    [
        ProjectName,
        ProjectPicker,
        widgets.HBox(
            [
                Add,
                ProjectInput,
            ]
        ),
    ]
)

# --------------------------------------------------------------------------------------------------------------------------------------------------------
# DataOpslagNaam
# --------------------------------------------------------------------------------------------------------------------------------------------------------
#Voor het Invoeren van de naam van een nieuwe dataset
DataNaamInput = widgets.Text(
    placeholder="Naam dataset (Geen speciale tekens!)",
    disabled=False,
    tooltip="Geef de naam van de nieuwe dataset(GEEN SPECIALE TEKENS). Als er al een dataset bestaat met deze naam word de data samengevoegd",
    style={"description_width": "initial"},
)
DataNaamInput.continuous_update = False
# --------------------------------------------------------------------------------------------------------------------------------------------------------
# FilePick
# --------------------------------------------------------------------------------------------------------------------------------------------------------
# Genereert dialoog boxen
ImagePickTitel = widgets.HTML("<b>Selecteer hier de folder met foto's en of segmenten")
ImagePick = FileChooser()
ImagePick.show_only_dirs = True

LabelPickTitel = widgets.HTML("<b>Selecteer hier de folder met bijbehorende annotaties en of labels")
LabelPick = FileChooser()
LabelPick.show_only_dirs = True

#Linkt de 2 widgets zodat wanneer je werkt met de folder organisatie van de pijplijn je maar een folder hoeft te zoeken en de andere automatie voor je klaar staat en je deze allen nog hoeft te accepteren
@ImagePick.register_callback
def LabelPickUpdate(PlaceHolder):
    path = ImagePick.value.replace("images", "labels").removesuffix("Check Later\\")
    if os.path.exists(path):
        LabelPick.default_path = path


@LabelPick.register_callback
def ImagePickUpdate(PlaceHolder):
    path = LabelPick.value.replace("labels", "images")
    if os.path.exists(path):
        ImagePick.default_path = path

#Bouwt de interface op
FilePickInterface = widgets.VBox([ImagePickTitel, ImagePick, LabelPickTitel, LabelPick])
