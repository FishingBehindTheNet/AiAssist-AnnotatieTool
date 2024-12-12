from Modules.Q_UniversalFunction import ImageToLabel
from Modules.Q_UIparts import OutputScherm
from Modules import Q_UIparts
import ipywidgets as widgets
import random
import shutil   
import os

def AnnotationMove():
    #Maakt widgets om de data split in te voeren
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

    Train = widgets.FloatSlider(
        value = (100 - Val.value - Test.value),
        min = 0,
        max = 100,
        step = 1,
        description ='Training set:',
        orientation ='horizontal',
        disabled = True, # zocht ervoor dat deze waarde niet aangepast kan worden door de gebruiker.
        readout_format = ''
    )

    # Maakt een linkt tussen test validatie en trainings persstage. dit zorgt ervoor dat:
    # * De trainingsdata altijd het het overblijfsel van test en validatie is
    # * Validatie of test set kleiner word wanneer de ander verhoogt word en het totaal boven de 100% komt:
    #    *  val:80 test:20, als ik val verhoog naar 90 word test automatics 10 om het totaal 100 te houden(Dit werkt twee kanten op en de waarde die aangepast word krijgt altijd voorrang.)
    @Val.observe
    def DataTekortVal(PlaceHolder):
        if Val.value + Test.value > 100:
            Test.value = 100-Val.value
        Train.value = (100 - Val.value - Test.value)
    
    @Test.observe
    def DataTekortTest(PlaceHolder):
        if Val.value + Test.value > 100:
            Val.value = 100-Test.value
        Train.value = (100 - Val.value - Test.value)

    # Maakt 2 knoppen voor het starten van de code, Als move True is word data verplaatst anders word het alleen gekopieerd naar de juiste locatie
    Verplaats = widgets.Button(
            description="Verplaats",
            button_style = "warning",
            tooltip="Start de code: Verplaatst alle foto's MET een annotatie in de label folder.",
            layout = widgets.Layout(width = "80px")
            )
    
    @Verplaats.on_click
    def MoveV(PlaceHolder):
        run(Move=True)
    

    Kopieer = widgets.Button(
            description="Kopieer",
            button_style = "success",
            tooltip="Start de code: Kopieert alle foto's MET een annotatie in de label folder.",
            layout = widgets.Layout(width = "80px")
            )
    
    @Kopieer.on_click
    def MoveK(Placeholder):
        run(Move=False)

    # Functie voor de controle van de invoer
    def run(Move):
        # If statement die controleert of alle velden zijn ingevoerd en anders een ergercode geeft om aan te geven welke gegevens missen.
        if Q_UIparts.ImagePick.selected and Q_UIparts.LabelPick.selected and Q_UIparts.DataNaamInput.value and Q_UIparts.ProjectPicker.value:
            # maakt eerst een succes scherm met de opgegeven waarde die weergeven zal worden wanneer alle bestanden verplaatst zijn.
            ImageLocation = f"{Q_UIparts.ProjectPicker.value}/Data/Train en Test sets/{Q_UIparts.DataNaamInput.value}/images"
            LabelLocation = f"{Q_UIparts.ProjectPicker.value}/Data/Train en Test sets/{Q_UIparts.DataNaamInput.value}/labels"
            ConfigLocation = f"{Q_UIparts.ProjectPicker.value}/Data/Train en Test sets/{Q_UIparts.DataNaamInput.value}/{Q_UIparts.DataNaamInput.value}_Config.yaml"
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
            #Sluit de interface en roept de functie aan die de bestanden gaat verplaatsen
            preTrain(
                Labels = Q_UIparts.LabelPick.selected_path,
                Images = Q_UIparts.ImagePick.selected_path,
                ProjectName= Q_UIparts.ProjectPicker.value,
                ModelName = Q_UIparts.DataNaamInput.value,
                Validatiepercentage = (Val.value/100),#Moet gegeven worden in fracties
                Testpercentage= (Test.value/100),#Moet gegeven worden in fracties
                Move = Move#Word bepaalt door welke knop ingedrukt is.
            )

            with OutputScherm:
                display(SuccesScherm)

        elif not Q_UIparts.ImagePick.selected_path:
            ErrorCode.value = """
                <div style="text-align: right;">
                    <i><b><code style="color:red;">Map met foto's niet geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>select</b></font></kbd> drukt na het kiezen van een map om je selectie te bevestigen.</code></b></i>
                </div>
                """
        elif not Q_UIparts.LabelPick.selected_path:
            ErrorCode.value = """
                <div style="text-align: right;">
                    <i><b><code style="color:red;">Map met labels niet geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>select</b></font></kbd> drukt na het kiezen van een map om je selectie te bevestigen.</code></b></i>
                </div>

                """
        elif not Q_UIparts.ProjectPicker.value:
            ErrorCode.value = """
                <div style="text-align: right;">
                    <i><b><code style="color:red;">Er is geen Project geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>Maak</b></font></kbd> drukt als je een nieuwe project wil maken/gebruiken.</code></b></i>
                </div>
                """
        elif not Q_UIparts.DataNaamInput.value:
            ErrorCode.value = """
                <div style="text-align: right;">
                    <i><b><code style="color:red;">Er is geen model naam opgegeven</code></b></i>
                </div>
                """

    # Een verzameling van veel van de text die gebruikt word in de interface
    Titel = widgets.HTML(value = "<h1>Data voorbereiding")
    TitelVL = widgets.HTML(value = "<h2>Huidige Locatie<hr>")
    TitelVR = widgets.HTML(value = "<h2>Toekomstige locatie<hr>")
    DataNaamInputTitel = widgets.HTML("<b>Geef hier de naam van het toekomstige model. <br></b>TIP: Houd deze voor het overzicht gelijk aan het naam van je nieuwe model.")
    DataSplitTitel = widgets.HTML("<b>Geef hier je gewenste verhoudingen tussen test, train en validatie set aan. <br></b>LET OP: Bij het trainen van een model is training en validatie data verplicht.")
    line = widgets.HTML(value = "<hr>")
    Of = widgets.HTML("<b> of ")
    Procent = widgets.HTML("%")
    # Deze is leeg en krijgt alleen een waarde als kopieer of verplaats is aangedrukt voordat alle velden zijn ingevuld.
    ErrorCode = widgets.HTML()

    # Clustert widgets die samen horen zodat het indelen of aanpassen van de interface overzichtelijk blijft.
    Eindlocatie = widgets.VBox([
        Q_UIparts.ProjectInterface,
        DataNaamInputTitel,
        Q_UIparts.DataNaamInput,
    ])
    
    DataSplit = widgets.VBox([
        DataSplitTitel, 
        widgets.HBox([
            Test, 
            Procent
        ]), 
        widgets.HBox([
            Val, 
            Procent
        ]), 
        widgets.HBox([
            Train, 
            Procent
        ])
    ])

    VlakL = widgets.VBox([TitelVL, Q_UIparts.FilePickInterface], layout= widgets.Layout(width='500px'))
    VlakR = widgets.VBox([TitelVR, Eindlocatie, DataSplit], layout= widgets.Layout(width='500px'))
    
    # de samenstelling van de complete interface
    View = widgets.VBox([
        Titel,
        widgets.HBox([
            VlakL, 
            VlakR
        ]),
        line,
        widgets.HBox([
            ErrorCode, 
            Verplaats, 
            Of, 
            Kopieer
        ], layout= widgets.Layout(justify_content="flex-end"))
        ], layout= widgets.Layout(width='1010px'))

    OutputScherm.close()    
    with OutputScherm:
        display(View)

