import face_recognition
import cv2
import os
import pickle
from config.settings import SERIAL_PORT, ENCODINGS_DIR, CAMERA_INDEX


def carregar_encodings(pasta_encodings='encodings'):
    encodings_conhecidos = []
    nomes_conhecidos = []
    ids_conhecidos = []

    for arquivo in os.listdir(pasta_encodings):
        if arquivo.endswith(".pkl"):
            caminho = os.path.join(pasta_encodings, arquivo)
            with open(caminho, "rb") as f:
                dados = pickle.load(f)
                encodings_conhecidos.append(dados["encoding"])
                nomes_conhecidos.append(dados["nome"])
                ids_conhecidos.append(dados["id"])

    return encodings_conhecidos, nomes_conhecidos, ids_conhecidos


# Carrega os encodings salvos
encodings_conhecidos, nomes_conhecidos, ids_conhecidos = carregar_encodings()

# Inicia a webcam
cap = cv2.VideoCapture(CAMERA_INDEX)

print("Iniciando reconhecimento facial... Pressione 'q' para sair.")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # Reduz a imagem para acelerar o processamento
    pequena_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_frame = cv2.cvtColor(pequena_frame, cv2.COLOR_BGR2RGB)

    # Detecta rostos e calcula encodings na imagem
    locais_rostos = face_recognition.face_locations(rgb_frame)
    encodings_rostos = face_recognition.face_encodings(rgb_frame, locais_rostos)

    for (top, right, bottom, left), encoding in zip(locais_rostos, encodings_rostos):
        matches = face_recognition.compare_faces(encodings_conhecidos, encoding)
        nome = "Desconhecido"

        if True in matches:
            idx = matches.index(True)
            nome = nomes_conhecidos[idx]
            id_usuario = ids_conhecidos[idx]
        else:
            id_usuario = "?"

        # Desenha retângulo e nome
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, f"{nome} (ID: {id_usuario})", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Reconhecimento Facial", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()