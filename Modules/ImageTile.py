import os
from PIL import Image
import ipywidgets as widgets
from itertools import product
from ipyfilechooser import FileChooser

def ImageTiler():
    def ImageTile(ImageMap, Output, Size, Overlap):
        docs = os.listdir(ImageMap)
        ProgressBar = widgets.IntProgress(value=0, max=len(docs), description="Progress:")
        WachtScherm = widgets.HTML(value = "<h3>Foto's worden gesegmenteerd:</h3>")
        display(WachtScherm, ProgressBar)

        for Files in os.listdir(ImageMap):
            ProgressBar.value += 1

            image = Image.open(os.path.join(ImageMap, Files))
            Width, Height = image.size

            FileName, FileType = os.path.splitext(Files)
            grid = product(range(0, Width, (Size-Overlap)), range(0, Height, (Size-Overlap)))

            for x, y in grid:
                box = (x, y, x+Size, y+Size)
                out = os.path.join(Output, f'{FileName}_{y}_{x}{FileType}')
                image.crop(box).save(out)
        
        ProgressBar.close()
        WachtScherm.close()


    Picker = widgets.Select(
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

    def add(PlaceHolder):
        if ProjectInput.value:
            NewLocation = os.path.join(os.getcwd(), ProjectInput.value)
            if not os.path.exists(NewLocation):
                os.makedirs(NewLocation)
                Picker.options= [Dir for Dir in os.listdir(os.getcwd()) if os.path.isdir(Dir) and Dir != 'Modules']
                Picker.value = ProjectInput.value
        ProjectInput.value = ""

    Add.on_click(add)
    ProjectInput.observe(add)

    ImagePick = FileChooser()
    ImagePick.show_only_dirs = True

    Size = widgets.BoundedIntText(
        value=640,
        min=0,
        max=2000,
        step=1,
        description='Tile grote:',
        disabled=False
    )

    Overlap = widgets.FloatSlider(
        value=10,
        min=0,
        max=100,
        step=1,
        description='Overlap:',
        orientation='horizontal',
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
        ImageLocation = os.path.join(Picker.value, "Data\\unlabeled\\images")
        LabelLocation = os.path.join(Picker.value, "Data\\unlabeled\\labels")
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
        if ImagePick.selected:
            dirs_to_create = [
                os.path.join(Picker.value, "Data\\unlabeled\\images"),
                os.path.join(Picker.value, "Data\\unlabeled\\labels")
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

    Titel = widgets.HTML(value = "<h3>_________________________________________________________Image Tiler/Cutter_________________________________________________</h3>")

    Box1 = widgets.VBox([ImagePick, TileSize])
    Box2 = widgets.VBox([
        widgets.HBox([
            ProjectInput,
            Add,
            ]),
        Picker,
        ])

    View = widgets.VBox([
        widgets.HBox([Titel, submit]),
        widgets.HBox([ 
            Box1,
            Box2
        ])])

    display(View)