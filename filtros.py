from PIL import Image

#LEITOR DE ARQUIVOS
#int int (largura altura da matriz)
#int int (o lugar em que um pivo será)
#float float float (matriz)
#float float float
#float float float

def converter_para_cinza(caminho_imagem):
    # Carregar a imagem
    imagem = Image.open(caminho_imagem).convert("RGB")

    # Método (a) - Banda G replicada
    def grayscale_by_green(im):
        r, g, b = im.split()
        return Image.merge("RGB", (g, g, g))

    # Método (b) - Banda Y do sistema YIQ
    def grayscale_by_Y(im):
        r, g, b = im.split()
        r = r.convert("L")  # Converter para escala de cinza (8 bits)
        g = g.convert("L")
        b = b.convert("L")

        # Calcular Y manualmente (pixel a pixel)
        Y = Image.eval(r, lambda i: int(0.299 * i))
        Y = Image.eval(g, lambda i: int(Y.getpixel((0, 0)) + 0.587 * i))
        Y = Image.eval(b, lambda i: int(Y.getpixel((0, 0)) + 0.114 * i))

        return Image.merge("RGB", (Y, Y, Y))

    # Aplicar os métodos
    imagem_g = grayscale_by_green(imagem)
    imagem_y = grayscale_by_Y(imagem)

    # Criar nomes para os arquivos de saída
    caminho_base = caminho_imagem.rsplit(".", 1)[0]  # Remove a extensão do nome do arquivo
    caminho_g = f"{caminho_base}_grayscale_G.jpg"
    caminho_y = f"{caminho_base}_grayscale_Y.jpg"

    # Salvar as imagens processadas
    imagem_g.save(caminho_g)
    imagem_y.save(caminho_y)

    print(f"Imagens salvas: {caminho_g}, {caminho_y}")
   
   
def ler_arquivo(caminho):
   with open(caminho, 'r') as f:
      linhas = f.readlines()
   
   # Lendo dimensões da matriz
   m, n = map(int, linhas[0].split())
   
   # Lendo a posição do pivô
   pivo_x, pivo_y = map(int, linhas[1].split())
   
   # Lendo a matriz
   matriz = []
   for i in range(2, 2 + m):
      linha = list(map(float, linhas[i].split()))
      matriz.append(linha)
   
   #TODO detecção de erros de escrita no arquivo de entrada
   
   return m, n, (pivo_x, pivo_y), matriz

def aplicar_filtro(caminho, m, n, pivo, matriz):
   img = Image.open(caminho) #carrega a imagem e recebe informações
   largura, altura = img.size
   pixels = img.load()
   
   pivo_x, pivo_y = pivo
   
   #fors para andar pela imagem
   for y in range(pivo_y - 1, altura - pivo_y + 1): #calculo com o pivo para nao usar extensao por 0
      for x in range(pivo_x - 1, largura - pivo_x + 1): #aka nao aplicar o filtro nas bordas da img
         red = 0
         green = 0
         blue = 0
         matrix_sum = 0 # num filtro gaussiano, este valor será 1 pois quem vai ser dividido são os valores individuais
                        # caso seja um filtro com pesos inteiros no final vai dividir pela soma desses pesos
         for j in range(1, n+1):#altura e largura da matriz para percorrer
            for i in range(1, m+1):
               dist_altura = -pivo_x + i#distancia do pivo, pois o pixel atual e x e y
               dist_largura = -pivo_y + j#a distancia e baseada em x e y
               r, g, b = pixels[x + dist_largura, y + dist_altura] #
               red = red + (r * matriz[i-1][j-1])# valor_R_no_pixel_selecionado * valor da matriz de entrada
               green = green + (g * matriz[i-1][j-1])
               blue = blue + (b * matriz[i-1][j-1])
               matrix_sum = matrix_sum + matriz[i-1][j-1]# adicionar os valores da matriz conforme passa para dividr dps
               
         red = round(red/matrix_sum)#calcular o valor final das cores
         green = round(green/matrix_sum)#arredondar para virar int
         blue = round(blue/matrix_sum)
         pixels[x, y] = (red, green, blue)#atribui o novo valor para o pixel atual
         
               
   img.save("imagem_filtrada.jpg")#salva a nova imagem com nome diferente

# Exemplo de uso:
m, n, pivo, matriz = ler_arquivo("entrada.txt")
# print("Dimensões:", m, "x", n)
# print("Pivô em:", pivo)
# print("Matriz:")
# for linha in matriz:
#    print(linha)

converter_para_cinza('imbu.png')

largura, altura = aplicar_filtro("imbu.png", m, n, pivo, matriz)

