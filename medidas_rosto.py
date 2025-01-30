import os
import cv2
import face_recognition
import psycopg2
from database import conn

pasta_imagens = "fotos/"

cursor = conn.cursor()

for arquivo in os.listdir(pasta_imagens):
    if arquivo.lower().endswith(('.jpg', '.jpeg', 'png')):
        caminho_imagem = os.path.join(pasta_imagens, arquivo)

        imagem = face_recognition.load_image_file(caminho_imagem)
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)

        faceLOC = face_recognition.face_locations(imagem)[0]
        cv2.rectangle(imagem, (faceLOC[3],faceLOC[0]), (faceLOC[1], faceLOC[2]), (0,255,0), 2)

        medidas = face_recognition.face_encodings(imagem)

        if len(medidas) > 0:
            medida = medidas[0]

            with open(caminho_imagem, "rb") as imagem_file:
                imagem_bin = imagem_file.read()

            nome = os.path.splitext(arquivo)[0]

            sql = "INSERT INTO base_facial (nome, imagem, medidas_rosto) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nome, psycopg2.Binary(imagem_bin), medida.tolist()))

            print(f"Imagem {arquivo} inserida no banco!")

        else:
            print(f"Nenhum rosto detectado em {arquivo}")

conn.commit()
cursor.close()