# de functie die de uiteindelijke data move uitvoert
def preTrain(Labels, Images, ProjectName, ModelName, Validatiepercentage, Testpercentage, Move):
    #Maakt een lijst van alle bestanden in de Image folder die gecontroleerd moeten worden
    Imagefiles = os.listdir(Images)
    #maakt een wachtscherm met progressbar zodat de gebruiker een indicatie heeft van hoelang het gaat duren
    ProgressBar = widgets.IntProgress(value=0, max=len(Imagefiles)-1, description="Progress:")
    WachtScherm = widgets.HTML(value = "<h3>Foto's en Labels worden verplaatst:</h3>")

    OutputScherm.clear_output(wait=True)
    with OutputScherm:
        display(WachtScherm, ProgressBar)

    #maakt een lijst van alle mappen die nodig zijn en maakt deze Aan als ze nog niet bestaan
    ModelDir = os.path.join(os.getcwd(), f"{ProjectName}/Data/Train en Test sets/{ModelName}")
    dirs_to_create = [
        os.path.join(ModelDir, f"images/test"),
        os.path.join(ModelDir, f"labels/test"),
        os.path.join(ModelDir, f"images/train"),
        os.path.join(ModelDir, f"labels/train"),
        os.path.join(ModelDir, f"images/validation"),
        os.path.join(ModelDir, f"labels/validation")
    ]
    for dir in dirs_to_create:
        if not os.path.exists(dir):
            os.makedirs(dir)

    # filtert over alle bestanden in de Image folder en checkt of er een label bestaat voor dat bestand.
    for image in Imagefiles:
        ImageLocation = os.path.join(Images, image)
        LabelLocation = os.path.join(Labels, ImageToLabel(image))
        ProgressBar.value += 1
        if os.path.exists(LabelLocation):
            #Afhankelijk of kopieer of verplaats is geklikt of sorteert dit stuk code alle foto's met labels over de test, train, en validatie map.
            #Iedere setje krijgt een random waarde van chance. Dit getal tussen de 0 en 1 word vergeleken met het percentage van
            #test en validatie en word op basis daarvan gekopieerd of verplaatst naar een van de 3 mappen
            chance = random.random()
            if Move:
                if chance < Testpercentage:
                    shutil.move(ImageLocation, os.path.join(ModelDir, f"images/test"))
                    shutil.move(LabelLocation, os.path.join(ModelDir, f"labels/test"))
                elif chance < (Validatiepercentage + Testpercentage):
                    shutil.move(ImageLocation, os.path.join(ModelDir, f"images/validation"))
                    shutil.move(LabelLocation, os.path.join(ModelDir, f"labels/validation"))
                else:
                    shutil.move(ImageLocation, os.path.join(ModelDir, f"images/train"))
                    shutil.move(LabelLocation, os.path.join(ModelDir, f"labels/train"))
            else:
                if chance < Testpercentage:
                    shutil.copy2(ImageLocation, os.path.join(ModelDir, f"images/test"))
                    shutil.copy2(LabelLocation, os.path.join(ModelDir, f"labels/test"))
                elif chance < (Validatiepercentage + Testpercentage):
                    shutil.copy2(ImageLocation, os.path.join(ModelDir, f"images/validation"))
                    shutil.copy2(LabelLocation, os.path.join(ModelDir, f"labels/validation"))
                else:
                    shutil.copy2(ImageLocation, os.path.join(ModelDir, f"images/train"))
                    shutil.copy2(LabelLocation, os.path.join(ModelDir, f"labels/train"))
    
    #Leest de Labels.txt uit de label folder in en maakt een dict van alle labels waarbij de key:i het regelnummer in Labels.txt is en de value:labels het bijbehorende label is.
    with open(os.path.join(Labels, "Labels.txt"), "r") as a:
        names = {i: label.strip() for i, label in enumerate(a.readlines())}

    #genereert de text die uiteindelijk in het config bestand moet komen
    yaml_dict = {
        "path": ModelDir,
        "train": "images/train",
        "val": "images/validation",
        "test": "images/test",
        "names": names
    }

    #Maakt het een leeg config bestand met de juiste naam aan.
    ConfigLocation = os.path.join(ModelDir, f"{ModelName}_Config.yaml")
    with open(ConfigLocation, "w+") as b:
        b.write("")
    
    #Schrijft het daadwerkelijke config bestand. Maakt een uitzondering voor names omdat deze een aparte notatie moet hebben
    with open(ConfigLocation, "a") as c:
        for key, value in yaml_dict.items():
            if key != "names":
                c.write(f"{key}: {value}\n")
            else:
                c.write(f"\nnames:\n")
                for k, v in names.items():
                    c.write(f"  {k}: {v}\n")
    
    OutputScherm.clear_output(wait=True)
    
    

