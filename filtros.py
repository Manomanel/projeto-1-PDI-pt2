from PIL import Image

#LEITOR DE ARQUIVOS
#int int (largura altura da matriz)
#int int (o lugar em que um pivo será)
#float float float (matriz)
#float float float
#float float float

   
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
   pivo_x, pivo_y = pivo
   
   pixels = img.load()
   #img2 = img.copy()
   nova_largura = largura - (pivo_y - 1) - (m - pivo_y)
   nova_altura = altura - (pivo_x - 1) - (n - pivo_x)
   img2 = Image.new("RGB", (nova_largura, nova_altura), (0, 0, 0))
   pixels2 = img2.load()
   
   #fors para andar pela imagem
   for y in range(pivo_y - 1, altura - m + pivo_y): #calculo com o pivo para nao usar extensao por 0
      for x in range(pivo_x - 1, largura - n + pivo_x): #aka nao aplicar o filtro nas bordas da img
         red = 0
         green = 0
         blue = 0
         matrix_sum = 0 # num filtro gaussiano, este valor será 1 pois quem vai ser dividido são os valores individuais
                        # caso seja um filtro com pesos inteiros no final vai dividir pela soma desses pesos
         for j in range(1, n+1):#altura e largura da matriz para percorrer
            for i in range(1, m+1):
               dist_altura = -pivo_x + i#distancia do pivo, pois o pixel atual e x e y
               dist_largura = -pivo_y + j#a distancia e baseada em x e y
               r, g, b = pixels[x + dist_largura, y + dist_altura] # recebe os valores RGB do pixel
               red = red + (r * matriz[i-1][j-1])# valor_R_no_pixel_selecionado * valor da matriz de entrada
               green = green + (g * matriz[i-1][j-1])
               blue = blue + (b * matriz[i-1][j-1])
               matrix_sum = matrix_sum + matriz[i-1][j-1]# adicionar os valores da matriz conforme passa para dividr dps
         
         red = round(red/matrix_sum)#calcular o valor final das cores
         green = round(green/matrix_sum)#arredondar para virar int
         blue = round(blue/matrix_sum)
         pixels2[x - (pivo_x - 1), y - (pivo_y - 1)] = (red, green, blue)#atribui o novo valor para o pixel atual
         
   img2.save("imagem_filtrada.jpg")#salva a nova imagem com nome diferente
   
   #img_pos_hist = exp_histograma(img2)
    
   #img_pos_hist.save("imagem_histograma.jpg")#salva a nova imagem da expansao de histograma com nome diferente

def exp_histograma(imagem):
   pixels = imagem.load()
   largura, altura = imagem.size
   high_R = 0              #valores iniciais
   high_G = 0
   high_B = 0
   low_R = 255
   low_G = 255
   low_B = 255
   
   for y in range(altura): #analisar qual o menor valor de cada cor para o calculo a expansao
      for x in range(largura):
         r, g, b = pixels[x, y]
         if(r < low_R): low_R = r
         if(g < low_G): low_G = g
         if(b < low_B): low_B = b
         if(r > high_R): high_R = r
         if(g > high_G): high_G = g
         if(b > high_B): high_B = b

   if(high_R - low_R == 0| high_G - low_G == 0| high_B - low_B == 0): exit() #evitar divisao por 0 quando a imagem inteira tem o mesmo valor de uma cor

   for y in range(altura): # passa de pixel em pixel usando os valores adquiridos
      for x in range(largura):
         r, g, b = pixels[x, y]
         new_R = round((r - low_R) / (high_R - low_R) * 255) #o calculo do histograma e ja atribui o novo valor
         new_G = round((g - low_G) / (high_G - low_G) * 255)
         new_B = round((b - low_B) / (high_B - low_B) * 255)
         pixels[x, y] = (new_R, new_G, new_B) #atribui o novo valor para o pixel atual
   
   return imagem

# Exemplo de uso:
m, n, pivo, matriz = ler_arquivo("entrada.txt")
# print("Dimensões:", m, "x", n)
# print("Pivô em:", pivo)
# print("Matriz:")
# for linha in matriz:
#    print(linha)

aplicar_filtro("imbu.png", m, n, pivo, matriz)

