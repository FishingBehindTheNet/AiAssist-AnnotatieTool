def Annoteren(ImageMap, Annotaties, Labels, Model, ProjectName):
    from Modules.LabelConvert import YoloToWidget, WidgetToYolo, load_label_names
    from jupyter_bbox_widget import BBoxWidget
    from ultralytics import YOLO
    import ipywidgets as widgets
    import random
    import base64
    import shutil
    import gc
    import os

    load_label_names(Labels)

    if not os.path.exists(f"{ImageMap}\\Check Later"):
        os.makedirs(f"{ImageMap}\\Check Later")

    #Work around om afbeeldingen zichtbaar te maken
    def encode_image(filepath):
        with open(filepath, 'rb') as f:
            image_bytes = f.read()
        encoded = str(base64.b64encode(image_bytes), 'utf-8')
        return "data:image/jpg;base64,"+encoded
    
    def BoxPicker(Overwrite):
        ImageView.bboxes = []
        PathLink()
        if Overwrite=="reGen":
            LabelLocation = os.path.join(os.getcwd(), f"""{ProjectName}\\Voorspellingen\\labels\\{Files[ProgressBar.value].replace(".jpg", ".txt").replace(".JPG", ".txt")}""")
            if os.path.exists(LabelLocation):
                os.remove(LabelLocation)
            ImagePath = os.path.join(ImageMap, Files[ProgressBar.value])
            model.predict(ImagePath, save_txt=True, conf=0.25, exist_ok=True, project=ProjectName, name="Voorspellingen", augment=True)
            ImageView.bboxes = YoloToWidget(
                ImageMap = ImageMap,
                ImageName = Files[ProgressBar.value],
                Annotaties = AiAnnotaties,
            )      
        elif os.path.exists(os.path.join(Annotaties, Files[ProgressBar.value].replace(".jpg", ".txt").replace(".JPG", ".txt"))):
            ImageView.bboxes = YoloToWidget(
                ImageMap = ImageMap,
                ImageName = Files[ProgressBar.value],
                Annotaties = Annotaties,
            )
        else:
            if AiAssist.value:
                AnnoLocation = os.path.join(AiAnnotaties, Files[ProgressBar.value].replace(".jpg", ".txt").replace(".JPG", ".txt"))
                if not os.path.exists(AnnoLocation):
                    ImagePath = os.path.join(ImageMap, Files[ProgressBar.value])
                    model.predict(ImagePath, save_txt=True, conf=0.25, exist_ok=True, project=ProjectName, name="Voorspellingen", augment=True)

                ImageView.bboxes = YoloToWidget(
                    ImageMap = ImageMap,
                    ImageName = Files[ProgressBar.value],
                    Annotaties = AiAnnotaties,
                )
            else:
                ImageView.bboxes = YoloToWidget(
                    ImageMap = ImageMap,
                    ImageName = Files[ProgressBar.value],
                    Annotaties = Annotaties,
                )

    LabeledImages = []
    UnlabeledImages = []

    # Loop through image directory and check for corresponding label files
    for filename in os.listdir(ImageMap):
        if filename.endswith('.JPG') or filename.endswith('.jpg'):
            LabelFilename = os.path.splitext(filename)[0] + '.txt'
            if os.path.exists(os.path.join(Annotaties, LabelFilename)):
                LabeledImages.append(filename)
            else:
                UnlabeledImages.append(filename)

    # Shuffle the list of unlabeled images
    random.shuffle(UnlabeledImages)

    # Concatenate the two lists to create the final list
    Files = LabeledImages + UnlabeledImages
    
    with open(Labels, 'r') as a:
        label_names = [label.strip() for label in a.readlines()]

    #laat zien hoeveel foto's je nog moet
    ProgressBar = widgets.IntProgress(
        value=len(LabeledImages)
        ,
        max=len(Files)-1, 
        description="Foto's geannoteerd:",
        style={'description_width': 'initial'},
        tooltip="procent van de foto's dat met een annotatie in de label map",
        layout=widgets.Layout(width="100%")
    )

    ImageTitle = widgets.HTML(
        value="",
        tooltip="Open",
    )

    def PathLink():
        Title = os.path.join(ImageMap, Files[ProgressBar.value])
        Title.replace("\\", "/")
        ImageTitle.value = f"<h2><a href='file:///{Title}'>{Files[ProgressBar.value]}</a></h2>"

    #voegt knop toe om terug te kunnen
    Back = widgets.Button(
        value = False,
        description = "Back",
        tooltip = "Terug naar de vorige foto",
        button_style = "warning"
    )

    AiAssist = widgets.ToggleButton(
        description="Handmatig",
        value = False,
        tooltip = "Ai annotaties aan/uit",
        button_style = ""
    )

    reGen = widgets.Button(
        value = False,
        description = "Genereer annotaties",
        tooltip = "Verwijder Ai annotaties en genereer nieuwe annotaties",
        button_style = "primary"
    )

    Later = widgets.Button(
        value = False,
        description = "Check Later",
        tooltip = f"Kopier de image naar {ImageMap}\\Check Later",
        button_style = "info"
    )

    Delete = widgets.Button(
        value = False,
        description = "Delete image",
        tooltip = f"Verwijder image uit {ImageMap}",
        button_style = "danger"
    )


    #Displays de foto en zorgt dat je kunt annoteren
    ImageView = BBoxWidget(
        image = encode_image(os.path.join(ImageMap, Files[ProgressBar.value])),
        classes = label_names,
        layout = widgets.Layout(width="100%")
    )
    BoxPicker("")

    ButtonF = '<kbd><font color="#424a48"><b>'
    ButtonB = '</b></font></kbd>'

    CheatSheet = widgets.HTML(
        value = f"""
        <style>
        td:first-child {{
            text-align: center;
        }}
        td:last-child {{
            text-align: left;
        }}
        </style>

        <h3>Key bindings</h3> 
        <table>
        <tr>
            <td>{ButtonF}1{ButtonB}-{ButtonF}9{ButtonB}</td>
            <td>Selecteer label</td>
        </tr>
        <tr>
            <td>{ButtonF}Tab{ButtonB}</td>
            <td>Volgende bounding box</td>
        </tr>
        <tr>
            <td>{ButtonF}Shift{ButtonB}-{ButtonF}Tab{ButtonB}</td>
            <td>Vorige bounding box</td>
        </tr>
        <tr>
            <td>{ButtonF}c{ButtonB}</td>
            <td>Verander label van geselecteerde bounding box</td>
        </tr>
        <tr>
            <td>{ButtonF}Delete{ButtonB}</td>
            <td>verwijder geselecteerde bounding box</td>
        </tr>
        <tr>
            <td>{ButtonF}Enter{ButtonB}</td>
            <td>Submit</td>
        </tr>
        <tr>
            <td>{ButtonF} Spatie {ButtonB}</td>
            <td>Skip</td>
        </tr>
        <tr>
            <td>{ButtonF}w{ButtonB} <br />
            {ButtonF}a{ButtonB}  {ButtonF}s{ButtonB}  {ButtonF}d{ButtonB}</td>
            <td>Move bounding box (Hold {ButtonF}Shift{ButtonB} to increase step size)</td>
        </tr>
        <tr>
            <td>{ButtonF}R{ButtonB} <br />
            {ButtonF}Q{ButtonB}  {ButtonF}F{ButtonB}  {ButtonF}E{ButtonB}</td>
            <td>Resize bounding box</td>
        </tr>
        """
    )

    WiteLine = widgets.HTML(" ")

    #voegt alle widgets samen voor gemakkelijk aanroepen
    if Model:
        model = YOLO(Model, task='detect')
        AiAnnotaties = os.path.join(ProjectName, "Voorspellingen", "labels")
        if not os.path.exists(AiAnnotaties):
            os.makedirs(AiAnnotaties)

        AnnoterenWidget = widgets.HBox([widgets.VBox([
            widgets.HBox([WiteLine, Back, AiAssist]),    
            ImageView]),
            widgets.VBox([ImageTitle,
                widgets.HBox([reGen, Later, Delete]),
                ProgressBar,
                CheatSheet]),
            ], layout=widgets.Layout(align_items='center'))
    else:
        AnnoterenWidget = widgets.HBox([widgets.VBox([
            widgets.HBox([WiteLine, Back,]),    
            ImageView]),
            widgets.VBox([ImageTitle,
                widgets.HBox([Later, Delete]),
                ProgressBar,
                CheatSheet]),
            ], layout=widgets.Layout(align_items='center'))

    def on_button_clicked(PlaceHolder):
        if AiAssist.value:
            AiAssist.description = "AI gegenereerd"
            AiAssist.button_style = "primary"
            BoxPicker("")        
        else:
            AiAssist.description = "Handmatig"
            AiAssist.button_style = ""
            BoxPicker("")

    AiAssist.observe(on_button_clicked)

    #gaat naar de volgende foto zonder vooruitgang op te slaan
    @ImageView.on_skip
    def skip():
        ProgressBar.value += 1
        image_file = Files[ProgressBar.value]
        ImageView.image = encode_image(os.path.join(ImageMap, image_file))
        BoxPicker("")
        if ProgressBar.value % 20 == 0:
            gc.collect()

    #slaat vooruitgang op en roept nieuwe foto aan en gebruikt dan de skip() functie
    @ImageView.on_submit
    def save():
        image_file = Files[ProgressBar.value]
        WidgetToYolo(
            ImageMap = ImageMap,
            ImageName = image_file,
            Annotaties = Annotaties,
            BBox = ImageView.bboxes,
        )

        skip()

    #Gaat een foto terug zonder op te slaan
    @Back.on_click
    def Back(PlaceHolder):
        ProgressBar.value -= 1
        image_file = Files[ProgressBar.value]
        ImageView.image = encode_image(os.path.join(ImageMap, image_file))
        BoxPicker("")

    @reGen.on_click
    def clear(PlaceHolder):
        BoxPicker(Overwrite="reGen")  

    @Delete.on_click
    def clear(PlaceHolder):
        image_file = Files[ProgressBar.value]
        del Files[ProgressBar.value]
        ProgressBar.max -= 1
        os.remove(os.path.join(ImageMap, image_file))
        image_file = Files[ProgressBar.value]
        ImageView.image = encode_image(os.path.join(ImageMap, image_file))
        BoxPicker("")

    @Later.on_click
    def move(PlaceHolder):
        image_file = Files[ProgressBar.value]
        ProgressBar.value += 1
        ImageView.image = encode_image(os.path.join(ImageMap, Files[ProgressBar.value]))
        BoxPicker("")
        shutil.copy2(os.path.join(ImageMap, image_file), f"{ImageMap}\\Check Later")

    display(AnnoterenWidget)