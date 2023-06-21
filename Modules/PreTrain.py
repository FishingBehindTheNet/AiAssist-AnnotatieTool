from Modules import UI_parts
import ipywidgets as widgets
import random
import shutil   
import os

def AnnotationMove():
    ModelInput = widgets.Text(
        placeholder='Model',
        description='Model naam:',
        disabled=False
        )
    ModelInput.continuous_update = False

    Move = widgets.ToggleButton(
            description="Copy",
            value = False,
            button_style = "info",
            layout = widgets.Layout(width = "75px")
            )

    def on_button_clicked(PlaceHolder):
        if Move.value:
            Move.description = "Move"
            Move.button_style = "warning"       
        else:
            Move.description = "Copy"
            Move.button_style = "info"

    Move.observe(on_button_clicked)

    Val = widgets.FloatSlider(
        value=20,
        min=0,
        max=100,
        step=1,
        description='Validatie set:',
        orientation='horizontal',
        readout_format=''
    )

    Test = widgets.FloatSlider(
        value=10,
        min=0,
        max=100,
        step=1,
        description='Test set:',
        orientation='horizontal',
        readout_format=''
    )

    def update(PlaceHolder):
        Train.value = (100 - Val.value - Test.value)

    Val.observe(update)
    Test.observe(update)

    Train = widgets.FloatSlider(
        value = (100 - Val.value - Test.value),
        min = 0,
        max = 100,
        step = 1,
        description ='Training set:',
        orientation ='horizontal',
        disabled = True,
        readout_format = ''
    )

    submit = widgets.Button(
        value = False,
        description = "Run",
        button_style = "success",
        layout = widgets.Layout(width = "80px")
    )

    WachtScherm = widgets.HTML(value = "<h3>Foto's en Labels worden verplaatst:</h3>")

    @submit.on_click
    def run(PlaceHolder):
        ImageLocation = os.path.join(os.getcwd(), f"{UI_parts.ProjectPicker.value}\\Model data\\{ModelInput.value}\\images")
        LabelLocation = os.path.join(os.getcwd(), f"{UI_parts.ProjectPicker.value}\\Model data\\{ModelInput.value}\\labels")
        ConfigLocation = os.path.join(os.getcwd(), f"{UI_parts.ProjectPicker.value}\\Model data\\{ModelInput.value}\\{ModelInput.value}_Config.yaml")
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
                <td><b>Labels:</b></td>
                <td>{LabelLocation}</td>
            </tr>
            <tr>
                <td><b>Config file:</b></td>
                <td>{ConfigLocation}</td>
            </tr>
            """
        )

        if UI_parts.ImagePick.selected and UI_parts.LabelPick.selected and ModelInput.value and UI_parts.ProjectPicker.value:
            View.close()
            preTrain(
                Labels = UI_parts.LabelPick.selected_path,
                Images = UI_parts.ImagePick.selected_path,
                ProjectName= UI_parts.ProjectPicker.value,
                ModelName = ModelInput.value,
                validatiepercentage = (Val.value/100),
                testpercentage= (Test.value/100),
                move = Move.value
            )
            display(SuccesScherm)
        elif not UI_parts.ImagePick.selected_path:
            ErrorCode.value = """
                <div style="text-align: right;">
                    <i><b><code style="color:red;">Map met foto's niet geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>select</b></font></kbd> drukt na het kiezen van een map om je selectie te bevestigen.</code></b></i>
                </div>
                """
        elif not UI_parts.LabelPick.selected_path:
            ErrorCode.value = """
                <div style="text-align: right;">
                    <i><b><code style="color:red;">Map met labels niet geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>select</b></font></kbd> drukt na het kiezen van een map om je selectie te bevestigen.</code></b></i>
                </div>

                """
        elif not UI_parts.ProjectPicker.value:
            ErrorCode.value = """
                <div style="text-align: right;">
                    <i><b><code style="color:red;">Er is geen Project geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>Maak</b></font></kbd> drukt als je een nieuwe project wil maken/gebruiken.</code></b></i>
                </div>
                """
        elif not ModelInput.value:
            ErrorCode.value = """
                <div style="text-align: right;">
                    <i><b><code style="color:red;">Er is geen model naam opgegeven</code></b></i>
                </div>
                """
            
    Procent = widgets.HTML("%")
    DataSplit = widgets.VBox([widgets.HBox([Test, Procent]), widgets.HBox([Val, Procent]), widgets.HBox([Train, Procent])])

    Titel = widgets.HTML(value = "<h3>______________________________________________________________Data move_________________________________________________________________</h3>")
    TitelV1 = widgets.HTML(value = "<h3>_______________________Huidige Locatie_____________________</h3>")
    TitelV2 = widgets.HTML(value = "<h3>_____________________Toekomstige locatie_____________________</h3>")
    line = widgets.HTML(value = "<h3>____________________________________________________________________________________________________________________________________________</h3>")
    ErrorCode = widgets.HTML()

    ModelPicker = widgets.VBox([
        UI_parts.ProjectInterface,
        ModelInput,])

    Vlak1 = widgets.HBox([TitelV1, Move, TitelV2])
    Vlak2 = UI_parts.FilePickInterface
    Vlak3 = widgets.VBox([ModelPicker, DataSplit])
    

    View = widgets.VBox([
        Titel,
        Vlak1,
        widgets.HBox([Vlak2, Vlak3]),
        line,
        widgets.HBox([ErrorCode, submit
        ], layout= widgets.Layout(justify_content="flex-end"))
        ], layout= widgets.Layout(width='888px'))
    
    display(View)

def preTrain(Labels, Images, ProjectName, ModelName, validatiepercentage=0.2, testpercentage=0.0, move=False):
    docs = os.listdir(Labels)
    ProgressBar = widgets.IntProgress(value=0, max=len(docs)-1, description="Progress:")
    WachtScherm = widgets.HTML(value = "<h3>Foto's en Labels worden verplaatst:</h3>")
    display(WachtScherm, ProgressBar)

    ModelDir = os.path.join(os.getcwd(), ProjectName)
        
    dirs_to_create = [
        os.path.join(ModelDir, f"Model data\\{ModelName}\\images\\test"),
        os.path.join(ModelDir, f"Model data\\{ModelName}\\labels\\test"),
        os.path.join(ModelDir, f"Model data\\{ModelName}\\images\\train"),
        os.path.join(ModelDir, f"Model data\\{ModelName}\\labels\\train"),
        os.path.join(ModelDir, f"Model data\\{ModelName}\\images\\validation"),
        os.path.join(ModelDir, f"Model data\\{ModelName}\\labels\\validation")
    ]
    for dir in dirs_to_create:
        if not os.path.exists(dir):
            os.makedirs(dir)
    
    docs = os.listdir(Labels)
    for doc in docs:
        image = doc.replace(".txt", ".JPG").replace(".txt", ".jpg")
        ImageLocation = os.path.join(Images, image)
        LabelLocation = os.path.join(Labels, doc)
        ProgressBar.value += 1
        #Progress bar_____________________________________________________________________________________________________________________
        if os.path.exists(ImageLocation):
            chance = random.random()
            if move:
                if chance < testpercentage:
                    shutil.move(ImageLocation, os.path.join(ModelDir, f"Model data\\{ModelName}\\images\\test"))
                    shutil.move(LabelLocation, os.path.join(ModelDir, f"Model data\\{ModelName}\\labels\\test"))
                elif chance < (validatiepercentage + testpercentage):
                    shutil.move(ImageLocation, os.path.join(ModelDir, f"Model data\\{ModelName}\\images\\validation"))
                    shutil.move(LabelLocation, os.path.join(ModelDir, f"Model data\\{ModelName}\\labels\\validation"))
                else:
                    shutil.move(ImageLocation, os.path.join(ModelDir, f"Model data\\{ModelName}\\images\\train"))
                    shutil.move(LabelLocation, os.path.join(ModelDir, f"Model data\\{ModelName}\\labels\\train"))
            else:
                if chance < testpercentage:
                    shutil.copy2(ImageLocation, os.path.join(ModelDir, f"Model data\\{ModelName}\\images\\test"))
                    shutil.copy2(LabelLocation, os.path.join(ModelDir, f"Model data\\{ModelName}\\labels\\test"))
                elif chance < (validatiepercentage + testpercentage):
                    shutil.copy2(ImageLocation, os.path.join(ModelDir, f"Model data\\{ModelName}\\images\\validation"))
                    shutil.copy2(LabelLocation, os.path.join(ModelDir, f"Model data\\{ModelName}\\\labels\\validation"))
                else:
                    shutil.copy2(ImageLocation, os.path.join(ModelDir, f"Model data\\{ModelName}\\images\\train"))
                    shutil.copy2(LabelLocation, os.path.join(ModelDir, f"Model data\\{ModelName}\\labels\\train"))
    
    with open(os.path.join(Labels, "Labels.txt"), "r") as a:
        labels = [line.strip() for line in a.readlines()]

    names = {}
    for i, label in enumerate(labels):
        names[i] = label

    yaml_dict = {
        "path": ModelDir,
        "train": f"Model data\\{ModelName}\\images\\train",
        "val": f"Model data\\{ModelName}\\images\\validation",
        "names": names
    }

    ConfigLocation = os.path.join(ModelDir, f"Model data\\{ModelName}\\{ModelName}_Config.yaml")
    with open(ConfigLocation, "w+") as b:
        b.write("")

    with open(ConfigLocation, "a") as c:
        for key, value in yaml_dict.items():
            if key != "names":
                c.write(f"{key}: {value}\n")
            else:
                c.write(f"\nnames:\n")
                for k, v in names.items():
                    c.write(f"  {k}: {v}\n")
    
    WachtScherm.close()
    ProgressBar.close()
    
    

