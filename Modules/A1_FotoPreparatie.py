import os
import shutil
from PIL import Image
import ipywidgets as widgets
from Modules import Q_UIparts
from itertools import product
from ipyfilechooser import FileChooser
from Modules.Q_UniversalFunction import ValidImageType, ImageToLabel

OutputScherm = widgets.Output()
display(OutputScherm)

RotationDic = {
    'horizontale (L)': (True, -90), 
    'horizontale (R)': (True, 90), 
    'verticale (L)': (False, -90), 
    'verticale (R)': (False, 90), 
    'variabele': (None, None)}

#Functie voor het opsnijden van foto's in segmenten
def FotoSegmentatie(ImageMap, Output, Size, Overlap, LangsteZijde, Rotatie):
    OutputScherm.clear_output(wait=True)

    #Maakt een lijst van alle afbeeldingen met ondersteunde bestandstype in de fotomap
    docs = [file for file in os.listdir(ImageMap) if ValidImageType(file)]

    #Maakt een wachtscherm en een laadbalk om aan te geven hoever de code is.
    ProgressBar = widgets.IntProgress(
        value=0,
        max=len(docs),
        description="Progress:",
    )
    WachtScherm = widgets.HTML(
        value="<h3>Foto's worden gesegmenteerd:</h3>",
    )

    with OutputScherm:
        display(WachtScherm, ProgressBar)

    RotatieHorizontaal, Draai = RotationDic[Rotatie]

    #gaat door alle afbeeldingen in de lijst
    for Files in docs:
        ProgressBar.value += 1

        #leest de foto is en checkt of deze verticaal georiënteerd staat. 
        #Zonder deze stap kloppen de coördinaten in de naam niet en is het samenvoegen van annotaties voor een hele plaat onnodig moeilijk
        image = Image.open(os.path.join(ImageMap, Files))
        Width, Height = image.size

        if RotatieHorizontaal == True:
            if Width < Height:
                image = image.rotate(Draai, expand=True)
                Width, Height = image.size
        elif RotatieHorizontaal == False:
            if Width > Height:
                image = image.rotate(Draai, expand=True)
                Width, Height = image.size        

        #Resized de foto zodat ongeacht de camera de foto's een constante grote hebben
        if Width>Height and Width != LangsteZijde:
            # Berekend de nieuwe hoogte van de foto zodat verhoudingen niet veranderd worden
            NewHeight = int(LangsteZijde/Width*Height)

            # Resize foto en bepaal de nieuwe hoogte en breedte
            image = image.resize((LangsteZijde, NewHeight))
            Width, Height = image.size
        elif Width<Height and Height != LangsteZijde:
            # Berekend de nieuwe hoogte van de foto zodat verhoudingen niet veranderd worden
            NewWidth = int(LangsteZijde/Height*Width)

            # Resize foto en bepaal de nieuwe hoogte en breedte
            image = image.resize((NewWidth, LangsteZijde))
            Width, Height = image.size

        #Is later nodig voor de nieuwe namen
        FileName, FileType = os.path.splitext(Files)

        #Berekent de hoek coördinaten voor alle toekomstige segmenten
        grid = product(
            range(0, Width, (Size - Overlap)), 
            range(0, Height, (Size - Overlap)),
        )

        #segmenteerd de foto en slaat deze op onder het {project)/data/annotaties/{Data set}/images waarbij de naam bestaat uit naam van de complete foto + de coördinaten (in pixels, hoek rechts boven)
        for x, y in grid:
            box = (x, y, x + Size, y + Size)
            out = os.path.join(Output, f"{FileName}_{y}_{x}{FileType}")
            image.crop(box).save(out)
        image.close()

    OutputScherm.clear_output(wait=True)

#Functie voor het Verplaatsen van foto's volgens de data ordening 
def FotoOrdening(ImageMap, OutputImage, LabelMap, OutputLabels):
    OutputScherm.clear_output(wait=True)

    #Maakt een lijst van alle afbeeldingen met ondersteunde bestandstype in de fotomap
    docs = [file for file in os.listdir(ImageMap) if ValidImageType(file)]

    #Maakt een wachtscherm en een laadbalk om aan te geven hoever de code is.
    ProgressBar = widgets.IntProgress(
        value=0,
        max=len(docs),
        description="Progress:",
    )
    WachtScherm = widgets.HTML(
        value="<h3>Foto's worden gekopieerd en geordend:</h3>",
    )

    with OutputScherm:
        display(WachtScherm, ProgressBar)

    #Checkt of de aangegeven Label map de label vertalingen heeft en kopieert deze als ze bestaan.
    if LabelMap and os.path.exists(os.path.join(LabelMap, "Labels.txt")):
        shutil.copy2(os.path.join(LabelMap, "Labels.txt"), OutputLabels)

    #Gaat over de lijst van afbeeldingen en kopieert ze naar de nieuwe locatie, checkt tegelijkertijd of er in de label map een annotatie bestaat voor de desbetreffende afbeelding en kopieert deze mee als hij bestaat. 
    for Files in docs:
        ProgressBar.value += 1
        shutil.copy2(os.path.join(ImageMap, Files), OutputImage)
        if LabelMap and os.path.exists(os.path.join(LabelMap, ImageToLabel(Files))):
            shutil.copy2(os.path.join(LabelMap, ImageToLabel(Files)), OutputLabels)

    OutputScherm.clear_output(wait=True)

