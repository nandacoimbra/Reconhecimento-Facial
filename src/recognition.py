import face_recognition
import cv2

def comparar_com_base(frame, encodings_conhecidos, nomes_conhecidos, ids_conhecidos):
    pequena = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb = cv2.cvtColor(pequena, cv2.COLOR_BGR2RGB)
    localizacoes = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, localizacoes)

    for encoding in encodings:
        matches = face_recognition.compare_faces(encodings_conhecidos, encoding)
        if True in matches:
            idx = matches.index(True)
            return nomes_conhecidos[idx], ids_conhecidos[idx]
    return "Desconhecido", "?"
