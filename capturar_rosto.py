import cv2
import face_recognition
from medidas_rosto import BaseRostos

class ReconhecimentoFacial:
    def __init__(self):
        self.classificador = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.captura = cv2.VideoCapture(0)
        self.captura.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.captura.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

        self.db = BaseRostos()
        self.nomes_salvos, self.medidas_salvas = self.db.buscar_medidas_banco()
        self.db.fechar_conexao()

    def reconhecer(self):
        while not cv2.waitKey(20) & 0xFF == ord("q"):
            ret, frame = self.captura.read()
            cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rostos = self.classificador.detectMultiScale(cinza, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in rostos:
                rostos_rgb = frame [y:y+h, x:x+w]
                medida_rosto = face_recognition.face_encodings(rostos_rgb)

                nome_identificado = "Desconhecido"

                if medida_rosto:
                    medida_rosto = medida_rosto[0]

                    resultados = face_recognition.compare_faces(self.medidas_salvas, medida_rosto, tolerance=0.6)

                    for i in range(len(resultados)):
                        if resultados[i]:
                            nome_identificado = self.nomes_salvos[i]
                            break
                                        
                cv2.rectangle(frame, (x, y), (x + w, y + w), (0,255,0), 3)
                cv2.putText(frame, nome_identificado, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

            cv2.imshow("Reconhecimento Facial", frame)

        self.captura.release()
        cv2.destroyAllWindows()
