import serial
import cv2
import face_recognition
import os
import pickle

# Configura a porta serial
ser = serial.Serial('COM7', 115200, timeout=1)

# Diretório onde os encodings serão salvos
ENCODINGS_DIR = "encodings"
os.makedirs(ENCODINGS_DIR, exist_ok=True)

def capturar_e_salvar_encoding(id_usuario, nome_usuario, pasta_encodings='encodings'):
    if not os.path.exists(pasta_encodings):
        os.makedirs(pasta_encodings)

    # Inicializa a câmera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro ao acessar a câmera.")
        return

    print("Pressione 'c' para capturar a imagem com o rosto...")
    encoding_salvo = False

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Falha ao capturar imagem.")
            continue

        cv2.imshow('Captura de Rosto', frame)

        tecla = cv2.waitKey(1)
        if tecla == ord('c'):
            # Converte a imagem BGR para RGB
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detecta rostos e calcula os encodings
            localizacoes = face_recognition.face_locations(rgb)
            encodings = face_recognition.face_encodings(rgb, localizacoes)

            if encodings:
                encoding = encodings[0]

                dados = {
                    "id": id_usuario,
                    "nome": nome_usuario,
                    "encoding": encoding
                }

                nome_arquivo = f"{id_usuario}_{nome_usuario}.pkl"
                caminho_completo = os.path.join(pasta_encodings, nome_arquivo)

                with open(caminho_completo, "wb") as f:
                    pickle.dump(dados, f)

                print(f"Encoding salvo em {caminho_completo}")
                encoding_salvo = True
                break
            else:
                print("Nenhum rosto detectado. Tente novamente.")

        elif tecla == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return encoding_salvo


capturar_e_salvar_encoding("002", "fernanda_coimbra")
# Loop principal aguardando comandos via Serial
# while True:
#     if ser.in_waiting:
#         linha = ser.readline().decode('utf-8').strip()
#         print("Recebido:", linha)

#         partes = linha.split("|")
#         if len(partes) == 3 and partes[0] == "tirar_foto":
#             id_usuario = partes[1]
#             nome_usuario = partes[2]

#             print(f"[COMANDO] Tirar foto de {nome_usuario} (ID: {id_usuario})")
#             capturar_e_salvar_encoding(id_usuario, nome_usuario)