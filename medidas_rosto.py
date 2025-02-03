import os
import cv2
import face_recognition
import psycopg2
import numpy as np
from database import ConexaoDB

class BaseRostos:
    def __init__(self):
        self.conexao = ConexaoDB()
        self.conexao.conectar()
        self.cursor = self.conexao.cur

    def rosto_existe(self, nome):
        sql = "SELECT COUNT(*) FROM base_facial WHERE nome = %s"
        self.cursor.execute(sql, (nome,))
        return self.cursor.fetchone()[0] > 0

    def inserir_rosto(self, nome, imagem_bin, medidas):
        sql = "INSERT INTO base_facial (nome, imagem, medidas_rosto) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (nome, psycopg2.Binary(imagem_bin), medidas.tolist()))
        print(f"Imagem {nome} inserida no banco!")

    def buscar_medidas_banco(self):  
        self.cursor.execute("SELECT nome, medidas_rosto FROM base_facial")
        registros = self.cursor.fetchall()
        nomes, medidas = [], []

        for nome, medida in registros:
            nomes.append(nome)
            medidas.append(np.array(medida))

        return nomes, medidas
    
    def commit(self):
        self.conexao.con.commit()

    def fechar_conexao(self):
        self.cursor.close()
        self.conexao.desconectar()

class MedidasRosto:
    def __init__(self, pasta_imagens = "fotos/"):
        self.pasta_imagens = pasta_imagens
        self.db = BaseRostos()

    def processar_imagens(self):
        for arquivo in os.listdir(self.pasta_imagens):
            if arquivo.lower().endswith(('.jpg', '.jpeg', 'png')):
                self.identifica_medida(arquivo)
        
        self.db.commit()
        self.db.fechar_conexao()

    def identifica_medida(self, arquivo):
        caminho_imagem = os.path.join(self.pasta_imagens, arquivo)
        nome = os.path.splitext(arquivo)[0]

        if self.db.rosto_existe(nome):
            print(f"Imagem {arquivo} já está cadastrada")
            return

        imagem = face_recognition.load_image_file(caminho_imagem)
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)

        faceLOCs = face_recognition.face_locations(imagem)
        if not faceLOC:
            print(f"Nenhum rosto detectado em {arquivo}")
            return
        
        faceLOC = faceLOCs[0]
        cv2.rectangle(imagem, (faceLOC[3],faceLOC[0]), (faceLOC[1], faceLOC[2]), (0,255,0), 2)

        medidas = face_recognition.face_encodings(imagem)

        if medidas:
            with open(caminho_imagem, "rb") as imagem_file:
                imagem_bin = imagem_file.read()

            self.db.inserir_rosto(nome, imagem_bin, medidas[0])
            os.remove(caminho_imagem)
            print(f"Imagem {arquivo} removida da pasta.")
        else:
            print(f"Não foi possível extrair medidas de {arquivo}")
