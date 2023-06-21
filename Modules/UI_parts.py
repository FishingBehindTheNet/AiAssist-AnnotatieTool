from ipyfilechooser import FileChooser
import ipywidgets as widgets
import os

#--------------------------------------------------------------------------------------------------------------------------------------------------------
#Project picker
#--------------------------------------------------------------------------------------------------------------------------------------------------------

ProjectName = widgets.HTML("<b>Project:")

opties = [Dir for Dir in os.listdir(os.getcwd()) if os.path.isdir(Dir) and Dir != 'Modules']
opties.append("")
ProjectPicker = widgets.Select(
    options=opties,
    value="",
    description="",
    tooltip='Selecteer een project',
    disabled=False
)

ProjectInput = widgets.Text(
placeholder='Nieuw (Geen speciale tekens!)',
description='',
disabled=False,
tooltip='Selecteer een project hierboven of geef de naam ven het nieuwe project(GEEN SPECIALE TEKENS) en druk op maak',
layout = widgets.Layout(width = '216px')
)
ProjectInput.continuous_update = False

DataNaamInput = widgets.Text(
placeholder='Naam dataset (Geen speciale tekens!)',
disabled=False,
tooltip = 'Geef de naam van de dataset(GEEN SPECIALE TEKENS). Als er al een dataset bestaat met deze naam word de data samengevoegd',
style={'description_width': 'initial'},
)
DataNaamInput.continuous_update = False

def ProjectLink(Placeholder):
    ProjectInput.value = ProjectPicker.value
ProjectPicker.observe(ProjectLink)

Add = widgets.Button(
    value = False,
    description = "Maak",
    button_style = "info",
    tooltip='Selecteer een project hierboven of geef de naam ven het nieuwe project(GEEN SPECIALE TEKENS) en druk op maak',
    layout = widgets.Layout(width = '80px')
)

def add(PlaceHolder):
    if ProjectInput.value:
        Project=ProjectInput.value
        NewLocation = os.path.join(os.getcwd(), Project)
        if not os.path.exists(NewLocation):
            os.makedirs(NewLocation)
            ProjectPicker.options= [Dir for Dir in os.listdir(os.getcwd()) if os.path.isdir(Dir) and Dir != 'Modules']
            ProjectPicker.value = Project

Add.on_click(add)
ProjectInput.observe(add)

ProjectInterface = widgets.VBox([
    ProjectName,
    ProjectPicker,
    widgets.HBox([
        Add,
        ProjectInput,
    ]),])

#--------------------------------------------------------------------------------------------------------------------------------------------------------
#FilePick
#--------------------------------------------------------------------------------------------------------------------------------------------------------
#Genereert dialoog boxen
ImagePickText = widgets.HTML(
    value = "<h3>Map locaties</h3> Deze map bevat alle <b>Foto's</b>:"
)

ImagePick = FileChooser()
ImagePick.show_only_dirs = True

LabelPickText = widgets.HTML(
    value = "Deze map bevat alle <b>Labels</b>:"
)

LabelPick = FileChooser()
LabelPick.show_only_dirs = True

FilePickInterface = widgets.VBox([
    ImagePickText,
    ImagePick,
    LabelPickText,
    LabelPick
])