#Deze functie maakt de interface van deze tool aan.
def FotoPreparatie():
    OutputScherm.clear_output(wait=True)
    
    DataNaamTitel = widgets.HTML(value ="<b>Geef hier de naam voor de nieuwe dataset:")

    ImagePickTitelSM = widgets.HTML(value = "<br><b>Selecteer hier de folder met foto's die gesegmenteerd gaan worden:")
    ImagePickTitelOR = widgets.HTML(value = "<br><b>Selecteer hier de folder met foto's die gekopieerd en herordend gaan worden:")
    LabelPickTitel = widgets.HTML(value = "<b>Niet verplicht!</b> Selecteer hier de folder met bijbehorende annotaties als je deze hebt:")

    LiggingTitel = widgets.HTML(value = "De foto's hebben een ")
    Ligging = widgets.Dropdown(
        options= list(RotationDic.keys()), #-90 is links om
        value='verticale (L)',
        description="",
        layout=widgets.Layout(width="120px")
    )

    LengteOGTitel = widgets.HTML(value = " ligging en een lange zijde van ")
    LengteOG = widgets.BoundedIntText(
        value=6936,
        min=10,
        max=20000,
        step=1,
        disabled=False,
        layout = widgets.Layout(width = "60px")
    )

    SizeTitel = widgets.HTML(value = "De foto's worden opgedeeld in vierkante segmenten met zijdes van ")
    Size = widgets.BoundedIntText(
        value=640,
        min=10,
        max=20000,
        step=1,
        disabled=False,
        layout = widgets.Layout(width = "60px")
    )

    OverlapTitel = widgets.HTML(value = "de segmenten hebben een overlap met naast liggende segmenten van:")
    OverlapNum = widgets.BoundedIntText(
        value=10,
        min=0,
        max=50,
        step=1,
        disabled=False,
        layout = widgets.Layout(width = "60px")
    )
    #Geeft een visuele indicatie hoeveel overlap op ieder segment zichtbaar is
    OverlapBar = widgets.IntRangeSlider(
        value=[10, 90],
        min=0,
        max=100,
        step=1,
        continuous_update=False,
        description="Overlap:",
        orientation='horizontal',
        readout=False,
        layout=widgets.Layout(width="300px", justify_content="flex-end"),
    )

    #2 functies voor het linken van het percentage overlap en de visualisatie hiervan
    @OverlapNum.observe
    def linkOverlap(PlaceHolder):
        OverlapBar.value = [OverlapNum.value, (100-OverlapNum.value)]
    
    @OverlapBar.observe
    def linkOverlap2(PlaceHolder):
        if OverlapBar.value[0]!=OverlapNum.value:
            OverlapNum.value = OverlapBar.value[0]
        else:
            OverlapNum.value = -(OverlapBar.value[1]-100)

    pixels = widgets.HTML("pixels")
    Procent = widgets.HTML("procent")

    #Een tussentijdse samenvoeging van widgets voor een overzichtelijker geheel
    TileSize = widgets.VBox([
        widgets.HBox([
            LiggingTitel, 
            Ligging, 
            LengteOGTitel,
            LengteOG,
            pixels
        ]),
        widgets.HBox([
            SizeTitel, 
            Size, 
            pixels
        ]), 
        widgets.HBox([
            OverlapTitel, 
            OverlapNum, 
            Procent
        ]),
        widgets.HBox([
            OverlapBar
        ], layout=widgets.Layout(width="400px", justify_content="flex-end")),
        
    ])

    Slice = widgets.Button(
        value=False,
        description="Slice",
        button_style="success",
        layout=widgets.Layout(width="80px"),
    )

    Orden = widgets.Button(
        value=False,
        description="Orden",
        button_style="success",
        layout=widgets.Layout(width="80px"),
    )
    
    #Functie voor het aanroepen en afronden van de functies voor het ordenen of segmenteren van foto's
    def Run(Button : str = ""):
        #Maakt een eindscherm voor het infomeren over de nieuwe folder locaties
        ImageLocation = os.path.join(Q_UIparts.ProjectPicker.value, rf"Data/Annoteren/{Q_UIparts.DataNaamInput.value}/images")
        LabelLocation = os.path.join(Q_UIparts.ProjectPicker.value, rf"Data/Annoteren/{Q_UIparts.DataNaamInput.value}/labels")
        SuccesScherm = widgets.HTML(
            value=f"""
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
            """
        )

        #If functie die probeert het ordenen/segmenteren te starten. Als dit niet lukt genereert het een ergercode naast de slice/orden knop.
        if Q_UIparts.ImagePick.selected and Q_UIparts.DataNaamInput.value and Q_UIparts.ProjectPicker.value and Button == "Slice":
            dirs_to_create = [ImageLocation, LabelLocation]
            for dir in dirs_to_create:
                if not os.path.exists(dir):
                    os.makedirs(dir)

            OutputScherm.clear_output(wait=True)
            FotoSegmentatie(
                ImageMap=Q_UIparts.ImagePick.value,
                Output=ImageLocation,
                Size=int(Size.value),
                Overlap=int(Size.value * (OverlapNum.value / 100)),
                LangsteZijde=LengteOG.value,
                Rotatie=Ligging.value
            )

            with OutputScherm:
                display(SuccesScherm)
        
        elif Q_UIparts.ImagePick.selected and Q_UIparts.DataNaamInput.value and Q_UIparts.ProjectPicker.value and Button == "Orden":
            dirs_to_create = [ImageLocation, LabelLocation]
            for dir in dirs_to_create:
                if not os.path.exists(dir):
                    os.makedirs(dir)

            OutputScherm.clear_output(wait=True)
            FotoOrdening(
                ImageMap=Q_UIparts.ImagePick.value,
                LabelMap=Q_UIparts.LabelPick.selected,                
                OutputImage=ImageLocation,
                OutputLabels=LabelLocation
            )

            with OutputScherm:
                display(SuccesScherm)

        elif not Q_UIparts.ImagePick.selected:
            ErrorCode.value = """
                <div style="text-align: right;">
                    <i><b><code style="color:red;">Folder met foto's niet geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>select</b></font></kbd> drukt na het kiezen van een folder om je selectie te bevestigen.</code></b></i>
                </div>
                """
        elif not Q_UIparts.ProjectPicker.value:
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
    
    #2 functies voor het aanropen van de functie hierboven. Dit is losgetrokken zodat een extra variabele meegegeven kan worden.
    @Slice.on_click
    def RunSlice(PlaceHolder):
        Run(Button = "Slice")

    @Orden.on_click
    def RunOrden(PlaceHolder):
        Run(Button = "Orden")

    #Voegt alle widgets samen tot een samenhangende Interface    
    line = widgets.HTML(value="<hr>")
    ErrorCode = widgets.HTML()

    Box1 = widgets.VBox([Q_UIparts.ProjectInterface, DataNaamTitel, Q_UIparts.DataNaamInput])
    Box2SM = widgets.VBox([ImagePickTitelSM, Q_UIparts.ImagePick, TileSize])
    Box2OR = widgets.VBox([ImagePickTitelOR, Q_UIparts.ImagePick, LabelPickTitel, Q_UIparts.LabelPick])

    ViewSM = widgets.VBox([
        widgets.HBox([
            Box1,
            Box2SM,
        ], layout=widgets.Layout(justify_content="space-around")
        ),
        line,
        widgets.HBox([
            ErrorCode,
            Slice,
        ], layout=widgets.Layout(justify_content="flex-end")
        )], layout=widgets.Layout(width="888px")
    )

    ViewOR = widgets.VBox([
        widgets.HBox([
            Box1,
            Box2OR,
        ], layout=widgets.Layout(justify_content="space-around")
        ),
        line,
        widgets.HBox([
            ErrorCode, 
            Orden
        ], layout=widgets.Layout(justify_content="flex-end")
        )], layout=widgets.Layout(width="888px"),
    )

    ViewCompleet = widgets.Tab(layout= widgets.Layout(width='920px'))
    ViewCompleet.children = [ViewSM, ViewOR]
    ViewCompleet.titles = ('Foto segmentatie', 'Foto herordening')

    with OutputScherm:
        display(ViewCompleet)