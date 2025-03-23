import numpy as np
from PIL import Image


def process_image(image, matriz):
    """Percorre uma imagem pixel por pixel, calcula a soma dos canais R, G e B e gera uma imagem em escala de cinza."""
    h, w, c = image.shape

    alturaFiltro = matriz.shape[0] #Define a altura do filtro
    alturaMet = alturaFiltro //2
    larguraFiltro = matriz.shape[1]  #Define a largura do filtro
    larguraMet = larguraFiltro //2

    # Criando matriz para a imagem em escala de cinza, os valores precisam ser a metade mais o valor aproximado pela perda de pixel (sem extensão)
    grayscale = np.zeros((h-alturaMet*2, w-larguraMet*2), dtype=np.uint8)
    
    
    # Percorrendo cada pixel da imagem e aplicando o filtro
    for i in range(larguraMet, h - larguraMet):
        for j in range(alturaMet, w - alturaMet):
            sub_matrix = image[i-larguraMet:i+larguraMet+1, j-alturaMet:j+alturaMet+1, :]
            matrizMultiplicada = sub_matrix*matriz
            grayscale[i-larguraMet, j-alturaMet] = round(np.sum(matrizMultiplicada))

    # Retorna a imagem filtrada no formato de uma matriz
    return grayscale

# Teste com um exemplo
if __name__ == "__main__":

    with open("entrada3.txt", "r") as file: #le o arquivo onde a matriz está
        lines = file.readlines()

    num_columns = len(lines[0].split()) #define quantas colunas tem o filtro
    num_lines = 0
    for i in lines:
        if i=='\n':
            break
        num_lines+=1                    #define quantas linhas tem o filtro
    
    matriz = np.loadtxt('entrada3.txt') #carrega a matriz pelo numpy array
    matriz = matriz.reshape(num_columns, num_lines, 3)  #caso tenha algum erro na leitura do np.loadtxt ele reajusta para o formato certo

    # Converter a imagem para NumPy array
    image = Image.open("Shapes.png") #Carrega a imagem de entrada
    image = np.array(image)
    image = image.astype(np.int32)      #converte para NumPy array no tipo int32

    # Convertendo para escala de cinza
    grayscale_array = process_image(image, matriz)

    #Transforma e salva a matriz em imagem
    grayscale_image = Image.fromarray(grayscale_array)
    grayscale_image.save("SaidaExercicio3.jpg")
    
    print("Imagem processada com sucesso")
