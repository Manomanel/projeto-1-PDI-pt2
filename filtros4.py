from PIL import Image, ImageMath
import numpy as np


def converter_para_cinza(caminho_imagem):
    # Carregar a imagem
   imagem = Image.open(caminho_imagem).convert("RGB")

    # Método (a) - Banda G replicada
   def grayscale_by_green(im):
      r, g, b = im.split()
      return Image.merge("RGB", (g, g, g))

    # Método (b) - Banda Y do sistema YIQ
   def grayscale_by_Y(im):
      arr = np.array(im)  # Converte para array NumPy (H, W, 3)
    
      # Aplicando fórmula de luminância
      Y = (0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]).astype(np.uint8)
      # Criar uma imagem RGB com tons de cinza Y
      return Image.fromarray(np.stack([Y, Y, Y], axis=-1))

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