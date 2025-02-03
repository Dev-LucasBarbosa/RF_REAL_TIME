from medidas_rosto import MedidasRosto
from capturar_rosto import ReconhecimentoFacial

if __name__ == "__main__":
    imagens = MedidasRosto()
    imagens.processar_imagens()

    reconhecimento = ReconhecimentoFacial()
    reconhecimento.reconhecer()
