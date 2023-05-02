def LabelCheck(ImageMap, Annotaties, Model, DataName):
    from Modules.AnotatieTool import Annoteren
    import ipywidgets as widgets
    import os

    #ceckt of er al een LabelDoc bestaat en maakt deze anders aan
    LabelDoc = os.path.join(Annotaties, "Labels.txt")
    if not os.path.exists(LabelDoc):
        open(LabelDoc, "w+")

    #functie om de weergegeven lijst van labels te updaten
    def LaadLabelLijst():
        with open(LabelDoc, "r") as f:
            labels = f.read()
            labels = labels.replace("\n", "<br> ")
            return "<b>De volgende Labels zijn al geregistreerd:</b><br>" + labels
    
    #weergeeft labels
    LabelLijst = widgets.HTML(
        value = LaadLabelLijst()
    )

    #weergeeft een text box die de input van nieuwe labels faciliteert
    LabelInput = widgets.Text(
        placeholder='Naam label',
        description='Add:',
        disabled=False   
    )

    LabelInput.continuous_update = False

    #Knop voor het toevoegen van Labels
    LabelSubmit = widgets.Button(
        value = False,
        description = "Permanent toevoegen",
        button_style = ""
    )

    #Functie om nieuwe labels toe te voegen en de weergave te updaten
    def AddToList(PlaceHolder):
        with open(LabelDoc, "r") as f:
            if LabelInput.value not in f.read():
                with open(LabelDoc, "a") as g:
                    g.write(LabelInput.value + "\n")
                LabelInput.value = ""
                LabelLijst.value = LaadLabelLijst()

    LabelSubmit.on_click(AddToList)
    LabelInput.observe(AddToList)

    #Knop om de annotatietool te starten
    Next = widgets.Button(
        value = False,
        description = "Start met annoteren",
        button_style = "success"
    )
    #geeft benodigde gegevens door aan de annotatietool
    @Next.on_click
    def SaveAndLaunch(PlaceHolder):
        Annoteren(
            ImageMap = ImageMap,
            Annotaties = Annotaties,
            Labels = LabelDoc,
            Model = Model,
            DataName = DataName
        )
        LabelCheck.close()
    
    WiteLine = widgets.HTML(" ")

    #Clustert de widgets in een interface
    LabelCheck = widgets.VBox([
        LabelLijst,
        widgets.HBox([
        LabelInput,
        LabelSubmit,
        WiteLine,
        Next
    ])])
    
    display(LabelCheck)