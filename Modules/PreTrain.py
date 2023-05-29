from ipyfilechooser import FileChooser
import ipywidgets as widgets
import random
import shutil   
import os

def AnnotationMove():
    #Genereert dialoog boxen
    info1 = widgets.HTML(
        value = "Deze map bevat alle <b>Foto's</b>:"
    )

    #Roept een widget aan die fungeert als interface om map locaties aan te vragen
    ImagePick = FileChooser()
    ImagePick.show_only_dirs = True

    #Genereert dialoog boxen
    info2 = widgets.HTML(
        value = "Deze map bevat de bijbehorende  <b>Labels</b>:"
    )
    #Roept een widget aan die fungeert als interface om map locaties aan te vragen
    LabelPick = FileChooser()
    LabelPick.show_only_dirs = True

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
        ImageLocation = os.path.join(os.getcwd(), f"{Picker.value}Data\\{ModelInput.value}\\images")
        LabelLocation = os.path.join(os.getcwd(), f"{Picker.value}Data\\{ModelInput.value}\\labels")
        ConfigLocation = os.path.join(os.getcwd(), f"{Picker.value}Data\\{ModelInput.value}\\{ModelInput.value}_Config.yaml")
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

        if ImagePick.selected and LabelPick.selected and ModelInput.value:
            View.close()
            preTrain(
                Labels = LabelPick.selected_path,
                Images = ImagePick.selected_path,
                ProjectName= Picker.value,
                ModelName = ModelInput.value,
                validatiepercentage = (Val.value/100),
                testpercentage= (Test.value/100),
                move = Move.value
            )
            display(SuccesScherm)

    Procent = widgets.HTML("%")
    DataSplit = widgets.VBox([widgets.HBox([Test, Procent]), widgets.HBox([Val, Procent]), widgets.HBox([Train, Procent])])

    Titel = widgets.HTML(value = "<h3>_______________________________________________________________________________Data move_________________________________________________</h3>")
    TitelV1 = widgets.HTML(value = "<h3>___________________Toekomstige locatie___________________</h3>")
    TitelV2 = widgets.HTML(value = "<h3>_________________________Huidige Locatie____________________________________</h3>")

    ModelPicker = widgets.VBox([
        widgets.HBox([
            ProjectInput,
            Add,
        ]),
        Picker,
        ModelInput,])

    DirPick = widgets.VBox([info1, ImagePick, info2, LabelPick])

    Vlak1 = widgets.VBox([TitelV1, ModelPicker, DataSplit])
    Vlak2 = widgets.VBox([TitelV2, DirPick])

    View = widgets.VBox([widgets.HBox([Titel, submit]), widgets.HBox([Vlak2, Move, Vlak1])])
    display(View)

def preTrain(Labels, Images, ProjectName, ModelName, validatiepercentage=0.2, testpercentage=0.0, move=False):
    docs = os.listdir(Labels)
    ProgressBar = widgets.IntProgress(value=0, max=len(docs)-1, description="Progress:")
    WachtScherm = widgets.HTML(value = "<h3>Foto's en Labels worden verplaatst:</h3>")
    display(WachtScherm, ProgressBar)

    ModelDir = os.path.join(os.getcwd(), ProjectName)
        
    dirs_to_create = [
        os.path.join(ModelDir, f"Data\\{ModelName}\\images\\test"),
        os.path.join(ModelDir, f"Data\\{ModelName}\\labels\\test"),
        os.path.join(ModelDir, f"Data\\{ModelName}\\images\\train"),
        os.path.join(ModelDir, f"Data\\{ModelName}\\labels\\train"),
        os.path.join(ModelDir, f"Data\\{ModelName}\\images\\validation"),
        os.path.join(ModelDir, f"Data\\{ModelName}\\labels\\validation")
    ]
    for dir in dirs_to_create:
        if not os.path.exists(dir):
            os.makedirs(dir)
    
    docs = os.listdir(Labels)
    for doc in docs:
        image = (doc.replace(".txt", ".JPG"))
        ImageLocation = os.path.join(Images, image)
        LabelLocation = os.path.join(Labels, doc)
        ProgressBar.value += 1
        #Progress bar_____________________________________________________________________________________________________________________
        if os.path.exists(ImageLocation):
            chance = random.random()
            if move:
                if chance < testpercentage:
                    shutil.move(ImageLocation, os.path.join(ModelDir, f"Data\\{ModelName}\\images\\test"))
                    shutil.move(LabelLocation, os.path.join(ModelDir, f"Data\\{ModelName}\\labels\\test"))
                elif chance < (validatiepercentage + testpercentage):
                    shutil.move(ImageLocation, os.path.join(ModelDir, f"Data\\{ModelName}\\images\\validation"))
                    shutil.move(LabelLocation, os.path.join(ModelDir, f"Data\\{ModelName}\\labels\\validation"))
                else:
                    shutil.move(ImageLocation, os.path.join(ModelDir, f"Data\\{ModelName}\\images\\train"))
                    shutil.move(LabelLocation, os.path.join(ModelDir, f"Data\\{ModelName}\\labels\\train"))
            else:
                if chance < testpercentage:
                    shutil.copy2(ImageLocation, os.path.join(ModelDir, f"Data\\{ModelName}\\images\\test"))
                    shutil.copy2(LabelLocation, os.path.join(ModelDir, f"Data\\{ModelName}\\labels\\test"))
                elif chance < (validatiepercentage + testpercentage):
                    shutil.copy2(ImageLocation, os.path.join(ModelDir, f"Data\\{ModelName}\\images\\validation"))
                    shutil.copy2(LabelLocation, os.path.join(ModelDir, f"Data\\{ModelName}\\\labels\\validation"))
                else:
                    shutil.copy2(ImageLocation, os.path.join(ModelDir, f"Data\\{ModelName}\\images\\train"))
                    shutil.copy2(LabelLocation, os.path.join(ModelDir, f"Data\\{ModelName}\\labels\\train"))
    
    with open(os.path.join(Labels, "Labels.txt"), "r") as f:
        labels = [line.strip() for line in f.readlines()]

    names = {}
    for i, label in enumerate(labels):
        names[i] = label

    yaml_dict = {
        "path": ModelDir,
        "train": f"Data\\{ModelName}\\images\\train",
        "val": f"Data\\{ModelName}\\images\\validation",
        "names": names
    }

    ConfigLocation = os.path.join(ModelDir, f"Data\\{ModelName}\\{ModelName}_Config.yaml")
    f = open(ConfigLocation, "w+")    

    with open(ConfigLocation, "a") as f:
        for key, value in yaml_dict.items():
            if key != "names":
                f.write(f"{key}: {value}\n")
            else:
                f.write(f"\nnames:\n")
                for k, v in names.items():
                    f.write(f"  {k}: {v}\n")
    
    WachtScherm.close()
    ProgressBar.close()
    
    

