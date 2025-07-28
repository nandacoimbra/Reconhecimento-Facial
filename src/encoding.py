import face_recognition
import cv2
import os
import pickle
import time


def carregar_encodings(pasta):
    encs, nomes, ids = [], [], []
    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".pkl"):
            with open(os.path.join(pasta, arquivo), "rb") as f:
                dados = pickle.load(f)
                encs.append(dados["encoding"])
                nomes.append(dados["nome"])
                ids.append(dados["id"])
    return encs, nomes, ids

def salvar_encoding(id_usuario, nome_usuario, pasta_encodings):

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro ao acessar a câmera.")
        return False

    print("Aguardando rosto para captura automática...")
    encoding_salvo = False
    inicio_contagem = None

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # Reduz e converte o frame para RGB (necessário para o face_recognition)
        pequena = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb = cv2.cvtColor(pequena, cv2.COLOR_BGR2RGB)

        # Detecta rostos no frame
        localizacoes = face_recognition.face_locations(rgb)

        if localizacoes:
            if inicio_contagem is None:
                inicio_contagem = time.time()
            elif time.time() - inicio_contagem >= 5.0:  # 5 segundos com rosto visível
                encodings = face_recognition.face_encodings(rgb, localizacoes)
                if encodings:
                    encoding = encodings[0]
                    dados = {"id": id_usuario, "nome": nome_usuario, "encoding": encoding}
                    nome_arquivo = f"{id_usuario}_{nome_usuario}.pkl"
                    caminho_completo = os.path.join(pasta_encodings, nome_arquivo)

                    with open(caminho_completo, "wb") as f:
                        pickle.dump(dados, f)

                    print(f"Encoding salvo com sucesso: {caminho_completo}")
                    encoding_salvo = True
                    break
                else:
                    print("Rosto não pôde ser codificado. Tente novamente.")
                    inicio_contagem = None  # Reinicia contagem
        else:
            inicio_contagem = None  # Nenhum rosto detectado, reinicia o tempo

        # Mostra o frame na tela para feedback visual
        cv2.imshow("Cadastro Facial", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return encoding_salvo