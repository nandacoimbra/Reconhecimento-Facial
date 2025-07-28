import cv2
import face_recognition
import os
import pickle
import time
import serial

# # Inicializa comunicação serial
# ser = serial.Serial('COM7', 115200, timeout=1)

# Diretório onde os encodings estão salvos
ENCODINGS_DIR = "encodings"
os.makedirs(ENCODINGS_DIR, exist_ok=True)


def carregar_encodings(pasta_encodings=ENCODINGS_DIR):
    encodings_conhecidos, nomes_conhecidos, ids_conhecidos = [], [], []

    for arquivo in os.listdir(pasta_encodings):
        if arquivo.endswith(".pkl"):
            caminho = os.path.join(pasta_encodings, arquivo)
            with open(caminho, "rb") as f:
                dados = pickle.load(f)
                encodings_conhecidos.append(dados["encoding"])
                nomes_conhecidos.append(dados["nome"])
                ids_conhecidos.append(dados["id"])

    return encodings_conhecidos, nomes_conhecidos, ids_conhecidos


def detectar_rosto_continuo(duracao_minima=2.0):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro ao acessar a câmera.")
        return None

    print("Detectando rosto... Mantenha o rosto visível por 2 segundos.")
    inicio_contagem = None

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        pequena_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb = cv2.cvtColor(pequena_frame, cv2.COLOR_BGR2RGB)

        rostos = face_recognition.face_locations(rgb)

        if rostos:
            if inicio_contagem is None:
                inicio_contagem = time.time()
            elif time.time() - inicio_contagem >= duracao_minima:
                print("Rosto detectado por tempo suficiente.")
                cap.release()
                cv2.destroyAllWindows()
                return frame
        else:
            inicio_contagem = None

        cv2.imshow("Detecção de Rosto", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None


def comparar_com_base(frame, encodings_conhecidos, nomes_conhecidos, ids_conhecidos):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    locais = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, locais)

    if not encodings:
        return None, None

    encoding = encodings[0]
    matches = face_recognition.compare_faces(encodings_conhecidos, encoding)
    
    if True in matches:
        idx = matches.index(True)
        return nomes_conhecidos[idx], ids_conhecidos[idx]
    
    return "Desconhecido", "?"


def fluxo_reconhecimento():
    encodings_conhecidos, nomes_conhecidos, ids_conhecidos = carregar_encodings()
    frame = detectar_rosto_continuo(duracao_minima=2)

    if frame is not None:
        nome, id_usuario = comparar_com_base(frame, encodings_conhecidos, nomes_conhecidos, ids_conhecidos)
        print(f"Resultado: {nome} (ID: {id_usuario})")

        # Envia o resultado via Serial
        if nome != "Desconhecido":
            print(f"Reconhecimento bem-sucedido: {nome} (ID: {id_usuario})")
            # ser.write(f"OK:{id_usuario}\n".encode())
        else:
            # ser.write("FALHA\n".encode())
            print("Reconhecimento falhou. Usuário desconhecido.")
    else:
        print("Nenhum rosto detectado ou operação cancelada.")


# Executa o fluxo
fluxo_reconhecimento()
