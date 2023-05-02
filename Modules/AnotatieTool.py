def Annoteren(ImageMap, Annotaties, Labels, Model, DataName):
    from Modules.LabelConvert import YoloToWidget, WidgetToYolo
    from jupyter_bbox_widget import BBoxWidget
    from ultralytics import YOLO
    import ipywidgets as widgets
    import random
    import base64
    import os

    AiAnnotaties = os.path.join("Data", DataName, "labels")
    if not os.path.exists(AiAnnotaties):
        os.makedirs(AiAnnotaties)

    #Work around om afbeeldingen zichtbaar te maken
    def encode_image(filepath):
        with open(filepath, 'rb') as f:
            image_bytes = f.read()
        encoded = str(base64.b64encode(image_bytes), 'utf-8')
        return "data:image/jpg;base64,"+encoded
    
    def BoxPicker(PlaceHolder):
        if AiAssist.value:
            AnnoName = Files[ProgressBar.value].replace(".jpg", ".txt").replace(".JPG", ".txt")
            AnnoLocation = os.path.join(AiAnnotaties, AnnoName)
            if not os.path.exists(AnnoLocation):
                model = YOLO(Model)
                ImagePath = os.path.join(ImageMap, Files[ProgressBar.value])
                model.predict(ImagePath, save_txt=True, conf=0.5, augment=True, exist_ok=True, project="Data", name=DataName)

            ImageView.bboxes = YoloToWidget(
                ImageMap = ImageMap,
                ImageName = Files[ProgressBar.value],
                Annotaties = AiAnnotaties,
                Labels = Labels
            )
        else:
            ImageView.bboxes = YoloToWidget(
                ImageMap = ImageMap,
                ImageName = Files[ProgressBar.value],
                Annotaties = Annotaties,
                Labels = Labels
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
    ProgressBar = widgets.IntProgress(value=len(LabeledImages), max=len(Files)-1, description="%Geanoteerd")

    #voegt knop toe om terug te kunnen
    Back = widgets.Button(
        value = False,
        description = "Back",
        button_style = "warning"
    )

    AiAssist = widgets.ToggleButton(
        description="Handmatig",
        value = False,
        button_style = ""
        )

    Delete = widgets.Button(
        value = False,
        description = "Delete all BBox",
        button_style = "danger"
    )

    #Displays de foto en zorgt dat je kunt annoteren
    ImageView = BBoxWidget(
        image = encode_image(os.path.join(ImageMap, Files[ProgressBar.value])),
        classes = label_names,
    )
    BoxPicker("")

    #voegt alle widgets samen voor gemakkelijk aanroepen
    AnnoterenWidget = widgets.VBox([
        widgets.HBox([Back, AiAssist]),    
        ImageView,
        widgets.HBox([ProgressBar, Delete])
        ], layout=widgets.Layout(width='600px'))

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

    #slaat vooruitgang op en roept nieuwe foto aan en gebruikt dan de skip() functie
    @ImageView.on_submit
    def save():
        image_file = Files[ProgressBar.value]
        WidgetToYolo(
            ImageMap = ImageMap,
            ImageName = image_file,
            Annotaties = Annotaties,
            Labels = Labels,
            BBox = ImageView.bboxes
        )

        skip()

    #Gaat een foto terug zonder op te slaan
    @Back.on_click
    def Back(PlaceHolder):
        ProgressBar.value -= 1
        image_file = Files[ProgressBar.value]
        ImageView.image = encode_image(os.path.join(ImageMap, image_file))
        BoxPicker("")  

    @Delete.on_click
    def clear(PlaceHolder):
        ImageView.bboxes = []

    display(AnnoterenWidget)