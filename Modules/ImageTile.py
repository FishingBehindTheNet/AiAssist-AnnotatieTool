import os
from PIL import Image
import ipywidgets as widgets
from Modules import UI_parts
from itertools import product
from ipyfilechooser import FileChooser


def ImageTiler():
    def ImageTile(ImageMap, Output, Size, Overlap):
        docs = [file for file in os.listdir(ImageMap) if file.endswith('.jpeg') or file.endswith('.png')or file.endswith('.jpg')]        
        ProgressBar = widgets.IntProgress(value=0, max=len(docs), description="Progress:")
        WachtScherm = widgets.HTML(value = "<h3>Foto's worden gesegmenteerd:</h3>")
        display(WachtScherm, ProgressBar)

        for Files in docs:
            ProgressBar.value += 1

            image = Image.open(os.path.join(ImageMap, Files))
            Width, Height = image.size

            if Width > Height:
                image = image.rotate(-90, expand=True)
                Width, Height = image.size

            FileName, FileType = os.path.splitext(Files)
            grid = product(range(0, Width, (Size-Overlap)), range(0, Height, (Size-Overlap)))

            for x, y in grid:
                box = (x, y, x+Size, y+Size)
                out = os.path.join(Output, f'{FileName}_{y}_{x}{FileType}')
                image.crop(box).save(out)
            image.close()
        
        ProgressBar.close()
        WachtScherm.close()

    DataNaamInput = widgets.Text(
    placeholder='Naam dataset (Geen speciale tekens!)',
    disabled=False,
    tooltip = 'Geef de naam van de dataset(GEEN SPECIALE TEKENS). Als er al een dataset bestaat met deze naam word de data samengevoegd',
    style={'description_width': 'initial'},
    )
    DataNaamInput.continuous_update = False

    info1 = widgets.HTML(
    value = "Deze map bevat alle <b>Foto's</b> die gesegmenteerd gaan worden:"
    )

    ImagePick = FileChooser()
    ImagePick.show_only_dirs = True

    Size = widgets.BoundedIntText(
        value=640,
        min=0,
        max=2000,
        step=1,
        description='Tile grootte:',
        tooltip="Geef de grote van je segmenten, 640 maakt bijvoorbeeld segmenten van 640 bij 640 pixels",
        disabled=False,
    )

    Overlap = widgets.FloatSlider(
        value=10,
        min=0,
        max=100,
        step=1,
        description='Overlap:',
        orientation='horizontal',
        tooltip="Geef de grote van je overlap, 10% bijvoorbeeld betekent dat er links, rechts, onder en boven 10 van het segment ook op het naastliggende segment afgebeeld word",
        readout_format=''
    )

    pixels = widgets.HTML("Pixels")
    Procent = widgets.HTML("%")
    TileSize = widgets.VBox([widgets.HBox([Size, pixels]), widgets.HBox([Overlap, Procent])])

    submit = widgets.Button(
        value = False,
        description = "Slice",
        button_style = "success",
        layout = widgets.Layout(width = "80px")
    )

    @submit.on_click
    def run(PlaceHolder):
        ImageLocation = os.path.join(UI_parts.ProjectPicker.value, f"Data\\{DataNaamInput.value}\\images")
        LabelLocation = os.path.join(UI_parts.ProjectPicker.value, f"Data\\{DataNaamInput.value}\\labels")
        SuccesScherm = widgets.HTML(
            value = f"""
            <style>
            td:first-child {{
                text-align: right;
            }}
            td:last-child {{
                text-align: left;
            }}
            </style>

            <h3>Succes!</h3> 
            <table>
            <tr>
                <td><b>Foto's:</b></td>
                <td>{ImageLocation}</td>
            </tr>
            <tr>
                <td><b>Labels (Lege map):</b></td>
                <td>{LabelLocation}</td>
            </tr>
            """
        )
        if ImagePick.selected and DataNaamInput.value and UI_parts.ProjectPicker.value:
            dirs_to_create = [
                os.path.join(UI_parts.ProjectPicker.value, f"Data\\{DataNaamInput.value}\\images"),
                os.path.join(UI_parts.ProjectPicker.value, f"Data\\{DataNaamInput.value}\\labels")
            ]
            for dir in dirs_to_create:
                if not os.path.exists(dir):
                    os.makedirs(dir)

            View.close()
            ImageTile(
                ImageMap = ImagePick.value,
                Output = ImageLocation,
                Size = int(Size.value),
                Overlap= int(Size.value*(Overlap.value/100))
            )
            display(SuccesScherm)
        
        elif not ImagePick.selected:
            ErrorCode.value = """
                <div style="text-align: right;">
                    <i><b><code style="color:red;">Map met foto's niet geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>select</b></font></kbd> drukt na het kiezen van een map om je selectie te bevestigen.</code></b></i>
                </div>
                """
        elif not UI_parts.ProjectPicker.value:
             ErrorCode.value = """
                <div style="text-align: right;">
                    <i><b><code style="color:red;">Er is geen Project geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>Maak</b></font></kbd> drukt als je een nieuwe project wil maken/gebruiken.</code></b></i>
                </div>
                """           
        else:
             ErrorCode.value = """
                <div style="text-align: right;">
                    <i><b><code style="color:red;">Er is geen naam opgegeven voor de nieuwe dataset.</code></b></i>
                </div>
                """              

    Titel = widgets.HTML(value =     "<h3>_________________________________________________________Image Tiler/Cutter______________________________________________________________</h3>")
    line = widgets.HTML(value = "<h3>____________________________________________________________________________________________________________________________________________</h3>")
    ErrorCode = widgets.HTML()

    Box1 = widgets.VBox([info1, ImagePick, TileSize])
    Box2 = widgets.VBox([UI_parts.ProjectInterface, DataNaamInput]) 

    View = widgets.VBox([
        Titel,
        widgets.HBox([ 
            Box1,
            Box2,
        ]),
        line,
        widgets.HBox([ErrorCode, submit
        ], layout= widgets.Layout(justify_content="flex-end"))
        ], layout= widgets.Layout(width='888px'))

    display(View)