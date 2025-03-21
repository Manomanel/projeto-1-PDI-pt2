from PIL import Image

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
   
converter_para_cinza("testePROF.tif")