import cv2 # type: ignore
import face_recognition # type: ignore
import time
from config.settings import SERIAL_PORT, ENCODINGS_DIR, CAMERA_INDEX


def detectar_rosto_continuo(duracao_minima=2.0, mostrar_camera=True):
    # Abre a câmera (0 = câmera padrão)
    cap = cv2.VideoCapture(CAMERA_INDEX)
    inicio = None  # Marca o tempo inicial em que um rosto foi detectado
    frame_detectado = None  # Frame que será retornado se rosto for confirmado

    while True:
        ret, frame = cap.read()  # Captura um frame da câmera
        if not ret:
            continue  # Se não conseguir capturar, tenta novamente

        # Reduz o tamanho do frame (1/4 da imagem → mais rápido)
        # Converte para RGB (necessário para o face_recognition)
        redimensionada = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb = cv2.cvtColor(redimensionada, cv2.COLOR_BGR2RGB)

        # Detecta rostos no frame
        rostos = face_recognition.face_locations(rgb)

        if rostos:
            # Se achou rosto pela primeira vez → marca tempo
            if inicio is None:
                inicio = time.time()
            # Se o rosto permanecer visível pelo tempo mínimo → captura frame
            elif time.time() - inicio >= duracao_minima:
                frame_detectado = frame  # Salva o frame original (não redimensionado)
                break
        else:
            # Se o rosto some, zera a contagem
            inicio = None

        # Mostra a câmera na tela (para feedback visual, se habilitado)
        if mostrar_camera:
            cv2.imshow("Detecção", frame)
            # Permite encerrar manualmente com a tecla 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Libera os recursos da câmera e fecha a janela de vídeo
    cap.release()
    cv2.destroyAllWindows()
    return frame_detectado
