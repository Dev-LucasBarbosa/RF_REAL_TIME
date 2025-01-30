import cv2
import psycopg2
import face_recognition
import numpy
from database import conn 
from medidas_rosto import buscar_medidas_banco

classificador = cv2.CascadeClassifier(
     cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

captura = cv2.VideoCapture(0)

captura.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
captura.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

nomes_salvos, medidas_salvas = buscar_medidas_banco()

while not cv2.waitKey(20) & 0xFF == ord("q"):
    ret, frame = captura.read()

    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    rostos = classificador.detectMultiScale(cinza, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in rostos:
        rostos_rgb = frame [y:y+h, x:x+w]
        medida_rosto = face_recognition.face_encodings(rostos_rgb)

        nome_identificado = "Desconhecido"

        if medida_rosto:
            medida_rosto = medida_rosto[0]

            resultados = face_recognition.compare_faces(medidas_salvas, medida_rosto, tolerance=0.6)

            for i in range(len(resultados)):
                if resultados[i]:
                    nome_identificado = nomes_salvos[i]
                    break
                                
        cv2.rectangle(frame, (x, y), (x + w, y + w), (0,255,0), 3)
        cv2.putText(frame, nome_identificado, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    cv2.imshow("Reconhecimento Facial", frame)

captura.release()
cv2.destroyAllWindows()
