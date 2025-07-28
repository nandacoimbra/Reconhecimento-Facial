import cv2
import face_recognition
import time

def detectar_rosto_continuo(duracao_minima=2.0, mostrar_camera=True):
    cap = cv2.VideoCapture(0)
    inicio = None
    frame_detectado = None

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        redimensionada = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb = cv2.cvtColor(redimensionada, cv2.COLOR_BGR2RGB)
        rostos = face_recognition.face_locations(rgb)

        if rostos:
            if inicio is None:
                inicio = time.time()
            elif time.time() - inicio >= duracao_minima:
                frame_detectado = frame
                break
        else:
            inicio = None

        if mostrar_camera:
            cv2.imshow("Detecção", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    return frame_detectado
