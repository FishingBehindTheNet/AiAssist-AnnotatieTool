# AiAssist-AnnotatieTool

Dit notebook is gemaakt als een pijplijn voor het annoteren en het maken van modellen voor het gebruik in ai assisted annoteren. Het idee hierbij is niet dat een complete dataset geannoteerd wordt voordat het eerste model getraind word maar in plaats daarvan periodiek een model getraind wordt wat daarna gebruikt kan worden om te helpen bij het annoteren van de rest van de dataset. Momenteel werkt de code voor .PNG .JPEG en .JPG bestanden. Op verzoek kan deze of andere functies aangepast of uitgebreid worden. Voor vragen, verzoeken of bugs kun je contact opnemen via de github issue tracker.

De tool is gebouwd op python 3.9 en maakt gebruikt van alle bibliotheken in BASIS_requirements.txt en CPU_requirements.txt. Wanneer de computer een Nvidia GPU heeft met CUDA-ondersteuning (https://developer.nvidia.com/cuda-gpus) word aanbevolen de GPU_requirements.txt te gebruiken in plaats van de CPU_requirements.txt voor een versnelde trainings tijd.

