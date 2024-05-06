from ipyfilechooser import FileChooser
import ipywidgets as widgets
from Modules import Q_UIparts
from ultralytics import YOLO
import os

#Test het model
def ModelTest(Model, ConfigFile, DataPick, Project, Confidence):
    #Stript de naam van de dataset uit de config file
    DataName = str(ConfigFile).split("/")[-1].removesuffix("_Config.yaml")

    # Controleert of het geselecteerde model uit de modelresultaten map komt of uit de modellen map. 
    # Output de huidige naam van het model en een naam zoals veker gebruikt: {naam van het model}_{Versie van het model: "last" of "best"}
    if str(Model).split("/")[-1] == "best.pt" or str(Model).split("/")[-1] == "last.pt":
        ModelName = str(Model).split("/")[-4]
        Versie = str(Model).split("/")[-1].removesuffix('.onnx').removesuffix('.pt')
        ModelVersion = f"{ModelName}_{Versie}"
    else:
        ModelName = str(Model).split("/")[-1]
        ModelVersion = str(Model).split("/")[-1].removesuffix('.onnx').removesuffix('.pt')

    #Start het validatie process met de geselecteerde waarde, Laatste map word samengesteld uit de verschillende instelleningen zodat later te herleiden is welke instellingen gebruikt zijn.
    Model = YOLO(Model, task="detect")
    Model.val(
        data=ConfigFile, 
        save_json=True, 
        conf=Confidence, 
        exist_ok=True, 
        split='test' if DataPick else 'val', 
        project=f"{Project}/Model Resultaten", 
        name=f"{ModelName}/M={ModelVersion}, DS={DataName} ({'TestSet' if DataPick else 'ValidatieSet'}, conf={Confidence})", 
        augment=True
    )
    return f"{Project}/Model Resultaten/{ModelName}/M={ModelVersion}, DS={DataName} ({'TestSet' if DataPick else 'ValidatieSet'}, conf={Confidence})"

#Functie die de interface opstart
def ModelValidation():
    # maakt een toggelbutton de functie update hoe de knop eruit ziet op Basis van zijn status
    TestOrValidation = widgets.ToggleButton(
        value=True,
        layout = widgets.Layout(width = "100px")
    )

    def on_button_clicked(PlaceHolder):
        if TestOrValidation.value:
            TestOrValidation.description = "Test set"
            TestOrValidation.button_style = "primary"
        else:
            TestOrValidation.description = "Validatie set"
            TestOrValidation.button_style = "warning"

    TestOrValidation.observe(on_button_clicked)
    on_button_clicked("")

    #maakt de selectie opties voor de model, confidence en config selectie.
    ConfigFile = FileChooser(filter_pattern="*.yaml", title="<b>Selecteer de Config.yaml file van je validatie en/of test set")
    Model = FileChooser(filter_pattern=["*.pt", "*.onnx"], title="<b>Selecteer het model (.pt of .onnx) wat je wil testen")

    Confidence = widgets.BoundedFloatText(
        value=0.25,
        min=0.001,
        max=1,
        step=0.001,
        description='',
        disabled=False,
        layout = widgets.Layout(width = "60px")
    )

    submit = widgets.Button(
        value = False,
        description = "Submit",
        button_style = "success",
        layout = widgets.Layout(width = "80px")
    )

    # Functie om te checken of alle waarden zijn ingevuld. als dit het geval is start het de validatie code
    @submit.on_click
    def SaveAndLaunch(PlaceHolder):
        # Schakelt de Submit kop uit tot de controle en of de validatie afgerond is. dit is om te voorkomen dat het validatie process onnodig vaak uitgevoerd word.
        # De interface word niet gesloten zoals standaard bij andere interfaces omdat deze tool meerdere malen met net iets andere instellingen per keer gebruikt gaat worden en dit versimpelt dat process.
        submit.disabled=True
        if not Q_UIparts.ProjectPicker.value:
            ErrorCode.value = """
            <div style="text-align: right;">
                <i><b><code style="color:red;">Er is een wel een model maar geen Project geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>Maak</b></font></kbd> drukt als je een nieuwe project wil maken/gebruiken.</code></b></i>
            </div>
            """
            submit.disabled=False
        if not ConfigFile.selected_filename:
            ErrorCode.value = """
            <div style="text-align: right;">
                <i><b><code style="color:red;">Er is geen config.yaml geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>select</b></font></kbd> drukt na het kiezen van het bestand om je selectie te bevestigen.</code></b></i>
            </div>
            """
            submit.disabled=False
        if not Model.selected:
            ErrorCode.value = """
            <div style="text-align: right;">
                <i><b><code style="color:red;">Er is geen model.pt geselecteerd.<br>Zorg ervoor dat je op <kbd><font color="#424a48"><b>select</b></font></kbd> drukt na het kiezen van model.pt om je selectie te bevestigen.</code></b></i>
            </div>
            """
            submit.disabled=False
        else:
            # verwijdert eventuele errorcodes
            ErrorCode.value = ""
            # Weergeeft running onder aan de interface
            Successcherm.value = "<hr><h1>Running..."
            Resultaten = ModelTest(
                Model= Model.selected,
                ConfigFile= ConfigFile.selected,
                DataPick= TestOrValidation.value,
                Project= Q_UIparts.ProjectPicker.value,
                Confidence= Confidence.value,
            )
            # Update Running naar de locatie van de test resultaten
            Successcherm.value = f"""
            <hr>
            <style>
            td:first-child {{
                text-align: right;
            }}
            td:last-child {{
                text-align: left;
            }}
            </style>

            <h1>Succes!</h1> 
            <table>
            <tr>
                <td><b>Resultaten:</b></td>
                <td>{os.path.join(os.getcwd(), str(Resultaten))}</td>
            </tr>
            """
            # Activeert de Submitbutton zodat de volgende validatie uitgevoert kan worden.
            submit.disabled=False

    #Genereert 2 lege text widget die alleen waarde krijgen tijdens het gebruik van de interface
    ErrorCode = widgets.HTML()
    Successcherm = widgets.HTML()
    # Genereert verschillenden stukjes text die op de interface gebruikt worden.
    line = widgets.HTML(value = "<hr>")
    Titel = widgets.HTML(value = "<h3>Model validatie</h3><hr>")
    WoordelijkeVraag1 = widgets.HTML(value = f"<b>De validatie  van dit model word uitgevoerd op de")
    WoordelijkeVraag2 = widgets.HTML(value = f"<b> van het config.yaml bestand met een confidence van")

    # voegt alle widgets samen tot 1 interface
    View = widgets.VBox([
        Titel,
        widgets.HBox([
            widgets.VBox([
                Model, 
                ConfigFile,
            ]),
            Q_UIparts.ProjectInterface,
        ]),
        line,
        widgets.HBox([
            WoordelijkeVraag1,
            TestOrValidation,
            WoordelijkeVraag2,
            Confidence,
        ]),
        line,        
        widgets.HBox([
            ErrorCode, 
            submit
        ], layout= widgets.Layout(justify_content="flex-end")),
        Successcherm,
        ], layout= widgets.Layout(width='888px'))
    

    display(View)