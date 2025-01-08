# AiAssist-AnnotatieTool

Dit notebook is gemaakt als een pijplijn voor het annoteren en het maken van modellen voor gebruik bij AI-assisted annoteren. Het idee hierbij is niet dat een complete dataset geannoteerd wordt voordat het eerste model getraind wordt, maar in plaats daarvan periodiek een model getraind wordt, dat daarna gebruikt kan worden om te helpen bij het annoteren van de rest van de dataset. Momenteel werkt de code voor .PNG-, .JPEG- en .JPG-bestanden. Op verzoek kunnen deze of andere functies worden aangepast of uitgebreid. Voor vragen, verzoeken of bugs kun je contact opnemen via de GitHub issue tracker.

De tool is gebouwd op Python 3.9 en maakt gebruik van alle bibliotheken in BASIS_requirements.txt en CPU_requirements.txt. Wanneer de computer een Nvidia GPU heeft met CUDA-ondersteuning (https://developer.nvidia.com/cuda-gpus), wordt aanbevolen om GPU_requirements.txt te gebruiken in plaats van CPU_requirements.txt voor een versnelde trainingstijd.

Voor hulp bij het installeren of gebruik van de AiAssist-AnnotatieTool kun je gebruikmaken van de gebruikershandleiding op YouTube:
https://youtube.com/playlist?list=PLwGilaj42u_BGJXtdqZDr2L8PZZgEVBhq&si=1MtIZU8fEtOM6cHQ 
