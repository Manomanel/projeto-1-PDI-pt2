from PIL import Image

#LEITOR DE ARQUIVOS
#int int (largura altura da matriz)
#int int (o lugar em que um pivo será)
#int (offset)
#int (passo P)
#int (Relu)
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
   
   # Lendo as novas variáveis do segundo passo do trabalho
   offset = int(linhas[2].strip())
   passoP = int(linhas[3].strip())
   
   # Lendo a matriz
   matriz = []
   for i in range(4, 4 + m):
      linha = list(map(float, linhas[i].split()))
      matriz.append(linha)
   
   #TODO detecção de erros de escrita no arquivo de entrada
   
   return m, n, (pivo_x, pivo_y), offset, passoP, matriz

def aplicar_filtro(caminho, m, n, pivo, offset, passoP, matriz):
   img = Image.open(caminho) #carrega a imagem e recebe informações
   largura, altura = img.size
   pixels = img.load()
   
   pivo_x, pivo_y = pivo
   
   count = 0 #count para o passo P
   
   #fors para andar pela imagem
   for y in range(pivo_y - 1, altura - pivo_y + 1): #calculo com o pivo para nao usar extensao por 0
      for x in range(pivo_x - 1, largura - pivo_x + 1): #aka nao aplicar o filtro nas bordas da img
         
         count += 1
         if (count % passoP != 0): continue #decidir se o pixel esta incluso no passo P ou nao 
         
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
         
         #Calcular offset
         red = red + offset
         green = green + offset
         blue = blue + offset
         
         #previnir que seja maior que 255
         if(red > 255): red = 255
         if(green > 255): green = 255
         if(blue > 255): blue = 255
         
         #funcao ReLU
         if(red < 0): red = 0
         if(green < 0): green = 0
         if(blue < 0): blue = 0
         
         pixels[x, y] = (red, green, blue)#atribui o novo valor para o pixel atual
         
   img.save("imagem_filtrada2.jpg")#salva a nova imagem com nome diferente

# Exemplo de uso:
m, n, pivo, offset, passoP, matriz = ler_arquivo("entrada2.txt")
# print("Dimensões:", m, "x", n)
# print("Pivô em:", pivo)
# print("Variáveis adicionais:", var1, var2, var3)
# print("Matriz:")
# for linha in matriz:
#    print(linha)

aplicar_filtro("choboco.jpg", m, n, pivo, offset, passoP, matriz)
