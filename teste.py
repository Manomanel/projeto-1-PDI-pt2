#Manel isso é só para testar se as imagens sairam igual!

import numpy as np
from PIL import Image

image = Image.open("saida.jpg") 
image = np.array(image)
image = image.astype(np.int32)

image2 = Image.open("SaidaExercicio3.jpg") 
image2 = np.array(image2)
image2 = image2.astype(np.int32)

resultado = image == image2  # Retorna uma matriz booleana

print(image2[0][0])

print(image[0][0])

print(resultado)